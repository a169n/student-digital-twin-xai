# AGENTS.md

## Purpose

This repository contains a **research-oriented prototype**, not a production LMS.

The project explores a teacher-oriented educational analytics system based on:

- **Student Digital Twin**
- **Explainable AI (XAI)**
- **early academic risk detection**
- **final grade prediction**
- **intervention-oriented decision support**

The main goal is to build a technically solid and academically defensible prototype.

---

## What This Project Is

This project is an **analytics and decision-support layer** for education.

It is meant to help instructors:

- identify students at risk early,
- understand why a student is considered at risk,
- inspect the student’s dynamic learning state,
- explore possible intervention scenarios.

---

## What This Project Is Not

Do **not** treat this repository as:

- a full LMS,
- a student information system,
- a production-ready edtech platform,
- a complete intervention management system,
- a place to invent unapproved business logic.

Do **not** expand scope casually.

---

## Core Research Framing

### Primary user

- **Teacher / instructor**

### Core object

- **Student as a Digital Twin**

### Primary target

- `risk_level`

### Secondary target

- `final_grade`

### Derived metric

- `passed`

### Expected XAI role

- explain why a student is high/medium/low risk,
- identify the strongest contributing factors,
- support intervention reasoning.

### Important principle

A Digital Twin is **not just a dashboard**.
The system must evolve toward:

- dynamic student state,
- time-aware snapshots,
- prediction,
- explanation,
- scenario analysis.

---

## Source of Truth Hierarchy

When making changes, follow this order of authority:

1. `docs/data_model/*`
2. `packages/contracts/schema_versions/*`
3. code implementation
4. tests
5. generated data artifacts

If code and docs disagree, **docs/contracts win** until explicitly updated.

---

## Change Discipline

### Rule 1 — Do not silently change the schema

If you add, rename, remove, or reinterpret a field:

- update schema contract files,
- update data dictionary,
- update target/feature docs,
- update changelog,
- then update code.

### Rule 2 — Do not invent domain details

If a field, rule, threshold, or workflow is not defined:

- do not pretend it is finalized,
- add a clear `TODO`,
- use a minimal placeholder,
- document the assumption.

### Rule 3 — Prefer explicit placeholders over fake completeness

It is better to leave a clean stub than to generate misleading “finished” logic.

### Rule 4 — Do not overengineer early

Before data contracts and dataset generation are stable:

- avoid deep backend implementation,
- avoid advanced UI work,
- avoid premature DB-heavy complexity.

---

## Versioning Rules

Schema and data model changes must be versioned.

### Minor change

Use a minor version bump when:

- adding optional fields,
- expanding documentation,
- adding non-breaking metadata.

### Major change

Use a major version bump when:

- renaming fields,
- changing field meaning,
- changing field types,
- removing fields,
- changing target logic.

Update:

- `packages/contracts/schema_versions/`
- `docs/data_model/05_change_log.md`

---

## Expected Monorepo Structure

- `apps/web`  
  Teacher-facing frontend

- `apps/api`  
  Backend API and domain access

- `services/ml`  
  Dataset generation, feature engineering, training, inference, explainability

- `packages/contracts`  
  Canonical schema contracts and shared data definitions

- `docs/architecture`  
  Architecture decisions and roadmap

- `docs/data_model`  
  Entities, dictionary, targets, features, changelog

- `docs/research`  
  Problem framing and research gap

- `data/raw`  
  Generated LMS-like raw datasets

- `data/processed`  
  Processed twin snapshots and derived data

- `data/artifacts`  
  Saved model artifacts and analysis outputs

---

## Development Priorities

Always prefer this implementation order:

1. repository architecture
2. schema contracts
3. data model docs
4. synthetic dataset generator
5. twin snapshot generation
6. baseline ML pipeline
7. explainability layer
8. backend endpoints
9. frontend views
10. scenario simulation flow

Do not skip ahead unless explicitly requested.

---

## Dataset and Data Modeling Rules

### General

The project starts with a **synthetic but structurally realistic LMS-like dataset**.

### Expected early scope

- one course,
- 10 weeks,
- weekly topics,
- assignments/quizzes,
- attendance,
- activity,
- final result.

### Data layers

