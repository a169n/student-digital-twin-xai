# Cross-Institution Engagement Comparison (exp_012) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a genuinely apples-to-apples engagement-only PASSED-classification comparison across three institutions (OULAD DDD 2013J, OULAD BBB 2013J, KU Leuven 1819) and a cross-institution importance-stability analysis, to honestly answer exp_011's open next-step.

**Architecture:** Extract the dataset-agnostic core of the existing KU Leuven engagement runner into a shared module so OULAD runs through the **identical** classification + permutation-importance code path. Add the two missing OULAD engagement columns (`cumulative_active_days_to_date`, `content_click_ratio_to_date`) to the OULAD adapter. Run matched engagement feature sets on both OULAD cohorts, then aggregate all three institutions' existing JSON artifacts in a new analysis module that reuses `stability.py`.

**Tech Stack:** Python 3, scikit-learn (`permutation_importance`), pandas, NumPy, Pydantic + PyYAML (frozen configs), pytest, scipy (`kendalltau`, already a dependency). No new runtime dependencies.

**Commit policy:** This repo does NOT auto-commit. Each task ends with a `git commit` the WORKER runs only after the user has reviewed — when executing via subagents, stage the commit message but defer the actual commit to the user per the project's manual-commit policy. (Commit commands are shown for completeness and message consistency.)

---

## Decision context (why this plan exists)

exp_011 ran engagement-only PASSED classification on KU Leuven and found richer engagement neutral (ΔF1 = −0.015). Its next-step is a 3-institution comparison vs OULAD. But OULAD's existing experiments use assessment-laden feature blocks, so the comparison is not valid as-is. This plan adds a **matched engagement-only OULAD run** (scope decision recorded in `docs/superpowers/specs/2026-06-10-cross-institution-engagement-design.md`).

**Hard rules carried from the public-first pivot (do not violate):**
- This is a robustness check, not a win-hunt. A null/mixed OULAD delta is the expected, on-message result.
- Always report a fixed-model (`gradient_boosting`) table alongside best-per-cell.
- Leakage-safe features only: to-date cumulative columns, no global/cross-row statistics, no test-set information.
- KU Leuven exp_011 is committed and `completed`. Any refactor touching its runner MUST be behavior-preserving — exp_011 outputs must reproduce.

---

## File structure map

| File | Task | Responsibility | Action |
|---|---|---|---|
| `services/ml/src/benchmarks/oulad_adapter.py` | 1 | Add `cumulative_active_days_to_date` + `content_click_ratio_to_date` engagement columns | Modify |
| `services/ml/tests/test_oulad_engagement_columns.py` | 1 | New engagement columns present, leakage-safe, bounded | Create |
| `services/ml/src/experiments/engagement_benchmark.py` | 2 | Dataset-agnostic engagement benchmark core (split, train/score, importance, diagnostics, render) | Create |
| `services/ml/src/experiments/run_engagement_benchmark_kuleuven.py` | 2 | Becomes a thin KU Leuven entry point calling the shared core | Modify |
| `services/ml/tests/test_engagement_benchmark_core.py` | 2 | Core helpers behave identically; KU entry still loads | Create |
| `services/ml/src/experiments/run_engagement_benchmark_oulad.py` | 3 | Thin OULAD entry point: build OULAD snapshots, call shared core | Create |
| `services/ml/configs/experiments/exp_012_oulad_engagement_ddd2013j.yaml` | 4 | Frozen config: matched engagement sets, DDD 2013J | Create |
| `services/ml/configs/experiments/exp_012_oulad_engagement_bbb2013j.yaml` | 4 | Frozen config: matched engagement sets, BBB 2013J | Create |
| `services/ml/tests/test_oulad_engagement_benchmark.py` | 4 | Configs load, declare matched engagement sets, classification-only | Create |
| `services/ml/src/experiments/analyze_cross_institution_engagement.py` | 5 | Concept-aligned 3-institution delta + importance-stability analysis | Create |
| `services/ml/tests/test_cross_institution_engagement.py` | 5 | Concept alignment, delta aggregation, τ over aligned concepts | Create |
| `docs/experiments/exp_012_oulad_engagement.md` + `registry.md` | 6 | Experiment record + registry rows | Create/Modify |
| `docs/dissertation/final_research_conclusions.md`, `defense_summary.md` | 7 | Cross-institution robustness write-up | Modify |

**Pre-execution reads (required, per phase):**
- Task 1: `oulad_adapter.py` lines 400–530 (VLE activity builder) and 1075–1205 (`_add_trend_and_index_features`, `_finalize_snapshot_frame`).
- Task 2: `run_engagement_benchmark_kuleuven.py` lines 69–595 in full (the dataclasses, config models, and the helpers `build_split`, `_train_and_score_classification`, `compute_permutation_importance`, `_best_classification_by_feature_set`, `_fixed_model_classification_by_feature_set`, `build_benchmark_diagnostics`, `_interpret_engagement_result`) and 660–1160 (`run_kuleuven_engagement_benchmark`, artifact writers, `render_experiment_markdown`). Identify exactly which functions are dataset-agnostic (everything except `build_weekly_engagement_snapshots` usage and `KuLeuvenDataConfig`).
- Task 3: the Task-2 core module's public surface; `oulad_adapter.build_weekly_snapshots` signature and its `OuladRawPaths` / `OuladCourseFilter`.
- Task 5: `analyze_cross_cohort_stability.py` (full — the model to mirror) and one of the exp_011 / exp_007 results JSON files to confirm the importance-row key names.

