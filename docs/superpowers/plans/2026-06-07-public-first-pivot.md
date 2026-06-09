# Public-First Pivot (OULAD-primary) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the dissertation's primary empirical evidence off the circular synthetic dataset and onto real OULAD data — full A/B/C feature-set ablation + a real-data XAI runner + explanation-stability analysis — while demoting the synthetic generator to one correctly-scoped XAI-faithfulness probe, and disclosing the synthetic-target circularity honestly.

**Architecture:** Reuse the existing dataset-agnostic ML kernel (`splits.py`, `preprocessing.py`, `models.py`, `evaluate.py`, `metadata.py`, `explainability.py`). Extend the existing OULAD path (`oulad_adapter.py` + `run_public_benchmark_oulad.py`) from a 2-feature-set transfer test into a full nested ablation, then add a new generic OULAD XAI runner parameterized off `explainability.py`. The synthetic generator is unchanged except documentation; a new `exp_006` reuses it read-only as a known-ground-truth probe.

**Tech Stack:** Python 3, scikit-learn, pandas, NumPy, Pydantic + PyYAML (frozen configs), pytest. Data: OULAD CSVs under `datasets/oulad/` (already present). No new runtime dependencies in Phases 1–5 (SHAP is an open question, gated behind a flag in Phase 5).

---

## Decision context (why this plan exists)

A 20-agent ultracode workflow (run `wf_3f8954af-6fa`, 2026-06-07) verified directly in the source that synthetic `final_grade` is a **deterministic, noise-free** weighted mean of the same behaviors the model features re-aggregate (`services/ml/src/generator/final_results.py:74-84`; week-10 reconstruction max abs error 0.008, corr 1.000000). All three independent judges ranked **Option A (public-first)** first. This plan implements Option A with a single grafted, correctly-scoped synthetic faithfulness appendix (the salvageable part of Option D).

**Hard rules carried from the verification (do not violate in any task or document):**
- Never describe `activity_score` as a "zero-weight confounder" and never treat permutation importance as the generator's structural coefficients. `activity_score` enters `base_score` at `+0.04` (`services/ml/src/generator/submissions.py:83`) — it is a genuine indirect/proxy signal. Frame importance findings as *importance under proxy/redundancy*, never as "XAI infidelity."
- Always report a **fixed-model** results table alongside best-per-cell, to neutralize the model-flip artifact (the synthetic mastery −0.206 win is gradient_boosting-on-student_group only; at a fixed model it is +0.41 worse on temporal_forward).
- The OULAD regression target is **partially circular** on assessment-score features (`cumulative_assessment_weighted_score_to_date` feeds `final_weighted_score`). Disclose this and lean interpretation on exogenous **clickstream** features and the classification target (F1 0.86–0.89).

---

## File structure map

| File | Phase | Responsibility | Action |
|---|---|---|---|
| `docs/data_model/03_targets_and_labels.md` | 1 | Disclose synthetic-target circularity at the source-of-truth doc | Modify |
| `docs/dissertation/limitations_and_threats_to_validity.md` | 1 | Upgrade "synthetic" limitation to "deterministic circular target" | Modify |
| `docs/dissertation/final_research_conclusions.md` | 1 | Add model-flip caveat + circularity non-claim | Modify |
| `docs/dissertation/defense_qna.md` | 1 | Add the circularity + model-flip Q&A entries | Modify |
| `docs/dissertation/core_claims_and_nonclaims.md` | 1 | Add "cannot claim synthetic numbers reflect learning" non-claim | Modify |
| `services/ml/src/benchmarks/oulad_adapter.py` | 2 | Add OULAD trend + composite-index analogue columns | Modify |
| `services/ml/configs/experiments/exp_006_oulad_full_ablation.yaml` | 2 | Frozen config: full nested OULAD feature sets, fixed-model reporting | Create |
| `services/ml/src/experiments/run_public_benchmark_oulad.py` | 2 | Add full-ablation diagnostics incl. fixed-model table | Modify |
| `services/ml/tests/test_oulad_full_ablation.py` | 2 | Column availability + ablation diagnostics tests | Create |
| `services/ml/src/experiments/run_xai_on_oulad.py` | 3 | Generic OULAD XAI runner (permutation + native + local) | Create |
| `services/ml/configs/experiments/exp_007_xai_on_oulad.yaml` | 3 | Frozen XAI config for OULAD | Create |
| `services/ml/tests/test_xai_on_oulad.py` | 3 | XAI runner produces ranked importances under both splits | Create |
| `services/ml/src/experiments/stability.py` | 4 | Rank-agreement (Kendall τ / Jaccard top-k) of importances | Create |
| `services/ml/tests/test_stability.py` | 4 | Stability metrics correctness on synthetic fixtures | Create |
| `services/ml/configs/experiments/exp_008_faithfulness_probe.yaml` | 5 | Frozen config: final-week synthetic faithfulness probe | Create |
| `services/ml/src/experiments/run_faithfulness_probe.py` | 5 | Final-week known-ground-truth importance recovery probe | Create |
| `services/ml/tests/test_faithfulness_probe.py` | 5 | Probe restricts to final week + reports recovery honestly | Create |

