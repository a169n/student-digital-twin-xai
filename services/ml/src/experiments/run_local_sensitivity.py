"""exp_028 — which week-2 findings belong to the data, and which to one configuration?

exp_027 measured local-attribution agreement at one course cutoff (1/3) on one
model family (gradient boosting): SHAP reproduces itself best, then occlusion,
then LIME; every cross pair sits below both of its members; occlusion-LIME is
the lowest pair; the SHAP-occlusion gap between institutions is not shared by
SHAP-LIME; and exp_026's gate signal ranks students within a cohort while
per-cohort calibration adds nothing over one global threshold. Any of these can
be a property of the students' data or of that one configuration. This repeats
exp_027's f33_background measurement over a grid of 3 cutoffs (0.25, 0.33, 0.50
of the course) x 3 families (gradient boosting, logistic regression, random
forest), everything else fixed, and runs exp_026's gate analysis on each cell.

Each claim is a rule with a fixed threshold (CRITERIA), written before the full
grid ran, and conditions.csv says per cell whether it holds. A claim that holds
in every cell whose model learned something reads as a property of the data; one
that flips with the family or the cutoff belongs to the configuration, and the
cells where it fails bound where it may be stated. A weak model (mean
within-cohort AUC below 0.60) is flagged rather than dropped: its explanations
describe little, so a failure there says little about the data.

"shap" keeps one meaning in every family, the exact interventional Shapley value
of the raw output (run_local_stability._shap_matrix). A random forest's raw
output is the probability, so there shap and kernelshap_prob coincide and the
link-function control (C4) has nothing to separate.

GBM at 0.33 is exp_027's f33_background run by construction, so its students.csv
must come out byte-identical; the runner stops if it does not.

Usage (from services/ml):
    uv run python -m src.experiments.run_local_sensitivity --workers 8
    uv run python -m src.experiments.run_local_sensitivity --limit-cohorts 3 \\
        --out exp_028_local_sensitivity_smoke
"""

from __future__ import annotations

import argparse
import inspect
import os
from collections.abc import Callable, Mapping
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from src.experiments import run_estimator_matrix as em
from src.experiments import run_gate_calibration as gc
from src.experiments import run_local_stability as ls
from src.experiments import transfer_benchmark as tb

OUT = gc.EXPERIMENTS / "exp_028_local_sensitivity"
SHORT = {"gradient_boosting": "gbm", "logistic_regression": "lr", "random_forest": "rf"}
SHAP_OUTPUT = {
    "gradient_boosting": "TreeSHAP, interventional, on log-odds",
    "logistic_regression": "KernelSHAP over all 126 coalitions on decision_function (log-odds)",
    "random_forest": "TreeSHAP, interventional, on the mean tree probability",
}
MODEL_THREADS = (
    "one thread per fit (run_local_stability._build sets n_jobs=1 on the random forest); "
    "the cohort pool is the parallelism. A threaded forest's predict_proba is not "
    "bit-reproducible and leaves 1e-16 residues where occlusion should be exactly zero."
)
ESTIMATORS = ("shap", "occlusion", "lime", "kernelshap_prob")
RUN = dict(seed=0, repeats=5, background=50, vary="background")  # exp_027 f33_background
REFERENCE = ("f33_gbm", em.OUT / "f33_background" / "students.csv")
PAIRS = (("shap", "occlusion"), ("shap", "lime"), ("occlusion", "lime"))
QUALITIES = {"occlusion": "cross_taub_shap__occlusion", "lime": "cross_taub_shap__lime"}
LARGE = ("KU Leuven", "OULAD", "Oviedo", "UKZN")

# Pre-specified: fixed in code before the full grid ran, never tuned on its results.
TIE_TOL = 0.03  # C3
LINK_TOL = 0.03  # C4
MIN_C_STAR = 0.05  # C6
SPREAD_RATIO = 0.5  # C7
WEAK_AUC = 0.60
YES, NO, NA = "yes", "no", "not_evaluable"


def config_name(fraction: float, model: str) -> str:
    return f"f{int(round(fraction * 100))}_{SHORT[model]}"


def _slug(institution: str) -> str:
    return institution.lower().replace(" ", "_")


