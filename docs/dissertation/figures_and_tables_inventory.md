# Figures and Tables Inventory

This inventory lists the existing repository artifacts that are most useful
as evidence for the dissertation. It is divided into result tables that can
be reused with light reformatting, artifact files that contain the
machine-readable evidence behind the headline numbers, and generated
figures/tables produced from the same frozen artifacts. The aim is to make
it easy to cite repository evidence directly without re-running experiments.

## 1. Result Tables Worth Reusing

### 1.1 Baseline feature-set comparison (exp_001_baseline)

Source: [docs/experiments/exp_001_baseline.md](../experiments/exp_001_baseline.md)

- Best `final_grade` RMSE by split and feature set, with `A_simple`,
  `B_lms`, `C_twin` across the primary student-grouped split and the
  secondary temporal-forward split.
- The `passed` saturation table at F1 = `1.000` across all sets and splits.

These two tables together establish the negative finding that motivates
the ablation.

### 1.2 Twin subgroup ablation (exp_002_twin_ablation)

Source: [docs/experiments/exp_002_twin_ablation.md](../experiments/exp_002_twin_ablation.md)

- Primary regression summary table ranked by RMSE, showing
  `B_lms_plus_mastery`, `B_lms_plus_trends_mastery`, `B_lms_plus_indices`,
  `B_lms_plus_temporal`, `B_lms_plus_trends`, `B_lms`, and `C_twin_full`.
- The same table for the temporal-forward split.
- The `passed` classification table for both splits, showing the
  saturation pattern.

### 1.3 Mastery validation (exp_003_mastery_validation)

Source: [docs/experiments/exp_003_mastery_validation.md](../experiments/exp_003_mastery_validation.md)

- Headline regression results table.
- Mastery vs `final_grade` correlation table (`current_topic_mastery`,
  `overall_mastery` with global Pearson r and weekly bounds).
- Mastery redundancy with LMS baseline features table.
- LMS baseline target-correlation table.
- Week-aware delta of `B_lms_plus_mastery` versus `B_lms` across weeks
  4–10.
- Drop-column results table for the candidate model.
- Permutation importance top-features table.

### 1.4 XAI on lean Twin (exp_004_xai_on_lean_twin)

Source: [docs/experiments/exp_004_xai_on_lean_twin.md](../experiments/exp_004_xai_on_lean_twin.md)

- Model behavior table: `B_lms`, `B_lms_plus_mastery`, and lean Twin
  without `overall_mastery`, reporting RMSE/MAE/R².
- Global permutation importance table for both feature sets, with
  importance share and direction note.
- Baseline-versus-lean top-feature comparison.
- Dominance audit summary (rank, importance share, RMSE delta when
  removed, average local mastery share, outcome and flags).
- Local case findings table for the five representative cases.

### 1.5 Public OULAD benchmark (exp_005_public_benchmark_oulad)

Source: [docs/experiments/exp_005_public_benchmark_oulad.md](../experiments/exp_005_public_benchmark_oulad.md)

- OULAD row counts and target distribution for `DDD` `2013J`.
- Headline regression table comparing `B_lms_oulad` and
  `B_lms_plus_mastery_oulad` on student-grouped and temporal-forward splits.
- Secondary classification table for `passed_observed`.
- Interpretation section recording the mixed transfer result.

### 1.6 OULAD DDD full ablation (exp_006_oulad_full_ablation)

Source: [docs/experiments/exp_006_oulad_full_ablation.md](../experiments/exp_006_oulad_full_ablation.md)

- Full nested A/B/C ablation summary on real OULAD `DDD` `2013J`
  (67830 snapshots, 1938 students), ranked by RMSE for both the
  student-grouped and temporal-forward splits.
- The fixed-model re-analysis table in the summary that neutralizes the
  model-flip artifact (mastery temporal Δ −0.381, grouped +0.061; index
  block temporal −0.218; `C_twin_oulad` within ±0.025; `A_simple_oulad`
  clearly worse).
- The `passed` classification table (F1 0.83–0.887, never 1.000),
  establishing the mixed-to-null real-data result that supersedes the
  exp_005 "complicates" framing.

