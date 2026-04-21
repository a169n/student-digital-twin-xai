# Data Model Change Log

## v1.1

- Date: 2026-04-21
- Status: additive contract update for the first usable dataset pipeline

### Summary

- Added `packages/contracts/schema_versions/schema_v1.1.yaml`.
- Extended `student_twin_snapshots` with pipeline-facing fields:
  - `avg_attempt_count_to_date`
  - `time_spent_to_date`
  - `current_topic_mastery`
  - `overall_mastery`
  - `predicted_final_grade`
- Extended `course_topics` with optional `topic_difficulty`.
- Kept trajectory enum values backward-compatible while documenting that `improving` behaves as the recovering pattern and `consistently_at_risk` behaves as the chronic-risk pattern.
- Promoted mastery and limited non-sensitive context from research-backed candidates into the active minor contract where needed for data generation.

### Impact

This version is the intended contract baseline for:

- the first synthetic dataset generator,
- schema-aware validation,
- weekly twin snapshot generation with mastery and time-spent features,
- reproducible research iteration on top of the ML service.

### Compatibility Note

This is a minor version bump because the added fields are optional and non-breaking relative to `schema_v1.0`.

## v1.0

- Date: 2026-04-21
- Status: first formalized schema contract

### Summary

- Added `packages/contracts/schema_versions/schema_v1.0.yaml` as the first stable research-baseline contract.
- Replaced placeholder data-model documents with aligned scope, entity, dictionary, target, and feature definitions.
- Formalized the raw LMS-like layer, processed digital twin layer, and end-of-course outcome layer.
- Standardized the core v1 targets:
  - `risk_level` as the primary weekly target
  - `final_grade` as the secondary end-of-course target
  - `passed` as a derived end-of-course metric
  - `risk_score` as the internal continuous score behind `risk_level`
- Documented hidden generation-only fields and marked them as non-user-facing.

### Impact

This version is intended to be the contract baseline for:

- synthetic dataset generation,
- schema validation,
- twin snapshot generation,
- downstream backend and ML integration.

### Documentation refinements after research review

- Clarified that `risk_score -> risk_level` thresholds should be calibrated to the dataset distribution rather than treated as fixed universal rules.
- Strengthened the feature documentation around mastery progression and limited course-internal context.
- Kept those additions as controlled future extensions rather than silently expanding the locked `schema_v1.0` field set.

### Change Discipline Reminder

Future schema changes must update all three of the following together:

1. the relevant schema contract in `packages/contracts/schema_versions/`
2. the matching documentation in `docs/data_model/`
3. any downstream code or generated artifacts that depend on the changed fields

### Breaking Change Guidance

Use a major version bump when changing:

- field names,
- field meanings,
- field types,
- target logic,
- core relationships.

Use a minor version bump for additive, non-breaking refinements such as optional fields or clarifying metadata.

## Historical Note

`v0.1` remains in the repository as a bootstrap placeholder and historical reference. It should not be treated as the active contract baseline now that `v1.0` exists.
