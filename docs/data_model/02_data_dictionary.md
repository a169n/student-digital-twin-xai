# Data Dictionary

This document summarizes the most important v1.2 fields in human-readable form. It is not meant to repeat every trivial identifier field, but it should cover the fields that define meaning, modeling intent, and visibility boundaries.

The main sections below describe fields that are part of `schema_v1.2`. A final section lists research-backed candidate fields that are still outside the locked contract.

## Classification Legend

- `raw`: observed LMS-like data.
- `derived`: computed from raw data or aggregation logic.
- `generation-only`: used to create synthetic realism, not intended for teacher-facing use.
- `target`: used as a prediction label or outcome.
- `heuristic-label`: teacher-facing label derived from a heuristic rule or score, not ML ground truth.

## `students`

| Field | Meaning | Type | Example | Class | Visibility | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `student_id` | Internal unique identifier | string | `student_001` | raw | internal | Stable join key across tables |
| `student_code` | Teacher-visible pseudonymous label | string | `STU-001` | raw | user-facing | Prefer this over real names in v1 |
| `course_id` | The student’s active v1 course | string | `course_prog_101` | raw | internal | v1 simplification instead of an enrollments table |
| `enrollment_status` | Current synthetic enrollment state | enum | `active` | raw | internal | Allowed values: `active`, `withdrawn`, `completed` |
| `baseline_level` | Hidden starting academic capability parameter | decimal | `0.72` | generation-only | internal | Range `0.0..1.0` |
| `motivation_level` | Hidden engagement/effort parameter | decimal | `0.61` | generation-only | internal | Range `0.0..1.0` |
| `discipline_level` | Hidden punctuality/reliability parameter | decimal | `0.55` | generation-only | internal | Range `0.0..1.0` |
| `trajectory_type` | Hidden behavioral trajectory archetype | enum | `declining` | generation-only | internal | v1.2 keeps `improving` and `consistently_at_risk`; in generator logic they correspond to recovering and chronic-risk patterns |

## `courses`

| Field | Meaning | Type | Example | Class | Visibility | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `course_id` | Unique course identifier | string | `course_prog_101` | raw | internal | Primary key |
| `course_code` | Human-readable course code | string | `CS101` | raw | user-facing | Teacher-friendly label |
| `course_name` | Course title | string | `Introduction to Programming` | raw | user-facing | Main course label |
| `duration_weeks` | Planned course duration | integer | `10` | raw | user-facing | Expected to be 10 in v1 |
| `grading_policy_pass_mark` | Numeric pass threshold | decimal | `50` | raw | internal | Used to derive `passed` |

## `course_topics`

| Field | Meaning | Type | Example | Class | Visibility | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `topic_id` | Unique topic identifier | string | `topic_w03` | raw | internal | Primary key |
| `week_number` | Instructional week number | integer | `3` | raw | user-facing | Range `1..10` |
| `topic_title` | Topic taught in the week | string | `Loops and Iteration` | raw | user-facing | Teacher-facing topic label |
| `topic_type` | Optional topic classification | enum | `lab` | raw | internal | Optional planning metadata |
| `planned_assignment_count` | Planned workload hint for generation | integer | `2` | raw | internal | Optional and still provisional |
| `topic_difficulty` | Normalized topic difficulty signal | decimal | `0.58` | raw | internal | Included in v1.2 as limited non-sensitive course context |

## `assignments`

| Field | Meaning | Type | Example | Class | Visibility | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `assignment_id` | Unique assessment identifier | string | `asg_w03_q1` | raw | internal | Primary key |
| `assignment_type` | Assessment category | enum | `quiz` | raw | user-facing | Initial v1 values: `assignment`, `quiz`, `lab` |
| `title` | Assessment title | string | `Quiz 3: Loops` | raw | user-facing | Teacher-facing |
| `max_score` | Maximum points available | decimal | `100` | raw | internal | Used to normalize performance later |
| `due_at` | Submission deadline | datetime | `2026-09-20T23:59:00` | raw | internal | Important for punctuality features |
| `weight_percent` | Grade contribution | decimal | `5` | raw | internal | Optional in v1 |
| `is_required` | Whether the item is required | boolean | `true` | raw | internal | Used when counting missed work |

