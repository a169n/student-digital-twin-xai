# exp_007_xai_on_oulad: OULAD model-behavior XAI: feature importance and concentration (DDD 2013J)

## Objective

Characterize which features drive the OULAD gradient-boosting regression model and how concentrated the explanations are, given exp_006's mixed-to-null improvement result across the nested ablation.  The goal is not to explain a "winning" model — the focus is on model behavior and explanation stability across the three most informative feature sets (LMS baseline, mastery augmented, full twin analogue).


## Hypothesis

If the OULAD model is primarily driven by assessment-score features (cumulative_assessment_weighted_score_to_date, overall_mastery_proxy) the explanations will be highly concentrated and dominated by the partial-circular target features.  If clickstream features (cumulative_*_clicks_to_date, current_week_clicks) rank highly alongside or above assessment-score features, this provides evidence of genuine behavioral signal beyond the accounting identity in the target construction.  We expect assessment-score features to dominate in B_lms_oulad; mastery features to appear in the top-5 for B_lms_plus_mastery_oulad; and C_twin_oulad to show either concentration in assessment/mastery features or moderate spread across the wider feature set.


## XAI method note

These are **model-behavior explanations**, not causal explanations and not structural-coefficient interpretations.  No SHAP is used.  The explanation layer consists of:

- **Permutation importance** (held-out RMSE increase when a feature is permuted, 15 repeats).
- **Model-native importance** (gradient-boosting feature importances).
- **Local one-feature perturbation** (replace one feature with its training median; measure prediction change).

Findings describe what the fitted model relies on, not what causes student outcomes.

## OULAD assessment-score partial circularity

`cumulative_assessment_weighted_score_to_date` partially feeds the regression target `final_weighted_score`.  Any high importance for this feature is **expected and does not reflect an exogenous causal signal** — it is a within-system accounting identity.  Interpretation should be weighted toward **exogenous clickstream features** (`cumulative_*_clicks_to_date`, `current_week_clicks`, `assessment_submission_rate_due_to_date`) which are not part of the target construction and are genuinely behavioural signals.

## Dataset / config used

- Experiment config: `services/ml/configs/experiments/exp_007_xai_on_oulad.yaml`
- Raw directory: `datasets/oulad`
- Processed snapshots: `data/artifacts/experiments/exp_007_xai_on_oulad/oulad_weekly_snapshots.csv`
- Output directory: `data/artifacts/experiments/exp_007_xai_on_oulad`
- Course filter: `{'code_module': 'DDD', 'code_presentation': '2013J'}`
- Weeks: `4..38`

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
| RMSE | 12.6598 |
| MAE | 7.8907 |
| R² | 0.8554 |
| train rows | 50890 |
| test rows | 16940 |

**Concentration**

- Top feature: `assessment_submission_rate_due_to_date`
- Top-1 share: 0.3807
- Top-3 share: 0.6696
- Herfindahl index: 0.2130
- Features with positive importance: 17

**Top-10 features by importance share**

| rank | feature | importance_share | mean_rmse_increase | native_importance | direction |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | `assessment_submission_rate_due_to_date` | 0.3807 | 10.7422 | 0.7112 | higher values generally align with higher predicted final_grade |
| 2 | `cumulative_submitted_weight_to_date` | 0.1541 | 4.3474 | 0.0448 | higher values generally align with higher predicted final_grade |
| 3 | `is_unregistered_by_week` | 0.1348 | 3.8047 | 0.0071 | higher values generally align with lower predicted final_grade |
| 4 | `cumulative_assessment_score_mean_to_date` | 0.1221 | 3.4446 | 0.1344 | higher values generally align with higher predicted final_grade |
| 5 | `cumulative_assessment_weighted_score_to_date` | 0.0935 | 2.6390 | 0.0319 | higher values generally align with higher predicted final_grade |
| 6 | `current_week_clicks` | 0.0382 | 1.0778 | 0.0197 | higher values generally align with higher predicted final_grade |
| 7 | `cumulative_clicks_to_date` | 0.0237 | 0.6677 | 0.0201 | higher values generally align with higher predicted final_grade |
| 8 | `cumulative_content_clicks_to_date` | 0.0162 | 0.4557 | 0.0013 | higher values generally align with higher predicted final_grade |
| 9 | `cumulative_social_clicks_to_date` | 0.0112 | 0.3152 | 0.0035 | higher values generally align with higher predicted final_grade |
| 10 | `current_week_activity_types` | 0.0084 | 0.2365 | 0.0107 | higher values generally align with higher predicted final_grade |