**Sequencing & effort (solo student, OULAD-only core = Phases 1–5):** P1 ≈ 3–4 days · P2 ≈ 1.5–2 wks · P3 ≈ 1.5–2 wks · P4 ≈ 0.5–1 wk · P5 ≈ 1 wk. KU Leuven second anchor is **out of scope** for this plan (separate follow-on plan if calendar allows).

> **Note on detail level:** Phase 1 below is fully specified (exact text to add). Phases 2–5 are specified to the level of exact file paths, reused function signatures (verified by reading `run_public_benchmark_oulad.py`, `featuresets.py`, `explainability.py`, and the OULAD column names), tasks, and acceptance criteria. **Before executing each of Phases 2–5, the worker MUST read the named source files in full** (especially `oulad_adapter.py`, `models.py`, `config.py`, `preprocessing.py`, `splits.py`) and fill exact code into that phase's steps — do not invent signatures against unread files. Each phase is independently testable and commits cleanly.

---

## Phase 1: Honesty documentation (zero compute, zero risk)

**Files:**
- Modify: `docs/data_model/03_targets_and_labels.md`
- Modify: `docs/dissertation/limitations_and_threats_to_validity.md`
- Modify: `docs/dissertation/final_research_conclusions.md`
- Modify: `docs/dissertation/defense_qna.md`
- Modify: `docs/dissertation/core_claims_and_nonclaims.md`

### Task 1: Disclose deterministic circularity in the data-model source of truth

- [ ] **Step 1: Read the current target/label doc**

Run: `Read docs/data_model/03_targets_and_labels.md` (full). Locate the section that defines `final_grade` / `passed`.

- [ ] **Step 2: Add a "Determinism and circularity of `final_grade`" subsection**

Append this exact subsection immediately after the `final_grade` definition:

```markdown
### Determinism and circularity of `final_grade` (synthetic dataset)

In the synthetic generator, `final_grade` is computed by a fixed closed-form
formula (`services/ml/src/generator/final_results.py:74-84`):

    final_grade = clamp(
        0.55 * assignment_avg
      + 0.25 * quiz_avg
      + 0.10 * attendance_rate * 100
      + 0.10 * on_time_rate * 100,
        0, 100)

There is **no stochastic term** in this formula. The four inputs are the
full-course versions of the same behaviors that the weekly snapshot features
re-aggregate cumulatively (`avg_assignment_score_to_date`,
`avg_quiz_score_to_date`, `attendance_rate_to_date`,
`on_time_submission_rate_to_date`). The only randomness anywhere upstream is a
per-submission Gaussian (sd 0.06, `submissions.py:85`) that is **baked into the
recorded scores and therefore shared by both the features and the grade**; it
averages out across ~10 assignments. As a result, the synthetic supervised task
is largely an algebraic identity: from week-10 features the grade is
reconstructible with max absolute error 0.008 and correlation 1.000000.

**Consequence:** synthetic `R² ≈ 0.99`, `RMSE ≈ 1.9`, and `passed` `F1 = 1.000`
are mathematical artifacts of the generator, not evidence of learnable signal.
This is the explicit reason the synthetic dataset is used only as a controlled
methods probe (see `exp_008`) and the primary empirical evidence is OULAD. Note
the consistency point: `risk_level` is already excluded as a supervised target
for exactly this circularity reason; the same reasoning applies to `final_grade`
on synthetic data and must be stated rather than applied selectively.
```

- [ ] **Step 3: Verify the disclosure is present and cross-referenced**

Run: `Grep -n "reconstructible with max absolute error 0.008" docs/data_model/03_targets_and_labels.md`
Expected: one match.

- [ ] **Step 4: Commit**

```bash
git add docs/data_model/03_targets_and_labels.md
git commit -m "docs: disclose deterministic circularity of synthetic final_grade"
```

### Task 2: Upgrade the limitations chapter from "synthetic" to "deterministic circular target"

- [ ] **Step 1: Locate Section 1 of the limitations doc**

In `docs/dissertation/limitations_and_threats_to_validity.md`, find the paragraph in `## 1. Synthetic Data Limitations` that currently reads (euphemism to replace):

> weekly aggregates reach near-perfect monotonic relationships with `final_grade` (Pearson r above `0.97` for several LMS aggregates), which is rare in real cohorts and is itself a sign that the generator emphasizes signal clarity over realistic noise.

- [ ] **Step 2: Replace the euphemism with the exact mechanism**

Replace that sentence with:

