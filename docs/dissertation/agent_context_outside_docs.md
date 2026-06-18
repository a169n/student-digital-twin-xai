# Agent Context: What to Know Outside `docs/` for Research Paper Writing

This document briefs an AI agent on repository sources outside the `docs/` folder
that are required to write the research paper correctly. The `docs/` folder provides
narrative and conclusions; these sources provide ground-truth numbers, exact
implementations, and dataset facts that a reviewer will ask about.

---

## 1. Exact Feature Set Membership

**Source**: `services/ml/src/experiments/featuresets.py`

The docs describe feature sets in prose. The code is the authoritative definition.

### Feature set column lists

| Feature set | Columns beyond `B_lms` base |
|---|---|
| `A_simple` | `avg_assignment_score_to_date`, `avg_quiz_score_to_date`, `attendance_rate_to_date` only |
| `B_lms` | 9 columns: `avg_assignment_score_to_date`, `avg_quiz_score_to_date`, `attendance_rate_to_date`, `activity_score_to_date`, `time_spent_to_date`, `on_time_submission_rate_to_date`, `missed_assignments_to_date`, `late_submissions_to_date`, `avg_attempt_count_to_date` |
| `C_twin` / `C_twin_full` | `B_lms` + trends (3) + mastery (2) + indices (3) + `week_number` — identical columns, different experiment alias |
| `B_lms_plus_mastery` | `B_lms` + `current_topic_mastery` + `overall_mastery` |
| `B_lms_plus_trends` | `B_lms` + `score_trend_3w`, `activity_trend_3w`, `attendance_trend_3w` |
| `B_lms_plus_indices` | `B_lms` + `engagement_index`, `performance_index`, `discipline_index` |
| `B_lms_plus_temporal` | `B_lms` + `week_number` only |
| `B_lms_plus_trends_mastery` | `B_lms` + all 3 trend columns + all 2 mastery columns |

### Hard-coded forbidden columns (never enter any model)

```
risk_score, risk_level, predicted_final_grade,
final_grade, passed, completion_status, completed_weeks,
baseline_level, motivation_level, discipline_level, trajectory_type,
snapshot_id, student_id, course_id, snapshot_date
```

`risk_level` is a teacher-facing heuristic excluded from supervised training.
`trajectory_type` is a generation-only latent field excluded from all models.

Every feature set also includes two explicit missingness indicator columns:
`has_assignment_score_to_date` and `has_quiz_score_to_date`.

---

## 2. Exact Model Hyperparameters

**Source**: `services/ml/src/experiments/models.py`

All reported RMSE headline numbers come from **GradientBoostingRegressor**,
which was selected as the reference model. RF and Ridge also ran; their results
appear in the full ablation tables.

| Model | Key hyperparameters |
|---|---|
| `GradientBoostingRegressor` (reference) | `n_estimators=300`, `learning_rate=0.05`, `max_depth=3`, `seed=42` |
| `RandomForestRegressor` | `n_estimators=400`, `max_depth=None`, `min_samples_leaf=2`, `seed=42` |
| `Ridge` (linear) | `alpha=1.0` with `StandardScaler` prepended in a Pipeline |
| `GradientBoostingClassifier` | `n_estimators=200`, `learning_rate=0.05`, `max_depth=3` |
| `RandomForestClassifier` | `n_estimators=300`, `min_samples_leaf=2` |
| `LogisticRegression` | `C=1.0`, `max_iter=2000`, `solver=lbfgs` with `StandardScaler` |

---

## 3. Full Numerical Results Tables

**Source**: `data/artifacts/experiments/`

The docs cite headline numbers. The artifact files contain complete tables needed
for Methods and Results sections.

### 3a. Full ablation regression results (`exp_002_twin_ablation_summary.md`)

Best RMSE per feature set × split (GBR model; `final_grade` target):

| Feature set | Primary split RMSE | Forward split RMSE | Primary Δ vs `B_lms` | Forward Δ vs `B_lms` |
|---|---:|---:|---:|---:|
| `B_lms` | 2.101 | 2.270 | — | — |
| `B_lms_plus_trends` | 2.096 | 2.531 | −0.005 | +0.261 |
| `B_lms_plus_mastery` | **1.894** | 2.276 | **−0.206** | +0.006 |
| `B_lms_plus_indices` | 2.035 | **2.202** | −0.066 | **−0.068** |
| `B_lms_plus_temporal` | 2.078 | 2.658 | −0.023 | +0.388 |
| `B_lms_plus_trends_mastery` | 1.973 | 2.555 | −0.128 | +0.285 |
| `C_twin_full` | 2.149 | 2.937 | +0.049 | +0.667 |

