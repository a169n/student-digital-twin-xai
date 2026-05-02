# Experiment result summary: `exp_002_twin_ablation`

This report compares the configured feature sets (`B_lms`, `B_lms_plus_indices`, `B_lms_plus_mastery`, `B_lms_plus_temporal`, `B_lms_plus_trends`, `B_lms_plus_trends_mastery`, `C_twin_full`) for the dissertation's current experimental targets: `final_grade` (regression) and, when configured, `passed` (classification). The teacher-facing heuristic `risk_level` is intentionally NOT used as a supervised target.

## Run metadata

- **snapshots_path**: C:\Users\a1byn\Desktop\dev\aitu\student-digital-twin-xai\data\processed\student_twin_snapshots.csv
- **final_results_path**: C:\Users\a1byn\Desktop\dev\aitu\student-digital-twin-xai\data\raw\final_results.csv
- **snapshot_week_min**: 4
- **snapshot_week_max**: 10
- **n_modeling_rows**: 798
- **n_modeling_students**: 114
- **feature_sets**: [{'name': 'B_lms', 'description': 'Stronger non-twin LMS baseline. Adds broader behavioral and submission-discipline signals that a typical LMS analytics view could plausibly expose without any digital-twin engineering.', 'columns': ['avg_assignment_score_to_date', 'avg_quiz_score_to_date', 'attendance_rate_to_date', 'activity_score_to_date', 'time_spent_to_date', 'on_time_submission_rate_to_date', 'missed_assignments_to_date', 'late_submissions_to_date', 'avg_attempt_count_to_date'], 'indicator_columns': ['has_assignment_score_to_date', 'has_quiz_score_to_date']}, {'name': 'B_lms_plus_trends', 'description': 'LMS baseline plus short-horizon trend features. Tests whether recent direction of performance, activity, and attendance adds predictive value beyond cumulative LMS indicators.', 'columns': ['avg_assignment_score_to_date', 'avg_quiz_score_to_date', 'attendance_rate_to_date', 'activity_score_to_date', 'time_spent_to_date', 'on_time_submission_rate_to_date', 'missed_assignments_to_date', 'late_submissions_to_date', 'avg_attempt_count_to_date', 'score_trend_3w', 'activity_trend_3w', 'attendance_trend_3w'], 'indicator_columns': ['has_assignment_score_to_date', 'has_quiz_score_to_date']}, {'name': 'B_lms_plus_mastery', 'description': 'LMS baseline plus current and overall mastery proxies. Tests whether topic-level Twin state adds value beyond raw performance and activity.', 'columns': ['avg_assignment_score_to_date', 'avg_quiz_score_to_date', 'attendance_rate_to_date', 'activity_score_to_date', 'time_spent_to_date', 'on_time_submission_rate_to_date', 'missed_assignments_to_date', 'late_submissions_to_date', 'avg_attempt_count_to_date', 'current_topic_mastery', 'overall_mastery'], 'indicator_columns': ['has_assignment_score_to_date', 'has_quiz_score_to_date']}, {'name': 'B_lms_plus_indices', 'description': 'LMS baseline plus composite engagement, performance, and discipline indices. Tests whether the current index layer adds compact value or mostly duplicates the underlying LMS signals.', 'columns': ['avg_assignment_score_to_date', 'avg_quiz_score_to_date', 'attendance_rate_to_date', 'activity_score_to_date', 'time_spent_to_date', 'on_time_submission_rate_to_date', 'missed_assignments_to_date', 'late_submissions_to_date', 'avg_attempt_count_to_date', 'engagement_index', 'performance_index', 'discipline_index'], 'indicator_columns': ['has_assignment_score_to_date', 'has_quiz_score_to_date']}, {'name': 'B_lms_plus_temporal', 'description': 'LMS baseline plus the snapshot week number. Tests whether coarse course-time context explains gains separately from richer trend or mastery features.', 'columns': ['avg_assignment_score_to_date', 'avg_quiz_score_to_date', 'attendance_rate_to_date', 'activity_score_to_date', 'time_spent_to_date', 'on_time_submission_rate_to_date', 'missed_assignments_to_date', 'late_submissions_to_date', 'avg_attempt_count_to_date', 'week_number'], 'indicator_columns': ['has_assignment_score_to_date', 'has_quiz_score_to_date']}, {'name': 'B_lms_plus_trends_mastery', 'description': 'Compact Twin candidate combining the LMS baseline with trend and mastery blocks while excluding composite indices. Intended as a lean candidate for the later XAI phase if it is competitive with the full Twin set.', 'columns': ['avg_assignment_score_to_date', 'avg_quiz_score_to_date', 'attendance_rate_to_date', 'activity_score_to_date', 'time_spent_to_date', 'on_time_submission_rate_to_date', 'missed_assignments_to_date', 'late_submissions_to_date', 'avg_attempt_count_to_date', 'score_trend_3w', 'activity_trend_3w', 'attendance_trend_3w', 'current_topic_mastery', 'overall_mastery'], 'indicator_columns': ['has_assignment_score_to_date', 'has_quiz_score_to_date']}, {'name': 'C_twin_full', 'description': 'Alias for the full Digital Twin representation used in ablation reports. Kept separate from `C_twin` naming so the baseline and ablation experiment pages can be cited cleanly.', 'columns': ['avg_assignment_score_to_date', 'avg_quiz_score_to_date', 'attendance_rate_to_date', 'activity_score_to_date', 'time_spent_to_date', 'on_time_submission_rate_to_date', 'missed_assignments_to_date', 'late_submissions_to_date', 'avg_attempt_count_to_date', 'score_trend_3w', 'activity_trend_3w', 'attendance_trend_3w', 'current_topic_mastery', 'overall_mastery', 'engagement_index', 'performance_index', 'discipline_index', 'week_number'], 'indicator_columns': ['has_assignment_score_to_date', 'has_quiz_score_to_date']}]
- **split_strategies**: ['student_group', 'temporal_forward']

