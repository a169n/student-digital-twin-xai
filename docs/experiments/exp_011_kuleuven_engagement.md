# exp_011_kuleuven_engagement: Third-institution engagement-only PASSED classification on KU Leuven (1819)

> **THIRD INSTITUTION — ENGAGEMENT-ONLY — CLASSIFICATION ONLY (PASSED)**
>
> KU Leuven has NO numeric intermediate assessment scores and NO meaningful
> continuous grade. Only binary PASSED classification is reported.
> Regression is NOT applicable (final_grade = float(passed) placeholder).
> The mastery/Twin feature ablation from OULAD experiments CANNOT be
> reproduced here.

## Objective

Transfer the engagement-only PASSED classification benchmark to KU Leuven (academic year 1819) — a THIRD institution outside OULAD — to test whether engagement signals derived from click-stream logs predict binary course outcomes without any mastery or intermediate assessment features. This experiment also runs permutation importance to identify WHICH engagement features drive PASSED prediction in this institution. NOTE: KU Leuven has NO numeric intermediate assessment scores and NO meaningful continuous grade. Only binary classification (PASSED) is reported. Regression is NOT applicable here (final_grade is a placeholder = float(passed)). The mastery/Twin feature ablation from exp_005/exp_006/exp_009 CANNOT be reproduced on KU Leuven due to the absence of assessment-score data.


## Hypothesis

Richer engagement features (B_engagement: multi-dimensional click behaviour, session patterns, content type ratios, forum activity, temporal progress) will improve PASSED classification F1 and ROC-AUC over the minimal two-feature baseline (A_simple_engagement: cumulative clicks + active days only) on both split strategies. The gain may be moderate rather than large given that the simple baseline already captures the dominant engagement signal. The permutation importance analysis is expected to surface cumulative_clicks_to_date and cumulative_active_days_to_date as the top drivers, with cumulative_sessions_to_date and avg_session_clicks_to_date also contributing under the richer feature set.


## Dataset

- Institution: KU Leuven (year 1819) — THIRD institution
- Citation: Tiukhova, E., Van Landuyt, D., Baesens, B., & Snoeck, M. (2026). Open data, private learners: a de-identified student activity and performance dataset for learning analytics. Scientific Data. CC-BY-4.0, Zenodo DOI 10.5281/zenodo.17087849.
- Experiment config: `services/ml/configs/experiments/exp_011_kuleuven_engagement.yaml`
- Data dir: `datasets/ku_leuven/dataset`
- Course info: `datasets/ku_leuven/course_info.json`
- Snapshot rows: 19474
- Students: 1495
- Weeks: 2–15
- PASSED rate (student-level): 0.6328
- n_passed: 946, n_failed: 549

## Feature sets

### `A_simple_engagement`

Minimal KU Leuven engagement baseline: cumulative click volume and cumulative active days only. Has-activity indicator added for leakage-safe missingness handling.


- Columns: `cumulative_clicks_to_date`, `cumulative_active_days_to_date`
- Indicator columns: `has_activity_to_date`

### `B_engagement`

Rich KU Leuven engagement feature set: full multi-dimensional click behaviour (total, sessions, active days, content-type, forum), session efficiency ratios, content focus ratios, temporal course progress, and the raw week counter. This is the candidate feature set that characterises WHICH engagement dimensions drive PASSED prediction.


- Columns: `cumulative_clicks_to_date`, `cumulative_active_days_to_date`, `cumulative_sessions_to_date`, `cumulative_content_clicks_to_date`, `current_week_clicks`, `avg_session_clicks_to_date`, `content_click_ratio_to_date`, `cumulative_forum_posts_to_date`, `days_since_course_start`, `week_number`
- Indicator columns: `has_activity_to_date`

## Split strategies

- Student-group split: `test_size=0.25`, `seed=42`
- Temporal-forward split: `train_weeks=8`, `student_test_size=0.25`, `student_seed=42`
- Classification models: `logistic_regression`, `random_forest`, `gradient_boosting`

## Headline classification results (best model per cell)

| split | feature set | best model | F1 | accuracy | ROC-AUC |
| --- | --- | --- | ---: | ---: | ---: |
| temporal_forward | A_simple_engagement | logistic_regression | 0.761 | 0.614 | 0.717 |
| temporal_forward | B_engagement | random_forest | 0.751 | 0.650 | 0.673 |
| student_group | A_simple_engagement | logistic_regression | 0.763 | 0.627 | 0.653 |
| student_group | B_engagement | logistic_regression | 0.755 | 0.644 | 0.703 |

## Fixed-model classification results (model = `gradient_boosting`)

Same model across all feature sets and both splits to neutralize model-flip artifacts. Delta is relative to `A_simple_engagement`.

| split | feature set | F1 | accuracy | ROC-AUC | delta F1 | delta AUC |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| temporal_forward | A_simple_engagement | 0.757 | 0.625 | 0.693 | +0.000 | +0.000 |
| temporal_forward | B_engagement | 0.741 | 0.639 | 0.702 | -0.015 | +0.009 |
| student_group | A_simple_engagement | 0.754 | 0.638 | 0.660 | +0.000 | +0.000 |
| student_group | B_engagement | 0.754 | 0.653 | 0.701 | +0.000 | +0.041 |

