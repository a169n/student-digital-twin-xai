"""exp_027 — is exp_025's cross-estimator agreement a property of one pair?

exp_025 found TreeSHAP and occlusion agree on a student's factor list at a mean
tau of about 0.35. One pair cannot say whether that is what local attribution
looks like on these models or what these two methods in particular do to each
other. This adds LIME — built differently from both (a weighted linear surrogate
fitted on discretised perturbations) — and reports the agreement matrix over the
three methods: the diagonal is each estimator's self-agreement across repeats,
the off-diagonal its agreement with another estimator on the same repeat.

KernelSHAP rides along as a control, not a fourth method. With 7 features it
enumerates every coalition, so on the predicted probability it is the exact
interventional Shapley value and differs from "shap" (TreeSHAP on log-odds) only
by the output space. How far it moves toward occlusion, which also measures
probability, is how much of the shap-occlusion gap is the link function rather
than the attribution method.

LIME is the only estimator with sampling noise of its own; lime_seed_tau reruns
it with nothing but its seed changed, so its self-agreement can be read against
that floor.

Every cell is reported twice. tau_strict is exp_025's statistic on factor lists
and stays for continuity; tau_b is computed on the |attribution| values, so
exact ties stay ties instead of being ordered by feature index. The difference
matters for occlusion, which ties often (ties.csv says how often), and for
nothing else.

The cohorts, split, model, backgrounds and repeats are exp_025's
(run_local_stability.cohort_students), so the shap/occlusion columns of a
matching run should reproduce exp_025's; the runner prints the difference.

Usage (from services/ml):
    uv run python -m src.experiments.run_estimator_matrix
"""

from __future__ import annotations

import argparse
import itertools
import os
import time
from concurrent.futures import ProcessPoolExecutor
from importlib.metadata import version
from pathlib import Path

import numpy as np
import pandas as pd

from src.experiments import run_local_stability as ls
from src.experiments import transfer_benchmark as tb

OUT = ls.REPO / "data" / "artifacts" / "experiments" / "exp_027_local_estimator_matrix"
N_BOOT = 1000


def _cells(estimators: tuple[str, ...]):
    """(metric, est_a, est_b, kind, tau column, jaccard column): diagonal, then pairs.

    Top-3 Jaccard is a statistic of the strict lists, so tau_b rows carry none.
    """
    for metric, tau in (("tau_strict", "tau"), ("tau_b", "taub")):
        strict = metric == "tau_strict"
        for est in estimators:
            jaccard = f"self_jaccard_{est}" if strict else None
            yield metric, est, est, "self", f"self_{tau}_{est}", jaccard
        for a, b in itertools.combinations(estimators, 2):
            jaccard = f"cross_jaccard_top3_{a}__{b}" if strict else None
            yield metric, a, b, "cross", f"cross_{tau}_{a}__{b}", jaccard


def agreement_matrix(
    frame: pd.DataFrame, estimators: tuple[str, ...], *, n_boot: int = N_BOOT, seed: int = 0
) -> pd.DataFrame:
    """Long-form agreement matrix with 95% CIs from a cluster bootstrap over cohorts.

    Cohorts, not students, are resampled: the students of one cohort share a
    model and every background draw, so they are not independent observations,
    and a student-level bootstrap would report intervals far too narrow.
    """
    cohorts = frame["cohort_id"].unique()
    draws = np.random.default_rng(seed).integers(0, len(cohorts), size=(n_boot, len(cohorts)))
    per_cohort = frame.groupby("cohort_id", sort=False)
    rows = []
    for metric, a, b, kind, tau_col, jaccard_col in _cells(estimators):
        sums = per_cohort[tau_col].sum().reindex(cohorts).to_numpy()
        counts = per_cohort[tau_col].count().reindex(cohorts).to_numpy()
        boot = sums[draws].sum(axis=1) / counts[draws].sum(axis=1)
        rows.append(
            {
                "metric": metric,
                "est_a": a,
                "est_b": b,
                "kind": kind,
                "tau_mean": float(frame[tau_col].mean()),
                "tau_ci_low": float(np.percentile(boot, 2.5)),
                "tau_ci_high": float(np.percentile(boot, 97.5)),
                "jaccard_top3_mean": float(frame[jaccard_col].mean()) if jaccard_col else np.nan,
                "n_students": int(frame[tau_col].notna().sum()),  # tau_b: undefined if constant
            }
        )
    return pd.DataFrame(rows)