## Classification results — target `passed`

| split | feature set | model | n_train | n_test | accuracy | precision | recall | f1 | roc_auc |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| student_group | B_lms | logistic_regression | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms | random_forest | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms | gradient_boosting | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms | logistic_regression | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms | random_forest | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms | gradient_boosting | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_trends | logistic_regression | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_trends | random_forest | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_trends | gradient_boosting | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_trends | logistic_regression | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_trends | random_forest | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_trends | gradient_boosting | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_mastery | logistic_regression | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_mastery | random_forest | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_mastery | gradient_boosting | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_mastery | logistic_regression | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_mastery | random_forest | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_mastery | gradient_boosting | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_indices | logistic_regression | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_indices | random_forest | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_indices | gradient_boosting | 602 | 196 | 0.995 | 0.993 | 1.000 | 0.996 | 1.000 |
| temporal_forward | B_lms_plus_indices | logistic_regression | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_indices | random_forest | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_indices | gradient_boosting | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_temporal | logistic_regression | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_temporal | random_forest | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_temporal | gradient_boosting | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_temporal | logistic_regression | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_temporal | random_forest | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_temporal | gradient_boosting | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_trends_mastery | logistic_regression | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_trends_mastery | random_forest | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_trends_mastery | gradient_boosting | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_trends_mastery | logistic_regression | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_trends_mastery | random_forest | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_trends_mastery | gradient_boosting | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | C_twin_full | logistic_regression | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | C_twin_full | random_forest | 602 | 196 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| student_group | C_twin_full | gradient_boosting | 602 | 196 | 0.995 | 0.993 | 1.000 | 0.996 | 1.000 |
| temporal_forward | C_twin_full | logistic_regression | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | C_twin_full | random_forest | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| temporal_forward | C_twin_full | gradient_boosting | 258 | 112 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

