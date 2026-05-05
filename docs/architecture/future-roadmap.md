# Future Roadmap

## Phase 0: Architecture Bootstrap
- Monorepo scaffolding
- Contracts v0.1 placeholder
- API/Web/ML starter modules
- Local Docker orchestration

## Phase 1: Data Contract Refinement
- Expand schema v0.2 with documented entity constraints
- Define temporal/event-level semantics
- Align synthetic generator output with contracts

## Phase 2: Baseline ML Pipeline
- Synthetic data generation scenarios
- Baseline models for `risk_level` and `final_grade`
- Metric baselines and validation protocol

## Phase 3: Explainability + Intervention Design
- Explanation payload standardization
- Teacher-facing explanation rendering patterns
- Intervention recommendation policy prototypes

## Phase 4 (Current Foundation): Minimal Research Platform Backbone
- Deterministic artifact payload imported into a local SQLite app store
- FastAPI read APIs for dashboard, students, Twin snapshots, predictions,
  explanations, and research evidence
- Next.js pages consuming API-backed platform DTOs
- Explicitly deferred auth, live LMS integration, retraining, and intervention
  management

## Phase 5: Persistence + Evaluation Workflow
- PostgreSQL migrations after application projection semantics stabilize
- Import workflow for new prepared datasets
- Prediction refresh and explanation refresh jobs
- Reproducible experiment tracking and artifact registry

## Phase 6: Research Reporting Hardening
- Ablation experiments
- Fairness and robustness checks
- Dissertation-ready reproducibility package
