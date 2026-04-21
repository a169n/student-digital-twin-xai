# Data Model Change Log

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