---

## Phase 1: OULAD engagement columns

### Task 1: Add `cumulative_active_days_to_date` and `content_click_ratio_to_date` to the OULAD adapter

**Files:**
- Modify: `services/ml/src/benchmarks/oulad_adapter.py`
- Test: `services/ml/tests/test_oulad_engagement_columns.py`

- [ ] **Step 1: Write the failing test**

```python
# services/ml/tests/test_oulad_engagement_columns.py
from pathlib import Path

import pandas as pd
from src.benchmarks.oulad_adapter import (
    OuladCourseFilter,
    OuladRawPaths,
    build_weekly_snapshots,
)

OULAD = Path("datasets/oulad")


def _snapshots():
    raw = OuladRawPaths(
        assessments=OULAD / "assessments.csv",
        courses=OULAD / "courses.csv",
        student_info=OULAD / "studentInfo.csv",
        student_registration=OULAD / "studentRegistration.csv",
        student_vle=OULAD / "studentVle.csv",
        vle=OULAD / "vle.csv",
        student_assessment=OULAD / "studentAssessment.csv",
    )
    return build_weekly_snapshots(
        raw,
        course_filter=OuladCourseFilter("DDD", "2013J"),
        min_week=4,
        max_week=None,
    ).snapshots


def test_engagement_columns_present_bounded_and_monotone():
    snaps = _snapshots()
    for col in ["cumulative_active_days_to_date", "content_click_ratio_to_date"]:
        assert col in snaps.columns, f"missing {col}"

    # content ratio is a proportion in [0, 1]
    ratio = pd.to_numeric(snaps["content_click_ratio_to_date"], errors="coerce")
    assert ratio.min() >= 0.0
    assert ratio.max() <= 1.0

    # cumulative active days never decreases within a student-course-presentation
    key = ["code_module", "code_presentation", "student_id"]
    ordered = snaps.sort_values(key + ["week_number"])
    diffs = ordered.groupby(key)["cumulative_active_days_to_date"].diff().dropna()
    assert (diffs >= -1e-9).all(), "cumulative_active_days_to_date must be monotone non-decreasing"
```

> Note: confirm the student-key column names against `KEY_COLUMNS` in `oulad_adapter.py` while reading; adjust `key` if the adapter names differ.

- [ ] **Step 2: Run test to verify it fails**

Run: `cd services/ml && python -m pytest tests/test_oulad_engagement_columns.py -v`
Expected: FAIL with `missing cumulative_active_days_to_date`.

- [ ] **Step 3: Collect distinct active days per week in the VLE activity builder**

In the VLE-activity function (the one ending `return activity, selected_rows` near line 527), inside the per-chunk loop add a day collector mirroring the existing `type_parts` pattern (the chunk already has `date` and `activity_week`). Near the top of the loop body where `type_parts` is appended (~line 452), add:

```python
        day_part = chunk.loc[
            :, list(KEY_COLUMNS) + ["activity_week", "date"]
        ].drop_duplicates()
        day_parts.append(day_part)
```

Initialize `day_parts: list[pd.DataFrame] = []` next to where `weekly_parts` / `type_parts` are initialized (above the chunk loop).

- [ ] **Step 4: Aggregate distinct days and add cumulative active-days column**

After the `type_counts` merge block (~line 508–515) and BEFORE the `activity = activity.sort_values(base_cols)` line (517), add:

```python
    if day_parts:
        day_frame = pd.concat(day_parts, ignore_index=True).drop_duplicates()
        day_counts = (
            day_frame.groupby(list(KEY_COLUMNS) + ["activity_week"])
            .size()
            .rename("current_week_active_days")
            .reset_index()
            .rename(columns={"activity_week": "week_number"})
        )
        activity = activity.merge(day_counts, on=base_cols, how="left")
    else:
        activity["current_week_active_days"] = 0
    activity["current_week_active_days"] = (
        pd.to_numeric(activity["current_week_active_days"], errors="coerce")
        .fillna(0)
        .astype(int)
    )
```

Then, in the cumulative block right after `group = activity.groupby(list(KEY_COLUMNS), sort=False)` (~line 518), add a cumulative active-days line alongside the existing `cumulative_clicks_to_date` cumsum:

```python
    activity["cumulative_active_days_to_date"] = group["current_week_active_days"].cumsum()
```

- [ ] **Step 5: Add `content_click_ratio_to_date` in `_add_trend_and_index_features`**

