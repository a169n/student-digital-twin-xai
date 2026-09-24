"""exp_026 — one gate threshold for everyone, or one per cohort?

exp_025 showed a factor list is shown more safely when it reproduces itself:
gating on self_tau_shap >= 0.80 keeps 56 % of students and lifts retained
cross-estimator agreement from 0.346 to 0.410. That is a pooled number. The
institutions sit far apart before any gate is applied (mean cross_tau 0.23 in
OULAD, 0.57 in KU Leuven), and one threshold passes a different share of
students at each. Two readings of that spread call for different claims:

    calibration  the spread is partly a threshold artifact. Choose the cut within
                 each cohort so every cohort shows the same share of students,
                 and the gate becomes a portable deployment rule.
    spread       the spread belongs to the institution. No choice of cut moves
                 OULAD's retained agreement toward KU Leuven's, and the result
                 to report is the spread itself.

Three regimes on the same students, with no model refit — everything here is
post-processing of exp_025's students.csv:

    global              keep self_tau_shap >= t, one t for every cohort
    cohort_calibrated   keep the top share c of each cohort by self_tau_shap.
                        Label-free: it sees only that cohort's own gate signal.
    oracle              the same, ranked by cross_tau itself — the most any gate
                        could retain at that coverage

A random gate retains the unconditional mean in expectation, so lift over the
no-gate mean is measured from zero, and efficiency = lift / oracle lift at the
same coverage is the share of the attainable lift the cheap signal delivers.

Intervals resample whole cohorts within each institution: students of one cohort
share a model and a background draw, so they are not independent observations.

Usage (from services/ml):
    uv run python -m src.experiments.run_gate_calibration
    uv run python -m src.experiments.run_gate_calibration --source exp_027_local_estimator_matrix \\
        --runs f33_background --quality cross_taub_shap__occlusion,cross_taub_shap__lime

The second form is the week-1 robustness check: the same analysis with the
quality measure swapped for exp_027's tie-aware tau-b or its LIME pairs. It
writes exp027_<run>__<quality>/ and leaves the exp_025 outputs alone.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterator
from pathlib import Path

import numpy as np
import pandas as pd

from src.experiments import transfer_benchmark as tb
from src.experiments.run_local_stability import GATE_TAU

REPO = Path(__file__).resolve().parents[4]
EXPERIMENTS = REPO / "data" / "artifacts" / "experiments"
SRC = EXPERIMENTS / "exp_025_local_stability"
OUT = EXPERIMENTS / "exp_026_gate_calibration"
DEFAULT_QUALITY = "cross_tau"  # exp_025's SHAP-vs-occlusion, strict list positions
PRIMARY = "f33_background"
THRESHOLDS = np.round(np.arange(0, 1.0001, 0.05), 2)
COVERAGES = np.round(np.arange(1.0, 0.0, -0.05), 2)
RANKED = {"cohort_calibrated": "rank_calibrated", "oracle": "rank_oracle"}
REGIMES = ("no_gate", "global", *RANKED)
DIFF = "calibrated_minus_global"
N_BOOT = 1000
SEED = 0
POOLED = "ALL"
SMALL = "Zambia"  # 2 cohorts, 40 students: every spread is reported with and without it
OP_METRICS = ["coverage", "mean_cross_tau", "lift", "efficiency"]
# exp_025_local_stability/f33_background/gate_curve.csv at threshold 0.80
PRIMARY_REFERENCE = {"coverage": 0.5555, "mean_cross_tau": 0.4099}


def cohort_rank(d: pd.DataFrame, column: str, seed: int = SEED) -> np.ndarray:
    """Position within the cohort by ``column`` descending, 0 = shown first.

    self_tau_shap is a mean of ten Kendall taus over seven features, so it takes
    few distinct values and ties are the rule. They are broken by a seeded
    permutation drawn per cohort in cohort-id order, so a rerun shows the same
    students rather than whichever happen to come first in the file.
    """
    rng = np.random.default_rng(seed)
    values = d[column].to_numpy()
    rank = np.empty(len(d), dtype=int)
    for _, idx in sorted(d.groupby("cohort_id").indices.items()):
        order = np.lexsort((rng.permutation(len(idx)), -values[idx]))
        rank[idx[order]] = np.arange(len(idx))
    return rank


def prepare(d: pd.DataFrame) -> pd.DataFrame:
    """Attach cohort size and both within-cohort rankings, computed once per run."""
    d = d.reset_index(drop=True)
    d["n_cohort"] = d.groupby("cohort_id")["cohort_id"].transform("size")
    for regime, rank in RANKED.items():
        d[rank] = cohort_rank(d, "self_tau_shap" if regime == "cohort_calibrated" else "cross_tau")
    return d


def jaccard_column(quality: str) -> str:
    """The top-3 jaccard that belongs to a quality measure's estimator pair."""
    if quality == DEFAULT_QUALITY:
        return "cross_jaccard_top3"
    return f"cross_jaccard_top3_{quality.split('_', 2)[-1]}"  # cross_taub_shap__lime -> shap__lime