## Permutation importance (candidate feature set: `B_engagement`)

Model: `gradient_boosting`, scoring: ROC-AUC, n_repeats=15.
Shares are normalised over positive importances only.

### Split: `student_group`

- Total positive importance sum: 0.207899
- Top-1 feature share: 17.5%
- Top-3 feature share: 48.1%

| rank | feature | mean importance | std | share of positive |
| ---: | --- | ---: | ---: | ---: |
| 1 | cumulative_clicks_to_date | 0.0364 | 0.0041 | 17.5% |
| 2 | cumulative_active_days_to_date | 0.0330 | 0.0044 | 15.9% |
| 3 | cumulative_sessions_to_date | 0.0307 | 0.0029 | 14.8% |
| 4 | current_week_clicks | 0.0220 | 0.0033 | 10.6% |
| 5 | content_click_ratio_to_date | 0.0213 | 0.0032 | 10.2% |
| 6 | avg_session_clicks_to_date | 0.0159 | 0.0024 | 7.7% |
| 7 | days_since_course_start | 0.0156 | 0.0016 | 7.5% |
| 8 | cumulative_content_clicks_to_date | 0.0154 | 0.0025 | 7.4% |
| 9 | week_number | 0.0123 | 0.0014 | 5.9% |
| 10 | cumulative_forum_posts_to_date | 0.0054 | 0.0010 | 2.6% |

### Split: `temporal_forward`

- Total positive importance sum: 0.190047
- Top-1 feature share: 45.6%
- Top-3 feature share: 68.6%

| rank | feature | mean importance | std | share of positive |
| ---: | --- | ---: | ---: | ---: |
| 1 | cumulative_active_days_to_date | 0.0867 | 0.0091 | 45.6% |
| 2 | cumulative_clicks_to_date | 0.0247 | 0.0036 | 13.0% |
| 3 | current_week_clicks | 0.0190 | 0.0023 | 10.0% |
| 4 | content_click_ratio_to_date | 0.0175 | 0.0044 | 9.2% |
| 5 | cumulative_sessions_to_date | 0.0124 | 0.0045 | 6.5% |
| 6 | cumulative_forum_posts_to_date | 0.0111 | 0.0018 | 5.8% |
| 7 | cumulative_content_clicks_to_date | 0.0108 | 0.0035 | 5.7% |
| 8 | avg_session_clicks_to_date | 0.0078 | 0.0040 | 4.1% |
| 9 | week_number | 0.0000 | 0.0000 | 0.0% |
| 10 | days_since_course_start | 0.0000 | 0.0000 | 0.0% |

## Interpretation

Richer engagement features provide negligible additional F1 lift over the minimal baseline on KU Leuven. The dominant PASSED signal is already captured by cumulative clicks and active days; the additional features do not materially shift classification accuracy.

- Outcome: `engagement_richness_neutral`
- Primary delta F1: `-0.015`
- Short conclusion: `B_engagement` was approximately level with `A_simple_engagement` (delta F1 = -0.015).

## Artifact paths

- Results JSON: `data/artifacts/experiments/exp_011_kuleuven_engagement/exp_011_kuleuven_engagement_results.json`
- Results CSV: `data/artifacts/experiments/exp_011_kuleuven_engagement/exp_011_kuleuven_engagement_results.csv`
- Importance CSV: `data/artifacts/experiments/exp_011_kuleuven_engagement/engagement_importance.csv`

## Limitations

- Dataset citation: Tiukhova, E., Van Landuyt, D., Baesens, B., & Snoeck, M. (2026). Open data, private learners: a de-identified student activity and performance dataset for learning analytics. Scientific Data. CC-BY-4.0, Zenodo DOI 10.5281/zenodo.17087849.

- KU Leuven has no numeric intermediate assessment scores, so the mastery and assessment-score feature blocks present in OULAD experiments CANNOT be built or compared here. The engagement-only design is a constraint of this dataset, not a design choice.

- The binary PASSED label encodes course-level outcome, not weekly learning progress; this makes the classification task somewhat easier than a continuous grade prediction because all weekly rows for a student share the same label.

- final_grade is set to float(passed) purely as a structural placeholder for the shared pipeline. Any regression metric on this column is meaningless and is NOT reported.

- The dataset covers two courses in academic year 1819 only; course-level heterogeneity is not controlled for.

- Permutation importance is computed with n_repeats=15 on the held-out test set; feature correlations can suppress individual importances.

- This benchmark cannot establish institutional deployment readiness; it is a third-institution engagement-transfer stress test.


## Next step

Compare the B-vs-A engagement delta here with the OULAD results from exp_005/exp_009. If richer engagement consistently helps across all three institutions, that strengthens the representation-transfer argument. If the improvement is null, report it honestly as a cross-institution robustness check. The permutation importance rankings across KU Leuven and OULAD should be compared to identify stable drivers of PASSED prediction.

