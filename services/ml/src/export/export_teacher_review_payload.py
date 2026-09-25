"""Export the precomputed cases behind the teacher explanation-review screen.

Practice week 6. The screen shows, for one student, the risk of not passing,
the three factors behind it and how far those factors can be trusted. The
trust part is the research result of weeks 1-3: a factor list is shown with a
reliability verdict from SHAP's own agreement across five background draws
(exp_025/027's self_tau_shap, gated at run_local_stability.GATE_TAU).

The model, split and background draws are exp_027's f33_background run. The
split and background lines below mirror run_local_stability.cohort_students
(vary="background") instead of refactoring that frozen-experiment code path;
main() then checks every student's self_tau against exp_027's students.csv and
refuses to write the payload if a single value differs.

Risk here is P(not passing) = 1 - P(pass). exp_025/027's p_risk column is
P(pass) (see the TODO(ml) in run_local_stability); it is never used as risk.

Usage (from services/ml):
    uv run python -m src.export.export_teacher_review_payload
"""

from __future__ import annotations

import json
from collections import Counter

import numpy as np
import pandas as pd
from scipy.stats import rankdata
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from src.experiments import run_local_stability as ls
from src.experiments import transfer_benchmark as tb
from src.experiments.run_transfer_ladder import (
    load_ku,
    load_oulad,
    load_oviedo,
    load_ukzn,
    load_zambia,
)

REPO = ls.REPO
OUT = REPO / "data" / "artifacts" / "research_demo" / "teacher_review_payload.json"
EXP027 = (
    REPO
    / "data"
    / "artifacts"
    / "experiments"
    / "exp_027_local_estimator_matrix"
    / "f33_background"
    / "students.csv"
)
GATE_SUMMARY = (
    REPO
    / "data"
    / "artifacts"
    / "experiments"
    / "exp_026_gate_calibration"
    / "exp027_f33_background__cross_tau"
    / "summary.csv"
)
FRACTION, SEED, REPEATS, BACKGROUND = 0.33, 0, 5, 50
INSTITUTIONS = {"OULAD": "OU", "KU Leuven": "KU", "UKZN": "UK", "Oviedo": "OV", "Zambia": "ZM"}
# Cohort ids of these end in an academic year ("1819"), the others in a calendar run.
ACADEMIC_YEAR_IDS = {"KU Leuven", "Oviedo"}
FLAGGED_PERCENTILES = (75, 25)
UNFLAGGED_PERCENTILE = 75
CALM_MAX_RANK = 0.5  # the non-flagged example comes from the lower half of course risk
FEATURE_LABELS = {
    "cum_clicks": "Total clicks so far",
    "cum_active_days": "Active days so far",
    "cum_content_clicks": "Course-material clicks so far",
    "cum_social": "Forum activity so far",
    "cur_clicks": "Clicks this week",
    "active_weeks": "Active weeks so far",
    "weeks_since_active": "Weeks since last activity",
}
SELECTION_RULE = (
    "Per course, in every course of the five institutions where the model ranks students "
    "better than chance (AUC > 0.5): among flagged students (top 20 % risk of the course), "
    "the students closest to the 75th and 25th percentiles of self_tau; plus, from the "
    "lower half of the course's risk ranking, the student closest to the 75th percentile. "
    "A course with fewer such students gives the ones it has. Risk ranks use midranks for "
    "ties; self_tau ties are broken by a seeded shuffle (seed 0). Students without a "
    "defined self_tau are never picked."
)


def course_label(cohort_id: str, institution: str, module: str) -> str:
    """The module plus its run, so two years of one course never share a label."""
    run = cohort_id.rsplit("_", 1)[1]
    if institution in ACADEMIC_YEAR_IDS:
        run = f"20{run[:2]}/{run[2:]}"
    return f"{module} {run}"


