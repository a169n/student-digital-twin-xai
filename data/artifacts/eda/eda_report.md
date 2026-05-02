# Modeling-readiness EDA report

This report summarizes the refined v1.3 dataset from the perspective of building leakage-safe baselines for `final_grade` (regression) and `passed` (classification). It is not a generic descriptive dump.

## Dataset shape

- Modeling rows: **798**
- Distinct students: **114**
- Weeks present: [4, 5, 6, 7, 8, 9, 10]

## Target distributions

- `final_grade` mean: **62.411**, std: **20.617**
- `passed` positive rate: **0.781**

## Top correlations with `final_grade`

Sorted by absolute Pearson correlation. High absolute values close to 1.0 for snapshot features hint at signal that may be too deterministic; the twin-target red flag list below makes the strong cases explicit.

| column                          | pearson |
| ------------------------------- | ------: |
| performance_index               |   0.986 |
| overall_mastery                 |   0.984 |
| activity_score_to_date          |   0.983 |
| avg_assignment_score_to_date    |   0.982 |
| avg_quiz_score_to_date          |   0.978 |
| engagement_index                |   0.971 |
| current_topic_mastery           |   0.935 |
| attendance_rate_to_date         |   0.915 |
| on_time_submission_rate_to_date |   0.884 |
| discipline_index                |   0.884 |
| time_spent_to_date              |   0.796 |
| avg_attempt_count_to_date       |   0.674 |

## Per-week target stability

Snapshot rows can come from any week. This table shows whether the target value seen in each week is similar enough to support training across weeks rather than per-week.

| week | n_rows | n_students | mean `final_grade` | `passed` rate |
| ---: | -----: | ---------: | -----------------: | ------------: |
|    4 |    114 |        114 |             62.411 |         0.781 |
|    5 |    114 |        114 |             62.411 |         0.781 |
|    6 |    114 |        114 |             62.411 |         0.781 |
|    7 |    114 |        114 |             62.411 |         0.781 |
|    8 |    114 |        114 |             62.411 |         0.781 |
|    9 |    114 |        114 |             62.411 |         0.781 |
|   10 |    114 |        114 |             62.411 |         0.781 |

## Redundancy / collinearity warnings

Pairs of twin features whose absolute Pearson correlation reaches `0.95` or higher.

| left                            | right                  |       | corr |     |
| ------------------------------- | ---------------------- | ----: | ---- | --- |
| avg_assignment_score_to_date    | avg_quiz_score_to_date | 0.976 |
| avg_assignment_score_to_date    | activity_score_to_date | 0.979 |
| avg_assignment_score_to_date    | overall_mastery        | 0.993 |
| avg_assignment_score_to_date    | engagement_index       | 0.959 |
| avg_assignment_score_to_date    | performance_index      | 0.996 |
| avg_quiz_score_to_date          | activity_score_to_date | 0.977 |
| avg_quiz_score_to_date          | overall_mastery        | 0.993 |
| avg_quiz_score_to_date          | engagement_index       | 0.962 |
| avg_quiz_score_to_date          | performance_index      | 0.991 |
| attendance_rate_to_date         | engagement_index       | 0.961 |
| activity_score_to_date          | overall_mastery        | 0.984 |
| activity_score_to_date          | engagement_index       | 0.978 |
| activity_score_to_date          | performance_index      | 0.984 |
| on_time_submission_rate_to_date | discipline_index       | 0.999 |
| overall_mastery                 | engagement_index       | 0.965 |
| overall_mastery                 | performance_index      | 0.999 |
| engagement_index                | performance_index      | 0.965 |

## Twin-target red flags

Snapshot features whose absolute correlation with `final_grade` reaches `0.97` or higher are listed here. They may be too deterministic and warrant ablation in later phases.

| column                       | pearson |
| ---------------------------- | ------: |
| performance_index            |   0.986 |
| overall_mastery              |   0.984 |
| activity_score_to_date       |   0.983 |
| avg_assignment_score_to_date |   0.982 |
| avg_quiz_score_to_date       |   0.978 |
| engagement_index             |   0.971 |

## Trajectory-type breakdown (generation-only context)

Aggregates joined from the hidden `trajectory_type` field to show that the modeling targets behave differently across the four synthetic trajectories. This field is NOT a feature; it is shown only to validate the generator.

| trajectory           | n_rows | n_students | mean `final_grade` | `passed` rate | mean `risk_score` |
| -------------------- | -----: | ---------: | -----------------: | ------------: | ----------------: |
| stable_high          |    182 |         26 |             87.778 |         1.000 |             0.150 |
| declining            |    231 |         33 |             69.364 |         1.000 |             0.273 |
| improving            |    210 |         30 |             60.885 |         1.000 |             0.378 |
| consistently_at_risk |    175 |         25 |             28.682 |         0.000 |             0.604 |

## Feature summary

Per-feature numeric summary (only top-level descriptive stats here; the full table is in `18` row CSV).

See `feature_summary.csv` next to this report for the full table.