In `_add_trend_and_index_features` (near line 1075), after the index computations and before `return out`, add (reuse the module's `_safe_divide`):

```python
    out["content_click_ratio_to_date"] = (
        _safe_divide(
            out["cumulative_content_clicks_to_date"],
            out["cumulative_clicks_to_date"],
        )
        .fillna(0.0)
        .clip(0.0, 1.0)
    )
```

- [ ] **Step 6: Register the new columns in `_finalize_snapshot_frame`**

Add both columns to the `fill_zero` list (so missing values become 0.0):

```python
        "current_week_active_days",
        "cumulative_active_days_to_date",
        "content_click_ratio_to_date",
```

And add `"cumulative_active_days_to_date"` and `"content_click_ratio_to_date"` to the `preferred_order` list (place them near `cumulative_clicks_to_date`, e.g. immediately after `"cumulative_other_clicks_to_date"`).

- [ ] **Step 7: Run test to verify it passes**

Run: `cd services/ml && python -m pytest tests/test_oulad_engagement_columns.py -v`
Expected: PASS.

- [ ] **Step 8: Run the existing OULAD adapter tests to confirm no regression**

Run: `cd services/ml && python -m pytest tests/test_oulad_full_ablation.py -v`
Expected: PASS (existing trend/index column tests unaffected).

- [ ] **Step 9: Commit**

```bash
git add services/ml/src/benchmarks/oulad_adapter.py services/ml/tests/test_oulad_engagement_columns.py
git commit -m "feat(oulad): add active-days and content-click-ratio engagement columns"
```

---

## Phase 2: Shared engagement-benchmark core

### Task 2: Extract the dataset-agnostic core from the KU Leuven runner

**Goal:** Make the classification + permutation-importance methodology reusable so OULAD runs through the identical path. Behavior-preserving for KU Leuven.

**Files:**
- Create: `services/ml/src/experiments/engagement_benchmark.py`
- Modify: `services/ml/src/experiments/run_engagement_benchmark_kuleuven.py`
- Test: `services/ml/tests/test_engagement_benchmark_core.py`

**Pre-execution read (required):** `run_engagement_benchmark_kuleuven.py` lines 69–595 and 660–1160 in full. The dataset-agnostic functions to MOVE are (verified present): `BenchmarkFeatureSet`, `_SplitPartition`, the generic config models (`DocumentationConfig`, `FeatureSetConfig`, `ComparisonConfig`, `StudentGroupSplitConfig`, `TemporalForwardSplitConfig`, `SplitsConfig`, `OutputsConfig`), `build_split`, `_train_and_score_classification`, `compute_permutation_importance`, `_best_classification_by_feature_set`, `_fixed_model_classification_by_feature_set`, `build_benchmark_diagnostics`, `_interpret_engagement_result`, the artifact writers (`_write_result_artifacts`, `_write_importance_csv`), and `render_experiment_markdown`. KEEP in the KU module: `KuLeuvenDataConfig`, `KuLeuvenEngagementConfig`, `load_kuleuven_engagement_config`, and `run_kuleuven_engagement_benchmark` (which calls `build_weekly_engagement_snapshots`).

- [ ] **Step 1: Write the characterization test FIRST (captures current KU behavior)**

```python
# services/ml/tests/test_engagement_benchmark_core.py
import numpy as np
import pandas as pd


def test_core_split_and_importance_importable():
    # After extraction these live in the shared core module.
    from src.experiments.engagement_benchmark import (
        BenchmarkFeatureSet,
        build_split,
        compute_permutation_importance,
        _fixed_model_classification_by_feature_set,
    )

    assert BenchmarkFeatureSet(name="x", description="d", columns=("a",)).all_columns() == ("a",)


def test_fixed_model_classification_filters_one_model():
    from src.experiments.engagement_benchmark import _fixed_model_classification_by_feature_set

    table = pd.DataFrame(
        [
            {"task": "classification", "split_strategy": "student_group", "feature_set": "A", "model": "gradient_boosting", "metric_f1": 0.75, "metric_accuracy": 0.6, "metric_roc_auc": 0.7, "n_train_rows": 1, "n_test_rows": 1},
            {"task": "classification", "split_strategy": "student_group", "feature_set": "A", "model": "logistic_regression", "metric_f1": 0.70, "metric_accuracy": 0.6, "metric_roc_auc": 0.65, "n_train_rows": 1, "n_test_rows": 1},
        ]
    )
    rows = _fixed_model_classification_by_feature_set(
        table, model="gradient_boosting", baseline_feature_set="A", primary_split="student_group"
    )
    assert all(r["model"] == "gradient_boosting" for r in rows)
```

> Adjust the column names in the second test to the actual keys produced by `results_to_dataframe` / `_fixed_model_classification_by_feature_set` (read them during the pre-execution read; the metric prefix may be `metric_` or bare). The test must reflect the real signature, not a guessed one.

- [ ] **Step 2: Run test to verify it fails**

Run: `cd services/ml && python -m pytest tests/test_engagement_benchmark_core.py -v`
Expected: FAIL with `ModuleNotFoundError: src.experiments.engagement_benchmark`.

- [ ] **Step 3: Create the core module by moving the dataset-agnostic functions**

Create `services/ml/src/experiments/engagement_benchmark.py`. MOVE (cut, not copy) the functions/classes listed in the pre-execution read, preserving their bodies verbatim. Carry over exactly the imports they need (`numpy`, `pandas`, `permutation_importance`, `ClassificationModelName`, `GROUP_COLUMN`, `WEEK_COLUMN`, `compute_classification_metrics`, `results_to_dataframe`, `build_classification_model`, `iter_classification_models`, `PreparedMatrix`, `build_modeling_matrix`, `fit_imputer_on_training`, `select_rows`, `student_group_split`, the metadata helpers used by the artifact writers, `ResultRow`). Keep `run_kuleuven_engagement_benchmark`'s body in the KU module but have it call the moved helpers via import.

- [ ] **Step 4: Update the KU runner to import from the core**

In `run_engagement_benchmark_kuleuven.py`, replace the moved definitions with:

```python
from src.experiments.engagement_benchmark import (
    BenchmarkFeatureSet,
    DocumentationConfig,
    FeatureSetConfig,
    ComparisonConfig,
    StudentGroupSplitConfig,
    TemporalForwardSplitConfig,
    SplitsConfig,
    OutputsConfig,
    build_split,
    compute_permutation_importance,
    build_benchmark_diagnostics,
    render_experiment_markdown,
    # ...and the remaining moved names actually used by the KU entry point
)
```

Keep `KuLeuvenDataConfig`, `KuLeuvenEngagementConfig`, `load_kuleuven_engagement_config`, `run_kuleuven_engagement_benchmark`, `main`.

- [ ] **Step 5: Run the new core test + the existing KU tests**

Run: `cd services/ml && python -m pytest tests/test_engagement_benchmark_core.py tests/test_kuleuven_engagement.py tests/test_ku_leuven_adapter.py -v`
Expected: PASS (KU behavior preserved; core importable).

- [ ] **Step 6: Behavior-preservation guard — re-run exp_011 and confirm headline unchanged**

Run: `cd services/ml && python -m src.experiments.run_engagement_benchmark_kuleuven --config configs/experiments/exp_011_kuleuven_engagement.yaml`
Then compare the regenerated `data/artifacts/experiments/exp_011_kuleuven_engagement/exp_011_kuleuven_engagement_results.csv` against git HEAD:

Run: `cd ../.. && git diff --stat services/ml/data/artifacts/experiments/exp_011_kuleuven_engagement/`
Expected: no substantive metric changes (numbers identical; only timestamps/paths may differ). If metrics changed, the extraction altered behavior — revert and redo verbatim. **Restore the artifacts to HEAD afterwards** (`git checkout -- services/ml/data/artifacts/experiments/exp_011_kuleuven_engagement/`) so exp_011 stays as committed.

- [ ] **Step 7: Commit**

```bash
git add services/ml/src/experiments/engagement_benchmark.py services/ml/src/experiments/run_engagement_benchmark_kuleuven.py services/ml/tests/test_engagement_benchmark_core.py
git commit -m "refactor(engagement): extract dataset-agnostic engagement benchmark core"
```

---

## Phase 3: OULAD engagement entry point

### Task 3: Create `run_engagement_benchmark_oulad.py`

**Files:**
- Create: `services/ml/src/experiments/run_engagement_benchmark_oulad.py`
- Test: extended in Task 4 (`test_oulad_engagement_benchmark.py`)

**Pre-execution read (required):** the Task-2 core public surface; `oulad_adapter.build_weekly_snapshots`, `OuladRawPaths`, `OuladCourseFilter`; the KU entry `run_kuleuven_engagement_benchmark` (to mirror its shape: build snapshots → set `passed`/`final_grade` placeholder → call core diagnostics → write artifacts).

- [ ] **Step 1: Write a smoke test that the OULAD entry builds a modeling frame with required columns**

```python
# append to services/ml/tests/test_oulad_engagement_benchmark.py (created in Task 4;
# if running Task 3 first, create the file with just this test)
from src.experiments.run_engagement_benchmark_oulad import build_oulad_engagement_frame


def test_oulad_engagement_frame_has_required_columns():
    frame = build_oulad_engagement_frame(
        code_module="DDD", code_presentation="2013J", min_week=4
    )
    for col in [
        "student_id", "week_number", "passed", "final_grade",
        "cumulative_clicks_to_date", "cumulative_active_days_to_date",
        "content_click_ratio_to_date",
    ]:
        assert col in frame.columns, f"missing {col}"
    # passed is binary; final_grade is the structural placeholder == float(passed)
    assert set(frame["passed"].dropna().unique()) <= {0, 1, 0.0, 1.0}
```

- [ ] **Step 2: Run, confirm FAIL** (`ModuleNotFoundError` / `ImportError`).

Run: `cd services/ml && python -m pytest tests/test_oulad_engagement_benchmark.py::test_oulad_engagement_frame_has_required_columns -v`

- [ ] **Step 3: Implement `build_oulad_engagement_frame` + the runner**

Create `run_engagement_benchmark_oulad.py` with:
- `build_oulad_engagement_frame(code_module, code_presentation, min_week, max_week=None, raw_dir="datasets/oulad") -> pd.DataFrame`: build snapshots via `oulad_adapter.build_weekly_snapshots`; map the modeling columns the core expects — rename/copy `student_id` (from `KEY_COLUMNS` student field) to the core's `GROUP_COLUMN`, ensure `week_number` == `WEEK_COLUMN`; set `passed = snapshots["passed_observed"]` and `final_grade = passed.astype(float)` (structural placeholder, matching KU Leuven's documented convention). Drop rows where `passed` is NaN.
- A `load_*` config loader and `run_oulad_engagement_benchmark(config_path)` that mirrors `run_kuleuven_engagement_benchmark` but swaps the snapshot source for `build_oulad_engagement_frame`, then calls the shared-core diagnostics, importance, artifact writers, and `render_experiment_markdown`. Reuse `KuLeuvenEngagementConfig`'s structure or define an analogous `OuladEngagementConfig` that points at OULAD raw files + a `course_filter`.
- A `main()` + argparse `--config`, mirroring the KU runner.

