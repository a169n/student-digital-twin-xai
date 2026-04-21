# Data Model Scope

## Purpose

This document defines the scope of the first stable data-model foundation for the Student Digital Twin XAI research prototype.

The goal of `schema_v1.0` is not to represent a full LMS. The goal is to provide a disciplined and versioned structure for:

- synthetic LMS-like raw data,
- weekly student digital twin snapshots,
- end-of-course outcomes used for prediction targets,
- later dataset generation, validation, backend access, and explainability work.

## In Scope for v1

- Teacher-first analytics framing.
- One synthetic course as the initial modeling environment.
- A 10-week instructional structure.
- Raw LMS-like entities for students, topics, assignments, attendance, submissions, activity, and final results.
- A processed `student_twin_snapshots` table with the canonical grain `1 row = 1 student x 1 week`.
- Primary weekly target `risk_level`.
- Internal numeric score `risk_score` that maps to `risk_level`.
- Secondary end-of-course target `final_grade`.
- Derived end-of-course metric `passed`.
- Hidden generation-only fields where needed to make synthetic behavior structurally realistic.
- Versioned documentation and change tracking.

## Intentionally Out of Scope for v1

- Full LMS workflows such as content authoring, grading workflows, messaging, or calendar management.
- Full student information system coverage.
- Production-ready database migrations and persistence strategy.
- Institution-specific academic policy modeling beyond a simple pass threshold.
- Finalized intervention management workflows.
- Full explanation artifact storage or model-serving contracts.
- Rich UI behavior or polished visualization layers.
- Advanced or finalized ML feature science beyond defensible v1 definitions.

## Teacher-First Orientation

The primary user remains the teacher or instructor. This means the data model is optimized around:

- identifying current academic concern early,
- inspecting the evolving state of a student digital twin,
- understanding why a student appears stable or at risk,
- supporting later intervention-oriented reasoning.

The data model is therefore not organized as a student self-service product schema and not as a general-purpose LMS replacement.

## Scope Boundaries

### Dataset framing

- Synthetic but structurally realistic LMS-like data.
- Initial assumption: one course, one cohort, 10 weeks.
- Programming-course-like structure is a working assumption, not a locked institutional standard.

### Layer separation

The schema intentionally separates three layers:

1. Raw LMS-like data: observed students, topics, assignments, attendance, submissions, and weekly platform activity.
2. Processed digital twin state: cumulative and trend-based weekly student snapshots.
3. Outcome layer: final realized results used for evaluation and target joins.

### Versioning principle

This scope is explicitly versioned. `schema_v1.0` is expected to evolve. Future revisions should change the schema deliberately rather than through silent field drift.

## Research Prototype Reminder

This repository is a research-oriented prototype. The v1 scope is intentionally narrow so later phases can build on a stable and documented contract instead of ad hoc tables or prematurely invented product logic.
