# exp_004_xai_on_lean_twin: XAI on lean Twin

## Objective

Explain the validated lean Twin candidate, `B_lms_plus_mastery`, and decide whether its predictive behavior is interpretable and teacher-meaningful or whether the model collapses into one dominating mastery feature.


## Hypothesis

The lean Twin candidate should keep the predictive improvement observed in mastery validation while producing explanations that combine LMS behavior, performance, and mastery signals. `overall_mastery` is expected to be important and redundant, but it should not suppress all other explanation factors.


## Dataset / config used

- Schema version: `v1.2`
- Dataset version/config: `v1_3_refined` / `generator_v1_3_refined.yaml`
- Experiment config: `services/ml/configs/experiments/exp_004_xai_on_lean_twin.yaml`
- Snapshot table: `data/processed/student_twin_snapshots.csv`
- Final results table: `data/raw/final_results.csv`
- Output directory: `data/artifacts/experiments/exp_004_xai_on_lean_twin`

## Reference model

- Split: `student_group`
- Model: `gradient_boosting`
- Primary target: `final_grade`
- Secondary context only: `passed`
- Baseline feature set: `B_lms`
- Lean Twin feature set: `B_lms_plus_mastery`

## Explainability methods

Global explanations use held-out permutation importance with `neg_root_mean_squared_error`, plus model-native tree importance where available. Local explanations use one-feature-at-a-time replacement with the training median. These are directional model-behavior explanations, not causal claims.

SHAP used: `False`. Fallback reason: SHAP is not part of the current project dependency contract; use documented sklearn permutation and local perturbation fallbacks.


## Model behavior

| feature set | RMSE | MAE | R^2 |
| --- | ---: | ---: | ---: |
| B_lms | 2.101 | 1.681 | 0.990 |
| B_lms_plus_mastery | 1.894 | 1.510 | 0.992 |
| `B_lms_plus_mastery` without `overall_mastery` | 2.122 | 1.686 | 0.990 |

Lean Twin delta vs baseline RMSE: `-0.206`. Without-`overall_mastery` delta vs lean RMSE: `+0.228`.

## Global findings

Top held-out permutation-importance features are shown below. Positive values
mean RMSE increases when the feature is permuted.

| feature set | rank | feature | RMSE increase | share | direction note |
| --- | ---: | --- | ---: | ---: | --- |
| B_lms | 1 | activity_score_to_date | 17.843 | 0.701 | higher values generally align with higher predicted final_grade |
| B_lms | 2 | avg_assignment_score_to_date | 3.687 | 0.145 | higher values generally align with higher predicted final_grade |
| B_lms | 3 | avg_quiz_score_to_date | 2.178 | 0.086 | higher values generally align with higher predicted final_grade |
| B_lms | 4 | on_time_submission_rate_to_date | 0.592 | 0.023 | higher values generally align with higher predicted final_grade |
| B_lms | 5 | attendance_rate_to_date | 0.577 | 0.023 | higher values generally align with higher predicted final_grade |
| B_lms | 6 | time_spent_to_date | 0.481 | 0.019 | higher values generally align with higher predicted final_grade |
| B_lms | 7 | avg_attempt_count_to_date | 0.084 | 0.003 | higher values generally align with higher predicted final_grade |
| B_lms | 8 | late_submissions_to_date | 0.026 | 0.001 | higher values generally align with lower predicted final_grade |
| B_lms | 9 | missed_assignments_to_date | 0.003 | 0.000 | higher values generally align with lower predicted final_grade |
| B_lms | 10 | avg_assignment_score_to_date_was_missing | 0.000 | 0.000 | direction unclear |
| B_lms | 11 | avg_quiz_score_to_date_was_missing | 0.000 | 0.000 | higher values generally align with lower predicted final_grade |
| B_lms_plus_mastery | 1 | activity_score_to_date | 16.288 | 0.648 | higher values generally align with higher predicted final_grade |
| B_lms_plus_mastery | 2 | overall_mastery | 4.489 | 0.178 | higher values generally align with higher predicted final_grade |
| B_lms_plus_mastery | 3 | avg_assignment_score_to_date | 2.272 | 0.090 | higher values generally align with higher predicted final_grade |
| B_lms_plus_mastery | 4 | time_spent_to_date | 0.550 | 0.022 | higher values generally align with higher predicted final_grade |
| B_lms_plus_mastery | 5 | on_time_submission_rate_to_date | 0.548 | 0.022 | higher values generally align with higher predicted final_grade |
| B_lms_plus_mastery | 6 | attendance_rate_to_date | 0.427 | 0.017 | higher values generally align with higher predicted final_grade |
| B_lms_plus_mastery | 7 | avg_quiz_score_to_date | 0.403 | 0.016 | higher values generally align with higher predicted final_grade |
| B_lms_plus_mastery | 8 | current_topic_mastery | 0.076 | 0.003 | higher values generally align with higher predicted final_grade |
| B_lms_plus_mastery | 9 | late_submissions_to_date | 0.042 | 0.002 | higher values generally align with lower predicted final_grade |
| B_lms_plus_mastery | 10 | avg_attempt_count_to_date | 0.030 | 0.001 | higher values generally align with higher predicted final_grade |
| B_lms_plus_mastery | 11 | missed_assignments_to_date | 0.028 | 0.001 | higher values generally align with lower predicted final_grade |
| B_lms_plus_mastery | 12 | avg_assignment_score_to_date_was_missing | 0.000 | 0.000 | direction unclear |