## Regression results — target `final_grade`

| split | feature set | model | n_train | n_test | MAE | RMSE | R^2 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| student_group | B_lms | linear_regression | 602 | 196 | 2.155 | 2.845 | 0.981 |
| student_group | B_lms | random_forest | 602 | 196 | 1.807 | 2.296 | 0.988 |
| student_group | B_lms | gradient_boosting | 602 | 196 | 1.681 | 2.101 | 0.990 |
| temporal_forward | B_lms | linear_regression | 258 | 112 | 1.778 | 2.270 | 0.988 |
| temporal_forward | B_lms | random_forest | 258 | 112 | 2.813 | 3.474 | 0.972 |
| temporal_forward | B_lms | gradient_boosting | 258 | 112 | 2.499 | 3.160 | 0.977 |
| student_group | B_lms_plus_trends | linear_regression | 602 | 196 | 2.069 | 2.718 | 0.983 |
| student_group | B_lms_plus_trends | random_forest | 602 | 196 | 1.803 | 2.303 | 0.988 |
| student_group | B_lms_plus_trends | gradient_boosting | 602 | 196 | 1.672 | 2.096 | 0.990 |
| temporal_forward | B_lms_plus_trends | linear_regression | 258 | 112 | 1.997 | 2.531 | 0.985 |
| temporal_forward | B_lms_plus_trends | random_forest | 258 | 112 | 2.882 | 3.587 | 0.970 |
| temporal_forward | B_lms_plus_trends | gradient_boosting | 258 | 112 | 2.606 | 3.310 | 0.975 |
| student_group | B_lms_plus_mastery | linear_regression | 602 | 196 | 2.052 | 2.756 | 0.982 |
| student_group | B_lms_plus_mastery | random_forest | 602 | 196 | 1.643 | 2.045 | 0.990 |
| student_group | B_lms_plus_mastery | gradient_boosting | 602 | 196 | 1.510 | 1.894 | 0.992 |
| temporal_forward | B_lms_plus_mastery | linear_regression | 258 | 112 | 1.776 | 2.276 | 0.988 |
| temporal_forward | B_lms_plus_mastery | random_forest | 258 | 112 | 2.744 | 3.364 | 0.974 |
| temporal_forward | B_lms_plus_mastery | gradient_boosting | 258 | 112 | 2.835 | 3.574 | 0.970 |
| student_group | B_lms_plus_indices | linear_regression | 602 | 196 | 2.122 | 2.812 | 0.982 |
| student_group | B_lms_plus_indices | random_forest | 602 | 196 | 1.759 | 2.232 | 0.988 |
| student_group | B_lms_plus_indices | gradient_boosting | 602 | 196 | 1.567 | 2.035 | 0.990 |
| temporal_forward | B_lms_plus_indices | linear_regression | 258 | 112 | 1.732 | 2.202 | 0.989 |
| temporal_forward | B_lms_plus_indices | random_forest | 258 | 112 | 2.580 | 3.150 | 0.977 |
| temporal_forward | B_lms_plus_indices | gradient_boosting | 258 | 112 | 2.399 | 2.952 | 0.980 |
| student_group | B_lms_plus_temporal | linear_regression | 602 | 196 | 2.162 | 2.851 | 0.981 |
| student_group | B_lms_plus_temporal | random_forest | 602 | 196 | 1.806 | 2.300 | 0.988 |
| student_group | B_lms_plus_temporal | gradient_boosting | 602 | 196 | 1.657 | 2.078 | 0.990 |
| temporal_forward | B_lms_plus_temporal | linear_regression | 258 | 112 | 2.166 | 2.658 | 0.984 |
| temporal_forward | B_lms_plus_temporal | random_forest | 258 | 112 | 2.785 | 3.449 | 0.972 |
| temporal_forward | B_lms_plus_temporal | gradient_boosting | 258 | 112 | 2.487 | 3.141 | 0.977 |
| student_group | B_lms_plus_trends_mastery | linear_regression | 602 | 196 | 2.024 | 2.695 | 0.983 |
| student_group | B_lms_plus_trends_mastery | random_forest | 602 | 196 | 1.638 | 2.042 | 0.990 |
| student_group | B_lms_plus_trends_mastery | gradient_boosting | 602 | 196 | 1.573 | 1.973 | 0.991 |
| temporal_forward | B_lms_plus_trends_mastery | linear_regression | 258 | 112 | 2.024 | 2.555 | 0.985 |
| temporal_forward | B_lms_plus_trends_mastery | random_forest | 258 | 112 | 2.793 | 3.445 | 0.972 |
| temporal_forward | B_lms_plus_trends_mastery | gradient_boosting | 258 | 112 | 2.767 | 3.442 | 0.972 |
| student_group | C_twin_full | linear_regression | 602 | 196 | 2.037 | 2.698 | 0.983 |
| student_group | C_twin_full | random_forest | 602 | 196 | 1.732 | 2.149 | 0.989 |
| student_group | C_twin_full | gradient_boosting | 602 | 196 | 1.680 | 2.265 | 0.988 |
| temporal_forward | C_twin_full | linear_regression | 258 | 112 | 2.396 | 2.937 | 0.980 |
| temporal_forward | C_twin_full | random_forest | 258 | 112 | 2.660 | 3.234 | 0.976 |
| temporal_forward | C_twin_full | gradient_boosting | 258 | 112 | 2.598 | 3.255 | 0.975 |

