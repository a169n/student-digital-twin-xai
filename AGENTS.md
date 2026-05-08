# AGENTS.md

Short, token-efficient context primer for AI coding agents working in this repo.
Read this first. Drill into the linked authoritative docs only when the task needs them.

---

## 1. What this project is

A **research prototype** for teacher-oriented educational analytics built around three ideas:

- **Student Digital Twin** — per-student, per-week stateful representation
- **Predictive analytics** — early academic risk + final grade prediction
- **Explainable AI (XAI)** — teacher-readable reasons behind predictions

It is **not** an LMS, SIS, or production edtech product. The dataset is synthetic
(plus an OULAD public benchmark). Auth, live LMS integration, and production
deployment are explicitly out of scope.

Primary user: **teacher / instructor**.
Primary ML target: `final_grade`. Secondary: `passed`. Heuristic teacher label: `risk_level` (NOT used as supervised target).

---

## 2. Current state (what actually exists today)

The dissertation experiment line is **complete**:

| ID | Purpose | Outcome |
| --- | --- | --- |
| `exp_001_baseline` | Compare feature sets `A_simple` / `B_lms` / `C_twin` | Full Twin did not beat LMS baseline reliably |
| `exp_002_twin_ablation` | Twin subgroup ablation | Carry forward `B_lms_plus_mastery` |
| `exp_003_mastery_validation` | Validate lean Twin candidate | Confirmed early-warning lift |
| `exp_004_xai_on_lean_twin` | XAI audit of lean candidate | Teacher-meaningful explanations |
| `exp_005_public_benchmark_oulad` | OULAD transfer stress test | Mixed: lift on temporal split, not grouped |

Built and working:

- Versioned schema contracts (`schema_v0.1` → `v1.2`) under [packages/contracts/schema_versions](packages/contracts/schema_versions/)
- Synthetic LMS-like dataset generator (`services/ml/src/generator`), latest config `generator_v1_3_refined.yaml`
- Twin snapshot pipeline (1 row = 1 student × 1 week)
- Baseline ML training, ablation, mastery validation, XAI audit, OULAD benchmark runners under [services/ml/src/experiments/](services/ml/src/experiments/)
- FastAPI backend with SQLite app store, fed from frozen experiment payload
- Next.js teacher-facing web app with read-only `/research-demo` route backed by frozen artifacts
- Dissertation synthesis package under [docs/dissertation/](docs/dissertation/) (final report, defense Q&A, claim guardrails, figures, tables)

Intentionally still missing: production backend workflows, polished product UI flows, validated scenario simulation, real institutional data integration.

---

## 3. Repo map

```
apps/
  api/        FastAPI backend. Domain-oriented layout.
              src/main.py, src/api/router.py, src/domain/{students,twins,predictions,
              explanations,interventions,dashboard,platform,research}, src/db (SQLite),
              src/import_research_payload.py (rebuilds SQLite from frozen payload).
  web/        Next.js 14 (App Router) teacher UI.
              app/{dashboard,students,twins,predictions,research-demo}, components/, lib/.
services/
  ml/         Python ML package. src/{generator,features,training,explainability,
              experiments,benchmarks,inference,validation,export,common}, configs/, tests/.
packages/
  contracts/  Canonical schema YAMLs (schema_versions/) + shared TS types (src/).
  config/     Shared config primitives.
docs/
  data_model/    Authoritative data dictionary, targets, features, change log.
  architecture/  Overview, decisions, future roadmap.
  research/      Problem statement, research gap, deep research report.
  experiments/   Per-experiment writeups + registry.md (canonical experiment index).
  dissertation/  Defense package: final report, Q&A, claims, figures, tables.
data/
  raw/           Generated raw LMS-like CSVs.
  processed/     Twin snapshots (CSV + Parquet).
  artifacts/
    experiments/ Versioned experiment outputs (do not overwrite).
    research_demo/  Frozen payload that feeds SQLite app store.
    reports/, eda/  Realism audits, EDA outputs.
  application/   Generated SQLite store (rebuildable from frozen payload).
scripts/      One-off scripts (e.g. generate_dissertation_assets.py).
```

---

## 4. Source-of-truth hierarchy

When code, contracts, and docs disagree, authority order is:

