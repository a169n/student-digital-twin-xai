# Data Model Change Log

## Minimal research platform projection (post-v1.2)

- Date: 2026-05-05
- Status: application layer, no schema change

### Summary

The web/API runtime now uses a local SQLite application projection seeded from
the deterministic research demo payload. This does not alter the canonical
research data model or frozen experiment evidence.

- Added an API importer from
  `data/artifacts/research_demo/research_demo_payload.json`.
- Added generated local persistence under `data/application/`.
- Exposed teacher-facing read APIs for dashboard, students, weekly Twin
  snapshots, predictions, explanations, and research evidence.
- Updated the Next.js runtime path to consume FastAPI endpoints instead of
  reading the demo payload directly.

### Compatibility Note

No schema fields were added, removed, renamed, or reinterpreted. The active
contract remains `schema_v1.2`.

## Versioned experiment logbook and Twin ablation (post-v1.2)

- Date: 2026-05-02
- Status: experimental layer, no schema change

### Summary

The experiment layer now treats modeling runs as versioned research artifacts.
This does not change the data model or schema contract.

- Added `docs/experiments/` as the experiment logbook.
- Preserved the existing baseline as `exp_001_baseline`.
- Added `exp_002_twin_ablation` to test Twin subgroups beyond `B_lms`.
- Added structured experiment metadata under each experiment artifact folder.
- Added versioned configs under `services/ml/configs/experiments/`.
- Added registry and comparison documentation for experiment history.

### Compatibility Note

No schema fields were added, removed, renamed, or reinterpreted. The active
contract remains `schema_v1.2`; `risk_level` remains excluded from supervised
training.

## Experimental scaffold (post-v1.2)

- Date: 2026-05-02
- Status: experimental layer, no schema change

### Summary

The first experimental modeling phase was added on top of the v1.2 contract
without modifying the schema. New code lives under `services/ml/src/experiments/`
and produces reproducible artifacts under `data/artifacts/eda/` and
`data/artifacts/experiments/baselines/`.

- Three explicit feature sets are now declared:
  - `A_simple` — minimal academic baseline (assignment / quiz averages plus
    attendance rate, plus the explicit missingness indicators).
  - `B_lms` — stronger LMS baseline that adds activity, time on platform, and
    submission-discipline signals.
  - `C_twin` — full Digital Twin representation that adds trend features,
    mastery proxies, and composite indices.
- A leakage-safe modeling pipeline:
  - joins `student_twin_snapshots` with `final_results` for the supervised
    targets `final_grade` and `passed`,
  - excludes identifiers, the snapshot-level heuristic risk fields, the
    snapshot-level `predicted_final_grade`, and all generation-only fields,
  - uses student-grouped splits (default) and a stricter temporal-forward
    split that also holds out students,
  - fits median imputation on the training partition only.
- Baseline models cover logistic regression, random forest, and gradient
  boosting for classification, and Ridge, random forest, and gradient
  boosting for regression.

### Why this is methodologically meaningful

`risk_level` continues to be excluded as a supervised target. The
experimental pipeline aligns with the v1.2 clarification that supervised
experiments use `final_grade` and `passed`, while `risk_level` stays as a
teacher-facing heuristic label.

### Compatibility Note

No schema fields were added, removed, renamed, or reinterpreted. The data
contract remains `schema_v1.2`.

## v1.2

- Date: 2026-04-21
- Status: methodological correction update

### Summary

- Added `packages/contracts/schema_versions/schema_v1.2.yaml`.
- Recalibrated the `risk_score -> risk_level` heuristic thresholds from `0.40/0.70` to `0.30/0.55`.
- Steepened at-risk and declining synthetic trajectories to produce a more realistic weekly risk distribution.
- Added explicit missing-data indicator fields to `student_twin_snapshots`:
  - `has_assignment_score_to_date`
  - `has_quiz_score_to_date`
- Reclassified `risk_level` from an ML target concept to a teacher-facing heuristic label.
- Clarified that supervised experiments should use:
  - `final_grade` for regression
  - `passed` for classification
- Added a realism-audit layer and report outputs in `data/artifacts/reports/`.
- Added leakage-safe split utilities for student-group and temporal-forward experiments.

### Impact

This version is the intended baseline for:

- methodologically safer synthetic dataset generation,
- realism auditing beyond structural schema validation,
- future baseline ML experiments without row-wise leakage,
- clearer separation between dashboard heuristics and experimental outcomes.

### Compatibility Note

This is a minor version bump because the schema changes are additive and clarifying, while the methodological interpretation of `risk_level` has been made explicit rather than silently assumed.

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
