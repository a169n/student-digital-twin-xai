# exp_006_oulad_full_ablation: Full nested A/B/C ablation on OULAD (DDD 2013J)

## Objective

Determine whether any twin feature block — short-horizon trends, lean mastery analogues, or composite engagement/performance/discipline indices — adds predictive value over the OULAD LMS baseline on both the student-group and temporal-forward splits, using a fixed model family. The nested A/B/C hierarchy isolates each additive block so that each layer's marginal contribution can be read directly from the results table.


## Hypothesis

If the lean Twin representation transfers on OULAD, each successive feature block (trends, mastery, indices) should improve at least one metric over `B_lms_oulad` on the headline temporal-forward split. The full twin analogue `C_twin_oulad` should be at least non-inferior to `B_lms_oulad`. All feature sets are compared under a fixed model family across both splits to guard against model-selection (model-flip) artifacts. Individual sub-blocks may cancel out or interact, so the ablation may reveal diminishing returns or interference between blocks.


## Dataset / config used

- Public benchmark dataset: Open University Learning Analytics Dataset (OULAD)
- Experiment config: `services/ml/configs/experiments/exp_006_oulad_full_ablation.yaml`
- Raw directory: `datasets/oulad`
- Processed benchmark snapshots: `data/artifacts/experiments/exp_006_oulad_full_ablation/oulad_weekly_snapshots.csv`
- Output directory: `data/artifacts/experiments/exp_006_oulad_full_ablation`
- Course filter: `{'code_module': 'DDD', 'code_presentation': '2013J'}`
- Course-filter rationale: Use one OULAD module-presentation to align the public benchmark with the repository's current one-course synthetic scope. `DDD` `2013J` has a sufficiently large cohort, dated TMA assessments, and observed exam score rows, making weekly assessment-state construction more defensible than presentations whose exam timing or exam score coverage is missing.

- Snapshot weeks used: `4..38`

## Exact OULAD files used

- `assessments.csv` from `datasets/oulad/assessments.csv`
- `courses.csv` from `datasets/oulad/courses.csv`
- `studentInfo.csv` from `datasets/oulad/studentInfo.csv`
- `studentRegistration.csv` from `datasets/oulad/studentRegistration.csv`
- `studentVle.csv` from `datasets/oulad/studentVle.csv`
- `vle.csv` from `datasets/oulad/vle.csv`
- `studentAssessment.csv` from `datasets/oulad/studentAssessment.csv`

## Targets

- Primary regression target: `final_weighted_score`
- Secondary classification target: `passed_observed`
- Excluded supervised target(s): `['risk_level']`

`final_weighted_score` is derived from OULAD `assessments.weight` and `studentAssessment.score` as sum(score_or_zero * assessment_weight) / sum(assessment_weight) over positive-weight assessments in the selected module-presentation that have score records in `studentAssessment`. Missing student submissions for those assessments contribute zero to the numerator. `passed_observed` is derived from `studentInfo.final_result`, with Pass and Distinction mapped to 1 and Fail and Withdrawn mapped to 0.


Target distribution is computed at the student-course-presentation level.

| target summary | value |
| --- | ---: |
| final_weighted_score count | 1938 |
| final_weighted_score mean | 36.180 |
| final_weighted_score std | 32.590 |
| final_weighted_score min | 0.000 |
| final_weighted_score median | 33.013 |
| final_weighted_score max | 98.075 |
| passed_observed counts | {'0.0': 1109, '1.0': 829} |

## Feature sets

### `A_simple_oulad`

Minimal OULAD academic baseline: cumulative assessment score signals only.

- Columns: `week_number`, `cumulative_assessment_score_mean_to_date`, `cumulative_assessment_score_count_to_date`
- Indicator columns: `has_assessment_score_to_date`

### `B_lms_oulad`

Strong OULAD LMS-style baseline analogue using cumulative assessment performance, submission discipline, VLE activity intensity and category signals, course-week progression, and registration state.


- Columns: `week_number`, `course_week_progress`, `is_registered_by_week`, `is_unregistered_by_week`, `days_since_registration_start`, `cumulative_assessment_score_mean_to_date`, `cumulative_assessment_score_count_to_date`, `cumulative_assessment_weighted_score_to_date`, `cumulative_submitted_weight_to_date`, `assessment_submission_rate_due_to_date`, `late_submission_rate_to_date`, `banked_assessment_rate_to_date`, `current_week_clicks`, `cumulative_clicks_to_date`, `current_week_activity_types`, `cumulative_assessment_clicks_to_date`, `cumulative_content_clicks_to_date`, `cumulative_social_clicks_to_date`, `cumulative_other_clicks_to_date`
- Indicator columns: `has_assessment_score_to_date`, `has_weighted_score_to_date`, `has_vle_activity_to_date`