def load(path: Path, quality: str = DEFAULT_QUALITY) -> tuple[pd.DataFrame, dict[str, int]]:
    """A run's students, with rows the gate cannot score dropped and counted per metric.

    Coverage and cross_tau need both the gate signal and cross_tau; a missing
    cross_jaccard_top3 only leaves that row out of the jaccard mean.

    ``quality`` swaps in another second-method agreement (exp_027 has tie-aware
    tau-b and LIME pairs) under the name cross_tau, so every regime, interval and
    spread below is computed the same way whatever the quality measure is. The
    matching top-3 jaccard comes along when the pair has one.
    """
    d = pd.read_csv(path)
    if quality != DEFAULT_QUALITY:
        jaccard = jaccard_column(quality)
        d = d.assign(
            cross_tau=d[quality],
            cross_jaccard_top3=d[jaccard] if jaccard in d else np.nan,
        )
    dropped = {
        q: int((d["self_tau_shap"].isna() | d[q].isna()).sum())
        for q in ("cross_tau", "cross_jaccard_top3")
    }
    return prepare(d.dropna(subset=["self_tau_shap", "cross_tau"])), dropped


def top_share(d: pd.DataFrame, rank: str, c: float) -> np.ndarray:
    """Keep the ceil(c * n) first-ranked students of every cohort."""
    # Round before ceil: 0.55 * 400 is 220.00000000000003 and would keep 221.
    return (d[rank] < np.ceil(np.round(c * d["n_cohort"], 9))).to_numpy()


def retained(d: pd.DataFrame, kept: np.ndarray) -> pd.DataFrame:
    """Coverage and retained agreement of one kept-mask, per institution and pooled."""
    jac = d["cross_jaccard_top3"].to_numpy()
    jac_kept = kept & ~np.isnan(jac)
    s = (
        pd.DataFrame(
            {
                "group": d["institution"].to_numpy(),
                "students": 1,
                "students_shown": kept.astype(int),
                "tau_all": d["cross_tau"].to_numpy(),
                "tau_kept": np.where(kept, d["cross_tau"].to_numpy(), 0.0),
                "jac_n": jac_kept.astype(int),
                "jac_kept": np.where(jac_kept, jac, 0.0),
            }
        )
        .groupby("group")
        .sum()
    )
    s.loc[POOLED] = s.sum()
    out = s[["students", "students_shown"]].astype(int)
    out["coverage"] = s["students_shown"] / s["students"]
    out["mean_cross_tau"] = s["tau_kept"] / s["students_shown"]
    out["mean_cross_jaccard_top3"] = s["jac_kept"] / s["jac_n"]
    out["no_gate_cross_tau"] = s["tau_all"] / s["students"]
    out["lift"] = out["mean_cross_tau"] - out["no_gate_cross_tau"]
    return out


def curves(d: pd.DataFrame) -> pd.DataFrame:
    """Coverage vs retained agreement for every regime; ``level`` is t or target c."""
    levels = [("global", t, d["self_tau_shap"].to_numpy() >= t) for t in THRESHOLDS]
    levels += [(r, c, top_share(d, rank, c)) for r, rank in RANKED.items() for c in COVERAGES]
    return _stack([retained(d, kept).assign(regime=r, level=lvl) for r, lvl, kept in levels])


def _stack(frames: list[pd.DataFrame]) -> pd.DataFrame:
    out = pd.concat(frames).reset_index(names="group")
    return out[["regime", "level", "group", *out.columns.drop(["regime", "level", "group"])]]


