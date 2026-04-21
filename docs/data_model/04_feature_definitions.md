# Feature Definitions

This document describes the major v1 features used to represent the student digital twin. The emphasis is on clarity and interpretability, not on claiming that every formula is final.

## Feature Design Principles

- Features should be understandable to teachers.
- Features should be computable from the raw LMS-like layer.
- Features should respect temporal cutoffs.
- Composite indices are allowed in v1, but their components should remain explainable.
- Formulas in this document are working assumptions for the first stable schema, not final research conclusions.

## Core Snapshot Grain

All features below are defined for `student_twin_snapshots` with the grain:

- `1 row = 1 student x 1 week`

## Major Feature Families

### Attendance and participation

| Feature | Conceptual meaning | Provisional v1 definition | Notes |
| --- | --- | --- | --- |
| `attendance_rate_to_date` | How consistently the student has attended scheduled sessions so far | `present_or_late_sessions_to_date / scheduled_sessions_to_date` | `excused` handling should stay explicit in generator logic |
| `attendance_trend_3w` | Whether attendance is improving or deteriorating recently | Rolling short-horizon change or slope over the last up to 3 weeks | Exact scaling is provisional |

### Performance

| Feature | Conceptual meaning | Provisional v1 definition | Notes |
| --- | --- | --- | --- |
| `avg_assignment_score_to_date` | Average performance on assignment-type tasks so far | Mean normalized score for `assignment_type = assignment` items completed to date | Excludes future assignments |
| `avg_quiz_score_to_date` | Average quiz performance so far | Mean normalized score for `assignment_type = quiz` items completed to date | Nullable early in the course if no quiz exists yet |
| `score_trend_3w` | Recent direction of academic performance | Rolling short-horizon change or slope in recent score history | Negative values indicate decline |

### Submission discipline

| Feature | Conceptual meaning | Provisional v1 definition | Notes |
| --- | --- | --- | --- |
| `on_time_submission_rate_to_date` | How reliably required work is submitted on time | `on_time_required_submissions_to_date / required_items_due_to_date` | Core punctuality feature |
| `missed_assignments_to_date` | Total missed required workload so far | Count of required due items with `submission_status = missing` | Non-negative cumulative count |
| `late_submissions_to_date` | Total late work so far | Count of submissions marked `late` up to the snapshot week | Non-negative cumulative count |

### LMS engagement

| Feature | Conceptual meaning | Provisional v1 definition | Notes |
| --- | --- | --- | --- |
| `activity_score_to_date` | Overall level of LMS-related participation so far | Normalized aggregation of weekly activity through the snapshot week | Keeps raw counts interpretable while reducing dimensional noise |
| `activity_trend_3w` | Whether activity is increasing or fading | Rolling short-horizon change or slope over recent weekly activity | Negative values indicate declining engagement |

## Composite Indices

Composite indices are allowed in v1 because they can support teacher interpretation and later XAI summaries, but they should stay transparent enough to explain.

| Feature | Intended interpretation | Provisional v1 construction idea | Notes |
| --- | --- | --- | --- |
| `engagement_index` | Overall course engagement | Weighted combination of attendance participation and LMS activity | Example inputs: attendance rate, activity score, active days |
| `performance_index` | Overall academic performance state | Weighted combination of assignment and quiz results | Example inputs: assignment average, quiz average, score trend |
| `discipline_index` | Reliability and submission discipline | Weighted combination of on-time rate with penalties for missed and late work | Helps explain risk from behavior rather than score alone |

## Risk-Oriented Fields

| Feature | Intended interpretation | Provisional v1 construction idea | Notes |
| --- | --- | --- | --- |
| `risk_score` | Continuous internal risk measure | Monotonic combination of low performance, low engagement, poor attendance, and weak discipline | Must remain explainable and should stay within `0.0..1.0` |
| `risk_level` | Teacher-facing categorical concern label | Thresholded mapping from `risk_score` | Current working levels are `low`, `medium`, `high` |

## Example V1 Assumptions

The following are acceptable as first-pass working assumptions, but they are intentionally not treated as final science:

- Normalize performance-like features to `0..100`.
- Normalize rate-like features to `0.0..1.0`.
- Compute short-horizon trends from the most recent up to 3 weeks.
- Let `engagement_index`, `performance_index`, and `discipline_index` stay on a `0..100` scale for easier teacher interpretation.
- Keep the risk formula interpretable and monotonic rather than complex.

## Anti-Leakage Note

Every feature in `student_twin_snapshots` must be computable using data available by the end of the snapshot week only.

That means:

- no future assignments,
- no future attendance,
- no end-of-course outcomes,
- no explanation artifacts derived after final evaluation.

## What Remains Open

- Exact weighting for the composite indices
- Exact scaling for the trend features
- Whether quiz and assignment categories need finer separation later
- Whether extra features such as volatility or topic mastery proxies should enter v1.1

TODO(data-model): finalize the exact snapshot feature calculation spec together with the first dataset generator implementation.
