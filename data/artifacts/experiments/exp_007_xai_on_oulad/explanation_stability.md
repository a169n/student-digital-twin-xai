# Explanation Stability: student_group vs temporal_forward

**top_k** = 5  |  **stable_tau_threshold** = 0.9  |  **all_stable** = False

| Feature Set | Kendall tau (SG vs TF) | Jaccard@5 | n_features |
|---|---|---|---|
| B_lms_oulad | 0.7922 | 0.6667 | 22 |
| B_lms_plus_mastery_oulad | 0.6815 | 1.0000 | 32 |
| C_twin_oulad | 0.5495 | 1.0000 | 37 |

**Mean Kendall tau**: 0.6744

## Verdict

regime_sensitive_finding: Feature-importance rankings differ meaningfully between student_group and temporal_forward evaluation splits (at least one Kendall tau < 0.90).  This is itself a reportable result: which features the model 'relies on' depends on the evaluation scenario (split strategy).  Combined with exp_006's mixed-to-null predictive finding, regime-sensitive explanations further caution against interpreting these importances as stable causal signals — they reflect model behavior under a specific evaluation regime, not an invariant mechanism.

## Interpretation

These metrics compare how consistently the gradient-boosting model ranks features across two evaluation regimes — student-grouped (random student split) and temporal-forward (train on earlier cohorts, test on later ones) — within the OULAD public benchmark. High Kendall tau indicates that the same features dominate regardless of which split is used; low tau indicates that the top-5 importance hierarchy is regime-sensitive. Critically, these are model-behavior importance rankings, not causal mechanisms: a feature ranked #1 by permutation importance is one whose removal most disrupts the model's learned input-output mapping, which may itself be a proxy or artifact. Linking to exp_006: the mixed-to-null predictive R² across feature sets and splits (particularly weaker temporal-forward performance) means that stable importance rankings, if found, confirm stability of an already-questionable signal, not confirmation of causal relevance. Regime-sensitive importances compound this concern: not only does predictive power vary by evaluation regime, but so does the model's reliance on individual features, limiting the interpretive value of any single importance ranking without anchoring it to a specific evaluation context.