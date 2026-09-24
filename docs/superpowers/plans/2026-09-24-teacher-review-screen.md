# Teacher Explanation-Review Screen Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A `/review` screen in the teacher app that shows 20 precomputed student cases with risk, three factors with direction, an explicit explanation-reliability scale, and a teacher decision that is stored by the API.

**Architecture:** An ML exporter writes a frozen JSON payload from exp_027's configuration; the FastAPI app imports it into SQLite and serves a new `review` domain (list, case, decision); the Next.js app renders a two-pane page and posts decisions through a server action.

**Tech Stack:** Python 3.11 + scikit-learn + shap (services/ml, uv); FastAPI + SQLAlchemy + SQLite + pytest (apps/api, uv); Next.js 14 App Router + React 18 + shadcn/Tailwind v4 + node:test (apps/web, npm).

**Spec:** `docs/superpowers/specs/2026-09-24-teacher-review-screen-design.md`

## Global Constraints

- UI copy in English; no authentication, roles or group analytics.
- Risk shown to the teacher is P(not passing) = 1 − `predict_proba[:, 1]`; the exp_025/027 `p_risk` column (P(pass)) is never used as risk.
- Threshold, coverage and agreement numbers come from files (`run_local_stability.GATE_TAU`, exp_026 summary), never typed into the UI or exporter.
- Frozen artifacts under `data/artifacts/experiments/` are read only; nothing there changes.
- `run_local_stability.py` is not modified: the exporter mirrors its split and background draw and is pinned by an exact check against exp_027.
- JSON payload and API keys are camelCase, like the existing research payloads.
- Teacher actions: `contact_student`, `keep_monitoring`, `no_action_needed`, `factor_looks_wrong` — a placeholder set, marked `TODO(domain)`.
- No commits during execution unless the user asks; git stash/checkout/reset are not used.
- Commands: ML `cd services/ml && uv run python -m pytest tests/<f> -q`; API `cd apps/api && uv run python -m pytest tests/<f> -q`; web `cd apps/web && npm run typecheck`, `node --test tests/review.test.mjs`, `npm run build`.

## Review Focus

- The review payload file has not been generated yet → the API starts normally, `/api/review/cases` returns `[]`, and the page tells the teacher how to generate it.
- A decision that names a factor with an action other than `factor_looks_wrong` → 422, not silently stored.
- A note of exactly 1000 characters → stored; 1001 → 422; a whitespace-only note → stored as null.
- The API is down while the page renders → an explicit "not available" notice, no crash and no invented data.
- An unknown case id in the URL or the POST path → 404 from the API and a "case not found" notice on the page, never a 500.

---

### Task 1: ML export of teacher-review cases

**Files:**
- Create: `services/ml/src/export/export_teacher_review_payload.py`
- Create: `services/ml/tests/test_teacher_review_export.py`
- Output: `data/artifacts/research_demo/teacher_review_payload.json` (generated)

**Interfaces:**
- Consumes: `run_local_stability`: `EVAL_CAP`, `MIN_BACKGROUND`, `GATE_TAU`, `MODEL`, `_build(model_name, seed)`, `_shap_matrix(model, x_eval, background)`, `_order(scores) -> list[str]`, `_mean_pairwise_tau(orders) -> float | None`, `load_cohorts(fraction) -> list[tb.Cohort]`; `transfer_benchmark`: `CANON`, `FLAG_RATE`, `Cohort`; `run_transfer_ladder` loaders for course length.
- Produces: `cohort_explanations(cohort) -> pd.DataFrame | None`; `select_cases(frame) -> pd.DataFrame`; `build_case(row, case_id) -> dict`; `main()`; the payload JSON with top-level keys `schemaVersion`, `generatedFrom`, `selectionRule`, `scaleContext` {`threshold`, `coverage`, `retainedAgreement`, `noGateAgreement`, `source`}, `featureLabels`, `cases[]`. Each case: `caseId`, `displayName`, `institution`, `source` {`cohortId`, `studentRow`}, `context` {`course`, `week`, `nWeeks`, `cohortSize`, `passRate`, `modelAuc`}, `risk`, `riskRankPct`, `flagged`, `factors[3]` {`feature`, `label`, `direction` ∈ `raises_risk`/`lowers_risk`/`no_effect`, `share`, `value`, `courseMedian`}, `reliability` {`selfTau`, `threshold`, `verdict` ∈ `stable`/`unstable`, `recomputations[]` {`feature`, `label`, `count`}}, `features[7]` {`feature`, `label`, `value`, `courseMedian`}.

- [ ] **Step 1: Write the failing tests**

```python
# services/ml/tests/test_teacher_review_export.py
import numpy as np
import pandas as pd

from src.experiments import transfer_benchmark as tb
from src.export import export_teacher_review_payload as ex


def _cohort(n: int = 240, seed: int = 0) -> tb.Cohort:
    rng = np.random.default_rng(seed)
    x = pd.DataFrame(rng.random((n, len(tb.CANON))) * 10, columns=list(tb.CANON))
    # Passing rises with activity, so risk must fall with it.
    y = (x["cum_active_days"] + rng.normal(0, 1, n) > 5).astype(int).to_numpy()
    return tb.Cohort(cohort_id="c1", institution="OULAD", module="AAA", X_raw=x, y=y)


def test_risk_is_probability_of_not_passing():
    frame = ex.cohort_explanations(_cohort())
    assert frame["risk"].between(0, 1).all()
    by_outcome = frame.groupby("y")["risk"].mean()
    assert by_outcome[0] > by_outcome[1]  # non-passers carry more risk
    assert frame["flagged"].mean() > 0
    flagged_min = frame.loc[frame["flagged"], "risk"].min()
    assert (frame.loc[~frame["flagged"], "risk"] <= flagged_min).all()


def test_self_tau_matches_the_run_local_stability_definition():
    frame = ex.cohort_explanations(_cohort())
    assert frame["self_tau"].between(-1, 1).all()
    assert len(frame["top_by_repeat"].iloc[0]) == ex.REPEATS


def _row(attribution):
    return pd.Series(
        {
            "institution": "OULAD",
            "cohort_id": "c1",
            "student_row": 7,
            "course": "AAA",
            "week": 13,
            "n_weeks": 39,
            "cohort_size": 240,
            "pass_rate": 0.5,
            "model_auc": 0.8,
            "risk": 0.72,
            "risk_rank_pct": 0.9,
            "flagged": True,
            "self_tau": 0.62,
            "attribution": list(attribution),
            "top_by_repeat": ["cum_active_days"] * 3 + ["cum_clicks"] * 2,
            "value": [float(v) for v in range(7)],
            "course_median": [1.0] * 7,
        }
    )


def test_direction_follows_the_sign_towards_passing():
    case = ex.build_case(_row([0.5, -2.0, 0.0, 0.1, 0.0, 0.0, 0.0]), "OU-1")
    names = [f["feature"] for f in case["factors"]]
    assert names == ["cum_active_days", "cum_clicks", "cum_social"]
    assert case["factors"][0]["direction"] == "raises_risk"  # negative towards passing
    assert case["factors"][1]["direction"] == "lowers_risk"


def test_zero_attribution_is_no_effect_not_lowers_risk():
    case = ex.build_case(_row([3.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0]), "OU-1")
    assert case["factors"][2]["direction"] == "no_effect"


def test_shares_sum_to_one_over_all_seven_features():
    shares = ex._shares(np.array([0.5, -2.0, 0.0, 0.1, 0.4, -0.3, 0.2]))
    assert abs(shares.sum() - 1.0) < 1e-12


def test_reliability_and_recomputations():
    case = ex.build_case(_row([0.5, -2.0, 0.0, 0.1, 0.0, 0.0, 0.0]), "OU-1")
    rel = case["reliability"]
    assert rel["verdict"] == "unstable" and rel["threshold"] == ex.ls.GATE_TAU
    assert rel["recomputations"][0] == {
        "feature": "cum_active_days",
        "label": ex.FEATURE_LABELS["cum_active_days"],
        "count": 3,
    }


def test_case_carries_no_student_identifier():
    case = ex.build_case(_row([0.5, -2.0, 0.0, 0.1, 0.0, 0.0, 0.0]), "OU-1")
    assert set(case) == {
        "caseId", "displayName", "institution", "source", "context", "risk",
        "riskRankPct", "flagged", "factors", "reliability", "features",
    }
    assert set(case["source"]) == {"cohortId", "studentRow"}


def _selection_frame():
    rng = np.random.default_rng(1)
    parts = []
    for inst in ex.INSTITUTIONS:
        n = 60
        parts.append(
            pd.DataFrame(
                {
                    "institution": inst,
                    "cohort_id": [f"{inst}_c{i % 3}" for i in range(n)],
                    "student_row": range(n),
                    "self_tau": rng.choice(np.linspace(0.3, 1.0, 8), n),
                    "flagged": [i % 3 == 0 for i in range(n)],
                }
            )
        )
    frame = pd.concat(parts, ignore_index=True)
    frame.loc[0, "self_tau"] = np.nan  # a constant ranking must never be picked
    return frame


def test_selection_is_deterministic_unique_and_complete():
    frame = _selection_frame()
    first, second = ex.select_cases(frame), ex.select_cases(frame)
    pd.testing.assert_frame_equal(first, second)
    assert len(first) == 5 * len(ex.INSTITUTIONS)
    assert not first.duplicated(["cohort_id", "student_row"]).any()
    assert first["self_tau"].notna().all()
    for inst, g in first.groupby("institution"):
        assert g["flagged"].sum() == 4 and (~g["flagged"]).sum() == 1
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd services/ml && uv run python -m pytest tests/test_teacher_review_export.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'src.export.export_teacher_review_payload'`