Honest-framing string in the generated summary: classification-only; regression intentionally omitted (engagement-only matched design); note the `cumulative_social_clicks_to_date` (forum clicks) ↔ KU `forum_posts` unit difference is handled at the ranking level in the cross-institution analysis.

- [ ] **Step 4: Run, confirm PASS.**

Run: `cd services/ml && python -m pytest tests/test_oulad_engagement_benchmark.py::test_oulad_engagement_frame_has_required_columns -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add services/ml/src/experiments/run_engagement_benchmark_oulad.py services/ml/tests/test_oulad_engagement_benchmark.py
git commit -m "feat(oulad): add OULAD engagement benchmark entry point on shared core"
```

---

## Phase 4: exp_012 configs and runs

### Task 4: Create the two exp_012 configs and run both cohorts

**Files:**
- Create: `services/ml/configs/experiments/exp_012_oulad_engagement_ddd2013j.yaml`
- Create: `services/ml/configs/experiments/exp_012_oulad_engagement_bbb2013j.yaml`
- Test: `services/ml/tests/test_oulad_engagement_benchmark.py`

The matched engagement feature sets (mirror KU Leuven exp_011, intersect with OULAD-buildable concepts):

- `A_simple_engagement_oulad`: columns `cumulative_clicks_to_date`, `cumulative_active_days_to_date`; indicator `has_vle_activity_to_date`.
- `B_engagement_oulad`: columns `cumulative_clicks_to_date`, `cumulative_active_days_to_date`, `current_week_clicks`, `cumulative_content_clicks_to_date`, `cumulative_social_clicks_to_date`, `content_click_ratio_to_date`, `week_number`; indicator `has_vle_activity_to_date`.

