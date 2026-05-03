# Local case explanations

Local contributions are one-feature perturbation effects against the
training median. They are directional model-behavior summaries, not
causal attributions.

## strong_performer - student_054 week 10

- Selection rule: latest held-out snapshot with the highest actual final_grade
- Predicted final_grade: `90.300`
- Actual final_grade: `93.140`
- Prediction error: `-2.840`
- Baseline predicted final_grade: `90.642`
- Mastery contribution share: `0.343`
- Assessment: teacher-meaningful with mastery as part of the student-state story

| rank | lean feature | contribution | direction |
| ---: | --- | ---: | --- |
| 1 | overall_mastery | +8.567 | raises_prediction |
| 2 | activity_score_to_date | +7.295 | raises_prediction |
| 3 | avg_quiz_score_to_date | +3.586 | raises_prediction |
| 4 | avg_assignment_score_to_date | +3.383 | raises_prediction |
| 5 | on_time_submission_rate_to_date | +2.093 | raises_prediction |
| 6 | time_spent_to_date | +0.790 | raises_prediction |

Baseline top contributors:

| rank | baseline feature | contribution | direction |
| ---: | --- | ---: | --- |
| 1 | activity_score_to_date | +9.770 | raises_prediction |
| 2 | avg_assignment_score_to_date | +8.266 | raises_prediction |
| 3 | avg_quiz_score_to_date | +7.150 | raises_prediction |
| 4 | on_time_submission_rate_to_date | +1.740 | raises_prediction |
| 5 | time_spent_to_date | +0.971 | raises_prediction |
| 6 | attendance_rate_to_date | -0.273 | lowers_prediction |

## at_risk - student_115 week 10

- Selection rule: latest held-out snapshot with the lowest actual final_grade
- Predicted final_grade: `23.265`
- Actual final_grade: `22.450`
- Prediction error: `+0.815`
- Baseline predicted final_grade: `23.354`
- Mastery contribution share: `0.213`
- Assessment: teacher-meaningful with mastery as part of the student-state story

| rank | lean feature | contribution | direction |
| ---: | --- | ---: | --- |
| 1 | activity_score_to_date | -30.720 | lowers_prediction |
| 2 | overall_mastery | -8.347 | lowers_prediction |
| 3 | attendance_rate_to_date | -3.546 | lowers_prediction |
| 4 | current_topic_mastery | -1.810 | lowers_prediction |
| 5 | on_time_submission_rate_to_date | -1.651 | lowers_prediction |
| 6 | avg_assignment_score_to_date | -0.822 | lowers_prediction |

Baseline top contributors:

| rank | baseline feature | contribution | direction |
| ---: | --- | ---: | --- |
| 1 | activity_score_to_date | -28.758 | lowers_prediction |
| 2 | avg_quiz_score_to_date | -4.253 | lowers_prediction |
| 3 | attendance_rate_to_date | -3.982 | lowers_prediction |
| 4 | avg_assignment_score_to_date | -2.037 | lowers_prediction |
| 5 | on_time_submission_rate_to_date | -1.444 | lowers_prediction |
| 6 | late_submissions_to_date | -0.667 | lowers_prediction |

## improving_trajectory - student_112 week 5

- Selection rule: held-out snapshot with the strongest positive score_trend_3w
- Predicted final_grade: `59.734`
- Actual final_grade: `61.870`
- Prediction error: `-2.136`
- Baseline predicted final_grade: `59.560`
- Mastery contribution share: `0.019`
- Assessment: teacher-meaningful and mostly LMS-behavior/performance driven

| rank | lean feature | contribution | direction |
| ---: | --- | ---: | --- |
| 1 | avg_assignment_score_to_date | -4.853 | lowers_prediction |
| 2 | activity_score_to_date | -0.615 | lowers_prediction |
| 3 | attendance_rate_to_date | -0.610 | lowers_prediction |
| 4 | avg_attempt_count_to_date | -0.562 | lowers_prediction |
| 5 | late_submissions_to_date | -0.423 | lowers_prediction |
| 6 | time_spent_to_date | +0.369 | raises_prediction |

