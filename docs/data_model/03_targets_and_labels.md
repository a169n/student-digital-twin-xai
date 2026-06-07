# Targets and Labels

This document defines the v1.2 meaning of the project’s core outcomes and teacher-facing labels.

## Target Hierarchy

### ML Experiment Targets

- Primary regression target: `final_grade`
- Primary classification target: `passed`

### Teacher-Facing Heuristic Labels

- Weekly heuristic label: `risk_level`
- Internal heuristic score: `risk_score`

## Why This Changed in v1.2

The methodological correction in `schema_v1.2` separates experimental outcomes from teacher-facing heuristic labels.

`risk_level` is still important for the digital twin and for teacher-oriented analytics, but it is not suitable as ML ground truth because it is already derived from the same weekly feature space used to describe the twin. Training on it would mostly teach a model to reproduce the existing heuristic rather than learn a defensible external outcome.

For baseline ML experiments:

- use `final_results.final_grade` for regression
- use `final_results.passed` for classification

### `final_grade`

`final_grade` is the primary supervised-learning outcome for regression experiments.

It represents the realized end-of-course numeric result stored in `final_results`. In v1.2 it is assumed to use a `0..100` scale unless a later contract explicitly changes that interpretation.

### Modeling note

- `final_grade` is only observed after course completion.
- It must not be used as an input feature when constructing weekly snapshots.
- Downstream ML pipelines may join it onto weekly snapshots only after the snapshot table has been built in a temporally clean way.

## Determinism and circularity of `final_grade` (synthetic dataset)

In the synthetic generator, `final_grade` is computed by a fixed closed-form
formula (`services/ml/src/generator/final_results.py:74-84`):

    final_grade = clamp(
        0.55 * assignment_avg
      + 0.25 * quiz_avg
      + 0.10 * attendance_rate * 100
      + 0.10 * on_time_rate * 100,
        0, 100)

There is **no stochastic term** in this formula. The four inputs are the
full-course versions of the same behaviors that the weekly snapshot features
re-aggregate cumulatively (`avg_assignment_score_to_date`,
`avg_quiz_score_to_date`, `attendance_rate_to_date`,
`on_time_submission_rate_to_date`). The only randomness anywhere upstream is a
per-submission Gaussian (sd 0.06, `submissions.py:85`) that is **baked into the
recorded scores and therefore shared by both the features and the grade**; it
averages out across ~10 assignments. As a result, the synthetic supervised task
is largely an algebraic identity: from week-10 features the grade is
reconstructible with max absolute error 0.008 and correlation 1.000000.

**Consequence:** synthetic `R² ≈ 0.99`, `RMSE ≈ 1.9`, and `passed` `F1 = 1.000`
are mathematical artifacts of the generator, not evidence of learnable signal.
This is the explicit reason the synthetic dataset is used only as a controlled
methods probe (see `exp_008`) and the primary empirical evidence is OULAD. Note
the consistency point: `risk_level` is already excluded as a supervised target
for exactly this circularity reason; the same reasoning applies to `final_grade`
on synthetic data and must be stated rather than applied selectively.

### `passed`

`passed` is the primary supervised-learning outcome for classification experiments.

It is derived from `final_grade` and the pass policy stored in `courses.grading_policy_pass_mark`.

### Current rule

- `passed = true` when `final_grade >= grading_policy_pass_mark`
- otherwise `passed = false`

If `final_grade` is missing because of withdrawal or incompletion, that handling must stay explicit in generator logic and later experiment code.

### `risk_score`

`risk_score` is the internal numeric heuristic used to support teacher interpretation and derive `risk_level`.

In v1.2:

- it lives on `student_twin_snapshots`
- it is normalized to `0.0..1.0`
- higher values indicate higher current academic concern
- it is recalibrated to produce a more useful distribution for monitoring and realism checks

### v1.2 threshold policy

- `low`: `risk_score < 0.30`
- `medium`: `0.30 <= risk_score < 0.55`
- `high`: `risk_score >= 0.55`

These thresholds are still heuristic and dataset-specific. They are not institutional policy and may evolve again in later versions.

### `risk_level`

`risk_level` is the weekly teacher-facing categorical concern label attached to `student_twin_snapshots`.

Allowed values:

- `low`
- `medium`
- `high`

### Interpretation

- `low`: the student currently appears comparatively stable.
- `medium`: the student shows meaningful warning signs and should be monitored.
- `high`: the student shows strong warning signs and likely warrants attention or intervention.

### Important methodological note

`risk_level` is **not** the ML ground truth in v1.2.

It is a heuristic label derived from `risk_score`, which is itself derived from weekly twin features such as attendance, activity, performance, and submission discipline. Because of that:

- it is valid for teacher-facing twin monitoring
- it is valid for realism audits and descriptive analytics
- it is **not** the primary supervised target for baseline dissertation experiments

### `predicted_final_grade`

`predicted_final_grade` is a snapshot-level heuristic estimate, not the realized regression target.

It exists to support teacher interpretation of the evolving twin state and should be derived only from information available by the snapshot week.

It must not be confused with `final_results.final_grade`.

## Temporal and Leakage Rules

The following rules remain non-negotiable:

1. Weekly twin features must only use information available up to that week.
2. End-of-course outcomes such as `final_grade` and `passed` belong to the outcome layer and are joined later for training or evaluation.
3. `risk_level` is a weekly heuristic concern label, not an external ground-truth outcome.
4. Any later change to threshold logic, target meaning, or pass policy requires a schema and changelog update.

## What Remains Provisional

- The exact mathematical formula for `risk_score`
- The final operational definition of the risk horizon
- The final calibrated threshold cut points after empirical realism checks
- How withdrawals and incompletes should influence weekly heuristic labeling

TODO(domain): finalize the exact experimental evaluation strategy after baseline feature validation and first ML scaffolding are in place.