def check_reference(students: Path, limit_cohorts: int | None) -> None:
    """GBM at 0.33 is exp_027's f33_background: same code path, same machine, same bytes.

    A partial run is held to its own cohorts' rows. A mismatch means the refactor
    or the model-aware estimators moved exp_027's numbers, and then no cell of
    this grid is comparable with week 2.
    """
    ours = students.read_text()
    lines = REFERENCE[1].read_text().splitlines(keepends=True)
    ids = {line.split(",", 1)[0] for line in ours.splitlines()[1:]}
    expected = "".join(lines[:1] + [x for x in lines[1:] if x.split(",", 1)[0] in ids])
    if ours != (expected if limit_cohorts else "".join(lines)):
        raise RuntimeError(f"{students} differs from {REFERENCE[1]}")
    print(
        f"  reference: {REFERENCE[0]} students.csv == exp_027 f33_background ({len(ids)} cohorts)"
    )


def model_auc(students: pd.DataFrame) -> float:
    """Mean within-cohort AUC on the held-out third.

    p_risk is P(pass) (the TODO(ml) in cohort_students) and y = 1 means passed, so
    AUC(y, p_risk) already has the right orientation. Within cohorts, because a
    pooled AUC would also score between-cohort pass-rate differences.
    """
    per_cohort = [
        roc_auc_score(g["y"], g["p_risk"])
        for _, g in students.groupby("cohort_id")
        if g["y"].nunique() == 2
    ]
    return float(np.mean(per_cohort))


def _gate_columns(gate_dir: Path, prefix: str) -> dict:
    s = pd.read_csv(gate_dir / "summary.csv").iloc[0]
    within = pd.read_csv(gate_dir / "signal.csv").set_index("group")
    w = "spearman_within_cohort_mean"
    cols = {
        "c_star": s["c_star"],
        "global_lift": s["global_lift"],
        "global_lift_ci_low": s["global_lift_ci_low"],
        "global_lift_ci_high": s["global_lift_ci_high"],
        "cal_minus_global": s["calibrated_minus_global_lift"],
        "cal_minus_global_ci_low": s["calibrated_minus_global_lift_ci_low"],
        "cal_minus_global_ci_high": s["calibrated_minus_global_lift_ci_high"],
        "spearman_within": within.at[gc.POOLED, w],
        "spearman_within_ci_low": within.at[gc.POOLED, f"{w}_ci_low"],
        "spearman_within_ci_high": within.at[gc.POOLED, f"{w}_ci_high"],
        **{
            f"spearman_within_ci_low_{_slug(inst)}": within[f"{w}_ci_low"].get(inst, np.nan)
            for inst in LARGE
        },
        "spread_no_gate": s["spread_mean_cross_tau_no_gate"],
        "spread_no_gate_no_zambia": s["spread_mean_cross_tau_no_gate_no_zambia"],
    }
    return {prefix + k: v for k, v in cols.items()}


def sensitivity_row(out: Path, fraction: float, model: str) -> dict:
    """One config's headline numbers, read back from its run and gate outputs."""
    name = config_name(fraction, model)
    students = pd.read_csv(out / name / "students.csv")
    row = {
        "config": name,
        "fraction": fraction,
        "model": model,
        "cohorts": students["cohort_id"].nunique(),
        "students": len(students),
        "institutions": ";".join(sorted(students["institution"].unique())),
        "auc_mean": model_auc(students),
    }
    cells = pd.read_csv(out / name / "matrix.csv").set_index(["metric", "est_a", "est_b"])
    wanted = [("tau_b", e, e, f"taub_self_{e}") for e in ("shap", "occlusion", "lime")]
    wanted += [
        ("tau_b", a, b, f"taub_{a}__{b}")
        for a, b in (*PAIRS, ("shap", "kernelshap_prob"), ("occlusion", "kernelshap_prob"))
    ]
    wanted.append(("tau_strict", "shap", "occlusion", "strict_shap__occlusion"))
    for metric, a, b, col in wanted:
        cell = cells.loc[(metric, a, b)]
        row |= {
            col: cell["tau_mean"],
            f"{col}_ci_low": cell["tau_ci_low"],
            f"{col}_ci_high": cell["tau_ci_high"],
        }
    ties = pd.read_csv(out / name / "ties.csv").set_index(["group", "estimator"])
    row["occlusion_tie_share"] = ties.at[("all", "occlusion"), "mean_tied"]
    lime = pd.read_csv(out / name / "lime_noise.csv").set_index("group")
    row["lime_seed_tau"] = lime.at["all", "mean_lime_seed_tau"]
    for method, quality in QUALITIES.items():
        row |= _gate_columns(out / "gate" / f"{name}__{quality}", f"gate_{method}_")
    return row


