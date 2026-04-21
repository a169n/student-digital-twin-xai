# Architecture Decisions

## ADR-001: Monorepo over polyrepo
- **Decision**: Use monorepo with `apps/`, `services/`, and `packages/`.
- **Rationale**: Shared contracts and synchronized iteration are key in research.

## ADR-002: Next.js + FastAPI + Python ML
- **Decision**: TypeScript web app, FastAPI backend, Python ML modules.
- **Rationale**: Strong productivity, mature ecosystems, and clear separation of concerns.

## ADR-003: Contract-first data evolution
- **Decision**: Maintain versioned schema documents in `packages/contracts/schema_versions`.
- **Rationale**: Research data semantics will evolve; explicit versions reduce accidental coupling.

## ADR-004: Use `uv` for Python dependency management
- **Decision**: Standardize Python env + deps with `uv`.
- **Rationale**: Fast resolution/lock behavior and good DX for multi-service Python setups.

## ADR-005: PostgreSQL is future persistence target
- **Decision**: Prepare DB wiring and Docker service but defer full persistence logic.
- **Rationale**: Keep architecture future-ready while avoiding premature schema lock-in.

## ADR-006: XAI as mandatory output contract
- **Decision**: Prediction endpoints will carry explanation placeholders from day one.
- **Rationale**: Interpretability is central to teacher trust and research validity.

> TODO: Add formal ADR template and status transitions in future phases.
