# Cross-Cohort Explanation Stability: DDD_2013J vs BBB_2013J

**Cohorts compared**: DDD_2013J (exp_007) vs BBB_2013J (exp_010)  |  **top_k** = 5  |  **stable_tau_threshold** = 0.9  |  **all_stable** = False

| Feature Set | Split | Kendall tau (DDD_2013J vs BBB_2013J) | Jaccard@5 | n_features |
|---|---|---|---|---|
| B_lms_oulad | student_group | 0.5411 | 0.6667 | 22 |
| B_lms_oulad | temporal_forward | 0.6104 | 0.4286 | 22 |
| B_lms_plus_mastery_oulad | student_group | 0.6129 | 0.6667 | 32 |
| B_lms_plus_mastery_oulad | temporal_forward | 0.5645 | 1.0000 | 32 |
| C_twin_oulad | student_group | 0.4655 | 1.0000 | 37 |
| C_twin_oulad | temporal_forward | 0.3213 | 0.6667 | 37 |

**Mean Kendall tau**: 0.5193

## Verdict

explanations_partly_course_specific

## Interpretation

These metrics compare how consistently the gradient-boosting model ranks features across the two OULAD courses — DDD_2013J (module DDD, presentation 2013J) and BBB_2013J (module BBB, presentation 2013J) — for each (feature_set, split_strategy) combination.  Both courses are processed through the same adapter and share the same feature columns, so the Kendall tau is computed over the full, identical feature universe (no alignment step needed).

**Ties to exp_009 ablation findings.** In exp_009's ablation, adding the mastery block (B_lms_plus_mastery_oulad vs B_lms_oulad) improved predictive performance on BBB 2013J but produced no consistent gain on DDD 2013J.  If that asymmetry is reflected in the importances, we would expect mastery features to rank higher relative to LMS features on BBB than on DDD — which would depress the B_lms_plus_mastery_oulad cross-cohort tau.  Conversely, stable tau on that feature set would suggest that, despite the performance difference, the model still leans on the same features in both courses; the mastery block's predictive benefit on BBB may then come from features already present in the LMS set acting more strongly, rather than the mastery features themselves rising in relative rank.

**Model-behavior caveat.** These are permutation-importance rankings of a gradient-boosting model's learned input-output mapping, not causal effect estimates.  A feature ranked #1 is one whose removal most disrupts the model's predictions; that disruption reflects the model's reliance on the feature within a particular cohort and evaluation regime, not an invariant causal mechanism.  Cross-cohort tau measures whether that learned reliance pattern transfers — high tau means the two course populations produce similar model behaviour, not that the same causal factors drive student outcomes in both courses.  Combined with the mixed-to-null predictive R² findings from exp_006/exp_009, any interpretation of these importances as actionable levers should be made with caution.