# --- pre-specified criteria: one sensitivity row in, (holds, numbers used) out ---


def _missing(*values) -> bool:
    return any(pd.isna(v) for v in values)


def _verdict(ok: bool, evidence: str) -> tuple[str, str]:
    return (YES if ok else NO), evidence


def _all_of(terms: list[tuple[str, bool | None, str]]) -> tuple[str, str]:
    """A "for every ..." rule over (label, passes or None if undefined, evidence).

    One defined failure already decides it, so NO outranks an undefined term;
    not_evaluable only when every defined term passes and some are undefined.
    """
    evidence = "; ".join(e for _, _, e in terms)
    if any(ok is False for _, ok, _ in terms):
        return NO, evidence
    undefined = [label for label, ok, _ in terms if ok is None]
    if undefined:
        return NA, f"undefined: {', '.join(undefined)}; {evidence}"
    return YES, evidence


def c1_cross_below_self(r: Mapping) -> tuple[str, str]:
    """C1 every cross pair sits below both members' self-agreement.

    Rule: for each of shap-occlusion, shap-lime and occlusion-lime, the tau-b
    cross interval's ci_high < min(ci_low of the two members' tau-b self
    intervals). Intervals are exp_027's cohort-bootstrap 95 % from matrix.csv.
    """
    terms = []
    for a, b in PAIRS:
        high = r[f"taub_{a}__{b}_ci_high"]
        lows = (r[f"taub_self_{a}_ci_low"], r[f"taub_self_{b}_ci_low"])
        if _missing(high, *lows):
            terms.append((f"{a}__{b}", None, f"{a}__{b} undefined"))
            continue
        evidence = f"{a}__{b} hi {high:.3f} vs self lo {min(lows):.3f}"
        terms.append((f"{a}__{b}", bool(high < min(lows)), evidence))
    return _all_of(terms)


def c2_occlusion_lime_lowest(r: Mapping) -> tuple[str, str]:
    """C2 occlusion-LIME is the lowest pair.

    Rule: its tau-b mean is strictly the smallest of the three cross means AND its
    ci_high < ci_low of both SHAP pairs (shap-occlusion, shap-lime).
    """
    mean = {f"{a}__{b}": r[f"taub_{a}__{b}"] for a, b in PAIRS}
    high = r["taub_occlusion__lime_ci_high"]
    lows = (r["taub_shap__occlusion_ci_low"], r["taub_shap__lime_ci_low"])
    if _missing(*mean.values(), high, *lows):
        return NA, "a cross cell is undefined"
    ok = mean["occlusion__lime"] < min(mean["shap__occlusion"], mean["shap__lime"])
    ok &= high < min(lows)
    means = ", ".join(f"{k} {v:.3f}" for k, v in mean.items())
    return _verdict(bool(ok), f"means {means}; occlusion__lime hi {high:.3f} vs {min(lows):.3f}")


def c3_ties_do_not_drive_agreement(r: Mapping) -> tuple[str, str]:
    """C3 occlusion ties do not drive SHAP-occlusion agreement.

    Rule: |tau-b - tau_strict| < 0.03 for pooled shap-occlusion.
    """
    taub, strict = r["taub_shap__occlusion"], r["strict_shap__occlusion"]
    if _missing(taub, strict):
        return NA, "undefined"
    diff = taub - strict
    return _verdict(abs(diff) < TIE_TOL, f"tau_b {taub:.3f} - strict {strict:.3f} = {diff:+.3f}")


def c4_output_space_explains_little(r: Mapping) -> tuple[str, str]:
    """C4 output space explains little of the SHAP-occlusion gap.

    Rule: |tau-b(kernelshap_prob, occlusion) - tau-b(shap, occlusion)| < 0.03
    pooled. not_evaluable for the random forest: its raw output already is the
    probability, so the difference is zero by construction, not by measurement.
    """
    if r["model"] == "random_forest":
        return NA, "shap is already in probability space"
    prob, raw = r["taub_occlusion__kernelshap_prob"], r["taub_shap__occlusion"]
    if _missing(prob, raw):
        return NA, "undefined"
    diff = prob - raw
    return _verdict(abs(diff) < LINK_TOL, f"prob {prob:.3f} - raw {raw:.3f} = {diff:+.3f}")