Notable: `B_lms_plus_indices` (not mastery) is the best feature set on the
forward split. `B_lms_plus_mastery` forward RMSE (2.276) is nearly identical
to `B_lms` (2.270), not substantially worse. `C_twin_full` is the worst on
both splits.

All classification results (`passed` target): **F1 = 1.000** for every
feature set, every model, and every split — a structural saturation property,
not a modeling success.

### 3b. Global feature importance (`exp_004_xai_on_lean_twin/global_feature_importance.md`)

Permutation importance (RMSE-increase share) on the held-out student-group split:

**`B_lms` — top features:**

| Rank | Feature | RMSE increase | Share |
|---:|---|---:|---:|
| 1 | `activity_score_to_date` | 17.843 | 0.701 |
| 2 | `avg_assignment_score_to_date` | 3.687 | 0.145 |
| 3 | `avg_quiz_score_to_date` | 2.178 | 0.086 |
| 4 | `on_time_submission_rate_to_date` | 0.592 | 0.023 |
| 5 | `attendance_rate_to_date` | 0.577 | 0.023 |

**`B_lms_plus_mastery` — top features:**

| Rank | Feature | RMSE increase | Share |
|---:|---|---:|---:|
| 1 | `activity_score_to_date` | 16.288 | 0.648 |
| 2 | `overall_mastery` | 4.489 | 0.178 |
| 3 | `avg_assignment_score_to_date` | 2.272 | 0.090 |
| 4 | `time_spent_to_date` | 0.550 | 0.022 |
| 5 | `on_time_submission_rate_to_date` | 0.548 | 0.022 |
| 6 | `attendance_rate_to_date` | 0.427 | 0.017 |
| 7 | `avg_quiz_score_to_date` | 0.403 | 0.016 |
| 8 | `current_topic_mastery` | 0.076 | 0.003 |

Adding mastery shifts `activity_score_to_date` from share 0.701 to 0.648.
The dominance audit outcome: `acceptable_with_caveat` (average local mastery
share = 0.194, below the 0.60 warning threshold).

### 3c. Local case explanations (`exp_004_xai_on_lean_twin/local_case_explanations.md`)

Five deterministically selected representative cases. Mastery contribution shares:

| Case | Student | Week | Mastery share | Assessment |
|---|---|---:|---:|---|
| `strong_performer` | student_054 | 10 | 0.343 | teacher-meaningful with mastery |
| `at_risk` | student_115 | 10 | 0.213 | teacher-meaningful with mastery |
| `improving_trajectory` | student_112 | 5 | 0.019 | mostly LMS-behavior driven |
| `declining_trajectory` | student_027 | 5 | 0.203 | teacher-meaningful with mastery |
| `borderline_medium` | student_020 | 10 | 0.194 | teacher-meaningful with mastery |

Local contributions are one-feature median-replacement perturbation effects —
directional model-behavior summaries, not causal attributions. Not SHAP.

---

## 4. Dataset and Generator Facts

**Source**: `services/ml/src/generator/config.py` and
`data/artifacts/experiments/exp_001_baseline/eda/eda_report.md`

### Generator configuration

| Parameter | Value |
|---|---|
| `num_students` | 120 generated |
| `withdrawal_rate` | 0.05 → **114 students** survive to modeling |
| `num_weeks` | 10 total; weeks **4–10** used for modeling |
| Modeling rows | 114 students × 7 weeks = **798 rows** |
| `seed` | 42 (all experiments) |
| `pass_mark` | 50.0 |
| Course domain | **"Introduction to Programming" (CS101)** — single synthetic course |
| `term_label` | Fall 2026 |

### Trajectory distribution (generation-only, excluded from models)

| Trajectory type | Students | Share |
|---|---:|---:|
| `stable_high` | 26 | 0.26 |
| `improving` | 30 | 0.22 (weight), 30 actual |
| `declining` | 33 | 0.22 (weight), 33 actual |
| `consistently_at_risk` | 25 | 0.30 (weight), 25 actual |

`trajectory_type` is a generation-only hidden field. It is **not** a model
feature. It is shown only in EDA to validate generator behavior.

### EDA summary

| Metric | Value |
|---|---|
| `final_grade` mean | 62.411 |
| `final_grade` std | 20.617 |
| `passed` positive rate | 0.781 |

### Key collinearity pairs (Pearson r ≥ 0.95)

| Feature pair | r |
|---|---:|
| `avg_assignment_score_to_date` ↔ `overall_mastery` | **0.993** |
| `overall_mastery` ↔ `performance_index` | **0.999** |
| `avg_assignment_score_to_date` ↔ `performance_index` | 0.996 |
| `activity_score_to_date` ↔ `avg_assignment_score_to_date` | 0.979 |
| `on_time_submission_rate_to_date` ↔ `discipline_index` | **0.999** |
| `avg_assignment_score_to_date` ↔ `avg_quiz_score_to_date` | 0.976 |