- [ ] **Step 1: Write the failing config test**

```python
# services/ml/tests/test_oulad_engagement_benchmark.py
from src.experiments.run_engagement_benchmark_oulad import load_oulad_engagement_config


def test_exp012_configs_declare_matched_engagement_sets():
    for cohort in ("ddd2013j", "bbb2013j"):
        config = load_oulad_engagement_config(
            f"configs/experiments/exp_012_oulad_engagement_{cohort}.yaml"
        )
        names = set(config.feature_sets)
        assert {"A_simple_engagement_oulad", "B_engagement_oulad"} <= names
        # classification-only: no regression model family declared (or empty)
        assert not getattr(config, "regression_models", []) , "exp_012 must be classification-only"
```

> Adjust the accessor names (`config.feature_sets`, `config.regression_models`) to match the config object the loader returns; if the loader returns `(config, raw)` like the OULAD benchmark loader, unpack accordingly.

- [ ] **Step 2: Run, confirm FAIL** (config files do not exist yet).

Run: `cd services/ml && python -m pytest tests/test_oulad_engagement_benchmark.py::test_exp012_configs_declare_matched_engagement_sets -v`

- [ ] **Step 3: Write `exp_012_oulad_engagement_ddd2013j.yaml`**

```yaml
experiment:
  experiment_id: "exp_012_oulad_engagement_ddd2013j"
  title: "Matched engagement-only PASSED classification on OULAD (DDD 2013J)"
  schema_version: "external_oulad_adapter_v1"
  dataset_version: "OULAD"
  dataset_config_name: "local OULAD CSV files; DDD 2013J engagement-only subset"
  parent_experiment: "exp_011_kuleuven_engagement"
  status: "completed"

documentation:
  objective: >
    Run an engagement-only (clickstream-derived) PASSED classification on OULAD
    DDD 2013J using feature sets matched to the KU Leuven exp_011 design, so the
    three-institution engagement comparison is apples-to-apples. No assessment
    or mastery features are used; no regression is reported.
  hypothesis: >
    Richer engagement features (B_engagement_oulad) will add little over the
    minimal click/active-days baseline (A_simple_engagement_oulad) on both
    splits, echoing the engagement-richness-neutral KU Leuven result.
  limitations:
    - >
      OULAD VLE logs are daily-granular and have no within-day session
      boundaries, so KU Leuven's session-based engagement features have no
      analog and are excluded from the matched set.
    - >
      cumulative_social_clicks_to_date counts forum/social CLICKS, whereas KU
      Leuven's forum signal counts POSTS; the cross-institution comparison uses
      importance RANKS, not magnitudes, to tolerate this unit difference.
    - >
      Engagement-only classification is a deliberate constraint to match KU
      Leuven, not a claim that engagement is the best OULAD predictor.
  next_step: >
    Feed these results into analyze_cross_institution_engagement together with
    the BBB 2013J run and KU Leuven exp_011 for the three-institution delta and
    importance-stability comparison.

oulad:
  raw_dir: "datasets/oulad"
  files:
    assessments: "assessments.csv"
    courses: "courses.csv"
    student_info: "studentInfo.csv"
    student_registration: "studentRegistration.csv"
    student_vle: "studentVle.csv"
    vle: "vle.csv"
    student_assessment: "studentAssessment.csv"
  processed_snapshots_csv: "data/artifacts/experiments/exp_012_oulad_engagement_ddd2013j/oulad_weekly_snapshots.csv"
  course_filter:
    code_module: "DDD"
    code_presentation: "2013J"
  min_week: 4
  max_week: null
  student_vle_chunk_size: 500000

feature_sets:
  A_simple_engagement_oulad:
    description: "Minimal OULAD engagement baseline: cumulative clicks and active days only."
    columns:
      - "cumulative_clicks_to_date"
      - "cumulative_active_days_to_date"
    indicator_columns:
      - "has_vle_activity_to_date"
  B_engagement_oulad:
    description: "Richer OULAD engagement set matched to KU Leuven B_engagement (intersection of buildable concepts)."
    columns:
      - "cumulative_clicks_to_date"
      - "cumulative_active_days_to_date"
      - "current_week_clicks"
      - "cumulative_content_clicks_to_date"
      - "cumulative_social_clicks_to_date"
      - "content_click_ratio_to_date"
      - "week_number"
    indicator_columns:
      - "has_vle_activity_to_date"

feature_set_order:
  - "A_simple_engagement_oulad"
  - "B_engagement_oulad"

comparison:
  baseline_feature_set: "A_simple_engagement_oulad"
  candidate_feature_set: "B_engagement_oulad"
  primary_split: "temporal_forward"
  fixed_model: "gradient_boosting"

classification_models:
  - "logistic_regression"
  - "random_forest"
  - "gradient_boosting"

regression_models: []

splits:
  primary: "student_group"
  secondary: "temporal_forward"
  student_group:
    test_size: 0.25
    validation_size: 0.0
    seed: 42
  temporal_forward:
    train_weeks: 20
    student_test_size: 0.25
    student_seed: 42

permutation_importance:
  feature_set: "B_engagement_oulad"
  n_repeats: 15
  scoring: "roc_auc"
  seed: 42

seed: 42

outputs:
  experiments_dir: "data/artifacts/experiments/exp_012_oulad_engagement_ddd2013j"
```