```markdown
weekly aggregates reach near-perfect relationships with `final_grade` (Pearson r
above `0.97` for several LMS aggregates). This is **not merely "signal clarity"**:
`final_grade` is a deterministic, noise-free closed-form weighted mean
(`0.55*assignment + 0.25*quiz + 0.10*attendance + 0.10*on_time`,
`services/ml/src/generator/final_results.py:74-84`) of the very behaviors the
features re-aggregate. The target is therefore an algebraic function of the
inputs (week-10 reconstruction error 0.008, correlation 1.000000), so the
synthetic predictive scores cannot, even in principle, demonstrate learnable
educational signal. This is why the primary empirical evidence in this work is
the real OULAD dataset and the synthetic data is retained only as a controlled
faithfulness probe (`exp_008`).
```

- [ ] **Step 3: Verify**

Run: `Grep -n "deterministic, noise-free closed-form weighted mean" docs/dissertation/limitations_and_threats_to_validity.md`
Expected: one match.

- [ ] **Step 4: Commit**

```bash
git add docs/dissertation/limitations_and_threats_to_validity.md
git commit -m "docs: state synthetic target circularity mechanism in limitations"
```

### Task 3: Add the model-flip caveat to the conclusions

- [ ] **Step 1: Open `docs/dissertation/final_research_conclusions.md`** and find section `## 2. A Lean Twin Subset Centered on Mastery Improved Prediction`.

- [ ] **Step 2: Append this caveat paragraph at the end of section 2**

```markdown
**Model-stability caveat.** The `-0.206` RMSE advantage of `B_lms_plus_mastery`
is realized only for gradient boosting on the student-grouped split. When the
model is held fixed across splits, the mastery candidate is approximately
`+0.41` RMSE *worse* than `B_lms` on the temporal-forward split, and
`B_lms_plus_indices` is the only block that improves on both splits (≈`-0.066`/
`-0.068`). Any carry-forward statement about mastery must therefore be reported
with a fixed-model table, not best-model-per-cell, to avoid a model-selection
artifact.
```

- [ ] **Step 3: Verify**

Run: `Grep -n "Model-stability caveat" docs/dissertation/final_research_conclusions.md`
Expected: one match.

- [ ] **Step 4: Commit**

```bash
git add docs/dissertation/final_research_conclusions.md
git commit -m "docs: add fixed-model / model-flip caveat to conclusions"
```

### Task 4: Add defense Q&A entries for the two killer questions

- [ ] **Step 1: Read `docs/dissertation/defense_qna.md`** to match its existing Q/A formatting.

- [ ] **Step 2: Append two entries in the same format the file already uses** (adapt headers to match; content below):

```markdown
**Q: Isn't your synthetic `final_grade` just a deterministic function of your own features, so the high accuracy is meaningless?**
A: Yes, and we state this explicitly. `final_grade` is a closed-form weighted
mean of assignment, quiz, attendance, and on-time behavior with no noise term
(`final_results.py:74-84`); week-10 reconstruction error is 0.008. That is
precisely why we do not base any empirical learning claim on synthetic accuracy.
Synthetic data is used only as a controlled faithfulness probe with known
ground truth (`exp_008`). The empirical claims rest on real OULAD data, where
the same pipeline yields F1 0.86–0.89 (not 1.000) — itself direct evidence that
the perfect synthetic scores were a generator artifact.

**Q: You claim mastery features help — but does that survive a fair comparison?**
A: It is split- and model-dependent. The `-0.206` win holds for gradient
boosting on the student-grouped split only; at a fixed model on the
temporal-forward split mastery is ≈`+0.41` worse, and only `B_lms_plus_indices`
improves on both splits. We report fixed-model tables for this reason and frame
the real-data finding as a mixed/conditional result, not "the twin wins."
```

- [ ] **Step 3: Verify**

Run: `Grep -c "deterministic function of your own features\|fair comparison" docs/dissertation/defense_qna.md`
Expected: at least 2.

- [ ] **Step 4: Commit**

```bash
git add docs/dissertation/defense_qna.md
git commit -m "docs: add circularity and model-flip defense Q&A"
```

### Task 5: Add the matching non-claim and soften the "Digital Twin" term

- [ ] **Step 1: Open `docs/dissertation/core_claims_and_nonclaims.md`**, `## Claims the Dissertation Cannot Make`.

- [ ] **Step 2: Add these bullets to the "Cannot Make" list**

```markdown
- It cannot claim that synthetic predictive accuracy (R²≈0.99, F1=1.000) reflects
  learnable signal; the synthetic target is a deterministic function of the
  features and the scores are algebraic artifacts.
- It cannot claim a what-if / counterfactual / simulation capability: none is
  implemented (`services/ml/src/features/engineering.py` and
  `src/explainability/xai.py` are stubs). The system is a lean, time-aware
  weekly state representation, not a simulating digital twin.
```

- [ ] **Step 3: Add a one-line framing note near the top of the doc**

```markdown
> Terminology: throughout, "Digital Twin" denotes a **lean, time-aware weekly
> state representation**. It does not denote a counterfactual/simulation engine;
> no such capability is implemented in this prototype.
```

- [ ] **Step 4: Verify**