Keep data conceptually separated into:

1. **raw LMS-like data**
2. **processed student twin snapshots**
3. **prediction / explanation outputs**

### Do not collapse everything into one giant table

Use normalized raw structures plus derived snapshot tables.

### Student twin snapshots

A key pattern is:

- **1 row = 1 student × 1 week**

This is central to the project.

---

## ML / Analytics Rules

### Early stage

Use simple, explainable, defensible baselines first.

Good early candidates:

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting / XGBoost later

Do not introduce unnecessary model complexity early.

### Explainability

XAI is not optional decoration.
Explanations should support:

- teacher interpretation,
- factor analysis,
- intervention reasoning.

### Data generation

Synthetic data must not be random noise.
It should reflect plausible relationships between:

- attendance,
- activity,
- submission discipline,
- performance,
- risk,
- final outcome.

### Hidden generation parameters are allowed

For example:

- `baseline_level`
- `motivation_level`
- `discipline_level`
- `trajectory_type`

But clearly mark them as **generation-only** if they are not part of the visible application domain.

---

## Backend Rules

### Architecture

Prefer clean, domain-oriented structure.
Use clear boundaries between:

- routers
- services
- repositories
- schemas/models
- config

### Persistence

Future target DB is PostgreSQL.
Before DB-heavy implementation is needed, file-based development is acceptable.

### API scope

Do not generate full CRUD blindly.
Expose only meaningful domain endpoints.

Examples of useful future domains:

- students
- twin snapshots
- predictions
- explanations
- interventions

---

## Frontend Rules

### Main audience

Teacher-first.

### Early UI scope

Keep UI restrained and functional:

- dashboard shell,
- student list,
- student twin view,
- predictions view,
- explanations placeholder,
- interventions placeholder.

Do not spend time on visual polish before data and API stabilize.

### Avoid fake charts

If data is not ready, use explicit stubs or placeholders.
Do not fabricate complex visuals just to fill screens.

---

## Documentation Rules

Every meaningful change should preserve documentation quality.

At minimum, keep these files aligned:

- `docs/data_model/00_scope.md`
- `docs/data_model/01_entities.md`
- `docs/data_model/02_data_dictionary.md`
- `docs/data_model/03_targets_and_labels.md`
- `docs/data_model/04_feature_definitions.md`
- `docs/data_model/05_change_log.md`

When changing architecture, also update:

- `docs/architecture/overview.md`
- `docs/architecture/decisions.md`
- `docs/architecture/future-roadmap.md`

---

## When Requirements Are Missing

If requirements are underspecified:

1. do not hallucinate a full solution,
2. preserve current architecture,
3. add minimal safe placeholders,
4. document assumptions,
5. leave actionable TODOs.

Use this pattern:

- `TODO(domain): clarify exact risk threshold strategy`
- `TODO(data-model): finalize snapshot feature list after schema review`
- `TODO(api): replace file-backed repository with PostgreSQL implementation`

---

## Code Quality Expectations

Prefer:

- clarity over cleverness,
- small coherent modules,
- explicit names,
- low surprise,
- maintainable defaults.

Avoid:

- speculative abstractions,
- unnecessary generic frameworks,
- hidden coupling,
- premature optimization,
- unexplained magic constants.

---

## Before You Commit Changes

Check all of the following:

- Does this change alter the data model?
- If yes, were contracts/docs updated first?
- Does this introduce fake domain logic?
- Does this preserve teacher-oriented scope?
- Does this move the project toward Digital Twin + XAI, not away from it?
- Is this a scaffold, placeholder, or real implementation?
- Is that made explicit in code/comments/docs?

---

## Preferred Working Style for Agents

When performing a task:

1. inspect relevant docs/contracts first,
2. make the smallest coherent change,
3. keep structure clean,
4. leave TODOs where the domain is intentionally unresolved,
5. summarize:
   - what changed,
   - what assumptions were made,
   - what remains unimplemented.

---

## Non-Negotiable Principle

This repository should evolve into a **credible research prototype**.

Do not optimize for looking complete.
Optimize for being:

- structured,
- honest,
- extensible,
- methodologically defensible.

A smaller, cleaner, correctly scoped system is better than a fake “full platform”.