> Match the exact config KEY names to whatever `load_oulad_engagement_config` (Task 3) expects. If the Task-3 loader reuses the KU Leuven config schema, align field names (e.g. `permutation_importance` block shape) to it. The values above are the contract; the keys must match the loader.

- [ ] **Step 4: Write `exp_012_oulad_engagement_bbb2013j.yaml`**

Copy the DDD file and change: `experiment_id` → `exp_012_oulad_engagement_bbb2013j`; `title` → `... (BBB 2013J)`; `dataset_config_name` → `... BBB 2013J ...`; `course_filter.code_module` → `"BBB"`; `processed_snapshots_csv` and `outputs.experiments_dir` → the `exp_012_oulad_engagement_bbb2013j` artifact dir. Keep everything else identical.

- [ ] **Step 5: Run, confirm config test PASS.**

Run: `cd services/ml && python -m pytest tests/test_oulad_engagement_benchmark.py -v`
Expected: PASS.

- [ ] **Step 6: Execute both runs**

Run:
```bash
cd services/ml
python -m src.experiments.run_engagement_benchmark_oulad --config configs/experiments/exp_012_oulad_engagement_ddd2013j.yaml
python -m src.experiments.run_engagement_benchmark_oulad --config configs/experiments/exp_012_oulad_engagement_bbb2013j.yaml
```
Expected: each writes `data/artifacts/experiments/exp_012_oulad_engagement_<cohort>/` with `*_results.{csv,json}`, `engagement_importance.csv`, `*_summary.md`, snapshots, and updates `docs/experiments/registry.md`.

- [ ] **Step 7: Sanity-check the headline.** Read each `*_summary.md`. Confirm: classification F1 is reported for both splits, a fixed-model table is present, ΔF1 (`B_engagement_oulad` − `A_simple_engagement_oulad`) is recorded, and no regression metrics appear.

- [ ] **Step 8: Commit code + artifacts**

```bash
git add services/ml/configs/experiments/exp_012_oulad_engagement_*.yaml \
        services/ml/data/artifacts/experiments/exp_012_oulad_engagement_* \
        docs/experiments/registry.md services/ml/tests/test_oulad_engagement_benchmark.py
git commit -m "exp(exp_012): run matched engagement-only classification on OULAD DDD and BBB 2013J"
```

---

## Phase 5: Cross-institution analysis

### Task 5: Build `analyze_cross_institution_engagement.py`

**Files:**
- Create: `services/ml/src/experiments/analyze_cross_institution_engagement.py`
- Test: `services/ml/tests/test_cross_institution_engagement.py`

**Pre-execution read (required):** `analyze_cross_cohort_stability.py` (full — mirror its structure) and one results JSON each from exp_011 and exp_012 to confirm: (a) the per-cell classification metric keys (for the delta table) and (b) the importance-row structure/keys for the importance-stability part.

The canonical concept-alignment map (from the spec):

```python
CONCEPT_ALIGNMENT = {
    "total_clicks":     {"oulad": "cumulative_clicks_to_date",        "ku_leuven": "cumulative_clicks_to_date"},
    "current_clicks":   {"oulad": "current_week_clicks",              "ku_leuven": "current_week_clicks"},
    "content_clicks":   {"oulad": "cumulative_content_clicks_to_date","ku_leuven": "cumulative_content_clicks_to_date"},
    "forum_engagement": {"oulad": "cumulative_social_clicks_to_date", "ku_leuven": "cumulative_forum_posts_to_date"},
    "content_ratio":    {"oulad": "content_click_ratio_to_date",      "ku_leuven": "content_click_ratio_to_date"},
    "active_days":      {"oulad": "cumulative_active_days_to_date",    "ku_leuven": "cumulative_active_days_to_date"},
    "week":             {"oulad": "week_number",                      "ku_leuven": "week_number"},
}
# KU-only (no OULAD analog): cumulative_sessions_to_date, avg_session_clicks_to_date, days_since_course_start
```

- [ ] **Step 1: Write the failing test**