### `B_lms_plus_trends_oulad`

OULAD LMS baseline plus short-horizon trend analogues (assessment-score and clicks week-over-week).

- Columns: `week_number`, `course_week_progress`, `is_registered_by_week`, `is_unregistered_by_week`, `days_since_registration_start`, `cumulative_assessment_score_mean_to_date`, `cumulative_assessment_score_count_to_date`, `cumulative_assessment_weighted_score_to_date`, `cumulative_submitted_weight_to_date`, `assessment_submission_rate_due_to_date`, `late_submission_rate_to_date`, `banked_assessment_rate_to_date`, `current_week_clicks`, `cumulative_clicks_to_date`, `current_week_activity_types`, `cumulative_assessment_clicks_to_date`, `cumulative_content_clicks_to_date`, `cumulative_social_clicks_to_date`, `cumulative_other_clicks_to_date`, `assessment_score_trend_to_date`, `clicks_trend_to_date`
- Indicator columns: `has_assessment_score_to_date`, `has_weighted_score_to_date`, `has_vle_activity_to_date`

### `B_lms_plus_mastery_oulad`

OULAD LMS baseline analogue plus a lean mastery-like block derived from dated assessment structure: due-to-date weighted mastery, current assessment-cluster mastery, assessment-type mastery aggregates, and assessment-coverage context.


- Columns: `week_number`, `course_week_progress`, `is_registered_by_week`, `is_unregistered_by_week`, `days_since_registration_start`, `cumulative_assessment_score_mean_to_date`, `cumulative_assessment_score_count_to_date`, `cumulative_assessment_weighted_score_to_date`, `cumulative_submitted_weight_to_date`, `assessment_submission_rate_due_to_date`, `late_submission_rate_to_date`, `banked_assessment_rate_to_date`, `current_week_clicks`, `cumulative_clicks_to_date`, `current_week_activity_types`, `cumulative_assessment_clicks_to_date`, `cumulative_content_clicks_to_date`, `cumulative_social_clicks_to_date`, `cumulative_other_clicks_to_date`, `overall_mastery_proxy`, `current_assessment_cluster_mastery`, `tma_mastery_to_date`, `cma_mastery_to_date`, `exam_mastery_to_date`, `mastery_assessment_coverage_to_date`
- Indicator columns: `has_assessment_score_to_date`, `has_weighted_score_to_date`, `has_vle_activity_to_date`, `has_current_assessment_cluster`, `has_due_assessment_to_date`

### `B_lms_plus_indices_oulad`

OULAD LMS baseline plus composite engagement/performance/discipline indices.

- Columns: `week_number`, `course_week_progress`, `is_registered_by_week`, `is_unregistered_by_week`, `days_since_registration_start`, `cumulative_assessment_score_mean_to_date`, `cumulative_assessment_score_count_to_date`, `cumulative_assessment_weighted_score_to_date`, `cumulative_submitted_weight_to_date`, `assessment_submission_rate_due_to_date`, `late_submission_rate_to_date`, `banked_assessment_rate_to_date`, `current_week_clicks`, `cumulative_clicks_to_date`, `current_week_activity_types`, `cumulative_assessment_clicks_to_date`, `cumulative_content_clicks_to_date`, `cumulative_social_clicks_to_date`, `cumulative_other_clicks_to_date`, `engagement_index_oulad`, `performance_index_oulad`, `discipline_index_oulad`
- Indicator columns: `has_assessment_score_to_date`, `has_weighted_score_to_date`, `has_vle_activity_to_date`

### `C_twin_oulad`

Full OULAD twin analogue: LMS baseline + trends + mastery block + composite indices.