### 1.7 OULAD DDD XAI and regime-sensitivity (exp_007_xai_on_oulad)

Source: [docs/experiments/exp_007_xai_on_oulad.md](../experiments/exp_007_xai_on_oulad.md)

- Global permutation-plus-native importance table per feature set
  (`assessment_submission_rate_due_to_date` 0.28–0.38,
  `overall_mastery_proxy` 0.23–0.43, `is_unregistered_by_week` 0.13–0.20,
  VLE clickstream 0.02–0.06).
- Importance-concentration summary and the cross-split explanation
  stability table (Kendall τ `B_lms_oulad` 0.79,
  `B_lms_plus_mastery_oulad` 0.68, `C_twin_oulad` 0.55; Jaccard top-5
  1.00/1.00/0.67), establishing regime-sensitivity (none ≥ 0.90).

### 1.8 Synthetic faithfulness probe (exp_008_faithfulness_probe)

Source: [docs/experiments/exp_008_faithfulness_probe.md](../experiments/exp_008_faithfulness_probe.md)

- Methods-appendix probe table: final-week oracle-ordering Kendall
  τ = 1.0, `activity_score_to_date` share 0.108,
  `overall_mastery`↔`avg_assignment_score_to_date` Pearson r 0.994.
  This is a controlled faithfulness check, not a headline result.

### 1.9 OULAD BBB full ablation (exp_009_oulad_ablation_bbb2013j)

Source: [docs/experiments/exp_009_oulad_ablation_bbb2013j.md](../experiments/exp_009_oulad_ablation_bbb2013j.md)

- Full nested A/B/C ablation summary on real OULAD `BBB` `2013J`
  (2237 students, 80532 snapshots), ranked by RMSE for both splits.
- The fixed-model re-analysis table showing the heterogeneous result:
  mastery temporal-forward Δ −1.026 RMSE (5.284 vs 6.311), crossing the
  1.0 threshold DDD never did; `C_twin_oulad` temporal Δ −0.765;
  student-grouped every block within 0.087 (null, as DDD); trend and
  index null on both splits.
- The `passed` classification table (F1 0.87–0.93, never 1.000).

### 1.10 OULAD BBB XAI and cross-cohort stability (exp_010_xai_on_oulad_bbb2013j)

Source: [docs/experiments/exp_010_xai_on_oulad_bbb2013j.md](../experiments/exp_010_xai_on_oulad_bbb2013j.md)

- Global importance table for the BBB cohort and the importance-
  concentration summary.
- Cross-cohort stability table (DDD vs BBB Kendall τ 0.32–0.61, mean
  0.52, lower than within-cohort 0.55–0.79; Jaccard top-5 0.43–1.00),
  showing shared topology but unstable rankings across courses.

### 1.11 KU Leuven engagement-only PASSED (exp_011_kuleuven_engagement)

Source: [docs/experiments/exp_011_kuleuven_engagement.md](../experiments/exp_011_kuleuven_engagement.md)

- Engagement-only classification summary on KU Leuven 1819 (1495
  students, 2 courses pooled, weeks 2–15): `A_simple_engagement` vs
  `B_engagement`, fixed-model F1 0.75–0.76, ROC-AUC 0.65–0.72, with the
  richer-versus-minimal deltas (F1 Δ −0.015 temporal / +0.000 grouped).
- Engagement importance table (`cumulative_active_days_to_date` and
  `cumulative_clicks_to_date` dominate; active-days 0.456 share
  temporal). Mastery ablation cannot be built here — itself a cross-
  institution heterogeneity finding.

### 1.12 Cross-institution engagement synthesis (exp_012)

Source: [docs/experiments/exp_012_oulad_engagement.md](../experiments/exp_012_oulad_engagement.md),
with per-cohort writeups
[docs/experiments/exp_012_oulad_engagement_ddd2013j.md](../experiments/exp_012_oulad_engagement_ddd2013j.md)
and [docs/experiments/exp_012_oulad_engagement_bbb2013j.md](../experiments/exp_012_oulad_engagement_bbb2013j.md)