def c5_gate_signal_within_institutions(r: Mapping) -> tuple[str, str]:
    """C5 the gate signal is informative within institutions.

    Rule: for BOTH qualities (shap-occlusion, shap-lime), the mean within-cohort
    Spearman(self_tau_shap, quality) has cohort-bootstrap ci_low > 0 in every
    large institution (KU Leuven, OULAD, Oviedo, UKZN). not_evaluable when any of
    those intervals is undefined (institution absent, or its signal constant).
    """
    lows = {
        f"{method}/{inst}": r.get(f"gate_{method}_spearman_within_ci_low_{_slug(inst)}", np.nan)
        for method in QUALITIES
        for inst in LARGE
    }
    return _all_of(
        [
            (k, None, f"{k} undefined") if _missing(v) else (k, bool(v > 0), f"{k} lo {v:.3f}")
            for k, v in lows.items()
        ]
    )


def c6_calibration_adds_nothing(r: Mapping) -> tuple[str, str]:
    """C6 cohort calibration adds nothing over one global threshold.

    Rule: calibrated-minus-global retained agreement at c* has pooled ci_low <= 0
    for both qualities. not_evaluable when c* < 0.05 for either quality: the
    matched operating point then shows almost nobody and compares nothing.
    """
    values = {m: (r[f"gate_{m}_c_star"], r[f"gate_{m}_cal_minus_global_ci_low"]) for m in QUALITIES}
    if _missing(*(v for pair in values.values() for v in pair)):
        return NA, "undefined"
    evidence = "; ".join(f"{m} c* {c:.3f}, ci_low {lo:+.3f}" for m, (c, lo) in values.items())
    if min(c for c, _ in values.values()) < MIN_C_STAR:
        return NA, evidence
    return _verdict(all(lo <= 0 for _, lo in values.values()), evidence)


def c7_spread_not_replicated(r: Mapping) -> tuple[str, str]:
    """C7 the SHAP-occlusion institution spread is not replicated by SHAP-LIME.

    Rule: no-gate spread without Zambia for shap-lime < 0.5 x that for
    shap-occlusion. not_evaluable with fewer than two large institutions (the
    spread of one institution is zero by construction) or an undefined spread.
    """
    lime = r["gate_lime_spread_no_gate_no_zambia"]
    occlusion = r["gate_occlusion_spread_no_gate_no_zambia"]
    present = [i for i in LARGE if i in str(r["institutions"]).split(";")]
    if len(present) < 2 or _missing(lime, occlusion):
        return NA, f"large institutions present: {len(present)}"
    return _verdict(
        lime < SPREAD_RATIO * occlusion,
        f"shap__lime {lime:.3f} vs {SPREAD_RATIO} x shap__occlusion {occlusion:.3f}",
    )


CRITERIA: dict[str, Callable[[Mapping], tuple[str, str]]] = {
    "C1": c1_cross_below_self,
    "C2": c2_occlusion_lime_lowest,
    "C3": c3_ties_do_not_drive_agreement,
    "C4": c4_output_space_explains_little,
    "C5": c5_gate_signal_within_institutions,
    "C6": c6_calibration_adds_nothing,
    "C7": c7_spread_not_replicated,
}


