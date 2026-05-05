# Figures and Tables Inventory

This inventory lists the existing repository artifacts that are most useful
as evidence for the dissertation. It is divided into result tables that can
be reused with light reformatting, artifact files that contain the
machine-readable evidence behind the headline numbers, and candidate
figures that could be produced later from the same artifacts. The aim is
to make it easy to cite repository evidence directly without re-running
experiments.

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

### 1.5 Cross-experiment progression

Source: [experiment_progression_summary.md](experiment_progression_summary.md)
and [docs/experiments/exp_001_vs_exp_002_comparison.md](../experiments/exp_001_vs_exp_002_comparison.md)

- The compact sequence table summarizing all four experiments by
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

### 2.5 Schema, data model, and realism artifacts

- `packages/contracts/schema_versions/schema_v1.2.yaml` (active contract)
- `docs/data_model/00_scope.md` through
  `docs/data_model/06_assumptions.md`
- `data/artifacts/reports/realism_metrics.json`
- `data/artifacts/reports/realism_report.md`

These artifacts ground the dissertation's data-contract claims and the
internal-realism argument.

## 3. Candidate Figures to Create Later

The repository currently contains tabular evidence rather than figures.
The following figures could be produced later from the same artifacts
without rerunning experiments. Each is a candidate, not a commitment.

| Candidate figure | Source artifact | Purpose |
| --- | --- | --- |
| RMSE bar chart per feature set, primary split | `exp_001_baseline` and `exp_002_twin_ablation` results CSV | Visualizes the central representation comparison and the lean candidate's advantage. |
| RMSE bar chart per feature set, temporal-forward split | same | Visualizes the asymmetry between primary and forward splits and the deterioration of `C_twin_full`. |
| Per-week delta line chart of `B_lms_plus_mastery` versus `B_lms` | `exp_003_mastery_validation/mastery_weekly_validation.csv` | Visualizes the early-week improvement pattern (weeks 4–8). |
| Drop-column delta bar chart for `B_lms_plus_mastery` | `exp_003_mastery_validation/mastery_diagnostics.json` | Visualizes the dependence on `overall_mastery`. |
| Top-feature permutation importance horizontal bar chart per feature set | `exp_004_xai_on_lean_twin/global_feature_importance.csv` | Visualizes the dominance of `activity_score_to_date` and the position of `overall_mastery`. |
| Local-case panel for the five representative cases | `exp_004_xai_on_lean_twin/local_case_explanations.json` | Visualizes the directional contributions per case. |
| Decision-chain diagram | this directory | Visualizes the dependency `exp_001 → exp_002 → exp_003 → exp_004`. |
| Mastery vs `final_grade` scatter or per-week correlation line | `exp_003_mastery_validation` | Visualizes the redundancy concern and the closeness of `overall_mastery` to `final_grade`. |

When figures are produced, they should be exported into a dedicated
subdirectory (for example `docs/dissertation/figures/`) and indexed back
into this inventory with their source artifact paths preserved.

## 4. Reuse Policy

The result tables in `docs/experiments/<experiment_id>.md` are the
canonical numerical references. The artifacts in
`data/artifacts/experiments/<experiment_id>/` are the canonical
machine-readable evidence. The dissertation should cite both when
appropriate: the writeups for human-readable summaries, and the artifacts
for exact numbers and reproducibility. This document should be updated
whenever a new experiment is added so that the dissertation source
material remains aligned with the repository.
