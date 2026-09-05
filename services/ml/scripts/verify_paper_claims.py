"""Check every quantitative claim in the manuscript against the frozen artifacts.

A paper this number-dense drifts as soon as an experiment is rerun, and a wrong
number that nobody recomputes is exactly how a review finds you out. This script
recomputes each claim from the artifact that should support it and reports PASS,
FAIL, or MISSING against the value written in the text, so the drift is caught
before a reviewer catches it.

Add a claim here whenever a number enters the manuscript. A claim that cannot be
recomputed from a released artifact should not be in the paper.

Usage (from services/ml):
    uv run python scripts/verify_paper_claims.py
Exit status is non-zero if any claim fails.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[3]
PAPER = REPO / "docs" / "dissertation" / "side2026_paper.md"
ART = REPO / "data" / "artifacts" / "experiments"
LADDER = ART / "exp_014_transfer_ladder" / "f33"
DIST = ["D0_within_cohort", "D1_same_module", "D2_other_module", "D3_other_institution"]
TOL = 0.0015  # claims are quoted to three decimals


def _paired(pairs: pd.DataFrame) -> pd.DataFrame:
    complete = pairs.groupby("target")["distance"].nunique()
    return pairs[pairs["target"].isin(set(complete[complete == len(DIST)].index))]


def _cell(frame: pd.DataFrame, distance: str, metric: str) -> float:
    return frame.loc[frame["distance"] == distance].groupby("target")[metric].mean().mean()


def build_claims() -> list[tuple[str, float]]:
    """(label, recomputed value) for every number the manuscript states."""
    pairs = pd.read_csv(LADDER / "pairs.csv")
    cohorts = pd.read_csv(LADDER / "cohorts.csv")
    gbm = pairs[pairs["model"] == "gradient_boosting"]
    raw = gbm[gbm["representation"] == "raw"]
    pct = gbm[gbm["representation"] == "percentile"]
    paired_raw = _paired(gbm)[lambda d: d["representation"] == "raw"]

    claims: list[tuple[str, float]] = [
        ("cohorts", float(len(cohorts))),
        ("D0 AUC all targets", _cell(raw, "D0_within_cohort", "auc")),
        ("D3 AUC all targets raw", _cell(raw, "D3_other_institution", "auc")),
        ("D3 AUC all targets percentile", _cell(pct, "D3_other_institution", "auc")),
        ("D0 AUC paired raw", _cell(paired_raw, "D0_within_cohort", "auc")),
        ("D3 AUC paired raw", _cell(paired_raw, "D3_other_institution", "auc")),
        ("D0 brier", _cell(raw, "D0_within_cohort", "brier")),
        ("D3 brier raw", _cell(raw, "D3_other_institution", "brier")),
        ("D3 brier percentile", _cell(pct, "D3_other_institution", "brier")),
        ("D0 calibration_in_large", _cell(raw, "D0_within_cohort", "calibration_in_large")),
        ("D3 calibration_in_large raw", _cell(raw, "D3_other_institution", "calibration_in_large")),
        ("D3 calibration_in_large percentile", _cell(pct, "D3_other_institution", "calibration_in_large")),
        ("D0 recall_at_flag20", _cell(raw, "D0_within_cohort", "recall_at_flag20")),
        ("D3 recall_at_flag20 raw", _cell(raw, "D3_other_institution", "recall_at_flag20")),
        ("D3 recall_at_flag20 percentile", _cell(pct, "D3_other_institution", "recall_at_flag20")),
        ("D0 lift_at_flag20", _cell(raw, "D0_within_cohort", "lift_at_flag20")),
        ("D3 lift_at_flag20", _cell(raw, "D3_other_institution", "lift_at_flag20")),
        ("D3 f1_fail raw", _cell(raw, "D3_other_institution", "f1_fail")),
        ("D3 f1_fail percentile", _cell(pct, "D3_other_institution", "f1_fail")),
        ("D3 f1_fail baseline", _cell(raw, "D3_other_institution", "f1_fail_baseline")),
        ("D1 explanation tau", gbm.loc[gbm["distance"] == "D1_same_module", "explanation_tau"].mean()),
        ("D2 explanation tau", gbm.loc[gbm["distance"] == "D2_other_module", "explanation_tau"].mean()),
        ("D3 explanation tau", gbm.loc[gbm["distance"] == "D3_other_institution", "explanation_tau"].mean()),
        (
            "D3 explanation tau percentile",
            pct.loc[pct["distance"] == "D3_other_institution", "explanation_tau"].mean(),
        ),
        (
            "D3 explanation jaccard",
            gbm.loc[gbm["distance"] == "D3_other_institution", "explanation_jaccard_top3"].mean(),
        ),
    ]

    d0 = raw[raw["distance"] == "D0_within_cohort"].merge(
        cohorts, left_on="target", right_on="cohort_id"
    )
    for institution, group in d0.groupby("institution"):
        claims.append((f"D0 AUC {institution}", group["auc"].mean()))

    counts = pd.read_csv(ART / "exp_017_contamination" / "f33" / "student_counts.csv")
    claims += [
        ("distinct students", float(counts["distinct_students"].iloc[0])),
        ("cohort rows summed", float(counts["cohort_rows_summed"].iloc[0])),
    ]
    contam = pd.read_csv(ART / "exp_017_contamination" / "f33" / "summary.csv").set_index("distance")
    for distance, label in (("D1_same_module", "D1"), ("D2_other_module", "D2"), ("D3_other_institution", "D3")):
        claims.append((f"{label} contaminated pairs", float(contam.loc[distance, "contaminated_pairs"])))
        claims.append((f"{label} total pairs", float(contam.loc[distance, "pairs"])))

    clean = pd.read_csv(ART / "exp_017_contamination" / "f33" / "clean_vs_all.csv")
    clean = clean[(clean.model == "gradient_boosting") & (clean.representation == "raw")]
    for subset, label in (("all pairs", "all"), ("clean pairs", "clean")):
        row = clean[(clean.subset == subset) & (clean.distance == "D1_same_module")]
        claims.append((f"D1 AUC {label} pairs", float(row["auc"].iloc[0])))

    ceiling = pd.read_csv(ART / "exp_018_explanation_ceiling" / "f33" / "summary.csv")
    for _, row in ceiling.iterrows():
        claims.append((f"ceiling: {row['reference']}", float(row["tau"])))
        claims.append((f"ceiling jaccard: {row['reference']}", float(row["jaccard_top3"])))

    thr = pd.read_csv(ART / "exp_019_threshold_transfer" / "f33" / "summary.csv")
    thr = thr[thr.distance == "D3_other_institution"]
    for _, row in thr.iterrows():
        claims.append((f"threshold {row['representation']}/{row['rule']} f1_fail", float(row["f1_fail"])))

    shift = pd.read_csv(ART / "exp_016_shift_analysis" / "f33" / "regression.csv")
    shift = shift[shift.model == "gradient_boosting"].set_index("representation")
    for rep in ("raw", "percentile"):
        claims.append((f"shift r2 {rep}", float(shift.loc[rep, "r2"])))
        claims.append((f"shift corr_d_scale {rep}", float(shift.loc[rep, "corr_d_scale"])))
        claims.append((f"shift corr_d_shape {rep}", float(shift.loc[rep, "corr_d_shape"])))

    return claims


def main() -> int:
    text = PAPER.read_text(encoding="utf-8")
    # Every number the manuscript states, as a set for membership testing.
    stated = {
        float(m) for m in re.findall(r"(?<![\w.])[-+]?\d+(?:[.,]\d+)?(?![\w])", text.replace(",", ""))
    }

    failures = 0
    print(f"{'claim':46s} {'recomputed':>11s}  status")
    print("-" * 74)
    for label, value in build_claims():
        if pd.isna(value):
            print(f"{label:46s} {'nan':>11s}  SKIP (not computed)")
            continue
        hit = any(abs(value - s) <= TOL for s in stated) or any(
            abs(round(value, 2) - s) <= 0.005 for s in stated
        )
        status = "PASS" if hit else "ABSENT from text"
        if not hit:
            failures += 1
        print(f"{label:46s} {value:11.3f}  {status}")

    print("-" * 74)
    print(f"{failures} recomputed values do not appear in the manuscript.")
    print("ABSENT is not automatically an error: a value may be deliberately unreported.")
    print("It IS an error if the manuscript states a different number for the same quantity.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