### B_lms_oulad / temporal_forward

| metric | value |
| --- | ---: |
| RMSE | 9.5610 |
| MAE | 6.3765 |
| R² | 0.9175 |
| train rows | 24718 |
| test rows | 8712 |

**Concentration**

- Top feature: `assessment_submission_rate_due_to_date`
- Top-1 share: 0.2783
- Top-3 share: 0.6954
- Herfindahl index: 0.1961
- Features with positive importance: 15

**Top-10 features by importance share**

| rank | feature | importance_share | mean_rmse_increase | native_importance | direction |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | `assessment_submission_rate_due_to_date` | 0.2783 | 8.4046 | 0.6048 | higher values generally align with higher predicted final_grade |
| 2 | `cumulative_assessment_weighted_score_to_date` | 0.2296 | 6.9335 | 0.1813 | higher values generally align with higher predicted final_grade |
| 3 | `cumulative_submitted_weight_to_date` | 0.1875 | 5.6610 | 0.0223 | higher values generally align with higher predicted final_grade |
| 4 | `is_unregistered_by_week` | 0.1640 | 4.9536 | 0.0060 | higher values generally align with lower predicted final_grade |
| 5 | `current_week_clicks` | 0.0479 | 1.4477 | 0.0460 | higher values generally align with higher predicted final_grade |
| 6 | `cumulative_assessment_score_mean_to_date` | 0.0271 | 0.8184 | 0.0528 | higher values generally align with higher predicted final_grade |
| 7 | `cumulative_content_clicks_to_date` | 0.0216 | 0.6533 | 0.0043 | higher values generally align with higher predicted final_grade |
| 8 | `current_week_activity_types` | 0.0124 | 0.3754 | 0.0397 | higher values generally align with higher predicted final_grade |
| 9 | `cumulative_clicks_to_date` | 0.0107 | 0.3221 | 0.0115 | higher values generally align with higher predicted final_grade |
| 10 | `cumulative_social_clicks_to_date` | 0.0072 | 0.2185 | 0.0100 | higher values generally align with higher predicted final_grade |

### B_lms_plus_mastery_oulad / student_group

| metric | value |
| --- | ---: |
| RMSE | 12.7208 |
| MAE | 7.8933 |
| R² | 0.8540 |
| train rows | 50890 |
| test rows | 16940 |

**Concentration**

- Top feature: `overall_mastery_proxy`
- Top-1 share: 0.3993
- Top-3 share: 0.6754
- Herfindahl index: 0.2217
- Features with positive importance: 23

**Top-10 features by importance share**

