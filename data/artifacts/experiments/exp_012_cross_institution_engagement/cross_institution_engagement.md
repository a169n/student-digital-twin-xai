# Cross-Institution Engagement-Only Comparison (exp_012)

Matched engagement-only PASSED comparison across three institution cohorts: KU_Leuven (ku_leuven), OULAD_BBB (oulad), OULAD_DDD (oulad).

**Fixed model** = `gradient_boosting`  |  **top_k** = 5  |  **stable_tau_threshold** = 0.9

## Part A -- Engagement delta (candidate B minus baseline A), fixed model

Change in fixed-model classification metrics when moving from the simple-engagement baseline feature set to the richer engagement candidate set.

| Institution | Split | A F1 | B F1 | delta F1 | A ROC-AUC | B ROC-AUC | delta ROC-AUC |
|---|---|---|---|---|---|---|---|
| KU_Leuven | student_group | 0.7536 | 0.7537 | 0.0001 | 0.6598 | 0.7005 | 0.0407 |
| KU_Leuven | temporal_forward | 0.7567 | 0.7411 | -0.0155 | 0.6927 | 0.7020 | 0.0093 |
| OULAD_BBB | student_group | 0.7727 | 0.8120 | 0.0393 | 0.8499 | 0.8843 | 0.0344 |
| OULAD_BBB | temporal_forward | 0.7873 | 0.8131 | 0.0258 | 0.8746 | 0.8983 | 0.0237 |
| OULAD_DDD | student_group | 0.7340 | 0.8058 | 0.0718 | 0.8602 | 0.8997 | 0.0396 |
| OULAD_DDD | temporal_forward | 0.7896 | 0.7892 | -0.0003 | 0.8929 | 0.9137 | 0.0208 |

## Part B -- Importance-rank stability across institutions (shared concepts)

Permutation-importance rankings aligned onto a shared engagement-concept set, then compared pairwise. Kendall tau over aligned concepts; Jaccard over top-5 concepts.

| Split | Pair | Kendall tau | Jaccard@5 | n_shared_concepts |
|---|---|---|---|---|
| student_group | KU_Leuven vs OULAD_BBB | 0.7143 | 0.6667 | 7 |
| student_group | KU_Leuven vs OULAD_DDD | 0.2381 | 0.4286 | 7 |
| student_group | OULAD_BBB vs OULAD_DDD | 0.5238 | 0.6667 | 7 |
| temporal_forward | KU_Leuven vs OULAD_BBB | 0.7143 | 0.6667 | 7 |
| temporal_forward | KU_Leuven vs OULAD_DDD | 0.5238 | 0.6667 | 7 |
| temporal_forward | OULAD_BBB vs OULAD_DDD | 0.6190 | 0.6667 | 7 |

**Mean Kendall tau (all pairs, all splits)**: 0.5556

## Verdict

drivers_partly_institution_specific

## Caveats

- **Forum/social proxy mismatch.** The `forum_engagement` concept maps to social CLICKS in OULAD (`cumulative_social_clicks_to_date`) but to forum POSTS in KU Leuven (`cumulative_forum_posts_to_date`). These are different units of behaviour; the cross-institution comparison uses RANKS, not magnitudes, precisely to avoid comparing incommensurable quantities.

- **Excluded KU-only concepts.** KU Leuven carries session-level features with no OULAD analog (`cumulative_sessions_to_date`, `avg_session_clicks_to_date`, `days_since_course_start`); these are dropped from Part B's shared-concept alignment, so the stability comparison covers only the concepts present in both institutions' feature sets.

- **Both splits reported.** Both `student_group` and `temporal_forward` splits are shown for completeness, but each per-cohort headline conclusion keys off only its primary split; cross-split disagreement within a cohort is expected and is not, by itself, evidence of cross-institution instability.

- **Model behaviour, not causality.** Importances are permutation-importance rankings of a gradient-boosting model's learned input-output mapping. High cross-institution tau means the learned reliance pattern transfers, not that the same causal factors drive student outcomes across institutions.