## `attendance`

| Field | Meaning | Type | Example | Class | Visibility | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `attendance_id` | Unique attendance record | string | `att_001003` | raw | internal | Primary key |
| `week_number` | Week of the session | integer | `3` | raw | user-facing | Matches the course timeline |
| `session_date` | Scheduled session date | date | `2026-09-18` | raw | internal | Raw time anchor |
| `session_type` | Session subtype | enum | `lecture` | raw | internal | Optional |
| `attendance_status` | Observed attendance outcome | enum | `late` | raw | user-facing | Initial values: `present`, `late`, `absent`, `excused` |

## `submissions`

| Field | Meaning | Type | Example | Class | Visibility | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `submission_id` | Unique submission record | string | `sub_001_asg_w03_q1` | raw | internal | Primary key |
| `submitted_at` | Timestamp of student submission | datetime | `2026-09-20T22:41:00` | raw | internal | Can be null for missing work |
| `submission_status` | Recorded submission outcome | enum | `late` | raw | user-facing | Values: `submitted`, `late`, `missing`, `excused` |
| `score` | Points awarded | decimal | `74` | raw | user-facing | Interpreted against `assignments.max_score` |
| `is_on_time` | Convenience punctuality flag | boolean | `false` | derived | internal | Derived from due date and submission time |
| `attempt_count` | Number of recorded attempts | integer | `1` | raw | internal | Optional in v1 |

## `weekly_activity`

| Field | Meaning | Type | Example | Class | Visibility | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `weekly_activity_id` | Unique weekly activity record | string | `act_001_w03` | raw | internal | Primary key |
| `week_number` | Activity week | integer | `3` | raw | user-facing | One row per student x week |
| `login_count` | LMS login count for the week | integer | `6` | raw | internal | Non-negative |
| `active_days` | Distinct active days during the week | integer | `4` | raw | internal | Range `0..7` |
| `content_views` | Course material views | integer | `18` | raw | internal | Non-negative |
| `practice_events` | Practice or coding events | integer | `9` | raw | internal | Non-negative |
| `time_on_platform_minutes` | Approximate active time | decimal | `142` | raw | internal | Non-negative |
| `activity_score` | Normalized weekly activity summary | decimal | `67.5` | derived | internal | Provisional v1 formula |

## `final_results`

| Field | Meaning | Type | Example | Class | Visibility | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `completion_status` | Resolved course completion outcome | enum | `completed` | raw | user-facing | Values: `completed`, `withdrawn`, `incomplete` |
| `final_grade` | Final numeric course grade | decimal | `78.4` | target | user-facing | Primary regression target for ML experiments |
| `passed` | Final pass/fail indicator | boolean | `true` | derived | user-facing | Derived from `final_grade` and pass policy; primary classification target for ML experiments |
| `completed_weeks` | Weeks meaningfully completed | integer | `10` | derived | internal | Useful for analysis and withdrawals |

## `student_twin_snapshots`