def operating_point(d: pd.DataFrame, c_star: float) -> pd.DataFrame:
    """The global gate at GATE_TAU, and both ranked regimes at its pooled coverage c*.

    The global gate's coverage differs per institution, so its efficiency divides
    by the oracle at that institution's own realised coverage. The oracle only
    reorders students within a cohort, while the global gate can also shift the
    cohort mix, so the global efficiency is not capped at 1.
    """
    regimes = {
        "no_gate": retained(d, np.ones(len(d), dtype=bool)),
        "global": retained(d, d["self_tau_shap"].to_numpy() >= GATE_TAU),
        **{r: retained(d, top_share(d, rank, c_star)) for r, rank in RANKED.items()},
    }
    oracle_at_global = pd.Series(
        {
            g: retained(d, top_share(d, "rank_oracle", cov)).at[g, "lift"]
            for g, cov in regimes["global"]["coverage"].items()
        }
    )
    regimes["global"]["efficiency"] = regimes["global"]["lift"] / oracle_at_global
    for r in RANKED:
        regimes[r]["efficiency"] = regimes[r]["lift"] / regimes["oracle"]["lift"]
    level = {"no_gate": np.nan, "global": GATE_TAU, **dict.fromkeys(RANKED, c_star)}
    frames = [f.assign(regime=r, level=level[r]) for r, f in regimes.items()]
    # Paired on the same students and the same bootstrap draws, so its interval,
    # not the overlap of two separate ones, answers "does calibration beat one cut?"
    diff = regimes["cohort_calibrated"][OP_METRICS] - regimes["global"][OP_METRICS]
    out = _stack([*frames, diff.assign(regime=DIFF, level=np.nan)])
    return out.astype({"students": "Int64", "students_shown": "Int64"})


def spread(op: pd.DataFrame) -> pd.DataFrame:
    """Cross-institution range (max - min) of coverage and retained cross_tau per regime.

    An institution that shows nobody has no retained mean. Skipping it would make
    the with-Zambia row silently equal the without-Zambia one, so the range over
    that set is left undefined (NaN) instead.
    """
    rows = []
    for includes_small in (True, False):
        inst = op[
            op["regime"].isin(REGIMES)
            & (op["group"] != POOLED)
            & (includes_small | (op["group"] != SMALL))
        ]
        for regime, g in inst.groupby("regime", sort=False):
            for metric in ("coverage", "mean_cross_tau"):
                s = g.set_index("group")[metric]
                defined = s.notna().all()
                rows.append(
                    {
                        "regime": regime,
                        "metric": metric,
                        "includes_zambia": includes_small,
                        "spread": s.max(skipna=False) - s.min(skipna=False),
                        "min_group": s.idxmin() if defined else None,
                        "min": s.min(skipna=False),
                        "max_group": s.idxmax() if defined else None,
                        "max": s.max(skipna=False),
                    }
                )
    return pd.DataFrame(rows)


def _spearman(g: pd.DataFrame) -> float:
    return g["self_tau_shap"].corr(g["cross_tau"], method="spearman")


def signal(d: pd.DataFrame) -> pd.DataFrame:
    """Does the cheap signal rank students by the expensive one inside an institution?

    The pooled coefficient mixes between-cohort differences into the answer. The
    mean within-cohort coefficient is what a cohort-calibrated gate can use,
    because it only ever compares students of the same cohort.
    """
    cols = ["self_tau_shap", "cross_tau"]
    within = d.groupby(["institution", "cohort_id"])[cols].apply(_spearman)
    out = pd.DataFrame(
        {
            "students": d.groupby("institution").size(),
            "cohorts": within.groupby(level="institution").size(),
            "spearman_pooled": d.groupby("institution")[cols].apply(_spearman),
            "spearman_within_cohort_mean": within.groupby(level="institution").mean(),
        }
    )
    out.loc[POOLED] = [len(d), len(within), _spearman(d), within.mean()]
    return out.astype({"students": int, "cohorts": int}).reset_index(names="group")


def cohort_resamples(
    d: pd.DataFrame, n_boot: int = N_BOOT, seed: int = SEED
) -> Iterator[pd.DataFrame]:
    """Cluster-bootstrap draws: whole cohorts, with replacement, within each institution.

    Drawing within institution keeps every institution in every draw, so the
    per-institution and pooled intervals come from the same replicates. A cohort
    drawn twice keeps its precomputed ranks and becomes two clusters.
    """
    rng = np.random.default_rng(seed)
    rows = d.groupby("cohort_id").indices
    by_inst = [np.sort(g.unique()) for _, g in d.groupby("institution")["cohort_id"]]
    for _ in range(n_boot):
        chosen = np.concatenate([rng.choice(ids, size=len(ids)) for ids in by_inst])
        idx = [rows[c] for c in chosen]
        yield d.iloc[np.concatenate(idx)].assign(
            cohort_id=np.repeat(np.arange(len(chosen)), [len(i) for i in idx])
        )