```python
# services/ml/tests/test_cross_institution_engagement.py
from src.experiments.analyze_cross_institution_engagement import (
    align_ranking_to_concepts,
    build_engagement_delta_table,
    build_cross_institution_importance,
)


def test_align_ranking_to_concepts_renames_and_drops_unmapped():
    ranking = [
        "cumulative_active_days_to_date",
        "cumulative_clicks_to_date",
        "cumulative_sessions_to_date",  # KU-only, must drop
    ]
    aligned = align_ranking_to_concepts(ranking, institution="ku_leuven")
    assert aligned == ["active_days", "total_clicks"]


def test_importance_stability_identical_rankings_tau_one():
    # Two institutions, identical concept ranking -> tau = 1.0
    rankings = {
        "OULAD_DDD": ["active_days", "total_clicks", "content_clicks", "week"],
        "KU_Leuven": ["active_days", "total_clicks", "content_clicks", "week"],
    }
    report = build_cross_institution_importance({"temporal_forward": rankings}, top_k=3)
    cell = report["per_split"]["temporal_forward"]["pairs"][0]
    assert cell["kendall_tau"] == 1.0


def test_delta_table_computes_b_minus_a():
    # fixed-model rows per institution; delta = B - A on F1
    per_institution = {
        "OULAD_DDD": {
            "temporal_forward": {"A_simple_engagement_oulad": {"f1": 0.70}, "B_engagement_oulad": {"f1": 0.68}},
        },
    }
    table = build_engagement_delta_table(
        per_institution,
        baseline_key_by_inst={"OULAD_DDD": "A_simple_engagement_oulad"},
        candidate_key_by_inst={"OULAD_DDD": "B_engagement_oulad"},
    )
    row = [r for r in table if r["institution"] == "OULAD_DDD" and r["split"] == "temporal_forward"][0]
    assert abs(row["delta_f1"] - (-0.02)) < 1e-9
```

> Adjust input shapes to whatever the real results JSON exposes once read; the three behaviors under test (concept alignment with drop, τ over aligned concepts, B−A delta) are the contract.

- [ ] **Step 2: Run, confirm FAIL** (`ModuleNotFoundError`).

Run: `cd services/ml && python -m pytest tests/test_cross_institution_engagement.py -v`

- [ ] **Step 3: Implement the analysis module**

Create `analyze_cross_institution_engagement.py` mirroring `analyze_cross_cohort_stability.py`, with:
- `CONCEPT_ALIGNMENT` and a reverse lookup per institution.
- `align_ranking_to_concepts(ranking, institution)`: map each raw feature to its canonical concept; drop features with no canonical mapping (KU-only / unmapped); preserve order; dedupe.
- `build_engagement_delta_table(per_institution, baseline_key_by_inst, candidate_key_by_inst)`: for each institution × split, `delta_f1 = candidate.f1 − baseline.f1` (and `delta_roc_auc`), from the fixed-model metrics.
- `build_cross_institution_importance(rankings_by_split, top_k)`: for each split, align each institution's importance ranking to concepts, then pairwise `stability.kendall_tau` + `stability.jaccard_topk` across institutions (reuse `src.experiments.stability`); return per-split pairs + mean τ + a verdict (`drivers_transfer_across_institutions` if all τ ≥ 0.9 else `drivers_partly_institution_specific`).
- `load_institution_results(path)` helpers that read the exp_011 / exp_012 results JSONs and extract (a) the fixed-model classification metrics per (split, feature_set) and (b) the importance ranking per split for the candidate feature set.
- A markdown renderer (Part A delta table + Part B τ/Jaccard table + verdict + the unit-difference and excluded-concepts caveats) and a `main()` with argparse for the three input JSONs + output prefix, writing `<output>.{json,md}`.

- [ ] **Step 4: Run, confirm PASS.**

Run: `cd services/ml && python -m pytest tests/test_cross_institution_engagement.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add services/ml/src/experiments/analyze_cross_institution_engagement.py services/ml/tests/test_cross_institution_engagement.py
git commit -m "feat(analysis): cross-institution engagement delta and importance-stability"
```

---

## Phase 6: Run analysis and write the experiment record

### Task 6: Generate the cross-institution report and the exp_012 doc

**Files:**
- Create: `docs/experiments/exp_012_oulad_engagement.md`
- Modify: `docs/experiments/registry.md`

- [ ] **Step 1: Run the analysis over all three institutions**

Run:
```bash
cd services/ml
python -m src.experiments.analyze_cross_institution_engagement \
  --oulad-ddd data/artifacts/experiments/exp_012_oulad_engagement_ddd2013j/exp_012_oulad_engagement_ddd2013j_results.json \
  --oulad-bbb data/artifacts/experiments/exp_012_oulad_engagement_bbb2013j/exp_012_oulad_engagement_bbb2013j_results.json \
  --ku-leuven data/artifacts/experiments/exp_011_kuleuven_engagement/exp_011_kuleuven_engagement_results.json \
  --output data/artifacts/experiments/exp_012_oulad_engagement_ddd2013j/cross_institution_engagement
```
> Confirm the exact JSON filenames the Task-4 runs produced and the analysis CLI flag names from Task 5; align if they differ.
Expected: writes `cross_institution_engagement.{json,md}`.

- [ ] **Step 2: Read the generated report** and record the headline: per-institution ΔF1 (B−A) on both splits, the cross-institution mean Kendall τ, and the verdict (drivers transfer vs partly institution-specific).

- [ ] **Step 3: Write `docs/experiments/exp_012_oulad_engagement.md`** following the existing experiment-doc format (see `exp_011_kuleuven_engagement.md`): objective, the matched feature sets, both cohorts' headline + fixed-model delta tables, the cross-institution delta table, the importance-stability table, interpretation (honest robustness framing), the unit-difference + excluded-concepts caveats, artifact paths, and a `## Next step`.