- Part A matched 3-institution fixed-model `B − A` F1 table
  (student_group DDD +0.072 / BBB +0.039 / KU +0.000; temporal_forward
  spread −0.016 to +0.026; ROC-AUC all six cells positive).
- Part B importance-rank stability table over 7 shared concepts (mean
  Kendall τ 0.56; most stable KU↔BBB τ 0.714, least KU↔DDD student_group
  τ 0.238; verdict `drivers_partly_institution_specific`). A robustness
  result, not an accuracy claim.

### 1.13 Cross-experiment progression

Source: [experiment_progression_summary.md](experiment_progression_summary.md)
and [docs/experiments/exp_001_vs_exp_002_comparison.md](../experiments/exp_001_vs_exp_002_comparison.md)

- The compact sequence table summarizing the experiment line by
  objective, comparison, target, splits, key result, and consequence.
- The before/after RMSE table comparing `exp_001_baseline` and
  `exp_002_twin_ablation`.

## 2. Artifact Files Containing Important Evidence

The machine-readable artifacts below should be cited or attached as
appendix material when the dissertation needs to refer to exact numbers.

### 2.1 exp_001_baseline

- `data/artifacts/experiments/exp_001_baseline/baseline_v1_results.csv`
- `data/artifacts/experiments/exp_001_baseline/baseline_v1_results.json`
- `data/artifacts/experiments/exp_001_baseline/baseline_v1_summary.md`
- `data/artifacts/experiments/exp_001_baseline/eda/eda_summary.json`
- `data/artifacts/experiments/exp_001_baseline/eda/eda_report.md`

### 2.2 exp_002_twin_ablation

- `data/artifacts/experiments/exp_002_twin_ablation/exp_002_twin_ablation_results.json`
- `data/artifacts/experiments/exp_002_twin_ablation/exp_002_twin_ablation_results.csv`
- `data/artifacts/experiments/exp_002_twin_ablation/exp_002_twin_ablation_summary.md`
- `data/artifacts/experiments/exp_002_twin_ablation/lean_twin_recommendation.md`

### 2.3 exp_003_mastery_validation

- `data/artifacts/experiments/exp_003_mastery_validation/exp_003_mastery_validation_results.json`
- `data/artifacts/experiments/exp_003_mastery_validation/exp_003_mastery_validation_results.csv`
- `data/artifacts/experiments/exp_003_mastery_validation/exp_003_mastery_validation_summary.md`
- `data/artifacts/experiments/exp_003_mastery_validation/mastery_diagnostics.json`
- `data/artifacts/experiments/exp_003_mastery_validation/mastery_weekly_validation.csv`
- `data/artifacts/experiments/exp_003_mastery_validation/mastery_carry_forward_recommendation.md`

### 2.4 exp_004_xai_on_lean_twin

- `data/artifacts/experiments/exp_004_xai_on_lean_twin/exp_004_xai_on_lean_twin_results.json`
- `data/artifacts/experiments/exp_004_xai_on_lean_twin/exp_004_xai_on_lean_twin_summary.md`
- `data/artifacts/experiments/exp_004_xai_on_lean_twin/global_feature_importance.csv`
- `data/artifacts/experiments/exp_004_xai_on_lean_twin/global_feature_importance.md`
- `data/artifacts/experiments/exp_004_xai_on_lean_twin/local_case_explanations.json`
- `data/artifacts/experiments/exp_004_xai_on_lean_twin/local_case_explanations.md`
- `data/artifacts/experiments/exp_004_xai_on_lean_twin/xai_carry_forward_recommendation.md`
- `data/artifacts/experiments/exp_004_xai_on_lean_twin/experiment_metadata.json`

### 2.5 exp_005_public_benchmark_oulad

