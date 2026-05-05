# Experiment Progression Summary

This document is the compact reference view of the experiment line. It is
intended as a one-page citation aid for the dissertation. The fuller
narrative is provided in
[experimental_results_synthesis.md](experimental_results_synthesis.md), and
the canonical numbers are recorded in the per-experiment writeups under
`docs/experiments/` and the metadata under
`data/artifacts/experiments/<experiment_id>/`.

The first four synthetic experiments share the following invariants:

- Schema version: `v1.2`
- Dataset / config: `v1_3_refined` / `generator_v1_3_refined.yaml`
- Snapshot grain: `1 row = 1 student × 1 week`
- Snapshot filter: weeks `4..10`
- Seed: `42`
- Primary supervised target: `final_grade`
- Secondary context target: `passed`
- Excluded supervised target: `risk_level`

`exp_005_public_benchmark_oulad` is separate: it uses the local OULAD files,
adapter schema `external_oulad_adapter_v1`, module-presentation `DDD` `2013J`,
primary target `final_weighted_score`, and secondary target `passed_observed`.

## 1. Sequence Table

| ID | Objective | Main comparison | Primary target | Primary split | Secondary split | Key result | Research consequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `exp_001_baseline` | Establish reproducible baseline by comparing nested feature sets. | `A_simple` vs `B_lms` vs `C_twin` | `final_grade` | student-grouped (`test_size = 0.25`) | temporal-forward with held-out students | On primary split: `B_lms` RMSE = 2.101, `C_twin` RMSE = 2.149. On forward split: `B_lms` RMSE = 2.270, `C_twin` RMSE = 2.937. `passed` saturates at F1 = 1.000 for all sets and splits. | Full `C_twin` is not justified. Decompose the Twin layer into subgroups in the next experiment. |
| `exp_002_twin_ablation` | Identify which Twin subgroups add value beyond `B_lms`. | `B_lms` vs single-block additions and `C_twin_full`. | `final_grade` | student-grouped | temporal-forward | On primary split: `B_lms_plus_mastery` RMSE = 1.894 (Δ = -0.206); `C_twin_full` RMSE = 2.149 (Δ = +0.049). On forward split: `B_lms_plus_mastery` Δ = +0.006; `C_twin_full` Δ = +0.667. | Carry forward `B_lms_plus_mastery` as the lean Twin candidate. Full `C_twin` remains not justified. |
| `exp_003_mastery_validation` | Audit whether the mastery block is genuine signal or a `final_grade` proxy. | `B_lms` vs `B_lms_plus_mastery`, with diagnostic checks. | `final_grade` | student-grouped | temporal-forward (and per-week) | Primary delta confirmed at `-0.206`. Mastery improves baseline at weeks 4–8. `overall_mastery` Pearson r vs `final_grade` = 0.984; |r| with `avg_assignment_score_to_date` = 0.993; drop-column delta = +0.228. | Decision: `carry_forward` with explicit redundancy caveat for `overall_mastery`. Use the lean candidate in the explanation phase. |
| `exp_004_xai_on_lean_twin` | Explain the lean Twin and audit single-feature dominance. | `B_lms` vs `B_lms_plus_mastery` under gradient boosting, with permutation and local-perturbation explanations. | `final_grade` | student-grouped | (none configured) | Lean RMSE = 1.894 vs baseline 2.101. Top global feature `activity_score_to_date` (share 0.648); `overall_mastery` rank 2 (share 0.178). Average local mastery share = 0.194. Dominance audit outcome: `acceptable_with_caveat`. | Decision: `carry_forward_with_caveat`. Explanations remain teacher-meaningful and do not collapse onto a single feature. SHAP not used in this phase. |
| `exp_005_public_benchmark_oulad` | Stress-test whether the lean representation logic transfers to OULAD. | `B_lms_oulad` vs `B_lms_plus_mastery_oulad`. | `final_weighted_score` | student-grouped | temporal-forward with held-out students | Primary grouped split: candidate RMSE = 12.724 vs baseline 12.658 (Δ = +0.066). Temporal-forward split: candidate RMSE = 9.161 vs baseline 9.566 (Δ = -0.406). | Decision: `complicates`. OULAD does not confirm the primary synthetic mastery advantage, but the secondary split keeps transfer plausibility open. |

## 2. Decision Chain

The experiments form a dependency chain in which each result
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
exp_005_public_benchmark_oulad
        │  public benchmark mixed → external transfer unresolved
        ▼
(dissertation narrative on lean Twin + XAI with OULAD transfer caveat)
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
| `complicates` | The public benchmark gives mixed evidence, so the internal finding remains valid but external transfer is unresolved. |

The terminal state of the synthetic experiment line is
`carry_forward_with_caveat` applied to `B_lms_plus_mastery`. The public OULAD
benchmark adds a `complicates` external-transfer caveat.

## 4. Internal Versus External Validity Status

The first four experiments provide the internal synthetic evidence base. Their
numbers are comparable because they share the same schema, generator,
snapshot filter, target, seed, and split discipline. They support the bounded
internal claim that `B_lms_plus_mastery` is the best lean candidate under the
current controlled setup.

`exp_005_public_benchmark_oulad` has a different role. It is an external
public-benchmark stress test with different data semantics, a derived
`final_weighted_score` target, OULAD-specific missingness, and a longer
weekly horizon. Its mixed result prevents a stronger external-validation
claim. It should be cited as transfer evidence that complicates the internal
finding, not as a replacement for institutional validation.

## 5. Citation-Friendly References

| Component | Path |
| --- | --- |
| Experiment registry | [docs/experiments/registry.md](../experiments/registry.md) |
| Baseline writeup | [docs/experiments/exp_001_baseline.md](../experiments/exp_001_baseline.md) |
| Ablation writeup | [docs/experiments/exp_002_twin_ablation.md](../experiments/exp_002_twin_ablation.md) |
| Mastery validation writeup | [docs/experiments/exp_003_mastery_validation.md](../experiments/exp_003_mastery_validation.md) |
| XAI writeup | [docs/experiments/exp_004_xai_on_lean_twin.md](../experiments/exp_004_xai_on_lean_twin.md) |
| OULAD benchmark writeup | [docs/experiments/exp_005_public_benchmark_oulad.md](../experiments/exp_005_public_benchmark_oulad.md) |
| OULAD feature mapping | [docs/experiments/oulad_feature_mapping.md](../experiments/oulad_feature_mapping.md) |
| Baseline vs ablation comparison | [docs/experiments/exp_001_vs_exp_002_comparison.md](../experiments/exp_001_vs_exp_002_comparison.md) |
| Lean Twin recommendation | `data/artifacts/experiments/exp_002_twin_ablation/lean_twin_recommendation.md` |
| Mastery carry-forward recommendation | `data/artifacts/experiments/exp_003_mastery_validation/mastery_carry_forward_recommendation.md` |
| XAI carry-forward recommendation | `data/artifacts/experiments/exp_004_xai_on_lean_twin/xai_carry_forward_recommendation.md` |
| OULAD benchmark interpretation | `data/artifacts/experiments/exp_005_public_benchmark_oulad/public_vs_synthetic_interpretation.md` |
| Final integrated report | [final_integrated_report.md](final_integrated_report.md) |
| Defense claim guardrails | [core_claims_and_nonclaims.md](core_claims_and_nonclaims.md) |
