# Experiment Progression Summary

This document is the compact reference view of the experiment line. It is
intended as a one-page citation aid for the dissertation. The fuller
narrative is provided in
[experimental_results_synthesis.md](experimental_results_synthesis.md), and
the canonical numbers are recorded in the per-experiment writeups under
`docs/experiments/` and the metadata under
`data/artifacts/experiments/<experiment_id>/`.

All four experiments share the following invariants:

- Schema version: `v1.2`
- Dataset / config: `v1_3_refined` / `generator_v1_3_refined.yaml`
- Snapshot grain: `1 row = 1 student × 1 week`
- Snapshot filter: weeks `4..10`
- Seed: `42`
- Primary supervised target: `final_grade`
- Secondary context target: `passed`
- Excluded supervised target: `risk_level`

## 1. Sequence Table

| ID | Objective | Main comparison | Primary target | Primary split | Secondary split | Key result | Research consequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `exp_001_baseline` | Establish reproducible baseline by comparing nested feature sets. | `A_simple` vs `B_lms` vs `C_twin` | `final_grade` | student-grouped (`test_size = 0.25`) | temporal-forward with held-out students | On primary split: `B_lms` RMSE = 2.101, `C_twin` RMSE = 2.149. On forward split: `B_lms` RMSE = 2.270, `C_twin` RMSE = 2.937. `passed` saturates at F1 = 1.000 for all sets and splits. | Full `C_twin` is not justified. Decompose the Twin layer into subgroups in the next experiment. |
| `exp_002_twin_ablation` | Identify which Twin subgroups add value beyond `B_lms`. | `B_lms` vs single-block additions and `C_twin_full`. | `final_grade` | student-grouped | temporal-forward | On primary split: `B_lms_plus_mastery` RMSE = 1.894 (Δ = -0.206); `C_twin_full` RMSE = 2.149 (Δ = +0.049). On forward split: `B_lms_plus_mastery` Δ = +0.006; `C_twin_full` Δ = +0.667. | Carry forward `B_lms_plus_mastery` as the lean Twin candidate. Full `C_twin` remains not justified. |
| `exp_003_mastery_validation` | Audit whether the mastery block is genuine signal or a `final_grade` proxy. | `B_lms` vs `B_lms_plus_mastery`, with diagnostic checks. | `final_grade` | student-grouped | temporal-forward (and per-week) | Primary delta confirmed at `-0.206`. Mastery improves baseline at weeks 4–8. `overall_mastery` Pearson r vs `final_grade` = 0.984; |r| with `avg_assignment_score_to_date` = 0.993; drop-column delta = +0.228. | Decision: `carry_forward` with explicit redundancy caveat for `overall_mastery`. Use the lean candidate in the explanation phase. |
| `exp_004_xai_on_lean_twin` | Explain the lean Twin and audit single-feature dominance. | `B_lms` vs `B_lms_plus_mastery` under gradient boosting, with permutation and local-perturbation explanations. | `final_grade` | student-grouped | (none configured) | Lean RMSE = 1.894 vs baseline 2.101. Top global feature `activity_score_to_date` (share 0.648); `overall_mastery` rank 2 (share 0.178). Average local mastery share = 0.194. Dominance audit outcome: `acceptable_with_caveat`. | Decision: `carry_forward_with_caveat`. Explanations remain teacher-meaningful and do not collapse onto a single feature. SHAP not used in this phase. |

## 2. Decision Chain

The four experiments form a single dependency chain in which each result
constrains the next experiment's question. The chain is also recorded in the
`parent_experiment` field of each experiment's configuration.

```
exp_001_baseline
        │  full Twin not justified → ablate
        ▼
exp_002_twin_ablation
        │  lean candidate identified → validate
        ▼
exp_003_mastery_validation
        │  mastery validated with caveat → explain
        ▼
exp_004_xai_on_lean_twin
        │  explanations teacher-meaningful → carry forward
        ▼
(dissertation narrative on lean Twin + XAI)
```

## 3. Outcome Tags

The repository uses a small vocabulary of outcome tags to record decisions
between experiments:

| Tag | Meaning |
| --- | --- |
| `unjustified` | The compared representation does not reliably improve on the reference baseline under the present setup. |
| `carry_forward` | The candidate is retained for the next experiment under documented assumptions. |
| `carry_forward_with_caveat` | The candidate is retained, but a specific structural concern (e.g., redundancy) is preserved as an explicit caveat. |
| `acceptable_with_caveat` | The dominance audit on the lean Twin's explanations passes, with one warning flag preserved. |

The terminal state of the experiment line is `carry_forward_with_caveat`
applied to `B_lms_plus_mastery`.

## 4. Citation-Friendly References

| Component | Path |
| --- | --- |
| Experiment registry | [docs/experiments/registry.md](../experiments/registry.md) |
| Baseline writeup | [docs/experiments/exp_001_baseline.md](../experiments/exp_001_baseline.md) |
| Ablation writeup | [docs/experiments/exp_002_twin_ablation.md](../experiments/exp_002_twin_ablation.md) |
| Mastery validation writeup | [docs/experiments/exp_003_mastery_validation.md](../experiments/exp_003_mastery_validation.md) |
| XAI writeup | [docs/experiments/exp_004_xai_on_lean_twin.md](../experiments/exp_004_xai_on_lean_twin.md) |
| Baseline vs ablation comparison | [docs/experiments/exp_001_vs_exp_002_comparison.md](../experiments/exp_001_vs_exp_002_comparison.md) |
| Lean Twin recommendation | `data/artifacts/experiments/exp_002_twin_ablation/lean_twin_recommendation.md` |
| Mastery carry-forward recommendation | `data/artifacts/experiments/exp_003_mastery_validation/mastery_carry_forward_recommendation.md` |
| XAI carry-forward recommendation | `data/artifacts/experiments/exp_004_xai_on_lean_twin/xai_carry_forward_recommendation.md` |
