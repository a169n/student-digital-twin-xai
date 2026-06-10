# exp_012_oulad_engagement_bbb2013j: Matched engagement-only PASSED classification on OULAD (BBB 2013J)

> **OULAD — ENGAGEMENT-ONLY — CLASSIFICATION ONLY (PASSED)**
>
> Matched engagement-only design for cross-institution comparison with the
> KU Leuven engagement benchmark. Only binary PASSED classification is
> reported. Regression is intentionally omitted (engagement-only matched
> design); final_grade = float(passed) is a structural placeholder.
> `cumulative_social_clicks_to_date` (forum/social CLICKS) is the OULAD
> analog of KU Leuven forum POSTS — different units, so the cross-institution
> comparison uses permutation-importance RANKS, not magnitudes.

## Objective

Run the engagement-only PASSED classification benchmark on OULAD (BBB 2013J) under a design MATCHED to the KU Leuven engagement benchmark (exp_011), so the two institutions can be compared head-to-head. Only binary PASSED classification is reported; OULAD's assessment-derived score is deliberately NOT used. Permutation importance identifies WHICH engagement features drive PASSED prediction so the cross-institution importance RANKS can be compared. final_grade is set to float(passed) purely as a structural placeholder for the shared pipeline; no real grade is used and no regression metric is reported.


## Hypothesis

Richer engagement features (B_engagement_oulad: multi-dimensional click behaviour, content-type ratios, social/forum clicks, temporal progress) are expected to be NEUTRAL — at most a small, non-decisive change in PASSED F1 and ROC-AUC — over the minimal two-feature baseline (A_simple_engagement_oulad: cumulative clicks + active days only) on both split strategies, mirroring the KU Leuven finding. The simple baseline already captures the dominant engagement signal, so a large gain is not expected.


## Dataset

- Institution: OULAD (BBB 2013J)
- Citation: Kuzilek, J., Hlosta, M., & Zdrahal, Z. (2017). Open University Learning Analytics dataset. Scientific Data, 4, 170171. https://doi.org/10.1038/sdata.2017.171
- Experiment config: `services/ml/configs/experiments/exp_012_oulad_engagement_bbb2013j.yaml`
- Raw dir: `datasets/oulad`
- Course filter: code_module=BBB, code_presentation=2013J
- Snapshot rows: 80532
- Students: 2237
- Weeks: 4–39
- PASSED rate (student-level): 0.4792
- n_passed: 1072, n_failed: 1165

## Feature sets

### `A_simple_engagement_oulad`

Minimal OULAD engagement baseline matched to KU Leuven A_simple_engagement: cumulative click volume and cumulative active days only. Has-VLE-activity indicator added for leakage-safe missingness handling.


- Columns: `cumulative_clicks_to_date`, `cumulative_active_days_to_date`
- Indicator columns: `has_vle_activity_to_date`

### `B_engagement_oulad`

Rich OULAD engagement feature set matched to KU Leuven B_engagement: total click volume, active days, current-week clicks, content-type click split (content vs social/forum), content focus ratio, and the raw week counter. Session features are omitted because OULAD VLE logs are daily, not session-resolved. cumulative_social_clicks_to_date is the OULAD analog of KU Leuven forum posts. This is the candidate feature set characterising WHICH engagement dimensions drive PASSED prediction.


- Columns: `cumulative_clicks_to_date`, `cumulative_active_days_to_date`, `current_week_clicks`, `cumulative_content_clicks_to_date`, `cumulative_social_clicks_to_date`, `content_click_ratio_to_date`, `week_number`
- Indicator columns: `has_vle_activity_to_date`

## Split strategies

- Student-group split: `test_size=0.25`, `seed=42`
- Temporal-forward split: `train_weeks=20`, `student_test_size=0.25`, `student_seed=42`
- Classification models: `logistic_regression`, `random_forest`, `gradient_boosting`

## Headline classification results (best model per cell)

| split | feature set | best model | F1 | accuracy | ROC-AUC |
| --- | --- | --- | ---: | ---: | ---: |
| temporal_forward | A_simple_engagement_oulad | logistic_regression | 0.813 | 0.798 | 0.885 |
| temporal_forward | B_engagement_oulad | random_forest | 0.820 | 0.813 | 0.885 |
| student_group | A_simple_engagement_oulad | gradient_boosting | 0.773 | 0.763 | 0.850 |
| student_group | B_engagement_oulad | logistic_regression | 0.822 | 0.824 | 0.890 |

## Fixed-model classification results (model = `gradient_boosting`)

Same model across all feature sets and both splits to neutralize model-flip artifacts. Delta is relative to `A_simple_engagement_oulad`.

| split | feature set | F1 | accuracy | ROC-AUC | delta F1 | delta AUC |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| temporal_forward | A_simple_engagement_oulad | 0.787 | 0.758 | 0.875 | +0.000 | +0.000 |
| temporal_forward | B_engagement_oulad | 0.813 | 0.816 | 0.898 | +0.026 | +0.024 |
| student_group | A_simple_engagement_oulad | 0.773 | 0.763 | 0.850 | +0.000 | +0.000 |
| student_group | B_engagement_oulad | 0.812 | 0.811 | 0.884 | +0.039 | +0.034 |

