# student-digital-twin-xai

Research-oriented monorepo scaffold for a **Student Digital Twin + Explainable AI (XAI)** prototype focused on teacher-facing educational analytics.

> This repository is intentionally an **architecture bootstrap**, not a production LMS and not a fully implemented product.

## Purpose

This project supports a master's/dissertation workflow and provides a clean foundation for iterative development of:

- early student `risk_level` detection,
- `final_grade` prediction,
- derived `passed` status,
- explainable predictions and intervention-oriented decision support.

The core concept is a **dynamic student digital twin** (longitudinal representation), not just a static dashboard.

## Architecture Overview

- **apps/web**: Next.js + TypeScript teacher UI scaffold.
- **apps/api**: FastAPI backend scaffold with domain routers and placeholder service/repository layers.
- **services/ml**: Python ML pipeline scaffold (synthetic generation, features, training, inference, explainability, validation).
- **packages/contracts**: Versioned schema contracts and shared lightweight model definitions.
- **packages/config**: Shared repository conventions and environment metadata.
- **docs/**: Architecture, data model, and research positioning docs.
- **data/**: Local raw/processed/artifacts directories for iterative experimentation.

## Monorepo Structure

```text
.
├── apps/
│   ├── api/
│   └── web/
├── services/
│   └── ml/
├── packages/
│   ├── contracts/
│   └── config/
├── docs/
│   ├── architecture/
│   ├── data_model/
│   └── research/
├── data/
│   ├── raw/
│   ├── processed/
│   └── artifacts/
├── scripts/
└── docker-compose.yml
```

## Setup (Local Development)

### Prerequisites

- Node.js 20+
- pnpm 9+
- Python 3.11+
- [uv](https://github.com/astral-sh/uv)
- Docker + Docker Compose

### Quick Start

```bash
cp apps/api/.env.example apps/api/.env
cp services/ml/.env.example services/ml/.env
cp apps/web/.env.example apps/web/.env.local

make bootstrap
make check
make up
```

## Current Status (Intentionally Not Implemented Yet)

- No production-grade domain logic.
- No finalized dataset schema (schema is versioned and expected to evolve).
- No real model training pipeline or calibrated evaluation.
- No full CRUD, auth, RBAC, or end-user workflows.
- No finalized PostgreSQL persistence implementation.

See `docs/architecture/future-roadmap.md` for planned phases.
