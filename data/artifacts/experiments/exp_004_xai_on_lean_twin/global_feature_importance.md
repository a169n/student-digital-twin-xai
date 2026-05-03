# Global feature importance

Importance is computed on the held-out student-group split. Positive
`mean_rmse_increase` values indicate that permuting the feature hurt
the model. Shares are normalized over positive permutation importance
when available.

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
| B_lms_plus_mastery | 1 | activity_score_to_date | 16.288 | 0.648 | higher values generally align with higher predicted final_grade |
| B_lms_plus_mastery | 2 | overall_mastery | 4.489 | 0.178 | higher values generally align with higher predicted final_grade |
| B_lms_plus_mastery | 3 | avg_assignment_score_to_date | 2.272 | 0.090 | higher values generally align with higher predicted final_grade |
| B_lms_plus_mastery | 4 | time_spent_to_date | 0.550 | 0.022 | higher values generally align with higher predicted final_grade |
| B_lms_plus_mastery | 5 | on_time_submission_rate_to_date | 0.548 | 0.022 | higher values generally align with higher predicted final_grade |
| B_lms_plus_mastery | 6 | attendance_rate_to_date | 0.427 | 0.017 | higher values generally align with higher predicted final_grade |
| B_lms_plus_mastery | 7 | avg_quiz_score_to_date | 0.403 | 0.016 | higher values generally align with higher predicted final_grade |
| B_lms_plus_mastery | 8 | current_topic_mastery | 0.076 | 0.003 | higher values generally align with higher predicted final_grade |
