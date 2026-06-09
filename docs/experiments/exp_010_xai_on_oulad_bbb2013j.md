# exp_010_xai_on_oulad_bbb2013j: Second-cohort OULAD model-behavior XAI (BBB 2013J)

## Objective

Characterize which features drive the OULAD gradient-boosting regression model on the BBB 2013J cohort and how concentrated the explanations are.  The primary purpose is cross-course comparison with exp_007 (DDD 2013J): if explanation importance structure is stable across courses, the model-behavior findings generalise; if BBB shows a different pattern (particularly for mastery and clickstream features, given exp_009's finding that the mastery block improves temporal_forward on BBB unlike DDD), this pinpoints cohort-specific model behaviour worth investigating further.


## Hypothesis

If the OULAD model on BBB 2013J is primarily driven by assessment-score features (cumulative_assessment_weighted_score_to_date, overall_mastery_proxy) the explanations will be highly concentrated and dominated by the partial-circular target features, consistent with DDD.  However, given exp_009's result that the mastery block improves temporal_forward on BBB but not DDD, we hypothesise that overall_mastery_proxy and related mastery features will rank relatively higher on BBB than on DDD for the temporal_forward split.  Clickstream features (cumulative_*_clicks_to_date, current_week_clicks) should appear alongside assessment features in B_lms_oulad; is_unregistered_by_week may appear as a strong driver if BBB has a different withdrawal pattern.


## XAI method note

These are **model-behavior explanations**, not causal explanations and not structural-coefficient interpretations.  No SHAP is used.  The explanation layer consists of:

- **Permutation importance** (held-out RMSE increase when a feature is permuted, 15 repeats).
- **Model-native importance** (gradient-boosting feature importances).
- **Local one-feature perturbation** (replace one feature with its training median; measure prediction change).

Findings describe what the fitted model relies on, not what causes student outcomes.

## OULAD assessment-score partial circularity

`cumulative_assessment_weighted_score_to_date` partially feeds the regression target `final_weighted_score`.  Any high importance for this feature is **expected and does not reflect an exogenous causal signal** — it is a within-system accounting identity.  Interpretation should be weighted toward **exogenous clickstream features** (`cumulative_*_clicks_to_date`, `current_week_clicks`, `assessment_submission_rate_due_to_date`) which are not part of the target construction and are genuinely behavioural signals.

## Dataset / config used

- Experiment config: `services/ml/configs/experiments/exp_010_xai_on_oulad_bbb2013j.yaml`
- Raw directory: `datasets/oulad`
- Processed snapshots: `data/artifacts/experiments/exp_010_xai_on_oulad_bbb2013j/oulad_weekly_snapshots.csv`
- Output directory: `data/artifacts/experiments/exp_010_xai_on_oulad_bbb2013j`
- Course filter: `{'code_module': 'BBB', 'code_presentation': '2013J'}`
- Weeks: `4..39`

## Feature sets explained

### `B_lms_oulad`

Strong OULAD LMS-style baseline analogue using cumulative assessment performance, submission discipline, VLE activity intensity and category signals, course-week progression, and registration state.


Columns: `week_number`, `course_week_progress`, `is_registered_by_week`, `is_unregistered_by_week`, `days_since_registration_start`, `cumulative_assessment_score_mean_to_date`, `cumulative_assessment_score_count_to_date`, `cumulative_assessment_weighted_score_to_date`, `cumulative_submitted_weight_to_date`, `assessment_submission_rate_due_to_date`, `late_submission_rate_to_date`, `banked_assessment_rate_to_date`, `current_week_clicks`, `cumulative_clicks_to_date`, `current_week_activity_types`, `cumulative_assessment_clicks_to_date`, `cumulative_content_clicks_to_date`, `cumulative_social_clicks_to_date`, `cumulative_other_clicks_to_date`
Indicator columns: `has_assessment_score_to_date`, `has_weighted_score_to_date`, `has_vle_activity_to_date`

### `B_lms_plus_mastery_oulad`

OULAD LMS baseline analogue plus a lean mastery-like block derived from dated assessment structure: due-to-date weighted mastery, current assessment-cluster mastery, assessment-type mastery aggregates, and assessment-coverage context.


Columns: `week_number`, `course_week_progress`, `is_registered_by_week`, `is_unregistered_by_week`, `days_since_registration_start`, `cumulative_assessment_score_mean_to_date`, `cumulative_assessment_score_count_to_date`, `cumulative_assessment_weighted_score_to_date`, `cumulative_submitted_weight_to_date`, `assessment_submission_rate_due_to_date`, `late_submission_rate_to_date`, `banked_assessment_rate_to_date`, `current_week_clicks`, `cumulative_clicks_to_date`, `current_week_activity_types`, `cumulative_assessment_clicks_to_date`, `cumulative_content_clicks_to_date`, `cumulative_social_clicks_to_date`, `cumulative_other_clicks_to_date`, `overall_mastery_proxy`, `current_assessment_cluster_mastery`, `tma_mastery_to_date`, `cma_mastery_to_date`, `exam_mastery_to_date`, `mastery_assessment_coverage_to_date`
Indicator columns: `has_assessment_score_to_date`, `has_weighted_score_to_date`, `has_vle_activity_to_date`, `has_current_assessment_cluster`, `has_due_assessment_to_date`

### `C_twin_oulad`

Full OULAD twin analogue: LMS baseline + trends + mastery block + composite indices.

Columns: `week_number`, `course_week_progress`, `is_registered_by_week`, `is_unregistered_by_week`, `days_since_registration_start`, `cumulative_assessment_score_mean_to_date`, `cumulative_assessment_score_count_to_date`, `cumulative_assessment_weighted_score_to_date`, `cumulative_submitted_weight_to_date`, `assessment_submission_rate_due_to_date`, `late_submission_rate_to_date`, `banked_assessment_rate_to_date`, `current_week_clicks`, `cumulative_clicks_to_date`, `current_week_activity_types`, `cumulative_assessment_clicks_to_date`, `cumulative_content_clicks_to_date`, `cumulative_social_clicks_to_date`, `cumulative_other_clicks_to_date`, `assessment_score_trend_to_date`, `clicks_trend_to_date`, `overall_mastery_proxy`, `current_assessment_cluster_mastery`, `tma_mastery_to_date`, `cma_mastery_to_date`, `exam_mastery_to_date`, `mastery_assessment_coverage_to_date`, `engagement_index_oulad`, `performance_index_oulad`, `discipline_index_oulad`
Indicator columns: `has_assessment_score_to_date`, `has_weighted_score_to_date`, `has_vle_activity_to_date`, `has_current_assessment_cluster`, `has_due_assessment_to_date`

## Splits

- student_group: test_size=0.25, seed=42
- temporal_forward (headline): train_weeks=20, student_test_size=0.25, student_seed=42

## Results: global feature importance

### B_lms_oulad / student_group

| metric | value |
| --- | ---: |
| RMSE | 10.6970 |
| MAE | 5.7703 |
| R² | 0.8937 |
| train rows | 60408 |
| test rows | 20124 |

**Concentration**

- Top feature: `assessment_submission_rate_due_to_date`
- Top-1 share: 0.3749
- Top-3 share: 0.8348
- Herfindahl index: 0.2820
- Features with positive importance: 18

**Top-10 features by importance share**

| rank | feature | importance_share | mean_rmse_increase | native_importance | direction |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | `assessment_submission_rate_due_to_date` | 0.3749 | 13.5215 | 0.8280 | higher values generally align with higher predicted final_grade |
| 2 | `cumulative_submitted_weight_to_date` | 0.3511 | 12.6621 | 0.0402 | higher values generally align with higher predicted final_grade |
| 3 | `cumulative_assessment_weighted_score_to_date` | 0.1088 | 3.9224 | 0.0781 | higher values generally align with higher predicted final_grade |
| 4 | `is_unregistered_by_week` | 0.0668 | 2.4081 | 0.0020 | higher values generally align with lower predicted final_grade |
| 5 | `cumulative_assessment_score_count_to_date` | 0.0340 | 1.2255 | 0.0034 | higher values generally align with higher predicted final_grade |
| 6 | `current_week_clicks` | 0.0184 | 0.6631 | 0.0169 | higher values generally align with higher predicted final_grade |
| 7 | `cumulative_content_clicks_to_date` | 0.0145 | 0.5221 | 0.0007 | higher values generally align with higher predicted final_grade |
| 8 | `cumulative_assessment_clicks_to_date` | 0.0074 | 0.2686 | 0.0077 | higher values generally align with higher predicted final_grade |
| 9 | `late_submission_rate_to_date` | 0.0057 | 0.2062 | 0.0069 | higher values generally align with higher predicted final_grade |
| 10 | `current_week_activity_types` | 0.0053 | 0.1922 | 0.0054 | higher values generally align with higher predicted final_grade |

### B_lms_oulad / temporal_forward

| metric | value |
| --- | ---: |
| RMSE | 6.3108 |
| MAE | 4.1238 |
| R² | 0.9630 |
| train rows | 28526 |
| test rows | 10621 |

**Concentration**

- Top feature: `cumulative_submitted_weight_to_date`
- Top-1 share: 0.3525
- Top-3 share: 0.7452
- Herfindahl index: 0.2326
- Features with positive importance: 16

**Top-10 features by importance share**

| rank | feature | importance_share | mean_rmse_increase | native_importance | direction |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | `cumulative_submitted_weight_to_date` | 0.3525 | 16.6662 | 0.0336 | higher values generally align with higher predicted final_grade |
| 2 | `assessment_submission_rate_due_to_date` | 0.2953 | 13.9619 | 0.7621 | higher values generally align with higher predicted final_grade |
| 3 | `cumulative_assessment_weighted_score_to_date` | 0.0974 | 4.6060 | 0.0850 | higher values generally align with higher predicted final_grade |
| 4 | `cumulative_assessment_score_count_to_date` | 0.0819 | 3.8743 | 0.0050 | higher values generally align with higher predicted final_grade |
| 5 | `cumulative_content_clicks_to_date` | 0.0434 | 2.0509 | 0.0029 | higher values generally align with higher predicted final_grade |
| 6 | `is_unregistered_by_week` | 0.0418 | 1.9741 | 0.0078 | higher values generally align with lower predicted final_grade |
| 7 | `cumulative_assessment_clicks_to_date` | 0.0228 | 1.0777 | 0.0079 | higher values generally align with higher predicted final_grade |
| 8 | `cumulative_clicks_to_date` | 0.0151 | 0.7149 | 0.0019 | higher values generally align with higher predicted final_grade |
| 9 | `current_week_clicks` | 0.0149 | 0.7040 | 0.0304 | higher values generally align with higher predicted final_grade |
| 10 | `late_submission_rate_to_date` | 0.0128 | 0.6029 | 0.0139 | higher values generally align with higher predicted final_grade |

### B_lms_plus_mastery_oulad / student_group

| metric | value |
| --- | ---: |
| RMSE | 10.6202 |
| MAE | 5.6234 |
| R² | 0.8952 |
| train rows | 60408 |
| test rows | 20124 |

**Concentration**

- Top feature: `overall_mastery_proxy`
- Top-1 share: 0.6109
- Top-3 share: 0.8198
- Herfindahl index: 0.4021
- Features with positive importance: 26

**Top-10 features by importance share**

| rank | feature | importance_share | mean_rmse_increase | native_importance | direction |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | `overall_mastery_proxy` | 0.6109 | 15.1440 | 0.7549 | higher values generally align with higher predicted final_grade |
| 2 | `is_unregistered_by_week` | 0.1312 | 3.2513 | 0.0018 | higher values generally align with lower predicted final_grade |
| 3 | `cumulative_submitted_weight_to_date` | 0.0777 | 1.9248 | 0.0116 | higher values generally align with higher predicted final_grade |
| 4 | `tma_mastery_to_date` | 0.0556 | 1.3792 | 0.1781 | higher values generally align with higher predicted final_grade |
| 5 | `cumulative_assessment_clicks_to_date` | 0.0325 | 0.8056 | 0.0160 | higher values generally align with higher predicted final_grade |
| 6 | `current_week_clicks` | 0.0309 | 0.7657 | 0.0066 | higher values generally align with higher predicted final_grade |
| 7 | `cumulative_assessment_weighted_score_to_date` | 0.0164 | 0.4053 | 0.0079 | higher values generally align with higher predicted final_grade |
| 8 | `assessment_submission_rate_due_to_date` | 0.0107 | 0.2642 | 0.0049 | higher values generally align with higher predicted final_grade |
| 9 | `cumulative_content_clicks_to_date` | 0.0073 | 0.1817 | 0.0006 | higher values generally align with higher predicted final_grade |
| 10 | `cumulative_assessment_score_mean_to_date` | 0.0054 | 0.1347 | 0.0037 | higher values generally align with higher predicted final_grade |

### B_lms_plus_mastery_oulad / temporal_forward

| metric | value |
| --- | ---: |
| RMSE | 5.2844 |
| MAE | 3.4259 |
| R² | 0.9741 |
| train rows | 28526 |
| test rows | 10621 |

**Concentration**

- Top feature: `overall_mastery_proxy`
- Top-1 share: 0.3991
- Top-3 share: 0.6511
- Herfindahl index: 0.2100
- Features with positive importance: 19

**Top-10 features by importance share**

| rank | feature | importance_share | mean_rmse_increase | native_importance | direction |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | `overall_mastery_proxy` | 0.3991 | 14.5935 | 0.6157 | higher values generally align with higher predicted final_grade |
| 2 | `cumulative_submitted_weight_to_date` | 0.1280 | 4.6794 | 0.0074 | higher values generally align with higher predicted final_grade |
| 3 | `tma_mastery_to_date` | 0.1240 | 4.5323 | 0.2531 | higher values generally align with higher predicted final_grade |
| 4 | `is_unregistered_by_week` | 0.0913 | 3.3396 | 0.0065 | higher values generally align with lower predicted final_grade |
| 5 | `cumulative_assessment_weighted_score_to_date` | 0.0626 | 2.2877 | 0.0216 | higher values generally align with higher predicted final_grade |
| 6 | `cumulative_content_clicks_to_date` | 0.0466 | 1.7025 | 0.0026 | higher values generally align with higher predicted final_grade |
| 7 | `cumulative_clicks_to_date` | 0.0464 | 1.6956 | 0.0035 | higher values generally align with higher predicted final_grade |
| 8 | `cumulative_assessment_clicks_to_date` | 0.0333 | 1.2174 | 0.0186 | higher values generally align with higher predicted final_grade |
| 9 | `current_week_clicks` | 0.0289 | 1.0565 | 0.0194 | higher values generally align with higher predicted final_grade |
| 10 | `cumulative_social_clicks_to_date` | 0.0156 | 0.5686 | 0.0044 | higher values generally align with higher predicted final_grade |

### C_twin_oulad / student_group

| metric | value |
| --- | ---: |
| RMSE | 10.6103 |
| MAE | 5.6045 |
| R² | 0.8954 |
| train rows | 60408 |
| test rows | 20124 |

**Concentration**

- Top feature: `overall_mastery_proxy`
- Top-1 share: 0.6330
- Top-3 share: 0.8419
- Herfindahl index: 0.4295
- Features with positive importance: 28

**Top-10 features by importance share**

| rank | feature | importance_share | mean_rmse_increase | native_importance | direction |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | `overall_mastery_proxy` | 0.6330 | 15.9461 | 0.7494 | higher values generally align with higher predicted final_grade |
| 2 | `is_unregistered_by_week` | 0.1419 | 3.5744 | 0.0021 | higher values generally align with lower predicted final_grade |
| 3 | `cumulative_submitted_weight_to_date` | 0.0670 | 1.6881 | 0.0110 | higher values generally align with higher predicted final_grade |
| 4 | `tma_mastery_to_date` | 0.0458 | 1.1526 | 0.1765 | higher values generally align with higher predicted final_grade |
| 5 | `current_week_clicks` | 0.0344 | 0.8656 | 0.0058 | higher values generally align with higher predicted final_grade |
| 6 | `cumulative_assessment_clicks_to_date` | 0.0257 | 0.6463 | 0.0151 | higher values generally align with higher predicted final_grade |
| 7 | `discipline_index_oulad` | 0.0095 | 0.2383 | 0.0057 | higher values generally align with higher predicted final_grade |
| 8 | `performance_index_oulad` | 0.0070 | 0.1772 | 0.0127 | higher values generally align with higher predicted final_grade |
| 9 | `cumulative_assessment_weighted_score_to_date` | 0.0055 | 0.1376 | 0.0029 | higher values generally align with higher predicted final_grade |
| 10 | `cumulative_content_clicks_to_date` | 0.0051 | 0.1294 | 0.0006 | higher values generally align with higher predicted final_grade |

### C_twin_oulad / temporal_forward

| metric | value |
| --- | ---: |
| RMSE | 5.5461 |
| MAE | 3.6194 |
| R² | 0.9714 |
| train rows | 28526 |
| test rows | 10621 |

**Concentration**

- Top feature: `overall_mastery_proxy`
- Top-1 share: 0.3440
- Top-3 share: 0.6350
- Herfindahl index: 0.1819
- Features with positive importance: 20

**Top-10 features by importance share**

| rank | feature | importance_share | mean_rmse_increase | native_importance | direction |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | `overall_mastery_proxy` | 0.3440 | 10.8823 | 0.6093 | higher values generally align with higher predicted final_grade |
| 2 | `is_unregistered_by_week` | 0.1559 | 4.9324 | 0.0062 | higher values generally align with lower predicted final_grade |
| 3 | `cumulative_submitted_weight_to_date` | 0.1351 | 4.2746 | 0.0093 | higher values generally align with higher predicted final_grade |
| 4 | `tma_mastery_to_date` | 0.1116 | 3.5301 | 0.2358 | higher values generally align with higher predicted final_grade |
| 5 | `cumulative_assessment_weighted_score_to_date` | 0.0545 | 1.7229 | 0.0112 | higher values generally align with higher predicted final_grade |
| 6 | `cumulative_clicks_to_date` | 0.0450 | 1.4225 | 0.0045 | higher values generally align with higher predicted final_grade |
| 7 | `performance_index_oulad` | 0.0316 | 1.0000 | 0.0286 | higher values generally align with higher predicted final_grade |
| 8 | `cumulative_content_clicks_to_date` | 0.0308 | 0.9743 | 0.0025 | higher values generally align with higher predicted final_grade |
| 9 | `cumulative_social_clicks_to_date` | 0.0227 | 0.7166 | 0.0033 | higher values generally align with higher predicted final_grade |
| 10 | `current_week_clicks` | 0.0218 | 0.6903 | 0.0164 | higher values generally align with higher predicted final_grade |

## Limitations

- These are model-behavior explanations under gradient_boosting; a different model family may produce different importance orderings.

- The OULAD regression target (final_weighted_score) is partially circular on assessment-score features; high importance for those features cannot be read as an exogenous causal signal.

- Permutation importance can be unreliable when correlated features are present; the mastery block features are correlated with assessment-score features, so importances may understate mastery's marginal contribution.

- Local perturbation explanations use training-median as the reference; this is not a Shapley baseline and may understate or overstate contribution for skewed distributions.

- This experiment does not establish causal or institutional claims; findings are bounded to model behavior on the BBB 2013J subset.

- Cross-course comparison with exp_007 (DDD 2013J) is qualitative; formal statistical tests for importance-rank stability are not performed.


## Next step

Compare the per-(feature_set, split) top-3 importance rankings and concentration metrics against exp_007 (DDD 2013J).  If clickstream features rank higher on BBB than DDD (especially under temporal_forward), this strengthens the claim that the model captures genuine engagement signals independent of target circularity.  If overall_mastery_proxy ranks higher on BBB temporal_forward (consistent with exp_009's ablation result), foreground this in the dissertation XAI narrative as evidence that the mastery block adds explanation value in courses where mastery signal generalises temporally.