## Headline comparison: do Digital Twin features help?

Best metric per (target, split, feature set), aggregated across models.

| task | split | feature set | metric | best value |
| --- | --- | --- | --- | ---: |
| classification | student_group | B_lms | f1 | 1.000 |
| classification | student_group | B_lms_plus_indices | f1 | 1.000 |
| classification | student_group | B_lms_plus_mastery | f1 | 1.000 |
| classification | student_group | B_lms_plus_temporal | f1 | 1.000 |
| classification | student_group | B_lms_plus_trends | f1 | 1.000 |
| classification | student_group | B_lms_plus_trends_mastery | f1 | 1.000 |
| classification | student_group | C_twin_full | f1 | 1.000 |
| classification | temporal_forward | B_lms | f1 | 1.000 |
| classification | temporal_forward | B_lms_plus_indices | f1 | 1.000 |
| classification | temporal_forward | B_lms_plus_mastery | f1 | 1.000 |
| classification | temporal_forward | B_lms_plus_temporal | f1 | 1.000 |
| classification | temporal_forward | B_lms_plus_trends | f1 | 1.000 |
| classification | temporal_forward | B_lms_plus_trends_mastery | f1 | 1.000 |
| classification | temporal_forward | C_twin_full | f1 | 1.000 |
| regression | student_group | B_lms | rmse | 2.101 |
| regression | student_group | B_lms_plus_indices | rmse | 2.035 |
| regression | student_group | B_lms_plus_mastery | rmse | 1.894 |
| regression | student_group | B_lms_plus_temporal | rmse | 2.078 |
| regression | student_group | B_lms_plus_trends | rmse | 2.096 |
| regression | student_group | B_lms_plus_trends_mastery | rmse | 1.973 |
| regression | student_group | C_twin_full | rmse | 2.149 |
| regression | temporal_forward | B_lms | rmse | 2.270 |
| regression | temporal_forward | B_lms_plus_indices | rmse | 2.202 |
| regression | temporal_forward | B_lms_plus_mastery | rmse | 2.276 |
| regression | temporal_forward | B_lms_plus_temporal | rmse | 2.658 |
| regression | temporal_forward | B_lms_plus_trends | rmse | 2.531 |
| regression | temporal_forward | B_lms_plus_trends_mastery | rmse | 2.555 |
| regression | temporal_forward | C_twin_full | rmse | 2.937 |