- [ ] **Step 3: Write the exporter**

```python
# services/ml/src/export/export_teacher_review_payload.py
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
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from src.experiments import run_local_stability as ls
from src.experiments import transfer_benchmark as tb
from src.experiments.run_transfer_ladder import load_ku, load_oulad, load_oviedo, load_ukzn

REPO = ls.REPO
OUT = REPO / "data" / "artifacts" / "research_demo" / "teacher_review_payload.json"
EXP027 = (
    REPO / "data" / "artifacts" / "experiments" / "exp_027_local_estimator_matrix"
    / "f33_background" / "students.csv"
)
GATE_SUMMARY = (
    REPO / "data" / "artifacts" / "experiments" / "exp_026_gate_calibration"
    / "exp027_f33_background__cross_tau" / "summary.csv"
)
FRACTION, SEED, REPEATS, BACKGROUND = 0.33, 0, 5, 50
# Zambia is left out: two cohorts, 40 evaluation students.
INSTITUTIONS = {"OULAD": "OU", "KU Leuven": "KU", "UKZN": "UK", "Oviedo": "OV"}
FLAGGED_PERCENTILES = (90, 65, 35, 10)
UNFLAGGED_PERCENTILE = 75
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
    "Per institution (OULAD, KU Leuven, UKZN, Oviedo): among flagged students (top 20 % "
    "risk of the cohort), the students closest to the 90th, 65th, 35th and 10th "
    "percentiles of self_tau; plus the non-flagged student closest to the 75th "
    "percentile. Ties broken by a seeded shuffle (seed 0). Students without a defined "
    "self_tau are never picked."
)


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
    cut = float(np.quantile(risk, 1 - tb.FLAG_RATE))
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
                "course": cohort.module,
                "cohort_size": cohort.n,
                "pass_rate": float(y.mean()),
                "model_auc": auc,
                "y": int(y_eval[i]),
                "risk": float(risk[i]),
                "risk_rank_pct": float((risk < risk[i]).mean()),
                "flagged": bool(risk[i] >= cut),
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
    """Four flagged students across the reliability range and one non-flagged, per institution."""
    frame = frame.dropna(subset=["self_tau"]).reset_index(drop=True)
    picked, taken = [], set()
    for inst in INSTITUTIONS:
        pool = frame[frame["institution"] == inst]
        flagged, calm = pool[pool["flagged"]], pool[~pool["flagged"]]
        for q in FLAGGED_PERCENTILES:
            target = float(np.percentile(flagged["self_tau"], q))
            picked.append(_closest(flagged, target, taken, SEED))
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
            "passRate": round(float(row["pass_rate"]), 4),
            "modelAuc": round(float(row["model_auc"]), 4),
        },
        "risk": round(float(row["risk"]), 4),
        "riskRankPct": round(float(row["risk_rank_pct"]), 4),
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
    weekly = {**load_oulad(), **load_ku(), **load_ukzn(), **load_oviedo()}
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
    cases, counter = [], Counter()
    for _, row in chosen.iterrows():
        prefix = INSTITUTIONS[row["institution"]]
        counter[prefix] += 1
        cases.append(build_case(row, f"{prefix}-{counter[prefix]}"))
    payload = {
        "schemaVersion": "teacher_review_v1",
        "generatedFrom": {
            "experiment": "exp_027_local_estimator_matrix/f33_background",
            "fraction": FRACTION, "model": ls.MODEL, "seed": SEED,
            "repeats": REPEATS, "background": BACKGROUND,
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
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd services/ml && uv run python -m pytest tests/test_teacher_review_export.py -q`
Expected: 8 passed

- [ ] **Step 5: Lint and format**

Run: `cd services/ml && uv run ruff check src/export/export_teacher_review_payload.py tests/test_teacher_review_export.py && uv run ruff format src/export/export_teacher_review_payload.py tests/test_teacher_review_export.py`
Expected: `All checks passed!`

- [ ] **Step 6: Generate the payload**