def attach_ci(
    point: pd.DataFrame, reps: pd.DataFrame, keys: list[str], metrics: list[str]
) -> pd.DataFrame:
    """95 % percentile interval of each metric from the bootstrap replicates.

    A replicate in which a group shows nobody has no value for it and is left out
    of that interval; ``<metric>_n_boot`` says how many replicates each one rests on.
    """
    q = reps.groupby(keys)[metrics]
    ci = pd.concat(
        [
            q.quantile(0.025).add_suffix("_ci_low"),
            q.quantile(0.975).add_suffix("_ci_high"),
            q.count().add_suffix("_n_boot"),
        ],
        axis=1,
    )
    out = point.merge(ci.reset_index(), on=keys, how="left")
    lead = [c for c in out.columns if c not in ci.columns and c not in metrics]
    tail = [f"{m}{s}" for m in metrics for s in ("", "_ci_low", "_ci_high", "_n_boot")]
    return out[lead + tail]


def check_against_exp025(run: str, curve: pd.DataFrame) -> None:
    """The global regime at GATE_TAU must be exp_025's own gate, or nothing here compares."""
    ours = curve.query("regime == 'global' and group == @POOLED and level == @GATE_TAU").iloc[0]
    ref = pd.read_csv(SRC / run / "gate_curve.csv").set_index("threshold").loc[GATE_TAU]
    expected = {m: float(ref[m]) for m in PRIMARY_REFERENCE}
    for m, value in expected.items():
        if abs(ours[m] - value) > 1e-4:
            raise RuntimeError(f"{run}: global@{GATE_TAU} {m} {ours[m]:.4f} != exp_025 {value:.4f}")
    if run == PRIMARY:
        for m, value in PRIMARY_REFERENCE.items():
            if abs(ours[m] - value) > 1e-4:
                raise RuntimeError(f"{run}: global@{GATE_TAU} {m} {ours[m]:.4f} != {value}")
    shown = ", ".join(f"{m} {v:.4f}" for m, v in expected.items())
    print(f"  sanity: global@{GATE_TAU} pooled matches exp_025 gate_curve.csv ({shown})")


def headline(run: str, d: pd.DataFrame, c_star: float, op, sp, sig) -> dict:
    """One summary.csv row: pooled numbers per regime and every cross-institution spread."""
    p = op[op["group"] == POOLED].set_index("regime")
    row = {"run": run, "students": len(d), "cohorts": d["cohort_id"].nunique(), "c_star": c_star}
    cols = ["coverage", "mean_cross_tau", "lift", "lift_ci_low", "lift_ci_high", "efficiency"]
    for r in (*REGIMES, DIFF):
        row.update({f"{r}_{m}": p.at[r, m] for m in cols})
    spreads = sp.set_index(["regime", "metric", "includes_zambia"])["spread"]
    for (r, metric, with_small), value in spreads.items():
        row[f"spread_{metric}_{r}" + ("" if with_small else "_no_zambia")] = value
    within = sig.set_index("group")["spearman_within_cohort_mean"]
    row["spearman_within_cohort_mean"] = within[POOLED]
    return row


def output_name(source: Path, run: str, quality: str) -> str:
    """exp_025 with its own cross_tau keeps the plain run name; anything else is
    prefixed with the source's experiment number and suffixed with the quality,
    so no two inputs collide as long as experiment numbers stay unique."""
    if source == SRC and quality == DEFAULT_QUALITY:
        return run
    return f"{''.join(source.name.split('_')[:2])}_{run}__{quality}"


