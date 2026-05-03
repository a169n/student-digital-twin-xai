# exp_003_mastery_validation: Mastery validation

## Objective

Validate whether the mastery block (`current_topic_mastery`, `overall_mastery`) is a trustworthy lean Twin component before the project moves into XAI. This experiment focuses specifically on whether mastery adds genuine signal beyond the `B_lms` baseline, or whether it acts as a near-direct proxy for `final_grade`.


## Hypothesis

Mastery features are derived from the same submission scores that already feed `B_lms` features such as `avg_assignment_score_to_date` and `avg_quiz_score_to_date`. The expected outcome is that mastery offers a modest improvement that is plausibly attributable to topic-level aggregation, but does not collapse into a direct copy of `final_grade`.


## Dataset / config used

- Schema version: `v1.2`
- Dataset version/config: `v1_3_refined` / `generator_v1_3_refined.yaml`
- Experiment config: `services/ml/configs/experiments/exp_003_mastery_validation.yaml`
- Snapshot table: `data/processed/student_twin_snapshots.csv`
- Final results table: `data/raw/final_results.csv`
- Output directory: `data/artifacts/experiments/exp_003_mastery_validation`

## Compared feature sets

- Baseline: `B_lms`
- Candidate: `B_lms_plus_mastery`
- Optional context sets: `B_lms_plus_trends_mastery`, `C_twin_full`

## Split strategies

- Primary: `student_group`
- Secondary: `temporal_forward`
- Seed: `42`

## Week-aware protocol

Per-week regression evaluation restricts snapshots to a single week and applies the student-group split (test_size=0.25, seed=42). The candidate feature set is `B_lms_plus_mastery`; the baseline is `B_lms`. Improvement at a week is `candidate_rmse - baseline_rmse < -0.05`. Weeks examined: [4, 5, 6, 7, 8, 9, 10]. Early-week window: weeks <= 6.

## Diagnostic checks

1. mastery vs `final_grade` correlations, globally and per week,
2. mastery vs LMS-baseline-feature redundancy (max |Pearson r|),
3. drop-column re-training of the candidate model,
4. permutation importance for the same model on the held-out split.

## Headline regression results

Primary regression on the full snapshot range (week >= 4). Lower RMSE is better. `delta_vs_B_lms_rmse` is computed within the same split after picking the best model per feature set.

| split | feature set | best model | RMSE | MAE | R^2 | delta vs `B_lms` |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| student_group | B_lms_plus_mastery | gradient_boosting | 1.894 | 1.510 | 0.992 | -0.206 |
| student_group | B_lms_plus_trends_mastery | gradient_boosting | 1.973 | 1.573 | 0.991 | -0.127 |
| student_group | B_lms | gradient_boosting | 2.101 | 1.681 | 0.990 | +0.000 |
| student_group | C_twin_full | random_forest | 2.149 | 1.732 | 0.989 | +0.049 |
| temporal_forward | B_lms | linear_regression | 2.270 | 1.778 | 0.988 | +0.000 |
| temporal_forward | B_lms_plus_mastery | linear_regression | 2.276 | 1.776 | 0.988 | +0.006 |
| temporal_forward | B_lms_plus_trends_mastery | linear_regression | 2.555 | 2.024 | 0.985 | +0.284 |
| temporal_forward | C_twin_full | linear_regression | 2.937 | 2.396 | 0.980 | +0.667 |

## Mastery vs `final_grade` correlations

| feature | global Pearson r | strongest weekly |r| | weakest weekly |r| |
| --- | ---: | ---: | ---: |
| current_topic_mastery | 0.935 | 0.963 | 0.891 |
| overall_mastery | 0.984 | 0.997 | 0.965 |

## Mastery redundancy with LMS baseline features

| mastery feature | strongest LMS correlate | |Pearson r| |
| --- | --- | ---: |
| current_topic_mastery | avg_quiz_score_to_date | 0.934 |
| overall_mastery | avg_assignment_score_to_date | 0.993 |

## Context: LMS baseline target correlations

Reported so the mastery vs target correlation can be compared to what `B_lms` already provides on this dataset.

| LMS feature | Pearson r vs `final_grade` |
| --- | ---: |
| avg_assignment_score_to_date | 0.982 |
| avg_quiz_score_to_date | 0.978 |
| attendance_rate_to_date | 0.915 |
| activity_score_to_date | 0.983 |
| time_spent_to_date | 0.796 |
| on_time_submission_rate_to_date | 0.884 |
| missed_assignments_to_date | -0.610 |
| late_submissions_to_date | -0.652 |
| avg_attempt_count_to_date | 0.674 |

## Week-aware delta of `B_lms_plus_mastery` vs `B_lms`

Negative `delta_rmse` means mastery improved on the LMS baseline at that week.