## Baseline vs lean Twin explanation comparison

Baseline top features: ['activity_score_to_date', 'avg_assignment_score_to_date', 'avg_quiz_score_to_date', 'on_time_submission_rate_to_date', 'attendance_rate_to_date']. Lean Twin top features: ['activity_score_to_date', 'overall_mastery', 'avg_assignment_score_to_date', 'time_spent_to_date', 'on_time_submission_rate_to_date']. Mastery features entering the lean top ranking: ['overall_mastery'].

## `overall_mastery` dominance audit

- Outcome: `acceptable_with_caveat`
- Rank: `2`
- Global importance share: `0.178`
- RMSE increase when removed: `+0.228`
- Average local mastery contribution share: `0.194`
- Interpretation: `overall_mastery` is influential and redundant enough to require explicit caveats, but the explanation does not collapse entirely into one mastery feature.

Flags:
- top global feature accounts for 0.648 of importance share

## Local case findings

| case | student | week | predicted | actual | mastery central? | assessment |
| --- | --- | ---: | ---: | ---: | :---: | --- |
| strong_performer | student_054 | 10 | 90.300 | 93.140 | yes | teacher-meaningful with mastery as part of the student-state story |
| at_risk | student_115 | 10 | 23.265 | 22.450 | yes | teacher-meaningful with mastery as part of the student-state story |
| improving_trajectory | student_112 | 5 | 59.734 | 61.870 | no | teacher-meaningful and mostly LMS-behavior/performance driven |
| declining_trajectory | student_027 | 5 | 33.235 | 29.950 | yes | teacher-meaningful with mastery as part of the student-state story |
| borderline_medium | student_020 | 10 | 56.479 | 53.940 | yes | teacher-meaningful with mastery as part of the student-state story |

## Interpretation

Carry `B_lms_plus_mastery` forward for dissertation XAI with an `overall_mastery` redundancy caveat; explanations remain teacher-meaningful and do not collapse into one feature.

## Decision / next step

- Outcome: `carry_forward_with_caveat`
- Carry-forward feature set: `B_lms_plus_mastery`
- Reference baseline: `B_lms`

## Artifact paths

- results_json: `data/artifacts/experiments/exp_004_xai_on_lean_twin/exp_004_xai_on_lean_twin_results.json`
- summary_markdown: `data/artifacts/experiments/exp_004_xai_on_lean_twin/exp_004_xai_on_lean_twin_summary.md`
- global_importance_csv: `data/artifacts/experiments/exp_004_xai_on_lean_twin/global_feature_importance.csv`
- global_importance_markdown: `data/artifacts/experiments/exp_004_xai_on_lean_twin/global_feature_importance.md`
- local_cases_json: `data/artifacts/experiments/exp_004_xai_on_lean_twin/local_case_explanations.json`
- local_cases_markdown: `data/artifacts/experiments/exp_004_xai_on_lean_twin/local_case_explanations.md`
- recommendation: `data/artifacts/experiments/exp_004_xai_on_lean_twin/xai_carry_forward_recommendation.md`

## Limitations

- The dataset is synthetic, so explanations reflect the current generator assumptions and cannot be interpreted as evidence of real-world causal mechanisms.

- `overall_mastery` is known from `exp_003_mastery_validation` to be highly redundant with LMS score aggregates; this experiment audits that risk rather than treating mastery as an independent construct.

- SHAP is not used because it is not part of the current project dependency contract. The experiment uses documented sklearn permutation importance and local perturbation fallbacks instead.

- Local explanations are compact representative snapshots selected by deterministic rules; they are not a full qualitative case study of every student trajectory.


## Next step

If explanations remain teacher-meaningful with acceptable mastery dominance, carry `B_lms_plus_mastery` into the dissertation XAI narrative. If `overall_mastery` dominates, narrow the lean Twin representation before building scenario-analysis logic.