Run: `Grep -n "lean, time-aware weekly" docs/dissertation/core_claims_and_nonclaims.md`
Expected: two matches (framing note + non-claim).

- [ ] **Step 5: Commit**

```bash
git add docs/dissertation/core_claims_and_nonclaims.md
git commit -m "docs: add circularity/no-simulation non-claims and soften Digital Twin term"
```

**Phase 1 done-criterion:** every doc that makes or guards a claim discloses the deterministic circularity in mechanism terms (not euphemism), the model-flip caveat is present, and "Digital Twin" is reframed. This is shippable on its own and pre-empts the examiner's strongest question regardless of how Phases 2–5 land.

---

## Phase 2: OULAD full nested A/B/C ablation

**Pre-execution read (required):** `services/ml/src/benchmarks/oulad_adapter.py` (full, ~700+ lines — the snapshot column construction around L700–860), `services/ml/src/experiments/config.py` (`FeatureSetName`, `RegressionModelName`, `ClassificationModelName`), `services/ml/src/experiments/models.py` (`iter_regression_models`), `services/ml/src/experiments/preprocessing.py` (`build_modeling_matrix`, `PreparedMatrix`).

**Why this phase:** `run_public_benchmark_oulad.py` already runs the full leakage-safe modeling loop over arbitrary `BenchmarkFeatureSet`s and both splits (verified: `run_benchmark_models` L380-422, `_build_split` L856-918). It currently only declares 2 feature sets (`feature_set_order` in `exp_005…yaml` L152-154). The ablation is therefore mostly **config + a few new adapter columns + a fixed-model diagnostic**, not a rewrite.

### Task 6: Add OULAD trend + composite-index analogue columns to the adapter

OULAD currently exposes cumulative assessment/clicks/discipline columns and mastery proxies but **no trend or composite-index analogues**, which are needed for `B_lms_plus_trends_oulad`, `B_lms_plus_indices_oulad`, and `C_twin_oulad`.

- [ ] **Step 1: Write failing test for the new columns** in `services/ml/tests/test_oulad_full_ablation.py`:

```python
from pathlib import Path
import pandas as pd
from src.benchmarks.oulad_adapter import OuladCourseFilter, OuladRawPaths, build_weekly_snapshots

OULAD = Path("datasets/oulad")

def _snapshots():
    raw = OuladRawPaths(
        assessments=OULAD/"assessments.csv", courses=OULAD/"courses.csv",
        student_info=OULAD/"studentInfo.csv", student_registration=OULAD/"studentRegistration.csv",
        student_vle=OULAD/"studentVle.csv", vle=OULAD/"vle.csv",
        student_assessment=OULAD/"studentAssessment.csv",
    )
    return build_weekly_snapshots(raw, course_filter=OuladCourseFilter("DDD","2013J"), min_week=4, max_week=None).snapshots

def test_trend_and_index_columns_present():
    snaps = _snapshots()
    for col in [
        "assessment_score_trend_to_date", "clicks_trend_to_date",
        "engagement_index_oulad", "performance_index_oulad", "discipline_index_oulad",
    ]:
        assert col in snaps.columns, f"missing {col}"
```

- [ ] **Step 2: Run it, confirm FAIL**

Run: `cd services/ml && python -m pytest tests/test_oulad_full_ablation.py::test_trend_and_index_columns_present -v`
Expected: FAIL (`missing assessment_score_trend_to_date`).

- [ ] **Step 3: Implement the columns in `oulad_adapter.py` (LOCKED design, controller-decided 2026-06-07).** Add a new function `_add_trend_and_index_features(snapshots: pd.DataFrame) -> pd.DataFrame` and call it in `build_weekly_snapshots` on the line IMMEDIATELY BEFORE `snapshots = _finalize_snapshot_frame(snapshots)` (currently line 289). At that point the frame still contains ALL weeks (1..duration) for every student and all cumulative columns, so week-over-week diffs at `min_week` correctly reference the prior week before the `min_week` filter (lines 291-296) drops it. Sort by `KEY_COLUMNS + ["week_number"]`, group by `KEY_COLUMNS`, and compute (all components are already in [0,1] or are leakage-safe to-date diffs — do NOT use any global min/max or cross-row statistics):
  - `assessment_score_trend_to_date = cumulative_assessment_score_mean_to_date − group.shift(1)` of the same column, `.fillna(0.0)`.
  - `clicks_trend_to_date = current_week_clicks − group.shift(1)` of `current_week_clicks`, `.fillna(0.0)`.
  - `performance_index_oulad = mean(clip(cumulative_assessment_score_mean_to_date/100, 0, 1), clip(cumulative_assessment_weighted_score_to_date/100, 0, 1))`.
  - `discipline_index_oulad = mean(assessment_submission_rate_due_to_date, 1 − late_submission_rate_to_date, banked_assessment_rate_to_date)` (all already 0–1).
  - `engagement_index_oulad = mean(assessment_submission_rate_due_to_date, has_vle_activity_to_date)` (a deliberately conservative, leakage-safe engagement composite using only bounded signals; documented as such).

  Add each new column to the `fill_zero` list in `_finalize_snapshot_frame` so missing values become 0.0. Document each formula in the function docstring, noting the deliberate avoidance of global statistics (leakage-safe) and the parallel to the synthetic index intent in `docs/research/deep-research-report.md` lines 27-30.

