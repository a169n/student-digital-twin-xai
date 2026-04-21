# Architecture Overview

## Research Positioning

`student-digital-twin-xai` is a research prototype for teacher-oriented educational analytics. The system centers on a dynamic **student digital twin** used for prediction, interpretation, and intervention planning.

## Core Principles

1. **Teacher-first decision support**: outputs must be actionable for instructional intervention.
2. **Digital Twin as a stateful representation**: not a static BI dashboard.
3. **XAI-by-design**: risk and grade predictions must be interpretable.
4. **Evolvable contracts**: schema versions are explicit and intentionally changeable.
5. **Modular monorepo**: isolate concerns while sharing contracts.

## System Boundaries (Current)

- In scope: architecture, contracts, placeholders, local scaffolding.
- Out of scope: production logic, complete training pipeline, finalized schema, enterprise hardening.

## High-Level Components

- Web app (Next.js): teacher-facing UI shell.
- API app (FastAPI): orchestration and domain APIs.
- ML service (Python): offline/online ML pipeline placeholders.
- Contracts package: versioned schema and cross-service structures.

## Data Flow (Planned)

Synthetic LMS-like inputs → feature generation → model inference (`risk_level`, `final_grade`) → XAI explanation payloads → teacher-facing recommendations.

> TODO: Add sequence diagrams after v0.2 API + ML contract stabilization.
