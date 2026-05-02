# exp_001_baseline: Baseline feature-set comparison

## Objective

Establish the first reproducible modeling baseline for the current refined
dataset by comparing simple academic, LMS-style, and full Digital Twin feature
sets.

## Hypothesis

The full Digital Twin feature set might improve `final_grade` prediction over
LMS-style features, but the comparison should reveal whether the engineered Twin
layer adds signal or mostly duplicates existing LMS aggregates.

## Dataset / config used

- Schema version: `v1.2`
- Dataset version/config: `v1_3_refined` / `generator_v1_3_refined.yaml`
- Experiment config: `services/ml/configs/experiments/exp_001_baseline.yaml`
- Original baseline config: `services/ml/configs/experiments_baseline.yaml`
- Snapshot table: `data/processed/student_twin_snapshots.csv`
- Final results table: `data/raw/final_results.csv`
- Preserved artifacts: `data/artifacts/experiments/exp_001_baseline/`

## Experimental Setup

- Primary target: `final_grade`
- Secondary context target: `passed`
- Explicitly excluded as supervised target: `risk_level`
- Snapshot filter: weeks `4..10`
- Primary split: grouped by `student_id`
- Secondary split: temporal-forward with held-out students
- Seed: `42`

## Feature Sets

| feature set | intent |
| --- | --- |
| `A_simple` | Minimal academic baseline using score averages and attendance. |
| `B_lms` | LMS baseline adding activity, time on platform, submission discipline, and missingness indicators. |
| `C_twin` | Full Twin set adding trends, mastery proxies, composite indices, and week context. |

## Models

- Regression: Ridge, random forest, gradient boosting
- Classification: logistic regression, random forest, gradient boosting

## Main Metrics

Best `final_grade` RMSE by split and feature set:

| split | `A_simple` | `B_lms` | `C_twin` | interpretation |
| --- | ---: | ---: | ---: | --- |
| student_group | 2.673 | 2.101 | 2.149 | `B_lms` was slightly better than full Twin. |
| temporal_forward | 2.210 | 2.270 | 2.937 | Full Twin degraded under the stricter forward split. |

The `passed` classification task was nearly saturated across feature sets, with
best F1 at `1.000` for all three sets on both splits. This makes `passed` useful
only as secondary context for the current synthetic dataset.

## Interpretation

The baseline is valid and reproducible, but it does not justify carrying the
full `C_twin` feature set forward uncritically. The strongest finding is
negative but useful: the current Twin layer contains redundancy, and richer
engineered features do not yet clearly outperform the stronger LMS baseline.

## Limitations

- Results use the current synthetic refined dataset only.
- `passed` is too easy in this dataset and should not drive feature-set choice.
- The baseline compares only coarse feature sets, not Twin subgroups.
- No SHAP or XAI artifacts are produced in this phase.

## Next Step

Run a targeted Twin subgroup ablation to identify which parts of the Twin layer,
if any, add value beyond `B_lms` before beginning the future XAI phase.

## Artifact Paths

- Preserved CSV results: `data/artifacts/experiments/exp_001_baseline/baseline_v1_results.csv`
- Preserved results: `data/artifacts/experiments/exp_001_baseline/baseline_v1_results.json`
- Preserved summary: `data/artifacts/experiments/exp_001_baseline/baseline_v1_summary.md`
- Preserved EDA summary: `data/artifacts/experiments/exp_001_baseline/eda/eda_summary.json`
- Preserved EDA report: `data/artifacts/experiments/exp_001_baseline/eda/eda_report.md`
- Original loose results remain available under `data/artifacts/experiments/baselines/`