- [ ] **Step 4: Run the test, confirm PASS**

Run: `cd services/ml && python -m pytest tests/test_oulad_full_ablation.py::test_trend_and_index_columns_present -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add services/ml/src/benchmarks/oulad_adapter.py services/ml/tests/test_oulad_full_ablation.py
git commit -m "feat(oulad): add trend and composite-index analogue columns"
```

### Task 7: Create the full-ablation frozen config `exp_006`

- [ ] **Step 1: Create `services/ml/configs/experiments/exp_006_oulad_full_ablation.yaml`** by copying `exp_005…yaml` and changing: `experiment_id: "exp_006_oulad_full_ablation"`, `parent_experiment: "exp_005_public_benchmark_oulad"`, `outputs.experiments_dir` + `processed_snapshots_csv` to the `exp_006…` artifact dir. Then expand `feature_sets` and `feature_set_order` to the full nested set, reusing the verified OULAD column names from `exp_005…yaml` L84-150 plus the Task-6 columns:
  - `A_simple_oulad`: `week_number`, `cumulative_assessment_score_mean_to_date`, `cumulative_assessment_score_count_to_date`; indicators `has_assessment_score_to_date`.
  - `B_lms_oulad`: exactly the existing 19-column list (`exp_005…yaml` L90-108) + indicators L110-112.
  - `B_lms_plus_trends_oulad`: `B_lms_oulad` + `assessment_score_trend_to_date`, `clicks_trend_to_date`.
  - `B_lms_plus_mastery_oulad`: the existing mastery set (`exp_005…yaml` L120-150).
  - `B_lms_plus_indices_oulad`: `B_lms_oulad` + `engagement_index_oulad`, `performance_index_oulad`, `discipline_index_oulad`.
  - `C_twin_oulad`: `B_lms_oulad` + trends + mastery + indices columns (deduplicated).
  - `feature_set_order`: all six, A first.
  - Keep `comparison.baseline_feature_set: "B_lms_oulad"`; set `candidate_feature_set: "C_twin_oulad"`.

- [ ] **Step 2: Write failing test that the config loads and declares 6 feature sets** (append to `tests/test_oulad_full_ablation.py`):

```python
from src.experiments.run_public_benchmark_oulad import load_public_benchmark_config

def test_exp006_config_has_full_nested_sets():
    config, _ = load_public_benchmark_config("configs/experiments/exp_006_oulad_full_ablation.yaml")
    names = set(config.feature_sets)
    assert {"A_simple_oulad","B_lms_oulad","B_lms_plus_trends_oulad","B_lms_plus_mastery_oulad","B_lms_plus_indices_oulad","C_twin_oulad"} <= names
    assert config.feature_set_order[0] == "A_simple_oulad"
```

- [ ] **Step 3: Run it (PASS expected once YAML is valid)**

Run: `cd services/ml && python -m pytest tests/test_oulad_full_ablation.py::test_exp006_config_has_full_nested_sets -v`
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add services/ml/configs/experiments/exp_006_oulad_full_ablation.yaml services/ml/tests/test_oulad_full_ablation.py
git commit -m "feat(oulad): add exp_006 full nested ablation config"
```

### Task 8: Add a fixed-model regression table to the diagnostics

The existing diagnostics report best-model-per-cell only (`_best_regression_by_feature_set`, L1016-1064). Add a parallel fixed-model view to neutralize the model-flip artifact.

- [ ] **Step 1: Write failing test** (append):

```python
from src.experiments.run_public_benchmark_oulad import _fixed_model_regression_by_feature_set
import pandas as pd

def test_fixed_model_table_filters_one_model():
    table = pd.DataFrame([
        {"task":"regression","split_strategy":"student_group","feature_set":"B_lms_oulad","model":"gradient_boosting","metric_rmse":12.6,"metric_mae":7.9,"metric_r2":0.85,"n_train_rows":1,"n_test_rows":1},
        {"task":"regression","split_strategy":"student_group","feature_set":"B_lms_oulad","model":"linear_regression","metric_rmse":15.0,"metric_mae":9.0,"metric_r2":0.7,"n_train_rows":1,"n_test_rows":1},
    ])
    rows = _fixed_model_regression_by_feature_set(table, model="gradient_boosting", baseline_feature_set="B_lms_oulad", primary_split="student_group")
    assert len(rows) == 1 and rows[0]["model"] == "gradient_boosting"