| rank | feature | importance_share | mean_rmse_increase | native_importance | direction |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | `overall_mastery_proxy` | 0.3993 | 9.5733 | 0.7437 | higher values generally align with higher predicted final_grade |
| 2 | `is_unregistered_by_week` | 0.1436 | 3.4428 | 0.0069 | higher values generally align with lower predicted final_grade |
| 3 | `cumulative_submitted_weight_to_date` | 0.1325 | 3.1779 | 0.0477 | higher values generally align with higher predicted final_grade |
| 4 | `tma_mastery_to_date` | 0.1281 | 3.0718 | 0.1249 | higher values generally align with higher predicted final_grade |
| 5 | `cumulative_assessment_weighted_score_to_date` | 0.0726 | 1.7398 | 0.0141 | higher values generally align with higher predicted final_grade |
| 6 | `current_week_clicks` | 0.0307 | 0.7366 | 0.0082 | higher values generally align with higher predicted final_grade |
| 7 | `cumulative_clicks_to_date` | 0.0277 | 0.6637 | 0.0143 | higher values generally align with higher predicted final_grade |
| 8 | `current_week_activity_types` | 0.0163 | 0.3916 | 0.0079 | higher values generally align with higher predicted final_grade |
| 9 | `cumulative_social_clicks_to_date` | 0.0139 | 0.3329 | 0.0026 | higher values generally align with higher predicted final_grade |
| 10 | `cumulative_content_clicks_to_date` | 0.0109 | 0.2611 | 0.0026 | higher values generally align with higher predicted final_grade |

### B_lms_plus_mastery_oulad / temporal_forward

| metric | value |
| --- | ---: |
| RMSE | 9.1804 |
| MAE | 6.0817 |
| R² | 0.9240 |
| train rows | 24718 |
| test rows | 8712 |

**Concentration**

- Top feature: `overall_mastery_proxy`
- Top-1 share: 0.3398
- Top-3 share: 0.6627
- Herfindahl index: 0.1898
- Features with positive importance: 17

**Top-10 features by importance share**

| rank | feature | importance_share | mean_rmse_increase | native_importance | direction |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | `overall_mastery_proxy` | 0.3398 | 9.0227 | 0.5781 | higher values generally align with higher predicted final_grade |
| 2 | `is_unregistered_by_week` | 0.1697 | 4.5065 | 0.0063 | higher values generally align with lower predicted final_grade |
| 3 | `cumulative_submitted_weight_to_date` | 0.1531 | 4.0656 | 0.0127 | higher values generally align with higher predicted final_grade |
| 4 | `tma_mastery_to_date` | 0.1091 | 2.8964 | 0.2581 | higher values generally align with higher predicted final_grade |
| 5 | `cumulative_assessment_weighted_score_to_date` | 0.0721 | 1.9139 | 0.0443 | higher values generally align with higher predicted final_grade |
| 6 | `current_week_clicks` | 0.0541 | 1.4355 | 0.0234 | higher values generally align with higher predicted final_grade |
| 7 | `cumulative_content_clicks_to_date` | 0.0352 | 0.9354 | 0.0050 | higher values generally align with higher predicted final_grade |
| 8 | `cumulative_assessment_score_mean_to_date` | 0.0182 | 0.4840 | 0.0199 | higher values generally align with higher predicted final_grade |
| 9 | `cumulative_clicks_to_date` | 0.0142 | 0.3779 | 0.0116 | higher values generally align with higher predicted final_grade |
| 10 | `cumulative_assessment_score_count_to_date` | 0.0129 | 0.3426 | 0.0007 | higher values generally align with higher predicted final_grade |

### C_twin_oulad / student_group

| metric | value |
| --- | ---: |
| RMSE | 12.6406 |
| MAE | 7.8144 |
| R² | 0.8559 |
| train rows | 50890 |
| test rows | 16940 |

**Concentration**

- Top feature: `overall_mastery_proxy`
- Top-1 share: 0.4275
- Top-3 share: 0.7068
- Herfindahl index: 0.2402
- Features with positive importance: 23

**Top-10 features by importance share**