- `data/artifacts/experiments/exp_005_public_benchmark_oulad/exp_005_public_benchmark_oulad_results.json`
- `data/artifacts/experiments/exp_005_public_benchmark_oulad/exp_005_public_benchmark_oulad_results.csv`
- `data/artifacts/experiments/exp_005_public_benchmark_oulad/exp_005_public_benchmark_oulad_summary.md`
- `data/artifacts/experiments/exp_005_public_benchmark_oulad/oulad_weekly_snapshots.csv`
- `data/artifacts/experiments/exp_005_public_benchmark_oulad/public_benchmark_mapping_summary.md`
- `data/artifacts/experiments/exp_005_public_benchmark_oulad/public_vs_synthetic_interpretation.md`
- `data/artifacts/experiments/exp_005_public_benchmark_oulad/experiment_metadata.json`

### 2.6 exp_006_oulad_full_ablation

- `data/artifacts/experiments/exp_006_oulad_full_ablation/exp_006_oulad_full_ablation_results.json`
- `data/artifacts/experiments/exp_006_oulad_full_ablation/exp_006_oulad_full_ablation_results.csv`
- `data/artifacts/experiments/exp_006_oulad_full_ablation/exp_006_oulad_full_ablation_summary.md` (includes the fixed-model re-analysis table)
- `data/artifacts/experiments/exp_006_oulad_full_ablation/oulad_weekly_snapshots.csv`
- `data/artifacts/experiments/exp_006_oulad_full_ablation/public_benchmark_mapping_summary.md`
- `data/artifacts/experiments/exp_006_oulad_full_ablation/public_vs_synthetic_interpretation.md`
- `data/artifacts/experiments/exp_006_oulad_full_ablation/experiment_metadata.json`

### 2.7 exp_007_xai_on_oulad

- `data/artifacts/experiments/exp_007_xai_on_oulad/exp_007_xai_on_oulad_results.json`
- `data/artifacts/experiments/exp_007_xai_on_oulad/exp_007_xai_on_oulad_summary.md`
- `data/artifacts/experiments/exp_007_xai_on_oulad/global_feature_importance.csv`
- `data/artifacts/experiments/exp_007_xai_on_oulad/explanation_stability.json` (cross-split Kendall τ / Jaccard)
- `data/artifacts/experiments/exp_007_xai_on_oulad/explanation_stability.md`
- `data/artifacts/experiments/exp_007_xai_on_oulad/oulad_weekly_snapshots.csv`
- `data/artifacts/experiments/exp_007_xai_on_oulad/experiment_metadata.json`

### 2.8 exp_008_faithfulness_probe

- `data/artifacts/experiments/exp_008_faithfulness_probe/exp_008_faithfulness_probe_results.json`
- `data/artifacts/experiments/exp_008_faithfulness_probe/exp_008_faithfulness_probe_summary.md`
- `data/artifacts/experiments/exp_008_faithfulness_probe/experiment_metadata.json`

### 2.9 exp_009_oulad_ablation_bbb2013j

- `data/artifacts/experiments/exp_009_oulad_ablation_bbb2013j/exp_009_oulad_ablation_bbb2013j_results.json`
- `data/artifacts/experiments/exp_009_oulad_ablation_bbb2013j/exp_009_oulad_ablation_bbb2013j_results.csv`
- `data/artifacts/experiments/exp_009_oulad_ablation_bbb2013j/exp_009_oulad_ablation_bbb2013j_summary.md` (includes the fixed-model re-analysis table, mastery temporal Δ −1.026)
- `data/artifacts/experiments/exp_009_oulad_ablation_bbb2013j/oulad_weekly_snapshots.csv`
- `data/artifacts/experiments/exp_009_oulad_ablation_bbb2013j/public_benchmark_mapping_summary.md`
- `data/artifacts/experiments/exp_009_oulad_ablation_bbb2013j/public_vs_synthetic_interpretation.md`
- `data/artifacts/experiments/exp_009_oulad_ablation_bbb2013j/experiment_metadata.json`

### 2.10 exp_010_xai_on_oulad_bbb2013j