1. `docs/data_model/*`
2. `packages/contracts/schema_versions/*`
3. code
4. tests
5. generated artifacts under `data/`

Docs/contracts win until explicitly updated.

---

## 5. How to run things

Full guide: [RUN_SERVICES.md](RUN_SERVICES.md). Quick reference (PowerShell, Windows):

```powershell
# ML — regenerate dataset
cd services\ml
python -m src.main --config configs/generator_v1_3_refined.yaml

# ML — run an experiment
python -m src.experiments.run_baselines --config configs/experiments/exp_001_baseline.yaml

# API — rebuild SQLite from frozen payload, then serve
cd apps\api
uv sync
uv run python -m src.import_research_payload
uv run uvicorn src.main:app --reload --port 8000   # docs at /docs, API at /api

# Web
pnpm install
pnpm dev:web                                       # http://localhost:3000
```

Tests: `pytest` from `services/ml` or `apps/api`. Web tests under `apps/web/tests`.

---

## 6. Hard rules for agents

1. **Do not silently change the schema.** Add/rename/remove a field only after updating: schema YAML in `packages/contracts/schema_versions/`, the relevant `docs/data_model/*` file, and `docs/data_model/05_change_log.md`. Then update code. Bump major version on rename / type / meaning / removal / target-logic change; minor for additive optional fields.
2. **Never use `risk_level` as a supervised ML target.** It is a teacher-facing heuristic label. Use `final_grade` (primary) or `passed` (secondary).
3. **Preserve experiment artifacts.** A new experiment ID is required when changing dataset version, schema version, feature-set, target, split strategy, or model family in a way that changes interpretation. Do not overwrite `data/artifacts/experiments/<exp_id>/`.
4. **No fake domain logic.** If a threshold, rule, or workflow is undefined, leave a `TODO(domain): ...` and a minimal placeholder rather than inventing finished logic.
5. **Synthetic ≠ random.** Generated data must reflect plausible relationships (attendance ↔ activity ↔ submission ↔ performance ↔ outcome). Hidden generation parameters (`baseline_level`, `motivation_level`, `discipline_level`, `trajectory_type`) are allowed but must be marked generation-only.
6. **Stay in scope.** Teacher-facing analytics + XAI. Don't build LMS features, content authoring, auth flows, or student-facing product surfaces.
7. **Backend layout discipline.** Keep `routers / services / repositories / models / config` boundaries inside each `src/domain/<area>/` package. Don't blanket-CRUD; expose only meaningful domain endpoints.
8. **UI restraint.** Don't fabricate charts on missing data — use explicit stubs/placeholders.
9. **Implementation order matters:** schema contracts → data model docs → dataset generator → twin snapshots → baseline ML → XAI → API → UI → scenario simulation. Don't skip ahead unless asked.

---

## 7. Where to look for deeper context (only when needed)

- Project intent and non-goals → [README.md](README.md)
- Data model authority → [docs/data_model/](docs/data_model/)
- Architecture decisions → [docs/architecture/decisions.md](docs/architecture/decisions.md), [docs/architecture/overview.md](docs/architecture/overview.md)
- Research framing → [docs/research/problem-statement.md](docs/research/problem-statement.md), [docs/research/research-gap.md](docs/research/research-gap.md)
- Experiments index → [docs/experiments/registry.md](docs/experiments/registry.md), [docs/experiments/README.md](docs/experiments/README.md)
- Dissertation package → [docs/dissertation/README.md](docs/dissertation/README.md)
- Local startup → [RUN_SERVICES.md](RUN_SERVICES.md)
- Schema YAMLs → [packages/contracts/schema_versions/](packages/contracts/schema_versions/)
- ML service usage → [services/ml/README.md](services/ml/README.md)
- API service usage → [apps/api/README.md](apps/api/README.md)

---

## 8. Working style

1. Read only the docs you need; don't preload the whole tree.
2. Make the smallest coherent change.
3. Update contracts/docs *before* code when touching the data model.
4. Leave actionable `TODO(domain|data-model|api|ml|ui): ...` markers where the domain is intentionally unresolved.
5. End with a short summary: what changed, what assumptions you made, what is still unimplemented.

The goal is a credible, methodologically defensible research prototype — not a feature-rich lookalike.