def square(matrix: pd.DataFrame, metric: str) -> pd.DataFrame:
    """Square tau table; Kendall tau is symmetric, so each pair fills both of its cells."""
    matrix = matrix[matrix["metric"] == metric]
    order = list(matrix.loc[matrix["kind"] == "self", "est_a"])
    cross = matrix[matrix["kind"] == "cross"]
    mirrored = cross.rename(columns={"est_a": "est_b", "est_b": "est_a"})
    full = pd.concat([matrix, mirrored])
    wide = full.pivot(index="est_a", columns="est_b", values="tau_mean").loc[order, order]
    return wide.rename_axis(index="estimator", columns=None).reset_index()


def lime_noise(frame: pd.DataFrame) -> pd.DataFrame:
    """LIME's seed-only noise floor, next to its self-agreement across repeats."""
    groups = [("all", frame), *frame.groupby("institution", sort=False)]
    return pd.DataFrame(
        {
            "group": name,
            "students": int(g["lime_seed_tau"].notna().sum()),
            "mean_lime_seed_tau": float(g["lime_seed_tau"].mean()),
            "median_lime_seed_tau": float(g["lime_seed_tau"].median()),
            "p10_lime_seed_tau": float(g["lime_seed_tau"].quantile(0.10)),
            "mean_self_tau_lime": float(g["self_tau_lime"].mean()),
        }
        for name, g in groups
    )


def ties(frame: pd.DataFrame, estimators: tuple[str, ...]) -> pd.DataFrame:
    """How much tie-breaking the strict columns contain, per institution and estimator."""
    groups = [("all", frame), *frame.groupby("institution", sort=False)]
    return pd.DataFrame(
        {
            "group": name,
            "estimator": est,
            "students": len(g),
            "mean_tied": float(g[f"tied_{est}"].mean()),
            "mean_zeros": float(g[f"zeros_{est}"].mean()),
        }
        for name, g in groups
        for est in estimators
    )


def summarise(frame: pd.DataFrame) -> pd.DataFrame:
    metrics = [c for c in frame.columns if c.startswith(("self_", "cross_", "lime_seed_"))]
    return pd.DataFrame(
        {
            "metric": m,
            "students": int(frame[m].notna().sum()),
            "mean": float(frame[m].mean()),
            "sd": float(frame[m].std()),
            "p10": float(frame[m].quantile(0.10)),
            "median": float(frame[m].median()),
        }
        for m in metrics
    )


def _timed(cohort: tb.Cohort, kwargs: dict) -> tuple[list[dict], float]:
    start = time.perf_counter()
    rows = ls.cohort_students(cohort, **kwargs)
    return rows, time.perf_counter() - start


def _compare_with_exp025(frame: pd.DataFrame, run: str) -> None:
    """Reference only: the frozen run may come from another platform or library build."""
    path = ls.OUT / run / "students.csv"
    if not path.exists():
        print(f"\n(no exp_025 run at {path}; nothing to compare)")
        return
    merged = frame.merge(
        pd.read_csv(path), on=["cohort_id", "student_row"], suffixes=("", "_exp025")
    )
    print(f"\n=== vs exp_025 {run} ({len(merged)} of {len(frame)} students matched) ===")
    for col in (
        "p_risk",
        "self_tau_shap",
        "self_tau_occlusion",
        "self_jaccard_shap",
        "cross_tau",
        "cross_jaccard_top3",
    ):
        if col in frame:
            diff = merged[col] - merged[f"{col}_exp025"]
            differ = diff.abs() > 1e-12
            print(
                f"  {col:20s} differ {differ.mean():6.2%}  mean diff {diff.mean():+.3g}  "
                f"max |diff| {diff.abs().max():.3g}  "
                f"cohorts {sorted(merged.loc[differ, 'cohort_id'].unique())}"
            )


