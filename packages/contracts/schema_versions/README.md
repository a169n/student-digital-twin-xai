# Schema Versions

This directory stores versioned schema contracts for the Student Digital Twin XAI research prototype.

## Current Files

- `schema_v0.1.yaml`: bootstrap placeholder contract kept for history.
- `schema_v1.0.yaml`: first formalized data-model contract for the synthetic LMS-like dataset and processed student twin snapshots.
- `schema_v1.1.yaml`: additive contract update that supports the first usable synthetic data pipeline and weekly twin enrichment fields.

## Active Baseline

The current implementation baseline is `schema_v1.1.yaml`. New generator, validation, and downstream ML work should target that contract unless a later version is explicitly introduced.

## Versioning Rules

1. Add a new file for every released schema version using the pattern `schema_vX.Y.yaml`.
2. Treat `docs/data_model/*` and the matching schema contract as the source of truth for downstream code and generated data.
3. When a schema change affects field names, meanings, types, targets, or relationships, update:
   - the relevant contract file in this directory,
   - `docs/data_model/02_data_dictionary.md`,
   - `docs/data_model/03_targets_and_labels.md`,
   - `docs/data_model/04_feature_definitions.md` when feature semantics change,
   - `docs/data_model/05_change_log.md`.
4. Use a minor version bump for non-breaking additions such as optional fields or clarifying metadata.
5. Use a major version bump for breaking changes such as renamed fields, removed fields, changed field meanings, or changed target logic.

## Working Principle

These contracts are intentionally readable. They are not meant to be a complex DSL or a full migration framework. Their purpose is to keep dataset generation, snapshot building, ML pipelines, and future backend work aligned around a shared and versioned structure.