def _risk_ranks(risk: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Each student's position in the course's risk ranking, and whether it is flagged.

    Ties take their midrank: a course where most students have no activity gives
    them one identical risk, and "riskier than" must not call that block the
    riskiest 20 %. Flagged means a midrank in the top FLAG_RATE, so the flag and
    the "riskier than X % of this course" line on the screen always agree.
    """
    rank = (rankdata(risk, method="average") - 0.5) / len(risk)
    return rank, rank >= 1 - tb.FLAG_RATE


def _risk_share_below(risk: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Share of the course's students with strictly lower risk, and share with the same risk.

    The screen states "higher than for X %": only strictly lower risks count,
    and a large tied block is named instead of being split in half.
    """
    low, high = rankdata(risk, method="min"), rankdata(risk, method="max")
    return (low - 1) / len(risk), (high - low + 1) / len(risk)


def cohort_explanations(cohort: tb.Cohort) -> pd.DataFrame | None:
    """Every evaluation student of one cohort: risk, SHAP per draw, self-agreement."""
    x_all, y = cohort.X("raw"), cohort.y
    try:
        train, evaluate = train_test_split(
            np.arange(len(y)), test_size=1 / 3, stratify=y, random_state=SEED
        )
    except ValueError:
        return None
    if min(len(set(y[train])), len(set(y[evaluate]))) < 2:
        return None
    evaluate = evaluate[: ls.EVAL_CAP]
    x_train, x_eval = x_all[train], x_all[evaluate]
    bg_size = min(BACKGROUND, len(x_train) // 2)
    if bg_size < ls.MIN_BACKGROUND:
        return None
    model = ls._build(ls.MODEL, SEED).fit(x_train, y[train])

    p_pass = model.predict_proba(x_eval)[:, 1]
    risk = 1.0 - p_pass
    rank, flagged = _risk_ranks(risk)
    below, tied = _risk_share_below(risk)
    mats = []
    for repeat in range(REPEATS):  # cohort_students, vary="background"
        rng = np.random.default_rng(SEED * 1000 + repeat)
        background = x_train[rng.choice(len(x_train), size=bg_size, replace=False)]
        mats.append(ls._shap_matrix(model, x_eval, background))

    y_eval = y[evaluate]
    auc = float(roc_auc_score(y_eval, p_pass)) if len(set(y_eval)) == 2 else float("nan")
    medians = np.median(x_eval, axis=0)
    rows = []
    for i, student_row in enumerate(evaluate):
        orders = [ls._order(m[i]) for m in mats]
        rows.append(
            {
                "institution": cohort.institution,
                "cohort_id": cohort.cohort_id,
                "student_row": int(student_row),
                "course": course_label(cohort.cohort_id, cohort.institution, cohort.module),
                "cohort_size": cohort.n,
                "pass_rate": float(y.mean()),
                "model_auc": auc,
                "y": int(y_eval[i]),
                "risk": float(risk[i]),
                "risk_rank_pct": float(rank[i]),
                "risk_below_pct": float(below[i]),
                "risk_tied_pct": float(tied[i]),
                "ranked_students": len(evaluate),
                "flagged": bool(flagged[i]),
                "self_tau": ls._mean_pairwise_tau(orders),
                "attribution": mats[0][i].tolist(),
                "top_by_repeat": [o[0] for o in orders],
                "value": x_eval[i].tolist(),
                "course_median": medians.tolist(),
            }
        )
    frame = pd.DataFrame(rows)
    frame["self_tau"] = frame["self_tau"].astype(float)
    return frame


def _closest(pool: pd.DataFrame, target: float, taken: set, seed: int) -> pd.Series:
    order = np.random.default_rng(seed).permutation(len(pool))
    ranked = pool.assign(_gap=(pool["self_tau"] - target).abs(), _shuffle=order)
    for _, row in ranked.sort_values(["_gap", "_shuffle"]).iterrows():
        key = (row["cohort_id"], row["student_row"])
        if key not in taken:
            taken.add(key)
            return row.drop(["_gap", "_shuffle"])
    raise ValueError("not enough students to select from")


def select_cases(frame: pd.DataFrame) -> pd.DataFrame:
    """Two flagged students across the reliability range and one calm one, per course."""
    # A course where the model ranks students no better than chance (AUC <= 0.5)
    # has nothing to explain; 0.5 is the definition of chance, not a tuned cut.
    frame = frame.dropna(subset=["self_tau"])
    frame = frame[frame["model_auc"] > 0.5].reset_index(drop=True)
    picked, taken = [], set()
    for inst in INSTITUTIONS:
        courses = frame[frame["institution"] == inst]
        for _, pool in courses.groupby("cohort_id", sort=True):
            flagged = pool[pool["flagged"]]
            # The calm example must look calm: a large tied block at maximal risk can sit
            # below the flag's midrank cut, so non-flagged alone is not enough.
            calm = pool[~pool["flagged"] & (pool["risk_rank_pct"] <= CALM_MAX_RANK)]
            for q in FLAGGED_PERCENTILES[: len(flagged)]:
                target = float(np.percentile(flagged["self_tau"], q))
                picked.append(_closest(flagged, target, taken, SEED))
            if len(calm):
                target = float(np.percentile(calm["self_tau"], UNFLAGGED_PERCENTILE))
                picked.append(_closest(calm, target, taken, SEED))
    return pd.DataFrame(picked).reset_index(drop=True)


def _shares(attribution: np.ndarray) -> np.ndarray:
    magnitude = np.abs(attribution)
    return magnitude / magnitude.sum()


def _direction(value: float) -> str:
    # Attributions push towards passing: negative means more risk of not passing.
    if value < 0:
        return "raises_risk"
    if value > 0:
        return "lowers_risk"
    return "no_effect"


def build_case(row: pd.Series, case_id: str) -> dict:
    attribution = np.asarray(row["attribution"], dtype=float)
    shares = _shares(attribution)
    index = {name: j for j, name in enumerate(tb.CANON)}
    features = [
        {
            "feature": name,
            "label": FEATURE_LABELS[name],
            "value": float(row["value"][j]),
            "courseMedian": float(row["course_median"][j]),
        }
        for j, name in enumerate(tb.CANON)
    ]
    factors = [
        {
            **features[index[name]],
            "direction": _direction(attribution[index[name]]),
            "share": round(float(shares[index[name]]), 4),
        }
        for name in ls._order(attribution)[:3]
    ]
    counts = Counter(row["top_by_repeat"]).most_common()
    return {
        "caseId": case_id,
        "displayName": f"Student {case_id}",
        "institution": row["institution"],
        "source": {"cohortId": row["cohort_id"], "studentRow": int(row["student_row"])},
        "context": {
            "course": row["course"],
            "week": int(row["week"]),
            "nWeeks": int(row["n_weeks"]),
            "cohortSize": int(row["cohort_size"]),
            "rankedStudents": int(row["ranked_students"]),
            "passRate": round(float(row["pass_rate"]), 4),
            "modelAuc": round(float(row["model_auc"]), 4),
        },
        "risk": round(float(row["risk"]), 4),
        "riskRankPct": round(float(row["risk_rank_pct"]), 4),
        "riskBelowPct": round(float(row["risk_below_pct"]), 4),
        "riskTiedPct": round(float(row["risk_tied_pct"]), 4),
        "flagged": bool(row["flagged"]),
        "factors": factors,
        "reliability": {
            "selfTau": round(float(row["self_tau"]), 4),
            "threshold": ls.GATE_TAU,
            "verdict": "stable" if row["self_tau"] >= ls.GATE_TAU else "unstable",
            "recomputations": [
                {"feature": f, "label": FEATURE_LABELS[f], "count": c} for f, c in counts
            ],
        },
        "features": features,
    }


def course_weeks() -> dict[str, tuple[int, int]]:
    """Cutoff week and course length per cohort, as tb.cutoff_rows computes them."""
    weekly = {**load_oulad(), **load_ku(), **load_ukzn(), **load_oviedo(), **load_zambia()}
    out = {}
    for cid, frame in weekly.items():
        n_weeks = int(frame["n_weeks"].max())
        out[cid] = (max(1, int(np.rint(FRACTION * n_weeks))), n_weeks)
    return out


def check_against_exp027(frame: pd.DataFrame) -> None:
    ref = pd.read_csv(EXP027, usecols=["cohort_id", "student_row", "self_tau_shap"])
    merged = frame.merge(ref, on=["cohort_id", "student_row"], how="left", validate="one_to_one")
    same = np.isclose(merged["self_tau"], merged["self_tau_shap"], rtol=0, atol=1e-12)
    same |= merged["self_tau"].isna() & merged["self_tau_shap"].isna()
    if not same.all():
        raise RuntimeError(f"{int((~same).sum())} students differ from exp_027; not writing")


def scale_context() -> dict:
    s = pd.read_csv(GATE_SUMMARY).iloc[0]
    return {
        "threshold": ls.GATE_TAU,
        "coverage": round(float(s["c_star"]), 4),
        "retainedAgreement": round(float(s["global_mean_cross_tau"]), 4),
        "noGateAgreement": round(float(s["no_gate_mean_cross_tau"]), 4),
        "source": str(GATE_SUMMARY.relative_to(REPO)),
    }


def main() -> None:
    cohorts = [c for c in ls.load_cohorts(FRACTION) if c.institution in INSTITUTIONS]
    frames = [f for f in map(cohort_explanations, cohorts) if f is not None]
    frame = pd.concat(frames, ignore_index=True)
    check_against_exp027(frame)
    weeks = course_weeks()
    frame["week"] = frame["cohort_id"].map(lambda c: weeks[c][0])
    frame["n_weeks"] = frame["cohort_id"].map(lambda c: weeks[c][1])

    chosen = select_cases(frame)
    eligible = frame.loc[frame["model_auc"] > 0.5, "cohort_id"].unique()
    per_course = chosen["cohort_id"].value_counts().reindex(eligible, fill_value=0)
    per_slot = len(FLAGGED_PERCENTILES) + 1
    for cid, n in per_course[per_course < per_slot].sort_index().items():
        print(f"{cid}: {n} of {per_slot} cases (course has too few eligible students)")
    cases, counter = [], Counter()
    for _, row in chosen.iterrows():
        prefix = INSTITUTIONS[row["institution"]]
        counter[prefix] += 1
        cases.append(build_case(row, f"{prefix}-{counter[prefix]}"))
    payload = {
        "schemaVersion": "teacher_review_v1",
        "generatedFrom": {
            "experiment": "exp_027_local_estimator_matrix/f33_background",
            "fraction": FRACTION,
            "model": ls.MODEL,
            "seed": SEED,
            "repeats": REPEATS,
            "background": BACKGROUND,
        },
        "selectionRule": SELECTION_RULE,
        "scaleContext": scale_context(),
        "featureLabels": FEATURE_LABELS,
        "cases": cases,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"{len(frame)} students checked against exp_027; {len(cases)} cases -> {OUT}")


if __name__ == "__main__":
    main()
