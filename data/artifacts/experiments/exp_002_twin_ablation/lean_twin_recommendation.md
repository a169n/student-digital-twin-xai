# exp_002_twin_ablation: Twin subgroup ablation

## Objective

Test which Digital Twin feature subgroups add predictive value beyond the `B_lms` baseline for the primary `final_grade` regression target.


## Hypothesis

The full Twin feature set is expected to be partly redundant because the baseline experiment showed that `C_twin` did not reliably outperform `B_lms`; a smaller subset may retain any useful Twin signal with less collinearity.


## Dataset / config used

- Schema version: `v1.2`
- Dataset version/config: `v1_3_refined` / `generator_v1_3_refined.yaml`
- Experiment config: `services/ml/configs/experiments/exp_002_twin_ablation.yaml`
- Snapshot table: `data/processed/student_twin_snapshots.csv`
- Final results table: `data/raw/final_results.csv`
- Output directory: `data/artifacts/experiments/exp_002_twin_ablation`

## Experimental setup

- Primary target: `final_grade`
- Secondary context target: `passed`
- Explicitly excluded as supervised target: `risk_level`
- Primary split: `student_group`
- Secondary split: `temporal_forward`
- Seed: `42`

## Feature sets

| feature set | columns | intent |
| --- | ---: | --- |
| B_lms | 11 | Stronger non-twin LMS baseline. Adds broader behavioral and submission-discipline signals that a typical LMS analytics view could plausibly expose without any digital-twin engineering. |
| B_lms_plus_trends | 14 | LMS baseline plus short-horizon trend features. Tests whether recent direction of performance, activity, and attendance adds predictive value beyond cumulative LMS indicators. |
| B_lms_plus_mastery | 13 | LMS baseline plus current and overall mastery proxies. Tests whether topic-level Twin state adds value beyond raw performance and activity. |
| B_lms_plus_indices | 14 | LMS baseline plus composite engagement, performance, and discipline indices. Tests whether the current index layer adds compact value or mostly duplicates the underlying LMS signals. |
| B_lms_plus_temporal | 12 | LMS baseline plus the snapshot week number. Tests whether coarse course-time context explains gains separately from richer trend or mastery features. |
| B_lms_plus_trends_mastery | 16 | Compact Twin candidate combining the LMS baseline with trend and mastery blocks while excluding composite indices. Intended as a lean candidate for the later XAI phase if it is competitive with the full Twin set. |
| C_twin_full | 20 | Alias for the full Digital Twin representation used in ablation reports. Kept separate from `C_twin` naming so the baseline and ablation experiment pages can be cited cleanly. |

## Models

- Regression: `linear_regression, random_forest, gradient_boosting`
- Classification: `logistic_regression, random_forest, gradient_boosting`

## Main metrics

Primary regression summary. Lower RMSE is better. `delta_vs_B_lms_rmse` is computed within the same split, after selecting the best model for each feature set.

| split | feature set | best model | features | RMSE | MAE | R^2 | delta vs `B_lms` |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| student_group | B_lms_plus_mastery | gradient_boosting | 13 | 1.894 | 1.510 | 0.992 | -0.206 |
| student_group | B_lms_plus_trends_mastery | gradient_boosting | 16 | 1.973 | 1.573 | 0.991 | -0.127 |
| student_group | B_lms_plus_indices | gradient_boosting | 14 | 2.035 | 1.567 | 0.990 | -0.066 |
| student_group | B_lms_plus_temporal | gradient_boosting | 12 | 2.078 | 1.657 | 0.990 | -0.023 |
| student_group | B_lms_plus_trends | gradient_boosting | 14 | 2.096 | 1.672 | 0.990 | -0.005 |
| student_group | B_lms | gradient_boosting | 11 | 2.101 | 1.681 | 0.990 | +0.000 |
| student_group | C_twin_full | random_forest | 20 | 2.149 | 1.732 | 0.989 | +0.049 |
| temporal_forward | B_lms_plus_indices | linear_regression | 14 | 2.202 | 1.732 | 0.989 | -0.068 |
| temporal_forward | B_lms | linear_regression | 11 | 2.270 | 1.778 | 0.988 | +0.000 |
| temporal_forward | B_lms_plus_mastery | linear_regression | 13 | 2.276 | 1.776 | 0.988 | +0.006 |
| temporal_forward | B_lms_plus_trends | linear_regression | 14 | 2.531 | 1.997 | 0.985 | +0.261 |
| temporal_forward | B_lms_plus_trends_mastery | linear_regression | 16 | 2.555 | 2.024 | 0.985 | +0.284 |
| temporal_forward | B_lms_plus_temporal | linear_regression | 12 | 2.658 | 2.166 | 0.984 | +0.388 |
| temporal_forward | C_twin_full | linear_regression | 20 | 2.937 | 2.396 | 0.980 | +0.667 |

Secondary classification context for `passed`. This is reported to show whether pass/fail behavior changes, but it is not the main selection criterion for the ablation.

| split | feature set | best model | F1 | accuracy | roc_auc |
| --- | --- | --- | ---: | ---: | ---: |
| student_group | B_lms | logistic_regression | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_indices | logistic_regression | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_mastery | logistic_regression | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_temporal | logistic_regression | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_trends | logistic_regression | 1.000 | 1.000 | 1.000 |
| student_group | B_lms_plus_trends_mastery | logistic_regression | 1.000 | 1.000 | 1.000 |
| student_group | C_twin_full | logistic_regression | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms | logistic_regression | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_indices | logistic_regression | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_mastery | logistic_regression | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_temporal | logistic_regression | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_trends | logistic_regression | 1.000 | 1.000 | 1.000 |
| temporal_forward | B_lms_plus_trends_mastery | logistic_regression | 1.000 | 1.000 | 1.000 |
| temporal_forward | C_twin_full | logistic_regression | 1.000 | 1.000 | 1.000 |

## Interpretation

`B_lms_plus_mastery` improves on `B_lms` enough to justify carrying that compact subset forward. The full Twin set is not currently justified.

## Lean Twin recommendation

- Best full Twin set: `C_twin_full`
- Best lean set: `B_lms_plus_mastery`
- Carry forward: `B_lms_plus_mastery`
- Full `C_twin` justified now: `False`
- Short conclusion: Carry forward `B_lms_plus_mastery`; full Twin justified: False.

## Artifact paths

- Results JSON: `data/artifacts/experiments/exp_002_twin_ablation/exp_002_twin_ablation_results.json`
- Results CSV: `data/artifacts/experiments/exp_002_twin_ablation/exp_002_twin_ablation_results.csv`
- Runner summary: `data/artifacts/experiments/exp_002_twin_ablation/exp_002_twin_ablation_summary.md`
- Lean recommendation artifact: `data/artifacts/experiments/exp_002_twin_ablation/lean_twin_recommendation.md`

## Limitations

- The experiment uses the current synthetic refined dataset only; results should not be interpreted as validated institutional findings.

- The ablation tests grouped feature blocks, not every individual feature, to keep the comparison interpretable.

- `passed` is reported only as secondary context because it is very easy on the current generated data.


## Next step

Carry the selected lean feature set into the future explanation phase only after reviewing redundancy and deciding whether the generator needs further realism calibration.