```

- [ ] **Step 2: Run, confirm FAIL** (`ImportError: _fixed_model_regression_by_feature_set`).

Run: `cd services/ml && python -m pytest tests/test_oulad_full_ablation.py::test_fixed_model_table_filters_one_model -v`

- [ ] **Step 3: Implement `_fixed_model_regression_by_feature_set`** in `run_public_benchmark_oulad.py` — same shape as `_best_regression_by_feature_set` but filter `regression = regression[regression["model"] == model]` before grouping, and add the result under a new diagnostics key `"regression_fixed_model_by_feature_set"` in `build_benchmark_diagnostics` (use the config's first regression model, or a new `comparison.fixed_model` field defaulting to `"gradient_boosting"`). Render it as an extra table in `render_experiment_markdown` after the headline table.

- [ ] **Step 4: Run, confirm PASS.** Then run the full file: `cd services/ml && python -m pytest tests/test_oulad_full_ablation.py -v` → all PASS.

- [ ] **Step 5: Commit**

```bash
git add services/ml/src/experiments/run_public_benchmark_oulad.py services/ml/tests/test_oulad_full_ablation.py
git commit -m "feat(oulad): add fixed-model regression diagnostics table"
```

### Task 9: Run the experiment and record results

- [ ] **Step 1: Execute the ablation**

Run: `cd services/ml && python -m src.experiments.run_public_benchmark_oulad --config configs/experiments/exp_006_oulad_full_ablation.yaml`
Expected: writes `data/artifacts/experiments/exp_006_oulad_full_ablation/` (results CSV/JSON, summary, snapshots) and `docs/experiments/exp_006_oulad_full_ablation.md`, updates `docs/experiments/registry.md`.

- [ ] **Step 2: Sanity-check the headline** — confirm classification F1 ≈ 0.86–0.89 (NOT 1.000) and that the fixed-model table is present. Read `data/artifacts/experiments/exp_006_oulad_full_ablation/exp_006_oulad_full_ablation_summary.md`.

- [ ] **Step 3: Apply the Phase-2 kill criterion.** If, with a fixed model, no block beats `B_lms_oulad` by >1 RMSE on at least one split, record that the "feature-group value" spine is a mixed/null result and flag the headline pivot toward stability/transfer (Phases 3–4). Write the verdict into the generated `exp_006…md` "Interpretation" section.

- [ ] **Step 4: Commit artifacts**

```bash
git add data/artifacts/experiments/exp_006_oulad_full_ablation docs/experiments/exp_006_oulad_full_ablation.md docs/experiments/registry.md
git commit -m "exp: run exp_006 OULAD full nested ablation"
```

---

## Phase 3: OULAD XAI runner

**Pre-execution read (required):** `services/ml/src/experiments/run_xai_on_lean_twin.py` (to see the synthetic-only hardwiring to strip), `services/ml/src/experiments/explainability.py` (already read — the generic engine: `train_regression_reference`, `build_global_explanation`, `compute_local_perturbation_contributions`, `select_representative_cases`, `compute_explanation_concentration`).

**Key constraint found:** `train_regression_reference` (explainability.py L64-151) is synthetic-coupled (`get_feature_set` + `student_group_split` only). But `build_global_explanation` (L154-238) and `compute_local_perturbation_contributions` (L480-516) operate purely on a `TrainedRegressionModel` dataclass and are dataset-agnostic except a hardcoded `"split_strategy": "student_group"` label (L217). `build_modeling_matrix(frame, feature_set)` (preprocessing.py) duck-types on `.columns/.indicator_columns/.name` and requires the frame to carry `student_id`, `week_number`, `final_grade`, `passed` — the OULAD benchmark runner already adds `final_grade`/`passed` before calling it (`run_benchmark_models`). `splits.py` exposes `student_group_split` and `temporal_forward_split` directly.

**LOCKED DESIGN (2026-06-08):** Do NOT bend `run_xai_on_lean_twin.py` (too synthetic-coupled). Instead: (Task 10) refactor `explainability.py` to extract a private core `_assemble_trained_model(working_frame, matrix, train_mask, test_mask, *, feature_set_name, model_name, seed, drop_columns, split_metadata)` doing the fit+predict+frame-bookkeeping (current L102-151), have `train_regression_reference` build the matrix via `get_feature_set`+`student_group_split` then call the core, and add a NEW public `train_regression_reference_for_matrix(frame, *, feature_set, train_mask, test_mask, model_name, seed, drop_columns=None, split_metadata=None)` that builds the matrix via `build_modeling_matrix(frame, feature_set)` (any object with `.columns/.indicator_columns/.name`) and calls the core — no `get_feature_set`, arbitrary splits. Add a `split_strategy: str = "student_group"` param to `build_global_explanation` replacing the L217 hardcode. (Task 11) `run_xai_on_oulad.py` builds OULAD snapshots, adds `final_grade`/`passed`, and for each feature set × split derives masks from `student_group_split`/`temporal_forward` on the modeling frame (student_group: held-out student set; temporal_forward: held-out students AND week>train_weeks for test, non-held-out AND week<=train_weeks for train — mirrors `_build_split`), assembles the model via `train_regression_reference_for_matrix`, then calls `build_global_explanation(..., split_strategy=strategy)` + `compute_local_perturbation_contributions`. No SHAP (resolved). Disclose OULAD assessment-score partial circularity; weight interpretation to clickstream features.

### Task 10: Generalize the XAI reference trainer to accept an explicit feature set

- [ ] **Step 1: Write failing test** in `services/ml/tests/test_xai_on_oulad.py` that calls a new `train_regression_reference_with_columns(frame, feature_columns, indicator_columns, model_name, ...)` and asserts it returns a `TrainedRegressionModel` with the expected `feature_columns`. (Worker writes the concrete fixture from a small OULAD snapshot slice.)

- [ ] **Step 2: Run, confirm FAIL.**

- [ ] **Step 3: Implement** a thin `train_regression_reference_with_columns(...)` in `explainability.py` that mirrors `train_regression_reference` but builds the modeling matrix from an explicit column list instead of `get_feature_set(...)` (factor the shared body so the existing function calls the new one with `get_feature_set(name)` columns — DRY, no duplication).

- [ ] **Step 4: Run, confirm PASS. Commit.**

```bash
git add services/ml/src/experiments/explainability.py services/ml/tests/test_xai_on_oulad.py
git commit -m "feat(xai): allow explicit feature-column reference training"
```

### Task 11: Create `run_xai_on_oulad.py` + `exp_007` config

- [ ] **Step 1:** Create `services/ml/src/experiments/run_xai_on_oulad.py` that: builds OULAD snapshots via `oulad_adapter.build_weekly_snapshots`, then for the configured feature sets and for **both** `student_group` and `temporal_forward` splits, calls the generalized trainer + `build_global_explanation` + `compute_local_perturbation_contributions`, and writes permutation + native importance + local perturbation + concentration audit artifacts. Critically: parameterize the split (the engine currently labels `student_group` only — pass the split masks in, do not hardcode). Reuse `_build_split` logic from `run_public_benchmark_oulad.py` (extract it to a shared helper if needed).
- [ ] **Step 2:** Create `services/ml/configs/experiments/exp_007_xai_on_oulad.yaml` listing the feature sets to explain (at minimum `B_lms_oulad`, `C_twin_oulad`, and whichever block won in `exp_006`), both splits, `permutation_repeats: 15`, `seed: 42`.
- [ ] **Step 3:** Write a test that the runner produces a ranked importance list (len > 0) for both splits and that no row is labeled with a structural-coefficient claim. Run → PASS.
- [ ] **Step 4:** Execute: `cd services/ml && python -m src.experiments.run_xai_on_oulad --config configs/experiments/exp_007_xai_on_oulad.yaml`.
- [ ] **Step 5:** In the generated summary, **disclose the OULAD partial target circularity** on assessment-score features and weight interpretation toward clickstream features. Commit code + config + artifacts.

---

## Phase 4: Explanation stability as a faithfulness proxy

**Pre-execution read:** outputs of Phase 3 (importance tables); `explainability.py` concentration helpers.

### Task 12: Implement rank-agreement metrics

- [ ] **Step 1:** Write `services/ml/tests/test_stability.py` with known fixtures: two identical rankings → Kendall τ = 1.0, Jaccard top-k = 1.0; one reversed → τ = -1.0. Run → FAIL.
- [ ] **Step 2:** Implement `services/ml/src/experiments/stability.py` with `kendall_tau(rank_a, rank_b)`, `jaccard_topk(features_a, features_b, k)`, and `stability_report(importance_tables: dict[str, list[dict]])` returning pairwise agreement across regimes. Use `scipy.stats.kendalltau` if scipy is present, else a self-contained implementation (check `pyproject.toml` first; prefer no new dependency). Run → PASS. Commit.

### Task 13: Apply stability across split regimes (and a 2nd presentation if cheap)

- [ ] **Step 1:** Add a stability step to `run_xai_on_oulad.py` that compares importance rankings across `student_group` vs `temporal_forward`. Optionally re-run the adapter with a second `code_presentation` (e.g. `DDD 2014J`) and compare cross-cohort.
- [ ] **Step 2:** Write the stability table into the `exp_007` summary as the headline-candidate contribution (extends Tiukhova et al. 2024). Apply the Phase-4 kill criterion: if τ > ~0.9 everywhere, demote stability to a confirmation paragraph. Commit.

---

## Phase 5: Controlled synthetic faithfulness probe (`exp_008`) — methods appendix

**Pre-execution read:** `services/ml/src/experiments/datasets.py` (synthetic snapshot loading), `final_results.py` (the oracle weights), `featuresets.py` (already read).

**Scope guard:** This is an appendix, never the headline. It exists to characterize importance behavior under **known** ground truth and redundancy — not to claim anything about learning.

### Task 14: Final-week probe with honest framing

- [ ] **Step 1:** Create `services/ml/configs/experiments/exp_008_faithfulness_probe.yaml`: synthetic dataset, restrict to `week_number == num_weeks` (final week, where to-date features equal the formula inputs; reconstruction error 0.008), feature set `C_twin`, `permutation_repeats: 15`, the oracle weight vector `{avg_assignment_score_to_date: 0.55, avg_quiz_score_to_date: 0.25, attendance_rate_to_date: 0.10, on_time_submission_rate_to_date: 0.10}`, and `shap_enabled: false` (open question — see below).
- [ ] **Step 2:** Write `services/ml/tests/test_faithfulness_probe.py` asserting: (a) the probe frame contains only final-week rows; (b) the report includes the oracle weights AND the measured permutation/native importance; (c) the report's narrative does NOT contain the strings "zero-weight" or "infidelity" (guard against the forbidden framing). Run → FAIL.
- [ ] **Step 3:** Implement `services/ml/src/experiments/run_faithfulness_probe.py`: load synthetic snapshots, filter final week, train reference (reuse `train_regression_reference`), compute global importance, and emit a report comparing measured importance ranking to the oracle ordering. The report MUST frame `activity_score_to_date`'s high share as *importance attributed to a high-fidelity correlated proxy* (built from the same latents, feeds `base_score` at +0.04 per `submissions.py:83`), and MUST report the `overall_mastery` ↔ `avg_assignment_score_to_date` |r|=0.993 redundancy failure mode. Run → PASS.
- [ ] **Step 4:** Execute, apply the Phase-5 kill criterion (if importance cleanly recovers the ordering with no interesting failure mode, cut to a one-paragraph sanity check). Commit code + config + artifacts.

---

## Kill criteria (measurable; check at each phase)

- **P2:** Fixed-model OULAD ablation shows no block beating `B_lms_oulad` by >1 RMSE on ≥1 split AND no cohort/split holds in stability → drop "feature-group value" headline; pivot to stability/transfer methodology + the faithfulness probe.
- **P3:** OULAD XAI runner needs a near-rewrite (not a re-point) of `explainability.py` within ~2 weeks → descope to ablation + stability; drop the local-perturbation arm.
- **P4:** Importance rankings highly stable everywhere (Kendall τ > ~0.9) → fold stability into a confirmation paragraph, not a contribution.
- **P5:** Importance cleanly recovers the 0.55/0.25/0.10/0.10 ordering with no interesting failure → cut the probe to one paragraph.
- **Any phase:** a draft claim depends on calling `activity_score` a "zero-weight confounder" or equating permutation importance with structural coefficients → STOP and reframe (verified-false per `submissions.py:83`).

## Risks to manage

- Stripped of synthetic saturation, the OULAD signal is single-source and may read as a mixed/near-null. Mitigation: frame the contribution as transfer/stability methodology + honest finding (supervisor has confirmed an honest mixed/negative result is acceptable).
- Plain OULAD prediction is over-published. Novelty must rest on feature-group-value transfer, explanation stability, and the known-ground-truth probe — not on accuracy.
- Scope creep across P2–P5. The OULAD-only core is a complete thesis; do not start KU Leuven from this plan.

## Open questions (resolved 2026-06-07)

- **SHAP:** RESOLVED — **No SHAP.** Keep permutation + native importance; do NOT add a SHAP dependency. `exp_008` keeps `shap_enabled: false`. The `shap.used=False` non-claim stays and is defended (not a gap). (Affects Tasks 11, 14.)
- **Canonical reporting split for OULAD:** RESOLVED — **Report BOTH** `student_group` and `temporal_forward`, always with a **fixed-model** table; the **headline is `temporal_forward`** (stricter, better for early-warning). (Affects Tasks 7, 8, 11.)
- **Second OULAD presentation** for cross-cohort stability (Task 13): still optional — decide within Phase 4 based on remaining time.

---

## Self-review notes

- **Spec coverage:** synthesis build steps 1–6 map to Phases 1–5 (KU Leuven step 7 intentionally excluded; step 8 dissertation rewrite is downstream of evidence and not a code phase).
- **Type consistency:** reused names verified against source — `BenchmarkFeatureSet`, `PublicBenchmarkOuladConfig`, `load_public_benchmark_config`, `run_benchmark_models`, `_best_regression_by_feature_set`, `_build_split` (run_public_benchmark_oulad.py); `TrainedRegressionModel`, `train_regression_reference`, `build_global_explanation`, `compute_local_perturbation_contributions` (explainability.py); `FeatureSet`, `get_feature_set`, `FORBIDDEN_FEATURE_COLUMNS` (featuresets.py); OULAD column names verified against `exp_005_public_benchmark_oulad.yaml`.
- **Placeholder honesty:** Phase 1 is fully specified. Phases 2–5 carry an explicit "read these files in full and fill exact code before executing" instruction rather than fabricated code against unread files (`oulad_adapter.py`, `models.py`, `config.py`, `datasets.py`).
