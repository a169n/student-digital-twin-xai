# Assumptions

This document records the main working assumptions behind `schema_v1.0`. These assumptions are deliberate placeholders for a research prototype, not claims of finalized institutional policy.

## Structural Assumptions

- The v1 dataset models one course only.
- The course is modeled over 10 instructional weeks.
- `course_topics` is expected to have one primary topic per week in v1.
- `student_twin_snapshots` uses the canonical grain `1 row = 1 student x 1 week`.
- `students.course_id` is a v1 simplification for the single-course prototype and may later be replaced by an explicit enrollments structure.

## Pedagogical Context Assumptions

- The initial synthetic context is programming-course-like rather than institution-specific.
- The course may include assignments, quizzes, and lab-style work.
- An initial workload pattern of roughly up to two assessed items per week is acceptable for generation, but it is not a hard schema rule.

## Synthetic Data Assumptions

- The dataset is synthetic but should encode plausible relationships between attendance, activity, submission discipline, performance, and final outcomes.
- Hidden generation-only fields are allowed when they improve synthetic realism.
- Initial hidden generation parameters include:
  - `baseline_level`
  - `motivation_level`
  - `discipline_level`
  - `trajectory_type`
- Initial `trajectory_type` values are:
  - `stable_high`
  - `improving`
  - `declining`
  - `consistently_at_risk`

## Target Assumptions

- `risk_level` is the primary weekly teacher-facing target.
- `risk_score` is the internal numeric precursor to `risk_level`.
- `final_grade` is the secondary end-of-course target.
- `passed` is derived from `final_grade` and the course pass policy.
- The v1 risk threshold mapping is provisional and may change after initial experimentation.

## Product Scope Assumptions

- The primary user is the teacher or instructor.
- The repository is an analytics and decision-support layer, not a full LMS.
- Hidden generation-only fields are not intended for teacher-facing UI exposure.
- Explanation logic and scenario simulation are future layers and are not fully specified by the v1 contract.

## Forward-Looking Assumptions

- This schema is designed to support future dataset generation, twin snapshot generation, baseline ML, XAI, backend endpoints, and restrained teacher-facing views.
- Future versions may add entities such as enrollments, explanations, interventions, and model artifact references.
- Any change to field meaning, target logic, or relationship structure must be versioned and documented.

## Open TODOs

TODO(domain): clarify the final operational risk-threshold strategy after first-pass synthetic data experiments.

TODO(data-model): decide whether future versions need explicit support for multiple sections or multiple concurrent courses.

TODO(generator): lock the exact weekly assessment density once the synthetic dataset generator is implemented.