| Field | Meaning | Type | Example | Class | Visibility | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `snapshot_id` | Unique weekly twin snapshot | string | `snap_001_w03` | raw | internal | Primary key |
| `week_number` | Snapshot week | integer | `3` | raw | user-facing | Canonical time axis |
| `snapshot_date` | End date of the observation window | date | `2026-09-21` | raw | internal | Must reflect data available only up to that point |
| `attendance_rate_to_date` | Cumulative attendance rate | decimal | `0.83` | derived | user-facing | Range `0.0..1.0` |
| `avg_assignment_score_to_date` | Average assignment score so far | decimal | `76.2` | derived | user-facing | Based on assignment-type items |
| `avg_quiz_score_to_date` | Average quiz score so far | decimal | `71.0` | derived | user-facing | Based on quiz-type items |
| `on_time_submission_rate_to_date` | Share of required work submitted on time | decimal | `0.67` | derived | user-facing | Range `0.0..1.0` |
| `missed_assignments_to_date` | Count of required missed items | integer | `1` | derived | user-facing | Non-negative |
| `late_submissions_to_date` | Count of late submissions | integer | `2` | derived | user-facing | Non-negative |
| `has_assignment_score_to_date` | Whether at least one assignment score exists by the snapshot week | boolean | `false` | derived | internal | Added in v1.2 to distinguish “not yet observed” from data error |
| `has_quiz_score_to_date` | Whether at least one quiz score exists by the snapshot week | boolean | `true` | derived | internal | Added in v1.2 as an explicit missing-data indicator |
| `avg_attempt_count_to_date` | Mean number of attempts on due assessments so far | decimal | `1.25` | derived | user-facing | Reflects work persistence across due assessments |
| `activity_score_to_date` | Cumulative activity summary | decimal | `64.8` | derived | user-facing | Range `0..100` |
| `time_spent_to_date` | Total time spent on the platform to date | decimal | `426.5` | derived | user-facing | Minutes accumulated through the snapshot week |
| `score_trend_3w` | Short-horizon performance direction | decimal | `-0.12` | derived | user-facing | Negative means decline; scaling is provisional |
| `activity_trend_3w` | Short-horizon activity direction | decimal | `-0.20` | derived | user-facing | Negative means reduced engagement |
| `attendance_trend_3w` | Short-horizon attendance direction | decimal | `0.05` | derived | user-facing | Positive means improvement |
| `current_topic_mastery` | Topic-specific mastery proxy for the current week | decimal | `69.4` | derived | user-facing | Teacher-readable mastery signal |
| `overall_mastery` | Cumulative mastery proxy across covered topics | decimal | `71.8` | derived | user-facing | Running mastery estimate across covered material |
| `engagement_index` | Composite engagement indicator | decimal | `62.3` | derived | user-facing | Interpretable summary index |
| `performance_index` | Composite performance indicator | decimal | `73.6` | derived | user-facing | Interpretable summary index |
| `discipline_index` | Composite reliability indicator | decimal | `58.4` | derived | user-facing | Interpretable summary index |
| `risk_score` | Internal continuous heuristic risk score | decimal | `0.68` | derived | internal | Maps to `risk_level`; recalibrated in v1.2 |
| `risk_level` | Weekly teacher-facing risk label | enum | `high` | heuristic-label | user-facing | Values: `low`, `medium`, `high`; not ML ground truth in v1.2 |
| `predicted_final_grade` | Provisional end-of-course estimate available at the snapshot week | decimal | `74.9` | derived | user-facing | Snapshot estimate, not the realized final target |

## Interpretation Notes

- Hidden generation-only fields exist to support realistic synthetic data generation, not to define the teacher-facing domain.
- `risk_level` is weekly, belongs to the digital twin layer, and should be treated as a teacher-facing heuristic label rather than an ML ground-truth target.
- `final_grade` and `passed` are end-of-course outcomes and belong to the outcome layer used for later supervised experiments.
- If future versions rename or reinterpret any field here, the schema contract and changelog must be updated first.

## Research-Backed Candidate Fields Still Outside the Locked Contract

These fields are intentionally not part of `schema_v1.2` yet. They are listed here because the literature review suggests they are good candidates for future refinement once the first synthetic generator is working.

| Candidate field | Intended location | Meaning | Why it may matter |
| --- | --- | --- | --- |
| `due_load` | `course_topics` or derived snapshot context | Number or normalized weight of items due in a given week | Helps interpret performance dips under heavier workload weeks |

These fields should be added only through a versioned schema update if they remain optional and non-breaking.