- Columns: `week_number`, `course_week_progress`, `is_registered_by_week`, `is_unregistered_by_week`, `days_since_registration_start`, `cumulative_assessment_score_mean_to_date`, `cumulative_assessment_score_count_to_date`, `cumulative_assessment_weighted_score_to_date`, `cumulative_submitted_weight_to_date`, `assessment_submission_rate_due_to_date`, `late_submission_rate_to_date`, `banked_assessment_rate_to_date`, `current_week_clicks`, `cumulative_clicks_to_date`, `current_week_activity_types`, `cumulative_assessment_clicks_to_date`, `cumulative_content_clicks_to_date`, `cumulative_social_clicks_to_date`, `cumulative_other_clicks_to_date`, `assessment_score_trend_to_date`, `clicks_trend_to_date`, `overall_mastery_proxy`, `current_assessment_cluster_mastery`, `tma_mastery_to_date`, `cma_mastery_to_date`, `exam_mastery_to_date`, `mastery_assessment_coverage_to_date`, `engagement_index_oulad`, `performance_index_oulad`, `discipline_index_oulad`
- Indicator columns: `has_assessment_score_to_date`, `has_weighted_score_to_date`, `has_vle_activity_to_date`, `has_current_assessment_cluster`, `has_due_assessment_to_date`

## Split strategies and models

- Primary split: `student_group`
- Secondary split: `temporal_forward`
- Student-group split: `test_size=0.25`, `seed=42`
- Temporal-forward split: `train_weeks=20`, `student_test_size=0.25`, `student_seed=42`
- Regression models: `linear_regression`, `random_forest`, `gradient_boosting`
- Classification models: `logistic_regression`, `random_forest`, `gradient_boosting`

## Row counts

| item | count |
| --- | ---: |
| assessments | 7 |
| courses | 1 |
| student_info | 1938 |
| student_registration | 1938 |
| vle | 462 |
| student_assessment | 7936 |
| student_vle | 680806 |
| snapshots | 67830 |
| students | 1938 |

## Headline regression results

| split | feature set | best model | RMSE | MAE | R^2 | delta vs baseline |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| temporal_forward | B_lms_plus_mastery_oulad | gradient_boosting | 9.180 | 6.082 | 0.924 | -0.381 |
| temporal_forward | B_lms_plus_indices_oulad | gradient_boosting | 9.343 | 6.168 | 0.921 | -0.218 |
| temporal_forward | B_lms_oulad | gradient_boosting | 9.561 | 6.377 | 0.918 | +0.000 |
| temporal_forward | C_twin_oulad | gradient_boosting | 9.585 | 6.393 | 0.917 | +0.024 |
| temporal_forward | B_lms_plus_trends_oulad | gradient_boosting | 9.638 | 6.535 | 0.916 | +0.077 |
| temporal_forward | A_simple_oulad | gradient_boosting | 13.666 | 9.394 | 0.832 | +4.105 |
| student_group | B_lms_plus_trends_oulad | gradient_boosting | 12.612 | 7.868 | 0.857 | -0.048 |
| student_group | C_twin_oulad | gradient_boosting | 12.641 | 7.814 | 0.856 | -0.019 |
| student_group | B_lms_oulad | gradient_boosting | 12.660 | 7.891 | 0.855 | +0.000 |
| student_group | B_lms_plus_indices_oulad | gradient_boosting | 12.668 | 7.901 | 0.855 | +0.008 |
| student_group | B_lms_plus_mastery_oulad | gradient_boosting | 12.721 | 7.893 | 0.854 | +0.061 |
| student_group | A_simple_oulad | gradient_boosting | 13.866 | 9.250 | 0.827 | +1.207 |

## Fixed-model regression results (model = `gradient_boosting`)

Same model across all feature sets and both splits, to neutralize best-model-per-cell (model-flip) artifacts. Headline split: `temporal_forward`.

| split | feature set | model | RMSE | MAE | R^2 | delta vs baseline |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| temporal_forward | B_lms_plus_mastery_oulad | gradient_boosting | 9.180 | 6.082 | 0.924 | -0.381 |
| temporal_forward | B_lms_plus_indices_oulad | gradient_boosting | 9.343 | 6.168 | 0.921 | -0.218 |
| temporal_forward | B_lms_oulad | gradient_boosting | 9.561 | 6.377 | 0.918 | +0.000 |
| temporal_forward | C_twin_oulad | gradient_boosting | 9.585 | 6.393 | 0.917 | +0.024 |
| temporal_forward | B_lms_plus_trends_oulad | gradient_boosting | 9.638 | 6.535 | 0.916 | +0.077 |
| temporal_forward | A_simple_oulad | gradient_boosting | 13.666 | 9.394 | 0.832 | +4.105 |
| student_group | B_lms_plus_trends_oulad | gradient_boosting | 12.612 | 7.868 | 0.857 | -0.048 |
| student_group | C_twin_oulad | gradient_boosting | 12.641 | 7.814 | 0.856 | -0.019 |
| student_group | B_lms_oulad | gradient_boosting | 12.660 | 7.891 | 0.855 | +0.000 |
| student_group | B_lms_plus_indices_oulad | gradient_boosting | 12.668 | 7.901 | 0.855 | +0.008 |
| student_group | B_lms_plus_mastery_oulad | gradient_boosting | 12.721 | 7.893 | 0.854 | +0.061 |
| student_group | A_simple_oulad | gradient_boosting | 13.866 | 9.250 | 0.827 | +1.207 |