## Permutation importance (candidate feature set: `B_engagement_oulad`)

Model: `gradient_boosting`, scoring: ROC-AUC, n_repeats=15.
Shares are normalised over positive importances only.

### Split: `student_group`

- Total positive importance sum: 0.332109
- Top-1 feature share: 45.2%
- Top-3 feature share: 83.6%

| rank | feature | mean importance | std | share of positive |
| ---: | --- | ---: | ---: | ---: |
| 1 | cumulative_clicks_to_date | 0.1501 | 0.0028 | 45.2% |
| 2 | cumulative_active_days_to_date | 0.0750 | 0.0024 | 22.6% |
| 3 | current_week_clicks | 0.0525 | 0.0016 | 15.8% |
| 4 | content_click_ratio_to_date | 0.0258 | 0.0009 | 7.8% |
| 5 | cumulative_social_clicks_to_date | 0.0173 | 0.0009 | 5.2% |
| 6 | week_number | 0.0101 | 0.0005 | 3.0% |
| 7 | cumulative_content_clicks_to_date | 0.0014 | 0.0003 | 0.4% |
| 8 | has_vle_activity_to_date | 0.0000 | 0.0000 | 0.0% |

### Split: `temporal_forward`

- Total positive importance sum: 0.246924
- Top-1 feature share: 38.5%
- Top-3 feature share: 84.0%

| rank | feature | mean importance | std | share of positive |
| ---: | --- | ---: | ---: | ---: |
| 1 | current_week_clicks | 0.0950 | 0.0021 | 38.5% |
| 2 | cumulative_active_days_to_date | 0.0582 | 0.0026 | 23.6% |
| 3 | cumulative_clicks_to_date | 0.0541 | 0.0026 | 21.9% |
| 4 | content_click_ratio_to_date | 0.0258 | 0.0015 | 10.4% |
| 5 | cumulative_content_clicks_to_date | 0.0069 | 0.0004 | 2.8% |
| 6 | cumulative_social_clicks_to_date | 0.0068 | 0.0007 | 2.8% |
| 7 | has_vle_activity_to_date | 0.0000 | 0.0000 | 0.0% |
| 8 | week_number | 0.0000 | 0.0000 | 0.0% |

## Interpretation

Richer engagement features modestly improve PASSED classification on OULAD. The additional session, content-type, forum, and temporal features provide signal beyond raw click volume and active days.

- Outcome: `richer_engagement_helps`
- Primary delta F1: `+0.026`
- Short conclusion: `B_engagement_oulad` improved F1 by +0.026 over `A_simple_engagement_oulad` on the primary split.

## Artifact paths

- Results JSON: `data/artifacts/experiments/exp_012_oulad_engagement_bbb2013j/exp_012_oulad_engagement_bbb2013j_results.json`
- Results CSV: `data/artifacts/experiments/exp_012_oulad_engagement_bbb2013j/exp_012_oulad_engagement_bbb2013j_results.csv`
- Importance CSV: `data/artifacts/experiments/exp_012_oulad_engagement_bbb2013j/engagement_importance.csv`

## Limitations

- Dataset citation: Kuzilek, J., Hlosta, M., & Zdrahal, Z. (2017). Open University Learning Analytics dataset. Scientific Data, 4, 170171. https://doi.org/10.1038/sdata.2017.171

- OULAD VLE interaction logs are aggregated at DAILY granularity, so session-level engagement features (session counts, average session clicks) that exist on KU Leuven CANNOT be reconstructed here. The matched OULAD feature set therefore omits session features by necessity, not by choice.

- cumulative_social_clicks_to_date (forum/social CLICKS) is the OULAD analog of KU Leuven forum POSTS. These are different units, so the cross-institution comparison relies on permutation-importance RANKS, not on raw importance magnitudes.

- final_grade is set to float(passed) purely as a structural placeholder for the shared pipeline. Any regression metric on this column is meaningless and is NOT reported. This is an engagement-only matched design: assessment-score and mastery feature blocks from exp_006/exp_009 are intentionally excluded.

- The binary PASSED label encodes course-level outcome, not weekly learning progress; all weekly rows for a student share the same label, which makes classification somewhat easier than continuous grade prediction.

- Permutation importance is computed with n_repeats=15 on the held-out test set; feature correlations can suppress individual importances.

- The selected OULAD subset is a single module-presentation (BBB 2013J); this benchmark cannot establish institutional deployment readiness and is a cross-institution engagement-transfer stress test only.


## Next step

Feed these BBB 2013J engagement-importance results, together with the DDD 2013J OULAD run and the KU Leuven exp_011 run, into analyze_cross_institution_engagement to compare the B-vs-A engagement deltas and the permutation-importance RANKS across all three cohorts. Stable top drivers of PASSED prediction across institutions strengthen the engagement-representation-transfer argument; a consistent null is reported honestly as a cross-institution robustness check.