| week | baseline RMSE | candidate RMSE | delta RMSE | candidate improves baseline? |
| ---: | ---: | ---: | ---: | :---: |
| 4 | 2.261 | 2.043 | -0.218 | yes |
| 5 | 3.497 | 2.906 | -0.591 | yes |
| 6 | 2.311 | 2.100 | -0.210 | yes |
| 7 | 2.169 | 2.081 | -0.089 | yes |
| 8 | 1.874 | 1.489 | -0.385 | yes |
| 9 | 1.179 | 1.161 | -0.019 | no |
| 10 | 0.404 | 0.379 | -0.025 | no |

## Drop-column tests on `B_lms_plus_mastery`

Best regression model for the candidate set: `gradient_boosting`. Full RMSE on student-group split: `1.894`.

| dropped feature | new RMSE | delta vs full RMSE |
| --- | ---: | ---: |
| current_topic_mastery | 1.931 | +0.036 |
| overall_mastery | 2.122 | +0.228 |

## Permutation importance (top features)

| feature | mean RMSE increase | std |
| --- | ---: | ---: |
| missed_assignments_to_date | -0.018 | 0.017 |
| avg_attempt_count_to_date | -0.035 | 0.017 |
| late_submissions_to_date | -0.043 | 0.014 |
| current_topic_mastery | -0.078 | 0.030 |
| avg_quiz_score_to_date | -0.408 | 0.067 |
| attendance_rate_to_date | -0.427 | 0.072 |
| time_spent_to_date | -0.536 | 0.079 |
| on_time_submission_rate_to_date | -0.548 | 0.075 |
| avg_assignment_score_to_date | -2.261 | 0.143 |
| overall_mastery | -4.406 | 0.186 |

## Temporal legitimacy of mastery features

### `current_topic_mastery`

- Source fields: submissions.normalized_score (filtered to current topic and week<=snapshot week), fallback: avg_quiz_score_to_date / avg_assignment_score_to_date
- Uses future information: `False`
- Uses end-of-course outcome fields: `False`
- Notes: Computed from cumulative submission scores filtered to `week_number <= snapshot week`. Falls back to other snapshot-time averages when the current topic has no submissions yet.

### `overall_mastery`

- Source fields: submissions.normalized_score (filtered to week<=snapshot week, grouped per topic), fallback: current_topic_mastery
- Uses future information: `False`
- Uses end-of-course outcome fields: `False`
- Notes: Mean of per-topic mean scores using only submissions up to the snapshot week. Does not read `final_results.final_grade` or any post-course field.

_Verification:_ Lineage is documented from the generator code, not enforced by an automated lineage check. See `services/ml/src/generator/snapshots.py` for the construction.

## Main findings

- Headline overall delta `candidate - baseline` (primary split): -0.206
- Weeks where mastery improved baseline (early): [4, 5, 6]
- Weeks where mastery improved baseline (late): [7, 8]
- Max absolute mastery vs `final_grade` Pearson r: 0.984
- Highly redundant mastery columns: ['overall_mastery']

## Interpretation

Carry `B_lms_plus_mastery` into XAI as the lean Twin candidate. It improves on `B_lms` overall and in at least one early-week cutoff, supporting the early-warning story.

### Flags

- `overall_mastery` is highly redundant with LMS feature `avg_assignment_score_to_date` (|r|=0.993)
- dropping `overall_mastery` increases RMSE by +0.228, indicating the candidate model leans heavily on a single mastery feature

## Decision

- Outcome: `carry_forward`
- Carry-forward feature set: `B_lms_plus_mastery` if outcome is `carry_forward`/`carry_forward_with_caveat`, otherwise revisit before XAI.
- Reference baseline: `B_lms`

## Artifact paths

- Results JSON: `data/artifacts/experiments/exp_003_mastery_validation/exp_003_mastery_validation_results.json`
- Results CSV: `data/artifacts/experiments/exp_003_mastery_validation/exp_003_mastery_validation_results.csv`
- Runner summary: `data/artifacts/experiments/exp_003_mastery_validation/exp_003_mastery_validation_summary.md`
- Diagnostics JSON: `data/artifacts/experiments/exp_003_mastery_validation/mastery_diagnostics.json`
- Weekly validation CSV: `data/artifacts/experiments/exp_003_mastery_validation/mastery_weekly_validation.csv`
- Carry-forward recommendation: `data/artifacts/experiments/exp_003_mastery_validation/mastery_carry_forward_recommendation.md`

## Limitations

- The dataset is synthetic and the comparison cannot prove generalization to real institutional data; it can only detect issues that already show up in the synthetic generator.

- Drop-column tests are run on the current best regression model only; they expose dependency on a single feature but do not produce a full causal attribution.

- Temporal legitimacy of mastery is documented from the generator code in `services/ml/src/generator/snapshots.py`; it is not currently enforced by an automated lineage check, only by code review and feature-set conventions.

- Per-week evaluation reuses the student-group split; week-cutoff regression scores can therefore vary with the small per-week test sets, so the validation looks at the early-week pattern as a whole rather than at any single week in isolation.


## Next step

If mastery is validated, carry `B_lms_plus_mastery` into the XAI phase as the lean Twin candidate. If mastery looks too target-like or only useful near the end of the course, narrow the carry-forward set or revisit the generator before adding any explanation layer on top.