def run_matrix(
    out_dir: Path,
    cohorts: list[tb.Cohort],
    *,
    fraction: float,
    seed: int,
    repeats: int,
    background: int,
    vary: str,
    estimators: tuple[str, ...],
    workers: int,
    limit_cohorts: int | None,
    model: str = ls.MODEL,
    experiment: str = OUT.name,
    extra: dict | None = None,
) -> dict[str, pd.DataFrame]:
    """Compute one run over ``cohorts`` and write its file set into ``out_dir``.

    exp_028 calls this once per (cutoff, model family), so every cell of its grid
    is computed and written exactly as exp_027's run was. ``extra`` is appended
    to config.json for what only such a caller knows.
    """
    print(f"cohorts: {len(cohorts)}, estimators: {estimators}, workers: {workers}", flush=True)
    kwargs = dict(
        seed=seed,
        repeats=repeats,
        background=background,
        vary=vary,
        estimators=estimators,
        model_name=model,
    )
    start = time.perf_counter()
    rows: list[dict] = []
    # map() yields in submission order, so the output equals a sequential run.
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for cohort, (cohort_rows, seconds) in zip(
            cohorts, pool.map(_timed, cohorts, itertools.repeat(kwargs)), strict=True
        ):
            rows.extend(cohort_rows)
            print(
                f"  {cohort.cohort_id:26s} {len(cohort_rows):4d} students {seconds:7.1f}s",
                flush=True,
            )
    wall = time.perf_counter() - start

    frame = pd.DataFrame(rows)
    matrix = agreement_matrix(frame, estimators)
    by_institution = pd.concat(
        [
            agreement_matrix(g, estimators).assign(institution=inst)
            for inst, g in frame.groupby("institution", sort=False)
        ]
    )
    outputs = dict(
        students=frame,
        matrix=matrix,
        matrix_wide_strict=square(matrix, "tau_strict"),
        matrix_wide_taub=square(matrix, "tau_b"),
        by_institution=by_institution[["institution", *matrix.columns]],
        ties=ties(frame, estimators),
        summary=summarise(frame),
    )
    if "lime" in estimators:
        outputs["lime_noise"] = lime_noise(frame)
    tb.write_outputs(out_dir, **outputs)
    tb.dump_json(
        out_dir / "config.json",
        {
            "experiment": experiment,
            "model": model,
            "vary": vary,
            "fraction": fraction,
            "seed": seed,
            "repeats": repeats,
            "background_size": background,
            "estimators": list(estimators),
            "cohorts": len(cohorts),
            "limit_cohorts": limit_cohorts,
            "students": len(frame),
            "eval_cap": ls.EVAL_CAP,
            "top_k": ls.TOP_K,
            "flag_rate": tb.FLAG_RATE,
            # Library defaults, not passed explicitly; recorded so a lime upgrade is visible.
            "lime": {
                "training_data": "the repeat's background sample",
                "discretize_continuous": True,
                "discretizer": "quartile",
                "kernel_width": "default 0.75 * sqrt(n_features)",
                "num_samples": 5000,
                "num_features": len(tb.CANON),
                "labels": [1],
                "random_state": "seed in every repeat; seed + 1 for lime_seed_tau",
            },
            "kernelshap_prob": {
                "output": "predict_proba[:, 1]",
                "nsamples": "auto",
                "coalitions_enumerated": 2 ** len(tb.CANON) - 2,
                "l1_reg": False,  # shap's default LARS selection zeroes small values
            },
            "agreement": {
                "tau_strict": "Kendall tau on factor-list positions (exp_025); ties by index",
                "tau_b": "scipy Kendall tau-b on |attribution|; constant vectors skipped",
            },
            "bootstrap": {"unit": "cohort", "resamples": N_BOOT, "seed": 0},
            "workers": workers,
            "wall_seconds": round(wall, 1),
            "versions": {pkg: version(pkg) for pkg in ("shap", "lime", "scikit-learn", "numpy")},
            **(extra or {}),
        },
    )

    print(f"\nwall time {wall:.1f}s for {len(frame)} students")
    return outputs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fraction", type=float, default=0.33)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--background", type=int, default=50)
    ap.add_argument("--vary", choices=ls.VARY_MODES, default="background")
    ap.add_argument("--estimators", default="shap,occlusion,lime,kernelshap_prob")
    ap.add_argument("--workers", type=int, default=max(1, min(8, (os.cpu_count() or 1) - 2)))
    ap.add_argument("--limit-cohorts", type=int, default=None, help="first N cohorts only")
    ap.add_argument("--run", default=None, help="output subfolder; defaults to f<pct>_<vary>")
    args = ap.parse_args()
    run = args.run or f"f{int(round(args.fraction * 100))}_{args.vary}"
    estimators = tuple(args.estimators.split(","))
    if estimators == ls.DEFAULT_ESTIMATORS:
        # cohort_students writes only exp_025's legacy columns for this pair.
        ap.error("shap,occlusion alone is exp_025 (run_local_stability); add an estimator")

    outputs = run_matrix(
        OUT / run,
        ls.load_cohorts(args.fraction)[: args.limit_cohorts],
        fraction=args.fraction,
        seed=args.seed,
        repeats=args.repeats,
        background=args.background,
        vary=args.vary,
        estimators=estimators,
        workers=args.workers,
        limit_cohorts=args.limit_cohorts,
    )
    matrix = outputs["matrix"]
    print("\n=== agreement matrix (diagonal = self across repeats, off = cross) ===")
    print(matrix.round(3).to_string(index=False))
    for metric in ("tau_strict", "tau_b"):
        print(f"\n{metric}")
        print(square(matrix, metric).round(3).to_string(index=False))
    print("\n=== exact ties in |attribution| ===")
    print(outputs["ties"].round(3).to_string(index=False))
    if "lime" in estimators:
        print("\n=== LIME seed-only noise floor ===")
        print(outputs["lime_noise"].round(3).to_string(index=False))
    _compare_with_exp025(outputs["students"], run)


if __name__ == "__main__":
    main()