## Secondary classification results

| split | feature set | best model | F1 | accuracy | ROC AUC |
| --- | --- | --- | ---: | ---: | ---: |
| student_group | A_simple_oulad | gradient_boosting | 0.844 | 0.859 | 0.942 |
| student_group | B_lms_oulad | gradient_boosting | 0.863 | 0.876 | 0.953 |
| student_group | B_lms_plus_indices_oulad | gradient_boosting | 0.863 | 0.876 | 0.953 |
| student_group | B_lms_plus_mastery_oulad | gradient_boosting | 0.861 | 0.874 | 0.953 |
| student_group | B_lms_plus_trends_oulad | gradient_boosting | 0.865 | 0.878 | 0.954 |
| student_group | C_twin_oulad | gradient_boosting | 0.864 | 0.877 | 0.953 |
| temporal_forward | A_simple_oulad | logistic_regression | 0.830 | 0.863 | 0.959 |
| temporal_forward | B_lms_oulad | logistic_regression | 0.887 | 0.900 | 0.970 |
| temporal_forward | B_lms_plus_indices_oulad | logistic_regression | 0.887 | 0.899 | 0.969 |
| temporal_forward | B_lms_plus_mastery_oulad | logistic_regression | 0.884 | 0.898 | 0.969 |
| temporal_forward | B_lms_plus_trends_oulad | logistic_regression | 0.887 | 0.900 | 0.971 |
| temporal_forward | C_twin_oulad | logistic_regression | 0.883 | 0.898 | 0.969 |

## Interpretation

The OULAD benchmark complicates the synthetic finding: the mastery analogue is approximately level with the LMS baseline under the configured tolerance. This suggests that the representation may be context-sensitive rather than universally advantageous.

- Outcome: `complicates`
- Primary delta RMSE: `+0.024`
- Short conclusion: `C_twin_oulad` was approximately level with `B_lms_oulad` on OULAD.

This is a representation-transfer stress test, not a claim that one dataset is better than another and not a claim of full external validity.

## Artifact paths

- Results CSV: `data/artifacts/experiments/exp_006_oulad_full_ablation/exp_006_oulad_full_ablation_results.csv`
- Results JSON: `data/artifacts/experiments/exp_006_oulad_full_ablation/exp_006_oulad_full_ablation_results.json`
- Summary Markdown: `data/artifacts/experiments/exp_006_oulad_full_ablation/exp_006_oulad_full_ablation_summary.md`
- Processed snapshots CSV: `data/artifacts/experiments/exp_006_oulad_full_ablation/oulad_weekly_snapshots.csv`
- Mapping artifact: `data/artifacts/experiments/exp_006_oulad_full_ablation/public_benchmark_mapping_summary.md`
- Public-vs-synthetic interpretation: `data/artifacts/experiments/exp_006_oulad_full_ablation/public_vs_synthetic_interpretation.md`

## Limitations

- This experiment isolates the marginal contribution of each twin feature block on a public dataset; it is not a comparison of synthetic versus public dataset quality.

- The primary OULAD target is a derived weighted assessment score, not the exact same construct as the synthetic `final_grade`.

- The selected OULAD subset is one module-presentation (`DDD`, `2013J`) to match the current one-course research scope and keep model training reproducible on local hardware.

- OULAD has no clean equivalents for attendance, synthetic weekly topics, hidden trajectory parameters, risk labels, or intervention state.

- This benchmark can support or complicate external transfer plausibility; it cannot establish full institutional external validity.

- The OULAD regression target (final_weighted_score) is partially circular on assessment-score features (cumulative_assessment_weighted_score_to_date feeds the target); interpretation leans on exogenous clickstream features and the classification target.


## Next step

Use the full-ablation results to identify which feature blocks transfer to OULAD and refine the dissertation external-validity discussion accordingly. Identify which specific blocks (if any) transfer to OULAD under the fixed-model comparison and carry only those block-level claims forward with a public-benchmark caveat; if no block improves over the LMS baseline on the temporal-forward split, report that the twin blocks do not transfer and narrow the claim accordingly.

