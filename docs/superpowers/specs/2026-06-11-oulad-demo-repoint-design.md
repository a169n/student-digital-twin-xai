# Re-point Teacher Dashboard Demo to Real OULAD Data (Approach B) — Design

> **Status:** approved (2026-06-11, Approach B). Build via implementation workflow.
> **Commit policy:** user commits manually (unless an explicit git-flow request says otherwise).

## Goal
The repo already has a WORKING teacher-facing dashboard (`apps/web` Next.js + `apps/api` FastAPI + SQLite), currently seeded from a frozen SYNTHETIC payload. The dissertation's honest pivot calls the synthetic target circular, so the demo must run on REAL OULAD data to be defensible. Build an OULAD→payload exporter that produces the SAME payload schema the app already consumes, then re-seed and verify the dashboard renders real OULAD students.

**No ML-experiment changes. No live serving. Interventions stay deferred (matches the "no simulation/counterfactual" non-claim).**

## Approach B (chosen): honest pass-risk
- **Cohort:** OULAD DDD 2013J (primary narrative cohort).
- **Predictions:** train the OULAD models on DDD 2013J via the existing pipeline (reuse `run_public_benchmark_oulad` / `explainability.train_regression_reference_for_matrix`), gradient boosting, feature set `B_lms_plus_mastery_oulad`:
  - `predicted_final_grade` = predicted `final_weighted_score` (0–100) from the **regression** model — shown with an explicit "partially circular target" disclosure.
  - `risk_score` / `risk_level` = derived from the **classification** model's P(not passing) — the honest, non-circular-leaning F1≈0.86 signal. Risk bands (default): P(fail) ≥ 0.60 → "high", ≥ 0.35 → "medium", else "low".
- **Sample:** a representative ~150-student subset of DDD 2013J (stratified by outcome/risk) to keep the demo snappy; the full cohort remains in the experiments. Disclosed in payload `limitations`.
- **Honest caveats embedded** in payload `limitations`/`xai`/`experiments`: target partial circularity, F1≈0.86 (not 1.000), mixed-to-null Twin value, OULAD has no attendance/quiz analog, predictions are model-behavior not causal.

## Field mapping (OULAD snapshot → payload)
Clean source: `engagement_index_oulad`/`performance_index_oulad`/`discipline_index_oulad` → indices; `overall_mastery_proxy` → overall_mastery; `current_assessment_cluster_mastery` → current_topic_mastery; `cumulative_assessment_score_mean_to_date` → assignment_average; `assessment_score_trend_to_date` → score_trend_3w; `clicks_trend_to_date` → activity_trend_3w; `final_weighted_score`/`passed_observed` (last week) → actual_final_grade/passed; `code_module`+`code_presentation` → cohort_label ("OULAD DDD 2013J").
Null (UI `missing-payload` handles): `quiz_average`, `attendance_rate`, `attendance_trend_3w`, `trajectory_label`.
Computed: `predicted_final_grade` (regression), `risk_level`/`risk_score` (classification P(fail)), `activity_score` (normalize `cumulative_clicks_to_date` to 0–100), representative `cases` + `topContributions` (via `select_representative_cases` + `compute_local_perturbation_contributions` on the OULAD model), `mastery_share`/`teacher_assessment`.
`student_label`: derive from `id_student` (e.g. "OULAD-<id>").

## Architecture
- New `services/ml/src/export/export_oulad_research_payload.py` — mirrors the synthetic exporter `export_research_demo_payload.py`, but reads OULAD snapshots + trains/uses the OULAD models + the OULAD XAI engine, emits the same payload JSON. CLI: build payload → write to `data/artifacts/research_demo/oulad_research_demo_payload.json`.
- Re-seed: `apps/api` import (`python -m src.import_research_payload`, pointed at the OULAD payload) → `data/application/research_platform.sqlite`.
- Web: minor label/copy tweaks only (cohort label, "weighted score (partially circular)" note on the grade field, "no attendance/quiz in OULAD" note). The `/research-demo` page already renders the honest caveats from the payload.

## Reuse vs build
- REUSE: the whole `apps/web` + `apps/api` + SQLite schema + importer + the synthetic exporter as the structural template + the OULAD adapter/model/XAI functions in `services/ml`.
- BUILD: the OULAD exporter + CLI; the model-inference + risk-derivation glue; minor web labels; a payload schema-validation check.

## Out of scope
- Live `/predict` serving; interventions/what-if; new ML experiments; retraining beyond what the exporter needs; full-cohort (1938) loading; mobile/responsive polish.

## Verification (acceptance)
1. Exporter runs and emits a payload that the `apps/api` importer ingests WITHOUT schema errors into a fresh SQLite.
2. Dashboard (`/dashboard`, `/students/[id]`, `/predictions`, `/research-demo`) renders REAL OULAD students: cohort = OULAD DDD 2013J; risk distribution non-degenerate; per-student weekly timeline + explanations populated; null fields (attendance/quiz) handled gracefully.
3. Honest framing visible: target-circularity + F1≈0.86 + "no attendance/quiz" disclosures present; risk driven by classification P(fail).
4. Screenshots captured of the key screens for the paper/defense.
5. No synthetic-only number (R²≈0.99 / F1=1.000) appears as a real capability anywhere in the running demo.