| rank | feature | importance_share | mean_rmse_increase | native_importance | direction |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | `overall_mastery_proxy` | 0.4275 | 9.8143 | 0.7403 | higher values generally align with higher predicted final_grade |
| 2 | `is_unregistered_by_week` | 0.1636 | 3.7570 | 0.0073 | higher values generally align with lower predicted final_grade |
| 3 | `tma_mastery_to_date` | 0.1157 | 2.6550 | 0.1214 | higher values generally align with higher predicted final_grade |
| 4 | `cumulative_submitted_weight_to_date` | 0.1136 | 2.6074 | 0.0483 | higher values generally align with higher predicted final_grade |
| 5 | `current_week_clicks` | 0.0392 | 0.9000 | 0.0103 | higher values generally align with higher predicted final_grade |
| 6 | `performance_index_oulad` | 0.0351 | 0.8067 | 0.0140 | higher values generally align with higher predicted final_grade |
| 7 | `cumulative_assessment_weighted_score_to_date` | 0.0249 | 0.5717 | 0.0098 | higher values generally align with higher predicted final_grade |
| 8 | `cumulative_clicks_to_date` | 0.0242 | 0.5553 | 0.0128 | higher values generally align with higher predicted final_grade |
| 9 | `current_week_activity_types` | 0.0146 | 0.3355 | 0.0067 | higher values generally align with higher predicted final_grade |
| 10 | `cumulative_social_clicks_to_date` | 0.0100 | 0.2301 | 0.0021 | higher values generally align with higher predicted final_grade |

### C_twin_oulad / temporal_forward

| metric | value |
| --- | ---: |
| RMSE | 9.5845 |
| MAE | 6.3929 |
| R² | 0.9171 |
| train rows | 24718 |
| test rows | 8712 |

**Concentration**

- Top feature: `overall_mastery_proxy`
- Top-1 share: 0.2279
- Top-3 share: 0.6329
- Herfindahl index: 0.1662
- Features with positive importance: 18

**Top-10 features by importance share**

| rank | feature | importance_share | mean_rmse_increase | native_importance | direction |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | `overall_mastery_proxy` | 0.2279 | 5.7931 | 0.4170 | higher values generally align with higher predicted final_grade |
| 2 | `is_unregistered_by_week` | 0.2045 | 5.1967 | 0.0066 | higher values generally align with lower predicted final_grade |
| 3 | `tma_mastery_to_date` | 0.2005 | 5.0960 | 0.4085 | higher values generally align with higher predicted final_grade |
| 4 | `cumulative_submitted_weight_to_date` | 0.1561 | 3.9663 | 0.0122 | higher values generally align with higher predicted final_grade |
| 5 | `current_week_clicks` | 0.0600 | 1.5255 | 0.0218 | higher values generally align with higher predicted final_grade |
| 6 | `performance_index_oulad` | 0.0495 | 1.2576 | 0.0267 | higher values generally align with higher predicted final_grade |
| 7 | `cumulative_assessment_weighted_score_to_date` | 0.0335 | 0.8511 | 0.0285 | higher values generally align with higher predicted final_grade |
| 8 | `cumulative_content_clicks_to_date` | 0.0184 | 0.4671 | 0.0047 | higher values generally align with higher predicted final_grade |
| 9 | `current_week_activity_types` | 0.0125 | 0.3189 | 0.0102 | higher values generally align with higher predicted final_grade |
| 10 | `cumulative_clicks_to_date` | 0.0097 | 0.2455 | 0.0122 | higher values generally align with higher predicted final_grade |

## Limitations

- These are model-behavior explanations under gradient_boosting; a different model family may produce different importance orderings.

- The OULAD regression target (final_weighted_score) is partially circular on assessment-score features; high importance for those features cannot be read as an exogenous causal signal.

- Permutation importance can be unreliable when correlated features are present; the mastery block features are correlated with assessment-score features, so importances may understate mastery's marginal contribution.

- Local perturbation explanations use training-median as the reference; this is not a Shapley baseline and may understate or overstate contribution for skewed distributions.

- This experiment does not establish causal or institutional claims; findings are bounded to model behavior on the DDD 2013J subset.


## Next step

Use the concentration and clickstream-vs-assessment pattern to frame the dissertation XAI narrative: if clickstream features appear prominently despite the partial circularity, the model is learning genuine behavioral engagement signals beyond score accounting.  If assessment features dominate with very high concentration, narrow the XAI claim to "the model relies heavily on cumulative performance, which is expected given target construction" and foreground the clickstream features as the interpretive signal of interest.