Baseline top contributors:

| rank | baseline feature | contribution | direction |
| ---: | --- | ---: | --- |
| 1 | avg_assignment_score_to_date | -5.700 | lowers_prediction |
| 2 | attendance_rate_to_date | -0.732 | lowers_prediction |
| 3 | avg_attempt_count_to_date | -0.619 | lowers_prediction |
| 4 | activity_score_to_date | -0.572 | lowers_prediction |
| 5 | late_submissions_to_date | -0.485 | lowers_prediction |
| 6 | missed_assignments_to_date | +0.338 | raises_prediction |

## declining_trajectory - student_027 week 5

- Selection rule: held-out snapshot with the strongest negative score_trend_3w
- Predicted final_grade: `33.235`
- Actual final_grade: `29.950`
- Prediction error: `+3.285`
- Baseline predicted final_grade: `33.345`
- Mastery contribution share: `0.203`
- Assessment: teacher-meaningful with mastery as part of the student-state story

| rank | lean feature | contribution | direction |
| ---: | --- | ---: | --- |
| 1 | activity_score_to_date | -23.472 | lowers_prediction |
| 2 | overall_mastery | -6.070 | lowers_prediction |
| 3 | avg_assignment_score_to_date | -2.424 | lowers_prediction |
| 4 | current_topic_mastery | -1.305 | lowers_prediction |
| 5 | attendance_rate_to_date | -1.166 | lowers_prediction |
| 6 | on_time_submission_rate_to_date | -0.942 | lowers_prediction |

Baseline top contributors:

| rank | baseline feature | contribution | direction |
| ---: | --- | ---: | --- |
| 1 | activity_score_to_date | -22.344 | lowers_prediction |
| 2 | avg_assignment_score_to_date | -3.544 | lowers_prediction |
| 3 | avg_quiz_score_to_date | -2.076 | lowers_prediction |
| 4 | on_time_submission_rate_to_date | -1.835 | lowers_prediction |
| 5 | attendance_rate_to_date | -1.020 | lowers_prediction |
| 6 | time_spent_to_date | +0.382 | raises_prediction |

## borderline_medium - student_020 week 10

- Selection rule: latest held-out snapshot closest to the configured borderline grade, preferring medium risk_level when available
- Predicted final_grade: `56.479`
- Actual final_grade: `53.940`
- Prediction error: `+2.539`
- Baseline predicted final_grade: `55.639`
- Mastery contribution share: `0.194`
- Assessment: teacher-meaningful with mastery as part of the student-state story

| rank | lean feature | contribution | direction |
| ---: | --- | ---: | --- |
| 1 | avg_assignment_score_to_date | -5.494 | lowers_prediction |
| 2 | activity_score_to_date | -3.010 | lowers_prediction |
| 3 | overall_mastery | -2.882 | lowers_prediction |
| 4 | on_time_submission_rate_to_date | -1.244 | lowers_prediction |
| 5 | avg_quiz_score_to_date | -0.841 | lowers_prediction |
| 6 | missed_assignments_to_date | -0.614 | lowers_prediction |

Baseline top contributors:

| rank | baseline feature | contribution | direction |
| ---: | --- | ---: | --- |
| 1 | avg_assignment_score_to_date | -7.040 | lowers_prediction |
| 2 | avg_quiz_score_to_date | -3.338 | lowers_prediction |
| 3 | on_time_submission_rate_to_date | -2.199 | lowers_prediction |
| 4 | activity_score_to_date | -1.700 | lowers_prediction |
| 5 | late_submissions_to_date | -1.075 | lowers_prediction |
| 6 | attendance_rate_to_date | -0.550 | lowers_prediction |
