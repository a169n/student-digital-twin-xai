# Targets and Labels

This document defines the v1.1 meaning of the project’s core targets and related outcome fields.

## Target Hierarchy

- Primary target: `risk_level`
- Secondary target: `final_grade`
- Derived metric: `passed`
- Internal numeric score: `risk_score`

## `risk_level`

`risk_level` is the primary target for the research prototype.

In v1, it is defined as a weekly teacher-facing categorical label attached to `student_twin_snapshots`. It summarizes the current level of academic concern for a student at the end of a given week.

Allowed values:

- `low`
- `medium`
- `high`

### Interpretation

- `low`: the student currently appears comparatively stable.
- `medium`: the student shows meaningful warning signs and should be monitored.
- `high`: the student shows strong warning signs and is likely to require attention or intervention.

### Important v1 note

`risk_level` is not meant to claim a finalized institutional policy. It is a research-oriented label that should be interpretable and useful for teacher reasoning. The exact thresholds and generation logic may evolve in later schema versions.

## `risk_score`

`risk_score` is the internal numeric value that supports `risk_level`.

In v1:

- it lives on `student_twin_snapshots`,
- it is expected to be normalized to the range `0.0..1.0`,
- higher values indicate higher academic concern,
- it is mapped to `risk_level` through provisional threshold rules.

### Provisional v1 threshold policy

The v1 documentation uses an example mapping rather than a fixed institutional rule:

- `low`: `risk_score < 0.40`
- `medium`: `0.40 <= risk_score < 0.70`
- `high`: `risk_score >= 0.70`

This mapping is intentionally provisional. The literature-backed recommendation is to calibrate thresholds after inspecting the synthetic data distribution and early validation results, rather than treating one threshold set as universally correct.

### Calibration note

For the first dataset release, the safest interpretation is:

- `risk_score` is the stable internal signal,
- `risk_level` is the teacher-facing categorization,
- the exact threshold cut points are dataset-specific and may be revised without changing the conceptual role of the target.

## `final_grade`

`final_grade` is the secondary target.

It represents the realized end-of-course numeric result stored in `final_results`. In v1 it is assumed to use a `0..100` scale unless a later contract explicitly changes that interpretation.

### Modeling note

`final_grade` is an outcome observed at course completion. It should not be used as a feature when constructing weekly student twin snapshots.

Downstream ML pipelines may join `final_results.final_grade` onto weekly snapshots for supervised learning, but the feature-generation side must remain temporally clean.

## `predicted_final_grade`

`predicted_final_grade` is a snapshot-level heuristic estimate, not the formal secondary target.

In v1.1 it lives on `student_twin_snapshots` and exists to support teacher interpretation of the evolving digital twin. It should be derived only from information available up to the snapshot week and must not be confused with the realized `final_results.final_grade`.

## `passed`

`passed` is a derived end-of-course metric, not the main research target.

It should be derived from `final_grade` and the course pass policy, represented in v1 by `courses.grading_policy_pass_mark`.

### Provisional v1 rule

- `passed = true` when `final_grade >= grading_policy_pass_mark`
- otherwise `passed = false`

If `final_grade` is missing because of withdrawal or incompletion, the exact handling should be explicit in generator logic and must not be silently assumed.

## Temporal and Leakage Rules

The following rules are part of the v1 label design:

1. Weekly twin features must only use information available up to that week.
2. End-of-course outcomes such as `final_grade` and `passed` belong to the outcome layer and should be joined later for training or evaluation.
3. `risk_level` is a weekly concern label, not a retrospective final outcome label.
4. Any later change to threshold logic, label meaning, or pass policy requires a schema and changelog update.

## What Remains Provisional

- The exact mathematical formula for `risk_score`
- The final operational definition of the risk horizon
- The final calibrated threshold cut points after empirical validation
- How withdrawals and incompletes should influence weekly risk labeling

TODO(domain): clarify the final risk-threshold strategy after the first synthetic dataset and baseline evaluation are available.