- `data/artifacts/experiments/exp_010_xai_on_oulad_bbb2013j/exp_010_xai_on_oulad_bbb2013j_results.json`
- `data/artifacts/experiments/exp_010_xai_on_oulad_bbb2013j/exp_010_xai_on_oulad_bbb2013j_summary.md`
- `data/artifacts/experiments/exp_010_xai_on_oulad_bbb2013j/global_feature_importance.csv`
- `data/artifacts/experiments/exp_010_xai_on_oulad_bbb2013j/cross_cohort_stability.json` (DDD vs BBB Kendall τ / Jaccard)
- `data/artifacts/experiments/exp_010_xai_on_oulad_bbb2013j/cross_cohort_stability.md`
- `data/artifacts/experiments/exp_010_xai_on_oulad_bbb2013j/oulad_weekly_snapshots.csv`
- `data/artifacts/experiments/exp_010_xai_on_oulad_bbb2013j/experiment_metadata.json`

### 2.11 exp_011_kuleuven_engagement

- `data/artifacts/experiments/exp_011_kuleuven_engagement/exp_011_kuleuven_engagement_results.json`
- `data/artifacts/experiments/exp_011_kuleuven_engagement/exp_011_kuleuven_engagement_results.csv`
- `data/artifacts/experiments/exp_011_kuleuven_engagement/exp_011_kuleuven_engagement_summary.md`
- `data/artifacts/experiments/exp_011_kuleuven_engagement/engagement_importance.csv`
- `data/artifacts/experiments/exp_011_kuleuven_engagement/experiment_metadata.json`

### 2.12 exp_012 cross-institution engagement (DDD + BBB + KU 1819)

Per-cohort engagement artifacts:

- `data/artifacts/experiments/exp_012_oulad_engagement_ddd2013j/exp_012_oulad_engagement_ddd2013j_results.json`
- `data/artifacts/experiments/exp_012_oulad_engagement_ddd2013j/exp_012_oulad_engagement_ddd2013j_results.csv`
- `data/artifacts/experiments/exp_012_oulad_engagement_ddd2013j/exp_012_oulad_engagement_ddd2013j_summary.md`
- `data/artifacts/experiments/exp_012_oulad_engagement_ddd2013j/engagement_importance.csv`
- `data/artifacts/experiments/exp_012_oulad_engagement_ddd2013j/experiment_metadata.json`
- `data/artifacts/experiments/exp_012_oulad_engagement_bbb2013j/exp_012_oulad_engagement_bbb2013j_results.json`
- `data/artifacts/experiments/exp_012_oulad_engagement_bbb2013j/exp_012_oulad_engagement_bbb2013j_results.csv`
- `data/artifacts/experiments/exp_012_oulad_engagement_bbb2013j/exp_012_oulad_engagement_bbb2013j_summary.md`
- `data/artifacts/experiments/exp_012_oulad_engagement_bbb2013j/engagement_importance.csv`
- `data/artifacts/experiments/exp_012_oulad_engagement_bbb2013j/experiment_metadata.json`

Cross-institution synthesis (Part A accuracy deltas, Part B importance-rank stability):

- `data/artifacts/experiments/exp_012_cross_institution_engagement/cross_institution_engagement.json`
- `data/artifacts/experiments/exp_012_cross_institution_engagement/cross_institution_engagement.md`

### 2.13 Schema, data model, and realism artifacts

- `packages/contracts/schema_versions/schema_v1.2.yaml` (active contract)
- `docs/data_model/00_scope.md` through
  `docs/data_model/06_assumptions.md`
- `data/artifacts/reports/realism_metrics.json`
- `data/artifacts/reports/realism_report.md`

These artifacts ground the dissertation's data-contract claims and the
internal-realism argument.

## 3. Generated Dissertation Figures

The following figures were generated by
`scripts/generate_dissertation_assets.py`. The script reads only frozen
experiment artifacts and writes outputs under `docs/dissertation/figures/`.