def conditions(sensitivity: pd.DataFrame) -> pd.DataFrame:
    """claim x config verdicts, each with the model-quality flag of its config."""
    rows = []
    for claim, rule in CRITERIA.items():
        for r in sensitivity.to_dict("records"):
            holds, evidence = rule(r)
            rows.append(
                {
                    "claim": claim,
                    "statement": inspect.getdoc(rule).splitlines()[0].split(" ", 1)[1],
                    "config": r["config"],
                    "fraction": r["fraction"],
                    "model": r["model"],
                    "holds": holds,
                    "evidence": evidence,
                    "auc_mean": r["auc_mean"],
                    "model_flag": "weak model" if r["auc_mean"] < WEAK_AUC else "ok",
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fractions", default="0.25,0.33,0.50")
    ap.add_argument("--models", default=",".join(SHORT))
    ap.add_argument("--workers", type=int, default=max(1, min(8, (os.cpu_count() or 1) - 2)))
    ap.add_argument("--limit-cohorts", type=int, default=None, help="first N cohorts only")
    ap.add_argument("--configs-only", action="store_true", help="skip gate analysis and tables")
    ap.add_argument("--force", action="store_true", help="recompute outputs that already exist")
    ap.add_argument("--out", default=OUT.name, help="experiment dir under data/.../experiments")
    args = ap.parse_args()
    out = gc.EXPERIMENTS / args.out
    if args.limit_cohorts is not None and out == OUT:
        # A partial config there would later be skipped as done by the full run.
        ap.error("--limit-cohorts writes a partial grid; send it elsewhere with --out")
    grid = [(float(f), m) for f in args.fractions.split(",") for m in args.models.split(",")]
    unknown = sorted({m for _, m in grid} - set(SHORT))
    if unknown:
        ap.error(f"unknown models {unknown}; known: {list(SHORT)}")

    fresh: set[str] = set()
    cohorts: dict[float, list[tb.Cohort]] = {}
    for fraction, model in grid:
        name = config_name(fraction, model)
        if (out / name / "students.csv").exists() and not args.force:
            print(f"{name}: outputs exist, skipped (--force recomputes)", flush=True)
            if name == REFERENCE[0]:  # a skipped reference is checked all the same
                check_reference(out / name / "students.csv", args.limit_cohorts)
            continue
        if fraction not in cohorts:  # one cutoff in memory at a time
            cohorts = {fraction: ls.load_cohorts(fraction)[: args.limit_cohorts]}
        print(f"\n##### {name} #####", flush=True)
        em.run_matrix(
            out / name,
            cohorts[fraction],
            fraction=fraction,
            estimators=ESTIMATORS,
            workers=args.workers,
            limit_cohorts=args.limit_cohorts,
            model=model,
            experiment=OUT.name,
            extra={"shap": SHAP_OUTPUT[model], "model_threads": MODEL_THREADS},
            **RUN,
        )
        if name == REFERENCE[0]:
            check_reference(out / name / "students.csv", args.limit_cohorts)
        fresh.add(name)
    if args.configs_only:
        return

    for fraction, model in grid:
        name = config_name(fraction, model)
        for quality in QUALITIES.values():
            target = out / "gate" / f"{name}__{quality}"
            if (target / "summary.csv").exists() and name not in fresh and not args.force:
                continue
            gc.analyse(name, out, quality, out=target)

    sensitivity = pd.DataFrame([sensitivity_row(out, f, m) for f, m in grid])
    verdicts = conditions(sensitivity)
    tb.write_outputs(out, sensitivity=sensitivity, conditions=verdicts)
    tb.dump_json(
        out / "config.json",
        {
            "experiment": OUT.name,
            "fractions": sorted({f for f, _ in grid}),
            "models": list(dict.fromkeys(m for _, m in grid)),
            "per_config": {**RUN, "estimators": list(ESTIMATORS)},
            "limit_cohorts": args.limit_cohorts,
            "workers": args.workers,
            "model_threads": MODEL_THREADS,
            "shap_output": SHAP_OUTPUT,
            "reference": f"{REFERENCE[0]}/students.csv == {REFERENCE[1].relative_to(ls.REPO)}",
            "gate": {
                "analysis": "run_gate_calibration.analyse, into gate/<config>__<quality>/",
                "qualities": list(QUALITIES.values()),
            },
            "auc": "mean over cohorts of roc_auc_score(y, p_risk); p_risk is P(pass)",
            "weak_model_auc": WEAK_AUC,
            "criteria": {claim: inspect.getdoc(rule) for claim, rule in CRITERIA.items()},
        },
    )
    with pd.option_context("display.width", 250, "display.max_columns", 40):
        print("\n=== sensitivity ===")
        print(sensitivity.round(3).to_string(index=False))
        print("\n=== conditions (claim x config) ===")
        print(verdicts.pivot(index="claim", columns="config", values="holds").to_string())
    print("\nwritten to", out)


if __name__ == "__main__":
    main()
