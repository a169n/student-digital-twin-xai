# exp_005_public_benchmark_oulad: Public OULAD benchmark for lean Twin transfer

## Objective

Test whether the representation logic carried forward from the synthetic experiments can be approximated on the Open University Learning Analytics Dataset (OULAD), and whether an OULAD lean mastery analogue improves over a strong OULAD LMS-style baseline.


## Hypothesis

If the lean Twin conclusion transfers directionally, then `B_lms_plus_mastery_oulad` should improve over `B_lms_oulad` on leakage-safe OULAD weekly snapshots. The benchmark may also weaken or complicate the synthetic finding because OULAD does not expose the same topic, attendance, or synthetic mastery fields.


## Dataset / config used

- Public benchmark dataset: Open University Learning Analytics Dataset (OULAD)
- Experiment config: `services/ml/configs/experiments/exp_005_public_benchmark_oulad.yaml`
- Raw directory: `datasets/oulad`
- Processed benchmark snapshots: `data/artifacts/experiments/exp_005_public_benchmark_oulad/oulad_weekly_snapshots.csv`
- Output directory: `data/artifacts/experiments/exp_005_public_benchmark_oulad`
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

### `B_lms_oulad`

Strong OULAD LMS-style baseline analogue using cumulative assessment performance, submission discipline, VLE activity intensity and category signals, course-week progression, and registration state.


- Columns: `week_number`, `course_week_progress`, `is_registered_by_week`, `is_unregistered_by_week`, `days_since_registration_start`, `cumulative_assessment_score_mean_to_date`, `cumulative_assessment_score_count_to_date`, `cumulative_assessment_weighted_score_to_date`, `cumulative_submitted_weight_to_date`, `assessment_submission_rate_due_to_date`, `late_submission_rate_to_date`, `banked_assessment_rate_to_date`, `current_week_clicks`, `cumulative_clicks_to_date`, `current_week_activity_types`, `cumulative_assessment_clicks_to_date`, `cumulative_content_clicks_to_date`, `cumulative_social_clicks_to_date`, `cumulative_other_clicks_to_date`
- Indicator columns: `has_assessment_score_to_date`, `has_weighted_score_to_date`, `has_vle_activity_to_date`

### `B_lms_plus_mastery_oulad`

OULAD LMS baseline analogue plus a lean mastery-like block derived from dated assessment structure: due-to-date weighted mastery, current assessment-cluster mastery, assessment-type mastery aggregates, and assessment-coverage context.


- Columns: `week_number`, `course_week_progress`, `is_registered_by_week`, `is_unregistered_by_week`, `days_since_registration_start`, `cumulative_assessment_score_mean_to_date`, `cumulative_assessment_score_count_to_date`, `cumulative_assessment_weighted_score_to_date`, `cumulative_submitted_weight_to_date`, `assessment_submission_rate_due_to_date`, `late_submission_rate_to_date`, `banked_assessment_rate_to_date`, `current_week_clicks`, `cumulative_clicks_to_date`, `current_week_activity_types`, `cumulative_assessment_clicks_to_date`, `cumulative_content_clicks_to_date`, `cumulative_social_clicks_to_date`, `cumulative_other_clicks_to_date`, `overall_mastery_proxy`, `current_assessment_cluster_mastery`, `tma_mastery_to_date`, `cma_mastery_to_date`, `exam_mastery_to_date`, `mastery_assessment_coverage_to_date`
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
| student_group | B_lms_oulad | gradient_boosting | 12.658 | 7.890 | 0.855 | +0.000 |
| student_group | B_lms_plus_mastery_oulad | gradient_boosting | 12.724 | 7.896 | 0.854 | +0.066 |
| temporal_forward | B_lms_plus_mastery_oulad | gradient_boosting | 9.161 | 6.069 | 0.924 | -0.406 |
| temporal_forward | B_lms_oulad | gradient_boosting | 9.566 | 6.378 | 0.917 | +0.000 |

## Secondary classification results

| split | feature set | best model | F1 | accuracy | ROC AUC |
| --- | --- | --- | ---: | ---: | ---: |
| student_group | B_lms_oulad | gradient_boosting | 0.863 | 0.876 | 0.953 |
| student_group | B_lms_plus_mastery_oulad | gradient_boosting | 0.861 | 0.874 | 0.953 |
| temporal_forward | B_lms_oulad | logistic_regression | 0.887 | 0.900 | 0.970 |
| temporal_forward | B_lms_plus_mastery_oulad | logistic_regression | 0.884 | 0.898 | 0.969 |

## Interpretation

The OULAD benchmark complicates the synthetic carry-forward claim: the mastery analogue is slightly worse than the LMS baseline on the primary student-grouped split, but improves the secondary temporal-forward split. This mixed result suggests transfer sensitivity rather than clear public-benchmark confirmation or rejection.

- Outcome: `complicates`
- Primary delta RMSE: `+0.066`
- Short conclusion: `B_lms_plus_mastery_oulad` did not improve the primary OULAD grouped split, but improved a secondary temporal-forward split.

This is a representation-transfer stress test, not a claim that one dataset is better than another and not a claim of full external validity.

## Artifact paths

- Results CSV: `data/artifacts/experiments/exp_005_public_benchmark_oulad/exp_005_public_benchmark_oulad_results.csv`
- Results JSON: `data/artifacts/experiments/exp_005_public_benchmark_oulad/exp_005_public_benchmark_oulad_results.json`
- Summary Markdown: `data/artifacts/experiments/exp_005_public_benchmark_oulad/exp_005_public_benchmark_oulad_summary.md`
- Processed snapshots CSV: `data/artifacts/experiments/exp_005_public_benchmark_oulad/oulad_weekly_snapshots.csv`
- Mapping artifact: `data/artifacts/experiments/exp_005_public_benchmark_oulad/public_benchmark_mapping_summary.md`
- Public-vs-synthetic interpretation: `data/artifacts/experiments/exp_005_public_benchmark_oulad/public_vs_synthetic_interpretation.md`

## Limitations

- This is an external public-benchmark stress test of representation logic, not a comparison between synthetic and public dataset quality.

- The primary OULAD target is a derived weighted assessment score, not the exact same construct as the synthetic `final_grade`.

- The selected OULAD subset is one module-presentation (`DDD`, `2013J`) to match the current one-course research scope and keep model training reproducible on local hardware.

- OULAD has no clean equivalents for attendance, synthetic weekly topics, hidden trajectory parameters, risk labels, or intervention state.

- This benchmark can support or complicate external transfer plausibility; it cannot establish full institutional external validity.


## Next step

Use the benchmark outcome to refine the dissertation external-validity discussion. If the mastery analogue helps, carry the lean Twin claim forward with a public-benchmark caveat. If it does not, narrow the claim to internal synthetic validity and treat mastery transfer as unresolved.