| Figure | Source artifact | Purpose |
| --- | --- | --- |
| [exp_001_primary_rmse_comparison.svg](figures/exp_001_primary_rmse_comparison.svg) | `data/artifacts/experiments/exp_001_baseline/baseline_v1_results.json` | Shows the primary split RMSE comparison for `A_simple`, `B_lms`, and `C_twin`. |
| [exp_002_ablation_rmse_comparison.svg](figures/exp_002_ablation_rmse_comparison.svg) | `data/artifacts/experiments/exp_002_twin_ablation/exp_002_twin_ablation_results.json` | Shows the ablation result that identifies `B_lms_plus_mastery` as the best internal candidate. |
| [exp_003_weekly_mastery_delta.svg](figures/exp_003_weekly_mastery_delta.svg) | `data/artifacts/experiments/exp_003_mastery_validation/mastery_diagnostics.json` | Shows week-wise RMSE delta for `B_lms_plus_mastery` versus `B_lms`. |
| [exp_003_mastery_drop_column_effect.svg](figures/exp_003_mastery_drop_column_effect.svg) | `data/artifacts/experiments/exp_003_mastery_validation/mastery_diagnostics.json` | Shows the drop-column dependency on mastery features, especially `overall_mastery`. |
| [exp_004_global_importance_comparison.svg](figures/exp_004_global_importance_comparison.svg) | `data/artifacts/experiments/exp_004_xai_on_lean_twin/global_feature_importance.csv` | Shows top global permutation importance shares for the LMS baseline and lean Twin model. |
| [exp_005_oulad_rmse_comparison.svg](figures/exp_005_oulad_rmse_comparison.svg) | `data/artifacts/experiments/exp_005_public_benchmark_oulad/exp_005_public_benchmark_oulad_results.json` | Shows the mixed OULAD result across grouped and temporal-forward splits. |
| [final_experiment_sequence.svg](figures/final_experiment_sequence.svg) | Dissertation synthesis files and experiment metadata | Shows the dependency chain from `exp_001` through `exp_005`. |

> Note: SVG figure assets currently cover only `exp_001`–`exp_005`. Figure assets
> for `exp_006`–`exp_012` are not yet generated; until they are, the
> `exp_006`–`exp_012` tables and artifacts are indexed in §1 (Result Tables) and §2
> (Artifact Files).

## 4. Generated Dissertation Tables

The following Markdown tables were generated alongside the figures and can be
used as appendix-ready table assets.

| Table | Source artifact | Purpose |
| --- | --- | --- |
| [exp_001_best_rmse.md](tables/exp_001_best_rmse.md) | `exp_001_baseline/baseline_v1_results.json` | Primary RMSE comparison for the baseline experiment. |
| [exp_002_ablation_best_rmse.md](tables/exp_002_ablation_best_rmse.md) | `exp_002_twin_ablation/exp_002_twin_ablation_results.json` | Primary ablation table with delta versus `B_lms`. |
| [exp_003_weekly_mastery_delta.md](tables/exp_003_weekly_mastery_delta.md) | `exp_003_mastery_validation/mastery_diagnostics.json` | Week-wise candidate versus baseline delta table. |
| [exp_003_mastery_drop_column_effect.md](tables/exp_003_mastery_drop_column_effect.md) | `exp_003_mastery_validation/mastery_diagnostics.json` | Drop-column effect table for mastery features. |
| [exp_004_global_importance_top_features.md](tables/exp_004_global_importance_top_features.md) | `exp_004_xai_on_lean_twin/global_feature_importance.csv` | Top-five global importance rows for baseline and lean Twin. |
| [exp_005_oulad_benchmark_summary.md](tables/exp_005_oulad_benchmark_summary.md) | `exp_005_public_benchmark_oulad/exp_005_public_benchmark_oulad_results.json` | OULAD grouped and temporal-forward benchmark summary. |
| [final_experiment_sequence.md](tables/final_experiment_sequence.md) | Dissertation synthesis files and experiment metadata | Compact final package sequence table. |

## 5. Reuse Policy

The result tables in `docs/experiments/<experiment_id>.md` are the
canonical numerical references. The artifacts in
`data/artifacts/experiments/<experiment_id>/` are the canonical
machine-readable evidence. The dissertation should cite both when
appropriate: the writeups for human-readable summaries, and the artifacts
for exact numbers and reproducibility. This document should be updated
whenever a new experiment is added so that the dissertation source
material remains aligned with the repository.