- [ ] **Step 4: Add registry rows** for `exp_012_oulad_engagement_ddd2013j` and `exp_012_oulad_engagement_bbb2013j` (and a combined cross-institution note) to `docs/experiments/registry.md`, matching the existing table format (the Task-4 runs may already have inserted per-cohort rows via `upsert_registry_entry`; only add what is missing and the comparison note).

- [ ] **Step 5: Commit**

```bash
git add docs/experiments/exp_012_oulad_engagement.md docs/experiments/registry.md \
        services/ml/data/artifacts/experiments/exp_012_oulad_engagement_ddd2013j/cross_institution_engagement.*
git commit -m "docs(exp_012): cross-institution engagement report and experiment record"
```

---

## Phase 7: Dissertation write-up

### Task 7: Fold the cross-institution robustness finding into the dissertation

**Files:**
- Modify: `docs/dissertation/final_research_conclusions.md`
- Modify: `docs/dissertation/defense_summary.md`

- [ ] **Step 1: Read both docs** to match their existing structure and the framing already used for exp_009/exp_011.

- [ ] **Step 2: Add a cross-institution robustness subsection** to `final_research_conclusions.md` stating: across three independent institutions (OULAD DDD 2013J, OULAD BBB 2013J, KU Leuven 1819), engagement→PASSED prediction is dominated by a minimal click/active-days baseline; richer engagement features add little (cite the per-institution ΔF1 values from the report); the top drivers' cross-institution rank stability (mean Kendall τ from the report) is reported as the transfer evidence. Frame as a robustness result, not an accuracy claim. Use the actual numbers from Task 6, not placeholders.

- [ ] **Step 3: Add a defense Q&A / summary line** to `defense_summary.md`: "Does the engagement finding hold beyond one dataset?" → the three-institution matched comparison with its consistent neutral delta and the importance-stability τ.

- [ ] **Step 4: Verify the numbers cited match the report**

Run: `cd services/ml && python -c "import json; d=json.load(open('data/artifacts/experiments/exp_012_oulad_engagement_ddd2013j/cross_institution_engagement.json')); print(d.get('verdict'), d.get('mean_kendall_tau'))"`
Cross-check the printed verdict/τ against what you wrote in the dissertation docs.

- [ ] **Step 5: Commit**

```bash
git add docs/dissertation/final_research_conclusions.md docs/dissertation/defense_summary.md
git commit -m "docs(dissertation): record three-institution engagement robustness result"
```

---

## Kill criteria (check at each phase)

- **P1:** `cumulative_active_days_to_date` cannot be built leakage-safe across VLE chunks → fall back to a click-only matched set (drop active_days from both OULAD feature sets and from `CONCEPT_ALIGNMENT`); document the reduced shared universe. (Active-days is additive-by-distinct-day, handled by the concat+dedup approach — this should not trigger.)
- **P2:** The KU runner extraction changes exp_011 metrics (Task 2 Step 6 fails) → revert; the extraction was not verbatim. Do NOT proceed to OULAD on a divergent core.
- **P4:** OULAD engagement-only F1 collapses to near-baseline-rate (model learns nothing) on both splits → the engagement signal is too weak in OULAD to support a meaningful delta; report that as the finding (engagement is institution-dependent) rather than forcing a comparison.
- **P5:** After concept alignment fewer than 2 shared concepts remain in any pair → Kendall τ is undefined (`stability.kendall_tau` returns None by design); report Jaccard-only for that pair and state the limitation. (With 6 mapped concepts this should not trigger.)

## Risks to manage

- Touching the committed exp_011 runner (Task 2). Mitigation: verbatim move + the Step-6 behavior-preservation guard + restore artifacts to HEAD.
- Forum CLICKS (OULAD) vs forum POSTS (KU Leuven) unit mismatch. Mitigation: Part B compares ranks, not magnitudes; caveat stated in both the report and the configs.
- OULAD engagement-only may underperform assessment-laden blocks. Expected and on-message — engagement-only is the deliberate matched constraint, not a best-predictor claim.

## Self-review notes

- **Spec coverage:** spec §1 → Task 1; §2 (shared-core architecture) → Tasks 2–4; §3 Part A/B → Task 5–6; §4 dissertation → Task 7; concept-alignment table → Task 5 `CONCEPT_ALIGNMENT`; testing section → tests in Tasks 1,2,3,4,5; out-of-scope (no SHAP, no regression, no synthetic) → enforced by `regression_models: []`, classification-only core, OULAD-only data.
- **Type consistency:** `BenchmarkFeatureSet`, `build_split`, `compute_permutation_importance`, `_fixed_model_classification_by_feature_set`, `build_benchmark_diagnostics`, `render_experiment_markdown` are the names extracted in Task 2 and imported in Tasks 2–3. `build_oulad_engagement_frame` / `load_oulad_engagement_config` (Task 3) are used in Task 4 tests. `align_ranking_to_concepts` / `build_engagement_delta_table` / `build_cross_institution_importance` (Task 5) are used in its tests and Task 6 CLI. `CONCEPT_ALIGNMENT` consistent between spec and Task 5.
- **Placeholder honesty:** Task 1 and Task 5 carry concrete code (new, self-contained). Tasks 2–4 carry an explicit "read these named functions/configs in full and align exact keys before filling" instruction (matching this repo's established plan convention) because the exact private-helper signatures and config schema must be read from source, not guessed.
