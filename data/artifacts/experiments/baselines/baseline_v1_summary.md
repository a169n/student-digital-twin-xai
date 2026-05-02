# Baseline experiment summary: `baseline_v1`

This report compares baseline models across three feature sets — `A_simple`, `B_lms`, and `C_twin` — for the dissertation's primary experimental targets: `final_grade` (regression) and `passed` (classification). The teacher-facing heuristic `risk_level` is intentionally NOT used as a supervised target.

## Run metadata

- **snapshots_path**: C:\Users\a1byn\Desktop\dev\aitu\student-digital-twin-xai\data\processed\student_twin_snapshots.csv
- **final_results_path**: C:\Users\a1byn\Desktop\dev\aitu\student-digital-twin-xai\data\raw\final_results.csv
- **snapshot_week_min**: 4
- **snapshot_week_max**: 10
- **n_modeling_rows**: 798
- **n_modeling_students**: 114
- **feature_sets**: [{'name': 'A_simple', 'description': 'Minimal academic baseline. Uses only the most basic teacher-visible performance and attendance signals available from the LMS. Intended as a deliberately weak reference point.', 'columns': ['avg_assignment_score_to_date', 'avg_quiz_score_to_date', 'attendance_rate_to_date'], 'indicator_columns': ['has_assignment_score_to_date', 'has_quiz_score_to_date']}, {'name': 'B_lms', 'description': 'Stronger non-twin LMS baseline. Adds broader behavioral and submission-discipline signals that a typical LMS analytics view could plausibly expose without any digital-twin engineering.', 'columns': ['avg_assignment_score_to_date', 'avg_quiz_score_to_date', 'attendance_rate_to_date', 'activity_score_to_date', 'time_spent_to_date', 'on_time_submission_rate_to_date', 'missed_assignments_to_date', 'late_submissions_to_date', 'avg_attempt_count_to_date'], 'indicator_columns': ['has_assignment_score_to_date', 'has_quiz_score_to_date']}, {'name': 'C_twin', 'description': 'Full Digital Twin representation. Includes the LMS baseline plus short-horizon trend features, mastery proxies, and composite engagement / performance / discipline indices.', 'columns': ['avg_assignment_score_to_date', 'avg_quiz_score_to_date', 'attendance_rate_to_date', 'activity_score_to_date', 'time_spent_to_date', 'on_time_submission_rate_to_date', 'missed_assignments_to_date', 'late_submissions_to_date', 'avg_attempt_count_to_date', 'score_trend_3w', 'activity_trend_3w', 'attendance_trend_3w', 'current_topic_mastery', 'overall_mastery', 'engagement_index', 'performance_index', 'discipline_index', 'week_number'], 'indicator_columns': ['has_assignment_score_to_date', 'has_quiz_score_to_date']}]
- **split_strategies**: ['student_group', 'temporal_forward']

## Classification results — target `passed`

| split | feature set | model | n_train | n_test | accuracy | precision | recall | f1 | roc_auc |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| student_group | A_simple | logistic_regression | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | A_simple | random_forest | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | A_simple | gradient_boosting | 602 | 196 | 0.990 | 0.986 | 1.000 | 0.993 | 1.000 |
| temporal_forward | A_simple | logistic_regression | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | A_simple | random_forest | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | A_simple | gradient_boosting | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms | logistic_regression | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms | random_forest | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms | gradient_boosting | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms | logistic_regression | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms | random_forest | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms | gradient_boosting | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | C_twin | logistic_regression | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | C_twin | random_forest | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | C_twin | gradient_boosting | 602 | 196 | 0.995 | 0.993 | 1.000 | 0.996 | 1.000 |
| temporal_forward | C_twin | logistic_regression | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | C_twin | random_forest | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | C_twin | gradient_boosting | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

## Regression results — target `final_grade`

| split | feature set | model | n_train | n_test | MAE | RMSE | R^2 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| student_group | A_simple | linear_regression | 602 | 196 | 2.261 | 2.935 | 0.980 |
| student_group | A_simple | random_forest | 602 | 196 | 2.224 | 3.770 | 0.967 |
| student_group | A_simple | gradient_boosting | 602 | 196 | 1.992 | 2.673 | 0.983 |
| temporal_forward | A_simple | linear_regression | 258 | 112 | 1.834 | 2.210 | 0.989 |
| temporal_forward | A_simple | random_forest | 258 | 112 | 2.537 | 3.216 | 0.976 |
| temporal_forward | A_simple | gradient_boosting | 258 | 112 | 2.693 | 3.451 | 0.972 |
| student_group | B_lms | linear_regression | 602 | 196 | 2.155 | 2.845 | 0.981 |
| student_group | B_lms | random_forest | 602 | 196 | 1.807 | 2.296 | 0.988 |
| student_group | B_lms | gradient_boosting | 602 | 196 | 1.681 | 2.101 | 0.990 |
| temporal_forward | B_lms | linear_regression | 258 | 112 | 1.778 | 2.270 | 0.988 |
| temporal_forward | B_lms | random_forest | 258 | 112 | 2.813 | 3.474 | 0.972 |
| temporal_forward | B_lms | gradient_boosting | 258 | 112 | 2.499 | 3.160 | 0.977 |
| student_group | C_twin | linear_regression | 602 | 196 | 2.037 | 2.698 | 0.983 |
| student_group | C_twin | random_forest | 602 | 196 | 1.732 | 2.149 | 0.989 |
| student_group | C_twin | gradient_boosting | 602 | 196 | 1.680 | 2.265 | 0.988 |
| temporal_forward | C_twin | linear_regression | 258 | 112 | 2.396 | 2.937 | 0.980 |
| temporal_forward | C_twin | random_forest | 258 | 112 | 2.660 | 3.234 | 0.976 |
| temporal_forward | C_twin | gradient_boosting | 258 | 112 | 2.598 | 3.255 | 0.975 |

## Headline comparison: do Digital Twin features help?

Best metric per (target, split, feature set), aggregated across models.

| task | split | feature set | metric | best value |
| --- | --- | --- | --- | ---: |
| classification | student_group | A_simple | f1 | 1.000 |
| classification | student_group | B_lms | f1 | 1.000 |
| classification | student_group | C_twin | f1 | 1.000 |
| classification | temporal_forward | A_simple | f1 | 1.000 |
| classification | temporal_forward | B_lms | f1 | 1.000 |
| classification | temporal_forward | C_twin | f1 | 1.000 |
| regression | student_group | A_simple | rmse | 2.673 |
| regression | student_group | B_lms | rmse | 2.101 |
| regression | student_group | C_twin | rmse | 2.149 |
| regression | temporal_forward | A_simple | rmse | 2.210 |
| regression | temporal_forward | B_lms | rmse | 2.270 |
| regression | temporal_forward | C_twin | rmse | 2.937 |