Run: `cd services/ml && uv run python -m src.export.export_teacher_review_payload`
Expected: `11835 students checked against exp_027; 20 cases -> …/teacher_review_payload.json` (the student count is the four institutions' evaluation students; any RuntimeError means the mirrored split or background drifted — stop and investigate). Then check `git status --short data/artifacts/experiments` is empty.

- [ ] **Step 7: Inspect the payload**

Run: `python3 -c "import json;p=json.load(open('data/artifacts/research_demo/teacher_review_payload.json'));print(p['scaleContext']);print([(c['caseId'],c['reliability']['verdict'],c['risk']) for c in p['cases']])"`
Expected: 20 cases, 5 per prefix OU/KU/UK/OV, a mix of `stable` and `unstable`, risks in [0, 1], `scaleContext.coverage` ≈ 0.56.

---

### Task 2: API storage, importer and startup seeding

**Files:**
- Modify: `apps/api/src/db/models.py` (append two records)
- Modify: `apps/api/src/core/config.py` (one setting)
- Create: `apps/api/src/importer/review_payload.py`
- Modify: `apps/api/src/domain/platform/bootstrap.py` (add `initialize_review_store`)
- Modify: `apps/api/src/main.py` (call it in lifespan)
- Modify: `apps/api/src/import_research_payload.py` (also import the review payload)
- Create: `apps/api/tests/review_fixtures.py`
- Test: `apps/api/tests/test_review_importer.py`

**Interfaces:**
- Consumes: the Task 1 payload shape.
- Produces: `ReviewCaseRecord(case_id: str PK, institution: str, position: int, payload_json: str)`, `ReviewDecisionRecord(id: int PK, case_id: str, action: str, factor: str | None, note: str | None, created_at: datetime)`, `ReviewMetadataRecord(id: int PK = 1, payload_json: str)`; `import_review_payload(session, *, payload_path) -> int`; `initialize_review_store() -> int | None`; setting `review_payload_path`; test helper `write_review_payload(path) -> dict`.

- [ ] **Step 1: Write the test fixture and failing tests**

```python
# apps/api/tests/review_fixtures.py
from __future__ import annotations

import json
from pathlib import Path


def _case(case_id: str, verdict: str) -> dict:
    factors = [
        {"feature": "cum_active_days", "label": "Active days so far", "value": 4.0,
         "courseMedian": 9.0, "direction": "raises_risk", "share": 0.41},
        {"feature": "cum_clicks", "label": "Total clicks so far", "value": 120.0,
         "courseMedian": 410.0, "direction": "raises_risk", "share": 0.3},
        {"feature": "cum_social", "label": "Forum activity so far", "value": 3.0,
         "courseMedian": 1.0, "direction": "lowers_risk", "share": 0.1},
    ]
    return {
        "caseId": case_id,
        "displayName": f"Student {case_id}",
        "institution": "OULAD",
        "source": {"cohortId": "oulad_BBB_2013J", "studentRow": 7},
        "context": {"course": "BBB", "week": 13, "nWeeks": 39, "cohortSize": 2237,
                    "passRate": 0.48, "modelAuc": 0.85},
        "risk": 0.72,
        "riskRankPct": 0.9,
        "flagged": True,
        "factors": factors,
        "reliability": {"selfTau": 0.62 if verdict == "unstable" else 0.9, "threshold": 0.8,
                        "verdict": verdict,
                        "recomputations": [{"feature": "cum_active_days",
                                            "label": "Active days so far", "count": 5}]},
        "features": [{k: f[k] for k in ("feature", "label", "value", "courseMedian")}
                     for f in factors],
    }


def write_review_payload(path: Path) -> dict:
    payload = {
        "schemaVersion": "teacher_review_v1",
        "generatedFrom": {"experiment": "test"},
        "selectionRule": "test",
        "scaleContext": {"threshold": 0.8, "coverage": 0.56, "retainedAgreement": 0.41,
                         "noGateAgreement": 0.35, "source": "test"},
        "featureLabels": {"cum_active_days": "Active days so far"},
        "cases": [_case("OU-1", "stable"), _case("OU-2", "unstable")],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return payload
```

```python
# apps/api/tests/test_review_importer.py
from __future__ import annotations

import uuid
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from src.db.models import Base, ReviewCaseRecord, ReviewDecisionRecord, ReviewMetadataRecord
from src.importer.review_payload import import_review_payload
from tests.review_fixtures import write_review_payload

TMP = Path(__file__).resolve().parents[3] / ".tmp_api_tests"


def _session():
    TMP.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{(TMP / f'review_{uuid.uuid4().hex}.sqlite').as_posix()}")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def test_import_loads_cases_in_payload_order_and_metadata():
    session = _session()
    path = TMP / f"payload_{uuid.uuid4().hex}.json"
    write_review_payload(path)
    assert import_review_payload(session, payload_path=path) == 2
    ids = session.scalars(select(ReviewCaseRecord.case_id).order_by(ReviewCaseRecord.position))
    assert list(ids) == ["OU-1", "OU-2"]
    assert session.get(ReviewMetadataRecord, 1) is not None


def test_reimport_replaces_cases_and_keeps_decisions():
    from datetime import datetime

    session = _session()
    path = TMP / f"payload_{uuid.uuid4().hex}.json"
    write_review_payload(path)
    import_review_payload(session, payload_path=path)
    session.add(ReviewDecisionRecord(case_id="OU-1", action="keep_monitoring", factor=None,
                                     note=None, created_at=datetime(2026, 9, 24)))
    session.commit()
    assert import_review_payload(session, payload_path=path) == 2
    assert session.scalar(select(ReviewDecisionRecord.case_id)) == "OU-1"
    assert len(list(session.scalars(select(ReviewCaseRecord)))) == 2
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd apps/api && uv run python -m pytest tests/test_review_importer.py -q`
Expected: FAIL — `ImportError: cannot import name 'ReviewCaseRecord'`

- [ ] **Step 3: Add the records** (append to `apps/api/src/db/models.py`)

```python
class ReviewMetadataRecord(Base):
    """Payload-level context for the review screen (scale context, labels, provenance)."""

    __tablename__ = "review_metadata"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)


class ReviewCaseRecord(Base):
    """One precomputed teacher-review case, stored as the exporter wrote it."""

    __tablename__ = "review_cases"

    case_id: Mapped[str] = mapped_column(String(16), primary_key=True)
    institution: Mapped[str] = mapped_column(String(64), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)


class ReviewDecisionRecord(Base):
    """A teacher's decision on a case. Append-only; survives a re-import of the cases."""

    __tablename__ = "review_decisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_id: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(32), nullable=False)
    factor: Mapped[str | None] = mapped_column(String(64))
    note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
```

- [ ] **Step 4: Add the setting** (in `Settings` in `apps/api/src/core/config.py`, after `research_demo_payload_path`)

```python
    review_payload_path: str = str(
        REPO_ROOT / "data" / "artifacts" / "research_demo" / "teacher_review_payload.json"
    )
```

- [ ] **Step 5: Write the importer**

```python
# apps/api/src/importer/review_payload.py
from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy import delete
from sqlalchemy.orm import Session

from src.db.models import ReviewCaseRecord, ReviewMetadataRecord

METADATA_KEYS = ("schemaVersion", "generatedFrom", "selectionRule", "scaleContext", "featureLabels")


def import_review_payload(session: Session, *, payload_path: str | Path) -> int:
    """Replace the review cases with the frozen payload's; decisions are left untouched."""
    payload = json.loads(Path(payload_path).read_text(encoding="utf-8"))
    session.execute(delete(ReviewCaseRecord))
    session.execute(delete(ReviewMetadataRecord))
    session.add(
        ReviewMetadataRecord(id=1, payload_json=json.dumps({k: payload[k] for k in METADATA_KEYS}))
    )
    for position, case in enumerate(payload["cases"]):
        session.add(
            ReviewCaseRecord(
                case_id=case["caseId"],
                institution=case["institution"],
                position=position,
                payload_json=json.dumps(case),
            )
        )
    session.commit()
    return len(payload["cases"])
```

- [ ] **Step 6: Seed at startup** — append to `apps/api/src/domain/platform/bootstrap.py`

```python
def initialize_review_store() -> int | None:
    """Load the review payload once, if it exists and nothing is loaded yet.

    Separate from the research seed above, which returns early once students
    exist, so an existing database still picks up review cases.
    """
    from sqlalchemy import select

    from src.db.models import ReviewCaseRecord
    from src.importer.review_payload import import_review_payload

    init_db()
    payload_path = Path(get_settings().review_payload_path)
    if not payload_path.exists():
        return None
    with get_sessionmaker()() as session:
        if session.scalar(select(ReviewCaseRecord.case_id).limit(1)) is not None:
            return None
        return import_review_payload(session, payload_path=payload_path)
```

In `apps/api/src/main.py`, import it next to `initialize_platform_store` and call it in `lifespan` right after `initialize_platform_store()`:

```python
from src.domain.platform.bootstrap import initialize_platform_store, initialize_review_store
...
    initialize_platform_store()
    initialize_review_store()
```

In `apps/api/src/import_research_payload.py` `main()`, after the research import:

```python
    review_path = Path(get_settings().review_payload_path)
    if review_path.exists():
        with get_sessionmaker()() as session:
            print(f"review cases imported: {import_review_payload(session, payload_path=review_path)}")
```

(with `from src.importer.review_payload import import_review_payload` added to its imports).

- [ ] **Step 7: Run the tests**

Run: `cd apps/api && uv run python -m pytest tests/test_review_importer.py tests/test_platform_routes.py tests/test_research_payload_importer.py -q`
Expected: all pass (the existing route and importer tests still pass).

---

### Task 3: API review domain (list, case, decision)

**Files:**
- Create: `apps/api/src/domain/review/__init__.py`, `models.py`, `repository.py`, `service.py`, `router.py`
- Modify: `apps/api/src/api/router.py` (mount `/review`)
- Test: `apps/api/tests/test_review_routes.py`

**Interfaces:**
- Consumes: Task 2 records and `write_review_payload`.
- Produces (HTTP): `GET /api/review/cases` → `[{caseId, displayName, institution, course, risk, flagged, verdict, selfTau, latestDecision: {action, factor, createdAt} | null}]`; `GET /api/review/cases/{caseId}` → `{case, scaleContext, featureLabels, decisions: [{id, action, factor, note, createdAt}]}` (newest first); `POST /api/review/cases/{caseId}/decisions` body `{action, factor?, note?}` → `201 {id, action, factor, note, createdAt}`; 404 unknown case; 422 invalid body.

- [ ] **Step 1: Write the failing route tests**

```python
# apps/api/tests/test_review_routes.py
from __future__ import annotations

import importlib
import uuid
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.core.config import get_settings
from src.db.session import reset_engine_for_tests
from tests.review_fixtures import write_review_payload

REPO_ROOT = Path(__file__).resolve().parents[3]
TMP = REPO_ROOT / ".tmp_api_tests"


def _client(monkeypatch: pytest.MonkeyPatch, with_payload: bool) -> TestClient:
    TMP.mkdir(parents=True, exist_ok=True)
    run = uuid.uuid4().hex
    payload = TMP / f"review_{run}.json"
    if with_payload:
        write_review_payload(payload)
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{(TMP / f'review_{run}.sqlite').as_posix()}")
    monkeypatch.setenv("AUTO_SEED_FROM_RESEARCH_PAYLOAD", "false")
    monkeypatch.setenv("REVIEW_PAYLOAD_PATH", str(payload))
    get_settings.cache_clear()
    reset_engine_for_tests()
    import src.main as main

    importlib.reload(main)
    return TestClient(main.app)


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    with _client(monkeypatch, with_payload=True) as c:
        yield c
    get_settings.cache_clear()
    reset_engine_for_tests()


def test_list_cases(client: TestClient) -> None:
    rows = client.get("/api/review/cases").json()
    assert [r["caseId"] for r in rows] == ["OU-1", "OU-2"]
    assert rows[1]["verdict"] == "unstable" and rows[0]["latestDecision"] is None


def test_get_case_with_context(client: TestClient) -> None:
    body = client.get("/api/review/cases/OU-2").json()
    assert body["case"]["caseId"] == "OU-2"
    assert body["scaleContext"]["threshold"] == 0.8
    assert body["decisions"] == []


def test_record_decision_and_see_it_newest_first(client: TestClient) -> None:
    first = client.post("/api/review/cases/OU-1/decisions", json={"action": "keep_monitoring"})
    assert first.status_code == 201
    second = client.post(
        "/api/review/cases/OU-1/decisions",
        json={"action": "factor_looks_wrong", "factor": "cum_clicks", "note": "  "},
    )
    assert second.status_code == 201 and second.json()["note"] is None
    body = client.get("/api/review/cases/OU-1").json()
    assert [d["action"] for d in body["decisions"]] == ["factor_looks_wrong", "keep_monitoring"]
    listed = client.get("/api/review/cases").json()[0]
    assert listed["latestDecision"]["action"] == "factor_looks_wrong"


def test_unknown_case_is_404(client: TestClient) -> None:
    assert client.get("/api/review/cases/XX-9").status_code == 404
    post = client.post("/api/review/cases/XX-9/decisions", json={"action": "keep_monitoring"})
    assert post.status_code == 404


@pytest.mark.parametrize(
    "body",
    [
        {"action": "expel_student"},
        {"action": "factor_looks_wrong"},
        {"action": "factor_looks_wrong", "factor": "weeks_since_active"},
        {"action": "contact_student", "factor": "cum_clicks"},
        {"action": "keep_monitoring", "note": "x" * 1001},
    ],
)
def test_invalid_decisions_are_422(client: TestClient, body: dict) -> None:
    assert client.post("/api/review/cases/OU-1/decisions", json=body).status_code == 422


def test_note_of_exactly_1000_characters_is_stored(client: TestClient) -> None:
    ok = client.post(
        "/api/review/cases/OU-1/decisions", json={"action": "keep_monitoring", "note": "x" * 1000}
    )
    assert ok.status_code == 201 and len(ok.json()["note"]) == 1000


def test_missing_payload_starts_with_no_cases(monkeypatch: pytest.MonkeyPatch) -> None:
    with _client(monkeypatch, with_payload=False) as c:
        assert c.get("/api/review/cases").json() == []
    get_settings.cache_clear()
    reset_engine_for_tests()
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd apps/api && uv run python -m pytest tests/test_review_routes.py -q`
Expected: FAIL — 404 for `/api/review/cases` (router not mounted).

- [ ] **Step 3: Write the domain package**

```python
# apps/api/src/domain/review/__init__.py
```

```python
# apps/api/src/domain/review/models.py
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

# TODO(domain): placeholder actions for the week-6 prototype, not a validated
# taxonomy of teacher responses. factor_looks_wrong feeds the week-7 loop.
Action = Literal["contact_student", "keep_monitoring", "no_action_needed", "factor_looks_wrong"]


class DecisionIn(BaseModel):
    action: Action
    factor: str | None = None
    note: str | None = Field(default=None, max_length=1000)

    @field_validator("note")
    @classmethod
    def _blank_note_is_none(cls, value: str | None) -> str | None:
        return value if value and value.strip() else None

    @model_validator(mode="after")
    def _factor_only_when_flagging(self) -> DecisionIn:
        if (self.action == "factor_looks_wrong") != (self.factor is not None):
            raise ValueError("factor is required for factor_looks_wrong and only for it")
        return self
```

```python
# apps/api/src/domain/review/repository.py
from __future__ import annotations

import json
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models import ReviewCaseRecord, ReviewDecisionRecord, ReviewMetadataRecord


class ReviewRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def cases(self) -> list[dict]:
        rows = self.session.scalars(select(ReviewCaseRecord).order_by(ReviewCaseRecord.position))
        return [json.loads(r.payload_json) for r in rows]

    def case(self, case_id: str) -> dict | None:
        row = self.session.get(ReviewCaseRecord, case_id)
        return json.loads(row.payload_json) if row else None

    def metadata(self) -> dict:
        row = self.session.get(ReviewMetadataRecord, 1)
        return json.loads(row.payload_json) if row else {}

    def decisions(self, case_id: str | None = None) -> list[ReviewDecisionRecord]:
        query = select(ReviewDecisionRecord).order_by(
            ReviewDecisionRecord.created_at.desc(), ReviewDecisionRecord.id.desc()
        )
        if case_id is not None:
            query = query.where(ReviewDecisionRecord.case_id == case_id)
        return list(self.session.scalars(query))

    def add_decision(
        self, case_id: str, action: str, factor: str | None, note: str | None
    ) -> ReviewDecisionRecord:
        record = ReviewDecisionRecord(
            case_id=case_id,
            action=action,
            factor=factor,
            note=note,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        self.session.add(record)
        self.session.commit()
        return record
```

```python
# apps/api/src/domain/review/service.py
from __future__ import annotations

from src.db.models import ReviewDecisionRecord
from src.domain.review.models import DecisionIn
from src.domain.review.repository import ReviewRepository


class CaseNotFound(Exception):
    pass


class FactorNotShown(Exception):
    pass


def _decision(record: ReviewDecisionRecord) -> dict:
    return {
        "id": record.id,
        "action": record.action,
        "factor": record.factor,
        "note": record.note,
        "createdAt": record.created_at.isoformat() + "Z",
    }


class ReviewService:
    def __init__(self, repository: ReviewRepository) -> None:
        self.repository = repository

    def list_cases(self) -> list[dict]:
        latest: dict[str, dict] = {}
        for record in self.repository.decisions():  # newest first
            latest.setdefault(record.case_id, _decision(record))
        return [
            {
                "caseId": case["caseId"],
                "displayName": case["displayName"],
                "institution": case["institution"],
                "course": case["context"]["course"],
                "risk": case["risk"],
                "flagged": case["flagged"],
                "verdict": case["reliability"]["verdict"],
                "selfTau": case["reliability"]["selfTau"],
                "latestDecision": latest.get(case["caseId"]),
            }
            for case in self.repository.cases()
        ]

    def get_case(self, case_id: str) -> dict:
        case = self.repository.case(case_id)
        if case is None:
            raise CaseNotFound(case_id)
        metadata = self.repository.metadata()
        return {
            "case": case,
            "scaleContext": metadata.get("scaleContext"),
            "featureLabels": metadata.get("featureLabels"),
            "decisions": [_decision(r) for r in self.repository.decisions(case_id)],
        }

    def record_decision(self, case_id: str, decision: DecisionIn) -> dict:
        case = self.repository.case(case_id)
        if case is None:
            raise CaseNotFound(case_id)
        shown = {f["feature"] for f in case["factors"]}
        if decision.factor is not None and decision.factor not in shown:
            raise FactorNotShown(decision.factor)
        record = self.repository.add_decision(
            case_id, decision.action, decision.factor, decision.note
        )
        return _decision(record)
```

```python
# apps/api/src/domain/review/router.py
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.session import get_db_session
from src.domain.review.models import DecisionIn
from src.domain.review.repository import ReviewRepository
from src.domain.review.service import CaseNotFound, FactorNotShown, ReviewService

router = APIRouter()
DbSession = Annotated[Session, Depends(get_db_session)]


def _service(session: Session) -> ReviewService:
    return ReviewService(ReviewRepository(session))


@router.get("/cases")
def list_cases(session: DbSession) -> list[dict]:
    return _service(session).list_cases()


@router.get("/cases/{case_id}")
def get_case(case_id: str, session: DbSession) -> dict:
    try:
        return _service(session).get_case(case_id)
    except CaseNotFound:
        raise HTTPException(status_code=404, detail="Case not found") from None


@router.post("/cases/{case_id}/decisions", status_code=201)
def record_decision(case_id: str, decision: DecisionIn, session: DbSession) -> dict:
    try:
        return _service(session).record_decision(case_id, decision)
    except CaseNotFound:
        raise HTTPException(status_code=404, detail="Case not found") from None
    except FactorNotShown:
        raise HTTPException(
            status_code=422, detail="factor must be one of the case's shown factors"
        ) from None
```

In `apps/api/src/api/router.py` add the import and mount:

```python
from src.domain.review.router import router as review_router
...
api_router.include_router(review_router, prefix="/review", tags=["review"])
```

- [ ] **Step 4: Run the tests**

Run: `cd apps/api && uv run python -m pytest tests/ -q`
Expected: all pass (new review tests plus the existing suite).

- [ ] **Step 5: Lint**

Run: `cd apps/api && uv run ruff check src tests`
Expected: `All checks passed!` (if the api project has no ruff, skip and note it).

---

### Task 4: Web data layer (types, loaders, formatting, server action)

**Files:**
- Create: `apps/web/lib/review/types.ts`, `apps/web/lib/review/loaders.ts`, `apps/web/lib/review/format.ts`, `apps/web/app/review/actions.ts`
- Create: `apps/web/tests/review.test.mjs`
- Modify: `apps/web/package.json` (script `test:review`)

**Interfaces:**
- Consumes: Task 3 HTTP contract.
- Produces: types `ReviewCaseSummary`, `ReviewCaseDetail`, `ReviewCase`, `ReviewFactor`, `ReviewDecision`, `ScaleContext`, `ReviewAction`; `tryLoadReviewCases(): Promise<ReviewCaseSummary[] | null>`; `tryLoadReviewCase(caseId): Promise<{ status: "ok"; detail: ReviewCaseDetail } | { status: "not_found" } | { status: "unavailable" }>`; `format.ts` exports `REVIEW_ACTIONS`, `actionLabel(a)`, `verdictLabel(v)`, `directionLabel(d)`, `formatPercent(x)`, `riskHeadline(risk, rankPct)`, `recomputationSummary(items)`; server action `saveDecision(caseId: string, prev: SaveState, formData: FormData): Promise<SaveState>` with `SaveState = { error: string | null; savedAt: string | null }`.

- [ ] **Step 1: Write the failing test**

```js
// apps/web/tests/review.test.mjs
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const web = path.resolve(here, "..");
const format = await import(path.join(web, "lib", "review", "format.ts"));

test("verdict and direction copy", () => {
  assert.equal(format.verdictLabel("stable"), "Stable explanation");
  assert.equal(format.verdictLabel("unstable"), "Unstable explanation");
  assert.equal(format.directionLabel("raises_risk"), "raises risk");
  assert.equal(format.directionLabel("lowers_risk"), "lowers risk");
  assert.equal(format.directionLabel("no_effect"), "no effect");
});

test("risk headline states risk of not passing and the cohort position", () => {
  assert.equal(format.riskHeadline(0.7234, 0.9), "72% risk of not passing · riskier than 90% of this course");
  assert.equal(format.formatPercent(0.005), "1%");
});

test("recomputation summary counts top factors", () => {
  const text = format.recomputationSummary([
    { feature: "cum_active_days", label: "Active days so far", count: 3 },
    { feature: "cum_clicks", label: "Total clicks so far", count: 2 }
  ]);
  assert.equal(text, "Active days so far ×3, Total clicks so far ×2");
});

test("every API action has a label", () => {
  for (const action of format.REVIEW_ACTIONS) {
    assert.ok(format.actionLabel(action).length > 0);
  }
  assert.deepEqual(format.REVIEW_ACTIONS, [
    "contact_student", "keep_monitoring", "no_action_needed", "factor_looks_wrong"
  ]);
});

test("the review page never hard-codes the gate threshold or invents data", () => {
  const files = [
    path.join(web, "app", "review", "page.tsx"),
    ...fs.readdirSync(path.join(web, "components", "review")).map((f) =>
      path.join(web, "components", "review", f)
    )
  ];
  for (const file of files) {
    const source = fs.readFileSync(file, "utf-8");
    assert.doesNotMatch(source, /0\.8\b|0\.80\b/, `${file} hard-codes the threshold`);
  }
  const page = fs.readFileSync(files[0], "utf-8");
  assert.match(page, /tryLoadReviewCases/);
  assert.match(page, /PlatformUnavailableNotice|not available/);
  assert.match(page, /XaiDisclaimer/);
});

test("the nav links to the review screen", () => {
  const nav = fs.readFileSync(path.join(web, "components", "layout", "nav-links.tsx"), "utf-8");
  assert.match(nav, /\["Explanation review", "\/review"\]/);
});
```

Add to `apps/web/package.json` scripts: `"test:review": "node --test tests/review.test.mjs"`.

- [ ] **Step 2: Run to verify it fails**

Run: `cd apps/web && node --test tests/review.test.mjs`
Expected: FAIL — cannot find module `lib/review/format.ts`.

- [ ] **Step 3: Write types, format helpers and loaders**

```ts
// apps/web/lib/review/types.ts
export type ReviewAction =
  | "contact_student"
  | "keep_monitoring"
  | "no_action_needed"
  | "factor_looks_wrong";
export type Verdict = "stable" | "unstable";
export type Direction = "raises_risk" | "lowers_risk" | "no_effect";

export type ReviewDecision = {
  id: number;
  action: ReviewAction;
  factor: string | null;
  note: string | null;
  createdAt: string;
};

export type ReviewCaseSummary = {
  caseId: string;
  displayName: string;
  institution: string;
  course: string;
  risk: number;
  flagged: boolean;
  verdict: Verdict;
  selfTau: number;
  latestDecision: ReviewDecision | null;
};

export type ReviewFeature = { feature: string; label: string; value: number; courseMedian: number };
export type ReviewFactor = ReviewFeature & { direction: Direction; share: number };
export type Recomputation = { feature: string; label: string; count: number };

export type ReviewCase = {
  caseId: string;
  displayName: string;
  institution: string;
  context: { course: string; week: number; nWeeks: number; cohortSize: number; passRate: number; modelAuc: number };
  risk: number;
  riskRankPct: number;
  flagged: boolean;
  factors: ReviewFactor[];
  reliability: { selfTau: number; threshold: number; verdict: Verdict; recomputations: Recomputation[] };
  features: ReviewFeature[];
};

export type ScaleContext = {
  threshold: number;
  coverage: number;
  retainedAgreement: number;
  noGateAgreement: number;
  source: string;
};

export type ReviewCaseDetail = {
  case: ReviewCase;
  scaleContext: ScaleContext | null;
  featureLabels: Record<string, string> | null;
  decisions: ReviewDecision[];
};
```

```ts
// apps/web/lib/review/format.ts
// Pure copy and number formatting for the review screen. No imports, so the
// node:test suite can load it directly with type stripping.

export const REVIEW_ACTIONS = [
  "contact_student",
  "keep_monitoring",
  "no_action_needed",
  "factor_looks_wrong"
] as const;

const ACTION_LABELS: Record<(typeof REVIEW_ACTIONS)[number], string> = {
  contact_student: "Contact the student",
  keep_monitoring: "Keep monitoring",
  no_action_needed: "No action needed",
  factor_looks_wrong: "A factor looks wrong"
};

export function actionLabel(action: (typeof REVIEW_ACTIONS)[number]): string {
  return ACTION_LABELS[action];
}

export function verdictLabel(verdict: "stable" | "unstable"): string {
  return verdict === "stable" ? "Stable explanation" : "Unstable explanation";
}

export function directionLabel(direction: "raises_risk" | "lowers_risk" | "no_effect"): string {
  if (direction === "raises_risk") return "raises risk";
  if (direction === "lowers_risk") return "lowers risk";
  return "no effect";
}

export function formatPercent(share: number): string {
  return `${Math.max(Math.round(share * 100), share > 0 ? 1 : 0)}%`;
}

export function riskHeadline(risk: number, rankPct: number): string {
  return `${formatPercent(risk)} risk of not passing · riskier than ${formatPercent(rankPct)} of this course`;
}

export function recomputationSummary(items: { label: string; count: number }[]): string {
  return items.map((item) => `${item.label} ×${item.count}`).join(", ");
}
```

```ts
// apps/web/lib/review/loaders.ts
import { fetchJson } from "@/lib/api/client";

import type { ReviewCaseDetail, ReviewCaseSummary } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

export async function tryLoadReviewCases(): Promise<ReviewCaseSummary[] | null> {
  try {
    return await fetchJson<ReviewCaseSummary[]>("/review/cases");
  } catch {
    return null;
  }
}

export type CaseLoad =
  | { status: "ok"; detail: ReviewCaseDetail }
  | { status: "not_found" }
  | { status: "unavailable" };

export async function tryLoadReviewCase(caseId: string): Promise<CaseLoad> {
  try {
    const response = await fetch(`${API_BASE_URL}/review/cases/${encodeURIComponent(caseId)}`, {
      cache: "no-store"
    });
    if (response.status === 404) return { status: "not_found" };
    if (!response.ok) return { status: "unavailable" };
    return { status: "ok", detail: (await response.json()) as ReviewCaseDetail };
  } catch {
    return { status: "unavailable" };
  }
}
```

- [ ] **Step 4: Write the server action**

```ts
// apps/web/app/review/actions.ts
"use server";

import { revalidatePath } from "next/cache";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

export type SaveState = { error: string | null; savedAt: string | null };

// Posts from the Next.js server, so the browser never calls the API directly
// and the API needs no CORS opening.
export async function saveDecision(
  caseId: string,
  _prev: SaveState,
  formData: FormData
): Promise<SaveState> {
  const action = String(formData.get("action") ?? "");
  const factor = formData.get("factor");
  const note = formData.get("note");
  const body: Record<string, string> = { action };
  if (action === "factor_looks_wrong" && factor) body.factor = String(factor);
  if (note && String(note).trim()) body.note = String(note);
  try {
    const response = await fetch(
      `${API_BASE_URL}/review/cases/${encodeURIComponent(caseId)}/decisions`,
      { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }
    );
    if (!response.ok) {
      const detail = await response.json().catch(() => null);
      return { error: `Not saved (${response.status}): ${JSON.stringify(detail?.detail ?? "")}`, savedAt: null };
    }
    revalidatePath("/review");
    return { error: null, savedAt: new Date().toISOString() };
  } catch {
    return { error: "Not saved: the API is not reachable.", savedAt: null };
  }
}
```

- [ ] **Step 5: Run the helper tests**

Run: `cd apps/web && node --test tests/review.test.mjs`
Expected: the four helper tests pass; the page and nav tests still fail (Task 5 creates those files).

---

### Task 5: Web UI — page, components, nav

**Files:**
- Create: `apps/web/app/review/page.tsx`
- Create: `apps/web/components/review/case-list.tsx`, `case-card.tsx`, `reliability-scale.tsx`, `factor-list.tsx`, `decision-form.tsx`
- Modify: `apps/web/components/layout/nav-links.tsx` (add link)

**Interfaces:**
- Consumes: Task 4 types, loaders, format helpers, `saveDecision`; existing `XaiDisclaimer`, `PlatformUnavailableNotice`, shadcn `Card`, `Badge`, `Button`.
- Produces: the `/review` route with query parameters `case`, `institution`, `verdict`.

Before writing the components, invoke the `frontend-design:frontend-design` skill and follow the existing app's visual language (tokens in `app/globals.css`, shadcn components); the structure below is fixed by the spec, the styling is not.

- [ ] **Step 1: Add the nav link** — in `components/layout/nav-links.tsx`:

```tsx
const links = [
  ["Dashboard", "/dashboard"],
  ["Students", "/students"],
  ["Explanation review", "/review"],
  ["Predictions", "/predictions"],
  ["Admin", "/admin"]
] as const;
```

- [ ] **Step 2: Write the page**

```tsx
// apps/web/app/review/page.tsx
import { CaseCard } from "@/components/review/case-card";
import { CaseList } from "@/components/review/case-list";
import { PlatformUnavailableNotice } from "@/components/common/platform-unavailable";
import { XaiDisclaimer } from "@/components/student/xai-disclaimer";
import { tryLoadReviewCase, tryLoadReviewCases } from "@/lib/review/loaders";

export const dynamic = "force-dynamic";
export const metadata = { title: "Explanation review" };

type SearchParams = { case?: string; institution?: string; verdict?: string };

export default async function ReviewPage({ searchParams }: { searchParams: SearchParams }) {
  const cases = await tryLoadReviewCases();
  if (!cases) {
    return (
      <main className="page">
        <PlatformUnavailableNotice />
      </main>
    );
  }
  if (cases.length === 0) {
    return (
      <main className="page">
        <div className="missing-notice">
          <h2>No review cases imported yet</h2>
          <p>Generate the frozen review payload, then restart the API (it imports on startup).</p>
          <pre>cd services/ml; uv run python -m src.export.export_teacher_review_payload</pre>
        </div>
      </main>
    );
  }

  const visible = cases.filter(
    (c) =>
      (!searchParams.institution || c.institution === searchParams.institution) &&
      (!searchParams.verdict || c.verdict === searchParams.verdict)
  );
  const selectedId = searchParams.case ?? visible[0]?.caseId ?? cases[0].caseId;
  const load = await tryLoadReviewCase(selectedId);

  return (
    <main className="page">
      <header className="page-header">
        <div>
          <p className="eyebrow">Explanation review</p>
          <h1>Can this student&apos;s explanation be trusted?</h1>
          <p className="page-header__lede">
            Historical cases from four universities. Each factor list comes with a reliability
            check: how much it changes when the explanation is recomputed.
          </p>
        </div>
      </header>
      <div className="review-layout">
        <CaseList
          cases={visible}
          all={cases}
          selectedId={selectedId}
          institution={searchParams.institution}
          verdict={searchParams.verdict}
        />
        <section aria-live="polite">
          {load.status === "ok" ? (
            <CaseCard detail={load.detail} />
          ) : load.status === "not_found" ? (
            <div className="missing-notice">
              <h2>Case not found</h2>
              <p>No review case has the id “{selectedId}”. Pick one from the list.</p>
            </div>
          ) : (
            <PlatformUnavailableNotice />
          )}
          <XaiDisclaimer />
        </section>
      </div>
    </main>
  );
}
```

- [ ] **Step 3: Write the case list**

```tsx
// apps/web/components/review/case-list.tsx
import Link from "next/link";

import { Badge } from "@/components/ui/badge";
import { formatPercent, verdictLabel } from "@/lib/review/format";
import type { ReviewCaseSummary } from "@/lib/review/types";

type Props = {
  cases: ReviewCaseSummary[];
  all: ReviewCaseSummary[];
  selectedId: string;
  institution?: string;
  verdict?: string;
};

function href(params: Record<string, string | undefined>) {
  const query = new URLSearchParams(
    Object.entries(params).filter((entry): entry is [string, string] => Boolean(entry[1]))
  );
  return `/review?${query.toString()}`;
}

export function CaseList({ cases, all, selectedId, institution, verdict }: Props) {
  const institutions = Array.from(new Set(all.map((c) => c.institution)));
  return (
    <nav className="review-list" aria-label="Review cases">
      <div className="review-list__filters">
        <Link href={href({ verdict })} className={!institution ? "is-active" : undefined}>All</Link>
        {institutions.map((name) => (
          <Link key={name} href={href({ institution: name, verdict })}
            className={institution === name ? "is-active" : undefined}>{name}</Link>
        ))}
      </div>
      <div className="review-list__filters">
        {(["stable", "unstable"] as const).map((v) => (
          <Link key={v} href={href({ institution, verdict: verdict === v ? undefined : v })}
            className={verdict === v ? "is-active" : undefined}>{verdictLabel(v)}</Link>
        ))}
      </div>
      <ul>
        {cases.map((c) => (
          <li key={c.caseId}>
            <Link href={href({ case: c.caseId, institution, verdict })}
              aria-current={c.caseId === selectedId ? "page" : undefined}
              className="review-list__item">
              <span className="review-list__name">{c.displayName}</span>
              <span className="review-list__meta">{c.institution} · {c.course}</span>
              <span className="review-list__risk">{formatPercent(c.risk)} risk</span>
              <Badge variant={c.verdict === "stable" ? "secondary" : "outline"}>
                {verdictLabel(c.verdict)}
              </Badge>
              {c.latestDecision ? <span className="review-list__decided">Decision recorded</span> : null}
            </Link>
          </li>
        ))}
      </ul>
      {cases.length === 0 ? <p className="muted">No cases match these filters.</p> : null}
    </nav>
  );
}
```

- [ ] **Step 4: Write the reliability scale**

```tsx
// apps/web/components/review/reliability-scale.tsx
import { Badge } from "@/components/ui/badge";
import { formatPercent, verdictLabel } from "@/lib/review/format";
import type { ReviewCase, ScaleContext } from "@/lib/review/types";

type Props = { reliability: ReviewCase["reliability"]; scale: ScaleContext | null };

// Kendall tau runs from -1 to 1; the scale shows 0..1, where every observed
// self-agreement sits, and clamps anything below 0 to the left edge.
const position = (tau: number) => `${Math.min(Math.max(tau, 0), 1) * 100}%`;

export function ReliabilityScale({ reliability, scale }: Props) {
  const stable = reliability.verdict === "stable";
  return (
    <section className="review-block" aria-labelledby="reliability-title">
      <div className="review-block__head">
        <h3 id="reliability-title">Explanation reliability</h3>
        <Badge variant={stable ? "secondary" : "destructive"}>{verdictLabel(reliability.verdict)}</Badge>
      </div>
      <div className="reliability-scale" role="img"
        aria-label={`Self-agreement ${reliability.selfTau.toFixed(2)} on a 0 to 1 scale; threshold ${reliability.threshold.toFixed(2)}`}>
        <div className="reliability-scale__track" />
        <div className="reliability-scale__threshold" style={{ left: position(reliability.threshold) }}>
          <span>threshold {reliability.threshold.toFixed(2)}</span>
        </div>
        <div className={`reliability-scale__marker${stable ? "" : " is-unstable"}`}
          style={{ left: position(reliability.selfTau) }}>
          <span>{reliability.selfTau.toFixed(2)}</span>
        </div>
        <div className="reliability-scale__ends"><span>0 · changes every time</span><span>1 · identical every time</span></div>
      </div>
      <p className="review-block__lede">
        {stable
          ? "Recomputing this explanation gives almost the same factor list."
          : "Recomputing this explanation reorders the factors — treat the list as a rough hint."}
      </p>
      {scale ? (
        <details className="review-details">
          <summary>About this scale</summary>
          <p>
            The explanation was recomputed 5 times with different reference samples; the score is
            how similar the factor orderings were (Kendall τ, 1 = identical). At the threshold{" "}
            {scale.threshold.toFixed(2)}, {formatPercent(scale.coverage)} of students get a factor
            list, and those lists agree with a second explanation method at{" "}
            {scale.retainedAgreement.toFixed(2)} instead of {scale.noGateAgreement.toFixed(2)}.
          </p>
        </details>
      ) : null}
    </section>
  );
}
```

- [ ] **Step 5: Write the factor list**

```tsx
// apps/web/components/review/factor-list.tsx
import { directionLabel, formatPercent, recomputationSummary } from "@/lib/review/format";
import type { ReviewCase } from "@/lib/review/types";

const fmt = (x: number) => (Number.isInteger(x) ? String(x) : x.toFixed(1));
const ARROW = { raises_risk: "↑", lowers_risk: "↓", no_effect: "–" } as const;

export function FactorList({ item }: { item: ReviewCase }) {
  const unstable = item.reliability.verdict === "unstable";
  return (
    <section className="review-block" aria-labelledby="factors-title">
      <h3 id="factors-title">Why the model flags this student</h3>
      {unstable ? (
        <p className="review-warning" role="note">
          This list changes when it is recomputed — do not act on single factors.
        </p>
      ) : null}
      <ol className={`factor-list${unstable ? " is-muted" : ""}`}>
        {item.factors.map((f) => (
          <li key={f.feature} className="factor-list__row">
            <span className={`factor-list__arrow is-${f.direction}`} aria-hidden="true">{ARROW[f.direction]}</span>
            <span className="factor-list__label">{f.label}</span>
            <span className="factor-list__dir">{directionLabel(f.direction)}</span>
            <span className="factor-list__value">{fmt(f.value)} <small>(course median {fmt(f.courseMedian)})</small></span>
            <span className="factor-list__bar" aria-label={`${formatPercent(f.share)} of the explanation`}>
              <span style={{ width: `${f.share * 100}%` }} />
            </span>
          </li>
        ))}
      </ol>
      {unstable ? (
        <details className="review-details">
          <summary>What 5 recomputations showed</summary>
          <p>Top factor each time: {recomputationSummary(item.reliability.recomputations)}.</p>
        </details>
      ) : null}
    </section>
  );
}
```

- [ ] **Step 6: Write the decision form (client) and the card**

```tsx
// apps/web/components/review/decision-form.tsx
"use client";

import { useState } from "react";
import { useFormState, useFormStatus } from "react-dom";

import { saveDecision, type SaveState } from "@/app/review/actions";
import { Button } from "@/components/ui/button";
import { actionLabel, REVIEW_ACTIONS } from "@/lib/review/format";
import type { ReviewDecision, ReviewFactor } from "@/lib/review/types";

const initial: SaveState = { error: null, savedAt: null };

function Submit() {
  const { pending } = useFormStatus();
  return <Button type="submit" disabled={pending}>{pending ? "Saving…" : "Save decision"}</Button>;
}

export function DecisionForm({ caseId, factors, decisions }: {
  caseId: string; factors: ReviewFactor[]; decisions: ReviewDecision[];
}) {
  const [state, formAction] = useFormState(saveDecision.bind(null, caseId), initial);
  const [action, setAction] = useState<string>("keep_monitoring");
  return (
    <section className="review-block" aria-labelledby="decision-title">
      <h3 id="decision-title">Teacher decision</h3>
      <form action={formAction} className="decision-form">
        <fieldset>
          <legend className="sr-only">Action</legend>
          {REVIEW_ACTIONS.map((a) => (
            <label key={a} className="decision-form__option">
              <input type="radio" name="action" value={a} checked={action === a}
                onChange={() => setAction(a)} />
              {actionLabel(a)}
            </label>
          ))}
        </fieldset>
        {action === "factor_looks_wrong" ? (
          <label className="decision-form__field">
            Which factor?
            <select name="factor" required defaultValue={factors[0]?.feature}>
              {factors.map((f) => <option key={f.feature} value={f.feature}>{f.label}</option>)}
            </select>
          </label>
        ) : null}
        <label className="decision-form__field">
          Note (optional)
          <textarea name="note" maxLength={1000} rows={3} />
        </label>
        <Submit />
        {state.error ? <p className="decision-form__error" role="alert">{state.error}</p> : null}
        {state.savedAt ? <p className="decision-form__ok" role="status">Decision saved.</p> : null}
      </form>
      <h4>History</h4>
      {decisions.length === 0 ? <p className="muted">No decisions yet.</p> : (
        <ul className="decision-history">
          {decisions.map((d) => (
            <li key={d.id}>
              <time dateTime={d.createdAt}>{new Date(d.createdAt).toLocaleString("en-GB")}</time>{" "}
              — {actionLabel(d.action)}
              {d.factor ? ` (${factors.find((f) => f.feature === d.factor)?.label ?? d.factor})` : ""}
              {d.note ? `: ${d.note}` : ""}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
```

```tsx
// apps/web/components/review/case-card.tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatPercent, riskHeadline } from "@/lib/review/format";
import type { ReviewCaseDetail } from "@/lib/review/types";

import { DecisionForm } from "./decision-form";
import { FactorList } from "./factor-list";
import { ReliabilityScale } from "./reliability-scale";

export function CaseCard({ detail }: { detail: ReviewCaseDetail }) {
  const item = detail.case;
  const c = item.context;
  return (
    <Card className="review-card">
      <CardHeader>
        <p className="eyebrow">{item.institution} · course {c.course} · week {c.week} of {c.nWeeks}</p>
        <CardTitle>{item.displayName}</CardTitle>
        <p className="review-card__risk">{riskHeadline(item.risk, item.riskRankPct)}</p>
        <p className="muted">
          Course: {c.cohortSize} students, {formatPercent(c.passRate)} passed. Model ranking quality
          on this course (AUC): {c.modelAuc.toFixed(2)}.
        </p>
      </CardHeader>
      <CardContent className="review-card__body">
        <ReliabilityScale reliability={item.reliability} scale={detail.scaleContext} />
        <FactorList item={item} />
        <DecisionForm caseId={item.caseId} factors={item.factors} decisions={detail.decisions} />
      </CardContent>
    </Card>
  );
}
```

- [ ] **Step 7: Add the styles** — append to `apps/web/app/globals.css` the classes used above (`review-layout`, `review-list*`, `review-card*`, `review-block*`, `reliability-scale*`, `factor-list*`, `review-warning`, `review-details`, `decision-form*`, `decision-history`), using the existing tokens (`--primary`, `--primary-soft`, `--border`, `--muted-foreground`); two columns at ≥ 1024 px (`grid-template-columns: 320px 1fr`), one column below; `is-muted` factor rows at reduced opacity; the unstable marker in the destructive colour; `focus-visible` outlines on list items and inputs.

- [ ] **Step 8: Run the tests, typecheck and build**

Run: `cd apps/web && node --test tests/review.test.mjs && npm run typecheck && npm run build`
Expected: all review tests pass; `tsc --noEmit` clean; `next build` succeeds (pages are dynamic, the build does not need the API).

---

### Task 6: End-to-end run, screenshots, docs

**Files:**
- Modify: `RUN_SERVICES.md` (review screen section)
- Modify: `docs/superpowers/specs/2026-09-24-teacher-review-screen-design.md` (the two deviations: mirrored split instead of refactor; seeded tie-break; camelCase keys; server action)

- [ ] **Step 1: Start the API on a fresh database**

Run: `cd apps/api && DATABASE_URL=sqlite:///../../.tmp_api_tests/review_demo.sqlite uv run uvicorn src.main:app --port 8000` (background)
Then: `curl -s localhost:8000/api/review/cases | python3 -c "import json,sys;d=json.load(sys.stdin);print(len(d), d[0]['caseId'])"`
Expected: `20 OU-1`

- [ ] **Step 2: Start the web app**

Run: `cd apps/web && npm run dev` (background), then open `http://localhost:3000/review`.

- [ ] **Step 3: Walk the demo path in a browser (Playwright MCP) and take screenshots**

Open `/review`; select a stable case and an unstable case; open "About this scale" and "What 5 recomputations showed"; choose "A factor looks wrong", pick a factor, add a note, save; confirm the decision appears in History and "Decision recorded" in the list; try `/review?case=XX-9` (case not found notice); stop the API and reload (not-available notice). Save screenshots to `docs/superpowers/specs/assets/teacher-review-*.png`.

- [ ] **Step 4: Document how to run it** — add to `RUN_SERVICES.md`:

```markdown
## Teacher explanation-review screen (practice week 6)

    cd services/ml; uv run python -m src.export.export_teacher_review_payload
    cd apps/api; uv run python -m src.import_research_payload   # or just start the API
    cd apps/api; uv run uvicorn src.main:app --reload --port 8000
    cd apps/web; npm run dev    # http://localhost:3000/review

The payload is frozen in `data/artifacts/research_demo/teacher_review_payload.json`;
decisions are stored in the local SQLite store and survive a re-import.
```

- [ ] **Step 5: Final verification**

Run: ML `uv run python -m pytest tests/test_teacher_review_export.py tests/test_local_stability.py -q`; API `uv run python -m pytest tests -q`; web `node --test tests/review.test.mjs && npm run typecheck`; `git status --short data/artifacts/experiments` empty.
Expected: all green; nothing under frozen experiments changed.