def analyse(
    run: str, source: Path = SRC, quality: str = DEFAULT_QUALITY, out: Path | None = None
) -> dict:
    """``out`` sends the outputs outside OUT (exp_028 keeps its gate analyses with
    its own runs), where robustness(), which reads only OUT, never picks them up."""
    name = output_name(source, run, quality)
    out = out or OUT / name
    print(f"\n##### {name} #####", flush=True)
    d, dropped = load(source / run / "students.csv", quality)
    curve = curves(d)
    if name == run:
        check_against_exp025(run, curve)
    at_gate = curve.query("regime == 'global' and group == @POOLED and level == @GATE_TAU")
    c_star = float(at_gate["coverage"].iloc[0])
    op, sig = operating_point(d, c_star), signal(d)

    op_reps, sp_reps, sig_reps = [], [], []
    for b, f in enumerate(cohort_resamples(d)):
        op_b = operating_point(f, c_star)
        op_reps.append(op_b.assign(replicate=b))
        sp_reps.append(spread(op_b).assign(replicate=b))
        sig_reps.append(signal(f).assign(replicate=b))

    op = attach_ci(op, pd.concat(op_reps), ["regime", "group"], OP_METRICS)
    sp_keys = ["regime", "metric", "includes_zambia"]
    sp = attach_ci(spread(op), pd.concat(sp_reps), sp_keys, ["spread"])
    sig = attach_ci(
        sig,
        pd.concat(sig_reps),
        ["group"],
        ["spearman_pooled", "spearman_within_cohort_mean"],
    )
    row = headline(name, d, c_star, op, sp, sig)
    tb.write_outputs(
        out,
        curves=curve,
        operating_point=op,
        spread=sp,
        signal=sig,
        summary=pd.DataFrame([row]),
    )
    tb.dump_json(
        out / "config.json",
        {
            "source": str((source / run / "students.csv").relative_to(REPO)),
            "gate_signal": "self_tau_shap",
            "quality": [quality, jaccard_column(quality)],
            "gate_tau": GATE_TAU,
            "thresholds": THRESHOLDS.tolist(),
            "target_coverages": COVERAGES.tolist(),
            "c_star": c_star,
            "tie_break_seed": SEED,
            "bootstrap": {
                "resamples": N_BOOT,
                "seed": SEED,
                "unit": "cohort, with replacement, within institution",
                "interval": "percentile 2.5-97.5",
                "c_star_held_fixed": True,
                "undefined_replicates": "left out of the interval; <metric>_n_boot counts "
                "the replicates each interval rests on",
            },
            "students_used": len(d),
            "dropped_rows": dropped,
            "small_institution_flag": SMALL,
        },
    )

    with pd.option_context("display.width", 250, "display.max_columns", 30):
        print(f"\nc* = {c_star:.4f}; dropped rows {dropped}")
        print("\n=== operating point ===")
        print(op.drop(columns=["students"]).round(3).to_string(index=False))
        print("\n=== cross-institution spread ===")
        print(sp.round(3).to_string(index=False))
        print("\n=== signal: Spearman(self_tau_shap, cross_tau) ===")
        print(sig.round(3).to_string(index=False))
    return row


ROBUST_KEEP = [
    "c_star",
    "no_gate_mean_cross_tau",
    "calibrated_minus_global_mean_cross_tau",
    "calibrated_minus_global_lift_ci_low",
    "calibrated_minus_global_lift_ci_high",
    "global_efficiency",
    "cohort_calibrated_efficiency",
    "spread_mean_cross_tau_no_gate",
    "spread_mean_cross_tau_global",
    "spread_mean_cross_tau_cohort_calibrated",
    "spread_mean_cross_tau_no_gate_no_zambia",
    "spread_mean_cross_tau_global_no_zambia",
    "spread_mean_cross_tau_cohort_calibrated_no_zambia",
    "spearman_within_cohort_mean",
]


def robustness() -> pd.DataFrame:
    """One row per analysed input, so the week-1 reading can be checked against the
    quality measure: do the institution order, the spread and the within-cohort
    signal survive tie-aware tau-b and a different second method (LIME)?

    Built from what every output directory already holds, so it always covers
    every input analysed so far, whichever invocation ran last.
    """
    rows = []
    for config in sorted(OUT.glob("*/config.json")):
        run_dir = config.parent
        meta = json.loads(config.read_text())
        summary = pd.read_csv(run_dir / "summary.csv").iloc[0]
        row = {"output": run_dir.name, "source": meta["source"], "quality": meta["quality"][0]}
        row |= {k: summary[k] for k in ROBUST_KEEP}
        op = pd.read_csv(run_dir / "operating_point.csv")
        for r in op[op["regime"].isin(["no_gate", "global", "cohort_calibrated"])].itertuples():
            row[f"{r.regime}_{r.group}"] = r.mean_cross_tau
        within = pd.read_csv(run_dir / "signal.csv").set_index("group")
        row |= {f"spearman_within_{g}": v for g, v in within["spearman_within_cohort_mean"].items()}
        rows.append(row)
    return pd.DataFrame(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=SRC.name, help="experiment dir holding <run>/students.csv")
    ap.add_argument("--runs", default=None, help="comma list; default every run in --source")
    ap.add_argument("--quality", default=DEFAULT_QUALITY, help="comma list of agreement columns")
    args = ap.parse_args()
    source = EXPERIMENTS / args.source
    runs = (
        args.runs.split(",")
        if args.runs
        else sorted(p.parent.name for p in source.glob("*/students.csv"))
    )
    rows = [analyse(run, source, q) for run in runs for q in args.quality.split(",")]
    if source == SRC and args.quality == DEFAULT_QUALITY and not args.runs:
        tb.write_outputs(OUT, summary=pd.DataFrame(rows))
    tb.write_outputs(OUT, robustness=robustness())
    print("\nwritten to", OUT)


if __name__ == "__main__":
    main()