Features with Pearson r ≥ 0.97 with `final_grade` (red-flag threshold):
`performance_index` (0.986), `overall_mastery` (0.984),
`activity_score_to_date` (0.983), `avg_assignment_score_to_date` (0.982),
`avg_quiz_score_to_date` (0.978), `engagement_index` (0.971).

---

## 5. Split and Preprocessing Implementation

**Source**: `services/ml/src/experiments/splits.py` and `preprocessing.py`

### Student-grouped split (primary split)

Splits at **student identity level** — all weekly snapshots of a student go
entirely to either train or test, never both.

- `test_size = 0.25` of students → ~28–29 test students × 7 weeks = **196 test rows**
- Training: ~85–86 students × 7 weeks = **602 train rows**
- Prevents leakage of student-specific patterns from train to test

### Temporal-forward split (secondary split)

Splits by `week_number ≤ train_weeks` (train) vs `week_number > train_weeks` (test).

- From actual results: n_train = 258, n_test = 112
- Cutoff is at week 5 (train = weeks 4–5; test = weeks 6–10)
- Also partially holds out students who only appear in later weeks
- Stricter generalization test than the grouped split

### Preprocessing (leakage-safe)

1. Missingness indicators (`has_assignment_score_to_date`, `has_quiz_score_to_date`)
   are included in every feature set.
2. Synthetic `*_was_missing` flags are added for any other numeric feature with NaN values.
3. Imputation: **train-only median imputation** — medians are fit exclusively on
   the training partition, then applied to test. Test statistics never influence
   the imputer.
4. Boolean indicators are cast to `int` for compatibility with linear models.

---

## 6. XAI Implementation Note

**Source**: `services/ml/src/explainability/xai.py` vs
`services/ml/src/experiments/explainability.py`

`services/ml/src/explainability/xai.py` is a **placeholder stub** containing
only a `TODO: integrate SHAP/LIME` comment. It is not the active XAI code.

The actual XAI implementation used in `exp_004` is in
`services/ml/src/experiments/explainability.py`. It implements:

- **Permutation importance**: held-out `neg_root_mean_squared_error` scorer,
  15 repeats, sklearn `permutation_importance` — produces RMSE-increase shares
  (not Shapley values)
- **Local perturbation explanations**: one-feature-at-a-time median replacement
  on five deterministically selected representative cases
- **Dominance audit**: flags if any single feature's average local contribution
  share exceeds 0.60

SHAP was not implemented in any phase. The `ExplainabilityEngine` class in
`xai.py` is unused scaffolding.

---

## 7. OULAD Benchmark Details

**Source**: `data/artifacts/experiments/exp_005_public_benchmark_oulad/`

| Comparison | Primary grouped split RMSE | Forward split RMSE |
|---|---:|---:|
| `B_lms_oulad` (baseline) | 12.658 | 9.566 |
| `B_lms_plus_mastery_oulad` (candidate) | 12.724 | 9.161 |
| Delta | +0.066 | −0.406 |

OULAD module-presentation used: `DDD 2013J`.
Target: derived `final_weighted_score` (not the same as synthetic `final_grade`).
Outcome tag: `complicates` — neither confirms nor invalidates the synthetic result.

---

## Summary: Files to Provide to the Agent

| File | Why it is needed |
|---|---|
| `data/artifacts/experiments/exp_001_baseline/eda/eda_report.md` | Dataset shape, target distributions, collinearity table |
| `data/artifacts/experiments/exp_002_twin_ablation/exp_002_twin_ablation_summary.md` | Full regression results across all feature sets, models, and splits |
| `data/artifacts/experiments/exp_004_xai_on_lean_twin/global_feature_importance.md` | Full importance tables for both `B_lms` and `B_lms_plus_mastery` |
| `data/artifacts/experiments/exp_004_xai_on_lean_twin/local_case_explanations.md` | All five local case explanations with contribution numbers |
| `data/artifacts/experiments/exp_005_public_benchmark_oulad/exp_005_public_benchmark_oulad_summary.md` | OULAD result table |
| `data/artifacts/experiments/exp_005_public_benchmark_oulad/public_vs_synthetic_interpretation.md` | OULAD transfer interpretation |
| `services/ml/src/experiments/featuresets.py` | Exact column membership for every feature set |
| `services/ml/src/experiments/models.py` | Exact hyperparameters for all models |
| `services/ml/src/experiments/splits.py` | Exact split mechanics |
| `services/ml/src/experiments/preprocessing.py` | Exact imputation and leakage-prevention logic |
| `services/ml/src/generator/config.py` | Dataset size, trajectory weights, course domain, seed |
