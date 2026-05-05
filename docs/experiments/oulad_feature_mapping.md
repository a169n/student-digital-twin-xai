# OULAD Feature Mapping for Public Benchmark

This document records the feature bridge used by
`exp_005_public_benchmark_oulad`. It is a benchmark-compatible mapping, not a
schema change and not an attempt to force OULAD into the synthetic
`student_twin_snapshots` contract.

## Source Tables Used

The benchmark uses only the local OULAD CSV files placed under `datasets/oulad`:

- `assessments.csv`
- `courses.csv`
- `studentInfo.csv`
- `studentRegistration.csv`
- `studentVle.csv`
- `vle.csv`
- `studentAssessment.csv`

The configured benchmark subset is `code_module = DDD`,
`code_presentation = 2013J`. This keeps the public benchmark aligned with the
repository's current one-course research scope and uses a presentation with
dated assessments and observed exam score rows.

## Snapshot Grain

The adapter builds weekly rows at:

`1 row = 1 OULAD student-course presentation x 1 week`

OULAD day offsets are converted to weeks using the course start as day `0`.
Negative pre-course activity dates are clipped into week `1`, so early VLE
activity is available to week-1 cumulative features rather than discarded.

## Target Mapping

Primary target:

- `final_weighted_score`

Construction:

`sum(score_or_zero * assessment_weight) / sum(assessment_weight)`

The denominator includes positive-weight assessments in the selected
module-presentation that have score records in `studentAssessment`. Missing
student submissions for those scored assessment components contribute zero to
the numerator. This is a derived weighted assessment score, not the same
construct as the synthetic `final_grade`.

Secondary target:

- `passed_observed`

Construction:

- `Pass` and `Distinction` from `studentInfo.final_result` map to `1`
- `Fail` and `Withdrawn` map to `0`

Excluded:

- `risk_level` is not present in OULAD and is not created as a supervised
  target.

## `B_lms_oulad`

`B_lms_oulad` is the strong LMS-style baseline analogue. It uses OULAD fields
that a conventional LMS analytics view could plausibly expose.

| Synthetic baseline idea | OULAD analogue | Source fields |
| --- | --- | --- |
| Course/week progression | `week_number`, `course_week_progress` | `courses.module_presentation_length`, OULAD date offsets |
| Registration state | `is_registered_by_week`, `is_unregistered_by_week`, `days_since_registration_start` | `studentRegistration.date_registration`, `studentRegistration.date_unregistration` |
| Cumulative score to date | `cumulative_assessment_score_mean_to_date` | `studentAssessment.score`, `studentAssessment.date_submitted` |
| Weighted score to date | `cumulative_assessment_weighted_score_to_date`, `cumulative_submitted_weight_to_date` | `assessments.weight`, `studentAssessment.score`, `studentAssessment.date_submitted` |
| Submission discipline | `assessment_submission_rate_due_to_date`, `late_submission_rate_to_date`, `banked_assessment_rate_to_date` | `assessments.date`, `studentAssessment.date_submitted`, `studentAssessment.is_banked` |
| Activity intensity | `current_week_clicks`, `cumulative_clicks_to_date` | `studentVle.sum_click`, `studentVle.date` |
| Activity diversity/category | `current_week_activity_types`, cumulative category clicks | `studentVle.id_site`, `vle.activity_type` |
| Missingness/context | `has_assessment_score_to_date`, `has_weighted_score_to_date`, `has_vle_activity_to_date` | derived indicators |

VLE activity categories are compact groups derived from `vle.activity_type`:

- assessment: `quiz`, `externalquiz`, `questionnaire`, `dataplus`
- content: `homepage`, `oucontent`, `resource`, `page`, `subpage`,
  `sharedsubpage`, `url`, `folder`, `htmlactivity`
- social: `forumng`, `oucollaborate`, `ouelluminate`, `ouwiki`
- other: all remaining OULAD activity types

## `B_lms_plus_mastery_oulad`

`B_lms_plus_mastery_oulad` adds a lean mastery-like block. OULAD does not
provide synthetic weekly topics or generated mastery fields, so the benchmark
uses dated assessment structure as the closest defensible public analogue.

| Synthetic mastery idea | OULAD analogue | Notes |
| --- | --- | --- |
| `overall_mastery` | `overall_mastery_proxy` | Due-to-date positive-weight assessment score, treating due but unsubmitted scored assessments as zero until submitted. |
| `current_topic_mastery` | `current_assessment_cluster_mastery` | Weighted score for assessments due in the current week; `NaN` when no assessment cluster is due. |
| Topic/type aggregation | `tma_mastery_to_date`, `cma_mastery_to_date`, `exam_mastery_to_date` | Assessment-type aggregates from OULAD `assessment_type`; unavailable types remain explicit missingness rather than invented values. |
| Assessment progress context | `mastery_assessment_coverage_to_date` | Positive scored assessment weight due so far divided by total positive scored assessment weight. |
| Missingness/context | `has_current_assessment_cluster`, `has_due_assessment_to_date` | Indicates whether mastery values are structurally available at that week. |

## No Clean OULAD Equivalent

Several synthetic features have no clean OULAD equivalent in this phase:

- attendance rate and attendance trends
- weekly synthetic topics and topic difficulty
- generated `risk_score` and `risk_level`
- hidden generation-only variables such as motivation, discipline, baseline
  ability, and trajectory type
- synthetic composite indices for engagement, performance, and discipline
- intervention state or scenario outcomes

These are not fabricated. They are left out of the benchmark.

## What This Benchmark Can Test

The benchmark can test whether an assessment-structure-aware mastery analogue
adds value beyond a strong LMS-style OULAD baseline under leakage-safe student
grouping and temporal-forward evaluation.

It can also test whether the synthetic carry-forward direction is robust to a
public dataset with different noise, assessment design, missingness, and
outcome semantics.

## What This Benchmark Cannot Test

The benchmark cannot prove full external validity. It does not show that the
synthetic generator is better or worse than OULAD, and it does not validate the
complete Digital Twin schema on real institutional data.

The correct interpretation is:

- synthetic experiments: internally valid development of the representation;
- OULAD benchmark: external public-dataset stress test of transfer plausibility.

