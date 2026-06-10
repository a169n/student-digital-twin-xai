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
| `exp_005_public_benchmark_oulad` | Stress-test whether the lean representation logic transfers to OULAD. | `B_lms_oulad` vs `B_lms_plus_mastery_oulad`. | `final_weighted_score` | student-grouped | temporal-forward with held-out students | Primary grouped split: candidate RMSE = 12.724 vs baseline 12.658 (Δ = +0.066). Temporal-forward split: candidate RMSE = 9.161 vs baseline 9.566 (Δ = -0.406). Classification F1 0.863/0.861 (grouped), 0.887/0.884 (temporal) — not saturated. | Decision: `complicates` (superseded). The 2-set transfer is mixed; the full DDD ablation in `exp_006` supersedes this as the DDD verdict (see below). |
| `exp_006_oulad_full_ablation` | Run the full nested `A`/`B`/`C` ablation on OULAD DDD under a fixed model. | `A_simple_oulad` vs `B_lms_oulad` vs single-block additions vs `C_twin_oulad`. | `final_weighted_score` | student-grouped | temporal-forward | 67830 snapshots, 1938 students. No Twin block beats `B_lms_oulad` by >1.0 RMSE on either split: mastery temporal 9.561→9.180 (Δ = -0.381) but grouped +0.061; index temporal -0.218, grouped +0.008; `C_twin_oulad` within ±0.025 both splits; `A_simple_oulad` clearly worse (+1.207 grouped, +4.105 temporal). F1 0.83–0.887, never 1.000. | Decision: `mixed-to-null` (DDD). Twin blocks add no robust DDD advantage; classification is genuinely predictive and non-circular. This is the DDD verdict superseding `exp_005`. |
| `exp_007_xai_on_oulad` | Explain the OULAD DDD models and test whether importance rankings are regime-invariant. | Permutation + native + local importance across splits. | `final_weighted_score` | student-grouped | temporal-forward | `assessment_submission_rate_due_to_date` 0.28–0.38 (LMS), `overall_mastery_proxy` 0.23–0.43 (co-circular), `is_unregistered_by_week` 0.13–0.20 (exogenous), VLE clickstream 0.02–0.06. Cross-split Kendall τ: `B_lms_oulad` 0.79, `B_lms_plus_mastery_oulad` 0.68, `C_twin_oulad` 0.55 (mean 0.67, none ≥ 0.90); Jaccard top-5 1.00/1.00/0.67. | Decision: `regime-sensitive XAI`. Rankings are directional model-behavior, not causal, and shift across split regime. |
| `exp_008_faithfulness_probe` | Controlled faithfulness probe against a known final-week oracle ordering. | Recovered importance ordering vs oracle. | `final_grade` (synthetic) | final-week oracle | (methods appendix) | Final-week oracle-ordering Kendall τ = 1.0; `activity_score_to_date` share 0.108 (latent-driven proxy); `overall_mastery`↔`avg_assignment_score_to_date` Pearson r = 0.994. | Decision: `faithfulness probe` (methods appendix). The XAI pipeline recovers the true ordering when ground truth is known; not a headline result. |
| `exp_009_oulad_ablation_bbb2013j` | Repeat the full ablation on a second OULAD course (BBB) with richer dated-assessment structure. | `A`/`B`/`C` nested ablation, fixed model. | `final_weighted_score` | student-grouped | temporal-forward | 2237 students, 80532 snapshots. Heterogeneous: mastery improves temporal-forward Δ = -1.026 RMSE (5.284 vs 6.311) — crosses the 1.0 threshold DDD never did; `C_twin_oulad` temporal Δ = -0.765; student-grouped every block within 0.087 (null, as DDD); trend & index null on both splits. F1 0.87–0.93, never 1.000. | Decision: `heterogeneous` (BBB). The mastery advantage appears on one course's temporal split but not the other's — OULAD is two distinct regimes, not one. |
| `exp_010_xai_on_oulad_bbb2013j` | Explain the BBB models and test explanation stability across cohorts (DDD vs BBB). | Importance topology + cross-cohort and cross-split stability. | `final_weighted_score` | student-grouped | temporal-forward | Shared topology (`overall_mastery_proxy`, submission discipline, `is_unregistered_by_week` dominate both courses) but unstable rankings: cross-cohort Kendall τ (DDD vs BBB) 0.32–0.61 (mean 0.52), below within-cohort 0.55–0.79 (mean 0.67); none ≥ 0.90; Jaccard top-5 0.43–1.00. | Decision: `cross-cohort instability` (τ 0.32–0.61). Explanation drivers are course-specific; topology recurs but ordering does not transfer. |
| `exp_011_kuleuven_engagement` | Test transfer to a second institution (KU Leuven) where only engagement and `PASSED` exist. | `A_simple_engagement` vs richer `B_engagement`, classification only. | `passed` | student-grouped | temporal-forward | 1495 students, 2 courses pooled, weeks 2–15. Mastery ablation cannot be built (no scored assessments — itself a heterogeneity finding). Engagement predicts `PASSED` only modestly: F1 0.75–0.76, ROC-AUC 0.65–0.72. Richer `B_engagement` ≈ minimal `A_simple_engagement`: fixed-model F1 Δ = -0.015 temporal / +0.000 grouped; ROC-AUC +0.009/+0.041. `cumulative_active_days_to_date` + `cumulative_clicks_to_date` dominate. | Decision: `engagement-neutral`. Feature-richness does not beat a 2-feature engagement baseline at a second institution. |
| `exp_012_oulad_engagement` | Matched 3-institution engagement-only `PASSED` comparison + importance-rank stability. | `A_simple_engagement` vs `B_engagement` across DDD + BBB + KU 1819. | `passed` | student-grouped | temporal-forward | Part A fixed-model `B − A` F1: student_group DDD +0.072 / BBB +0.039 / KU +0.000; temporal DDD -0.0003 / KU -0.015 / BBB +0.026; ROC-AUC all six cells +0.009 to +0.041. Part B importance-rank stability over 7 shared concepts: mean Kendall τ 0.56 (student_group 0.49, temporal_forward 0.62), below 0.90; most stable KU↔BBB τ 0.714, least KU↔DDD τ 0.238; clicks/active-days are the recurring top drivers. | Decision: `drivers_partly_institution_specific`. A 2-feature engagement baseline is hard to beat across three institutions; importance drivers transfer only partially (mean τ 0.56). A robustness result, not an accuracy claim. |

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
        │  2-set transfer mixed → run full DDD ablation
        ▼
exp_006_oulad_full_ablation (DDD)
        │  mixed-to-null, no block >1.0 RMSE → explain DDD
        ▼
exp_007_xai_on_oulad (DDD)  +  exp_008_faithfulness_probe (appendix)
        │  importance regime-sensitive (τ 0.55–0.79) → test a second course
        ▼
exp_009_oulad_ablation_bbb2013j (BBB)
        │  heterogeneous: mastery temporal −1.026 → explain BBB + compare cohorts
        ▼
exp_010_xai_on_oulad_bbb2013j (BBB + cross-cohort)
        │  drivers course-specific (cross-cohort τ 0.32–0.61) → test a second institution
        ▼
exp_011_kuleuven_engagement (KU Leuven)
        │  engagement-neutral (ΔF1 −0.015), mastery cannot be built → match 3 institutions
        ▼
exp_012_oulad_engagement (DDD + BBB + KU)
        │  drivers_partly_institution_specific (mean τ 0.56) → robustness, not accuracy
        ▼
(dissertation narrative: circular-artifact synthetic → heterogeneous real data
 → regime/course-specific explanations → cross-institution feature-richness
 does not robustly help; contribution = methodology + honest mixed/negative finding)
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
| `complicates` | The 2-set public benchmark (`exp_005`) gives mixed evidence. Superseded as the DDD verdict by `exp_006` `mixed-to-null`. |
| `mixed-to-null` | The full DDD ablation finds no Twin block beating `B_lms_oulad` by >1.0 RMSE on either split; the supervised target is genuinely predictive and non-circular. |
| `regime-sensitive XAI` | Importance rankings are directional model-behavior that shift across split regime (cross-split τ < 0.90), not regime-invariant or causal. |
| `faithfulness probe` | Methods-appendix check: the XAI pipeline recovers the true final-week oracle ordering (τ = 1.0) when ground truth is known. |
| `heterogeneous` | The mastery/Twin advantage appears on one OULAD course's temporal split (BBB, Δ −1.026) but not the other's (DDD null). OULAD is two regimes. |
| `cross-cohort instability` | Explanation topology recurs across courses but ordering does not transfer (cross-cohort τ 0.32–0.61, below within-cohort 0.55–0.79). |
| `engagement-neutral` | At a second institution (KU Leuven) a richer engagement set ≈ a 2-feature baseline (ΔF1 −0.015 temporal). |
| `drivers_partly_institution_specific` | Across three matched institutions, a 2-feature engagement baseline is hard to beat and importance drivers transfer only partially (mean τ 0.56). |

The terminal state of the synthetic experiment line is
`carry_forward_with_caveat` applied to `B_lms_plus_mastery`, with the
overriding caveat that the synthetic target is circular and its accuracy is an
artifact. The real-data line then resolves the external question honestly:
`exp_006` supersedes the `exp_005` `complicates` tag with `mixed-to-null` on
DDD, `exp_009` shows `heterogeneous` evidence on BBB, the explanations are
`regime-sensitive`/`cross-cohort`-unstable (`exp_007`/`exp_010`), and the
second-institution / 3-institution engagement work (`exp_011`/`exp_012`)
terminates at `drivers_partly_institution_specific` — feature-richness does not
robustly help. The contribution is the reproducible leakage-aware methodology
and the honest mixed/negative finding, not an accuracy or Twin-superiority
claim.

## 4. Internal Versus External Validity Status

The first four experiments provide the internal synthetic evidence base. Their
numbers are comparable because they share the same schema, generator,
snapshot filter, target, seed, and split discipline. They support the bounded
internal claim that `B_lms_plus_mastery` is the best lean candidate under the
current controlled setup.

The synthetic numbers themselves carry a structural caveat that must lead
wherever they appear: `final_grade` is a deterministic, noise-free closed-form
function of the same behaviors the features re-aggregate (week-10
reconstruction error 0.008, correlation 1.000000), so the synthetic R² ≈ 0.99
and `passed` F1 = 1.000 are algebraic artifacts, not learnable signal.

The real-data experiments (`exp_005`–`exp_012`) carry the external evidence and
resolve the transfer question honestly, superseding `exp_005`'s mixed 2-set
result. The full DDD ablation (`exp_006`) is `mixed-to-null` — no Twin block
beats `B_lms_oulad` by >1.0 RMSE on either split — while the BBB ablation
(`exp_009`) is `heterogeneous`, with mastery improving the temporal-forward
split by Δ −1.026 RMSE on that one course. Crucially, OULAD classification is
genuinely predictive and non-circular (F1 0.83–0.93, never 1.000). The
explanations are regime-sensitive (within-cohort cross-split τ 0.55–0.79) and
course-specific (cross-cohort τ 0.32–0.61), none reaching 0.90. The
second-institution KU Leuven work (`exp_011`) cannot even build a mastery
ablation (no scored assessments) and finds engagement-richness neutral
(ΔF1 −0.015), and the matched 3-institution engagement comparison (`exp_012`)
ends at `drivers_partly_institution_specific` (mean τ 0.56): a 2-feature
engagement baseline is hard to beat and importance drivers transfer only
partially.

The honest arc is therefore: a circular-target synthetic artifact, then
heterogeneous real-data evidence (DDD null, BBB partial), then regime- and
course-specific explanations, then cross-institution confirmation that
feature-richness does not robustly help. The dissertation contribution is the
reproducible leakage-aware methodology, the explanation-stability analysis, the
faithfulness probe, and the honest mixed/negative real-data finding — not
accuracy, not Digital-Twin superiority, and not a simulation engine.

## 5. Citation-Friendly References

| Component | Path |
| --- | --- |
| Experiment registry | [docs/experiments/registry.md](../experiments/registry.md) |
| Baseline writeup | [docs/experiments/exp_001_baseline.md](../experiments/exp_001_baseline.md) |
| Ablation writeup | [docs/experiments/exp_002_twin_ablation.md](../experiments/exp_002_twin_ablation.md) |
| Mastery validation writeup | [docs/experiments/exp_003_mastery_validation.md](../experiments/exp_003_mastery_validation.md) |
| XAI writeup | [docs/experiments/exp_004_xai_on_lean_twin.md](../experiments/exp_004_xai_on_lean_twin.md) |
| OULAD benchmark writeup (exp_005) | [docs/experiments/exp_005_public_benchmark_oulad.md](../experiments/exp_005_public_benchmark_oulad.md) |
| OULAD DDD full ablation (exp_006) | [docs/experiments/exp_006_oulad_full_ablation.md](../experiments/exp_006_oulad_full_ablation.md) |
| OULAD DDD XAI (exp_007) | [docs/experiments/exp_007_xai_on_oulad.md](../experiments/exp_007_xai_on_oulad.md) |
| Faithfulness probe (exp_008) | [docs/experiments/exp_008_faithfulness_probe.md](../experiments/exp_008_faithfulness_probe.md) |
| OULAD BBB ablation (exp_009) | [docs/experiments/exp_009_oulad_ablation_bbb2013j.md](../experiments/exp_009_oulad_ablation_bbb2013j.md) |
| OULAD BBB XAI + cross-cohort stability (exp_010) | [docs/experiments/exp_010_xai_on_oulad_bbb2013j.md](../experiments/exp_010_xai_on_oulad_bbb2013j.md) |
| KU Leuven engagement-only (exp_011) | [docs/experiments/exp_011_kuleuven_engagement.md](../experiments/exp_011_kuleuven_engagement.md) |
| 3-institution engagement synthesis (exp_012) | [docs/experiments/exp_012_oulad_engagement.md](../experiments/exp_012_oulad_engagement.md) |
| OULAD feature mapping | [docs/experiments/oulad_feature_mapping.md](../experiments/oulad_feature_mapping.md) |
| Baseline vs ablation comparison | [docs/experiments/exp_001_vs_exp_002_comparison.md](../experiments/exp_001_vs_exp_002_comparison.md) |
| Lean Twin recommendation | `data/artifacts/experiments/exp_002_twin_ablation/lean_twin_recommendation.md` |
| Mastery carry-forward recommendation | `data/artifacts/experiments/exp_003_mastery_validation/mastery_carry_forward_recommendation.md` |
| XAI carry-forward recommendation | `data/artifacts/experiments/exp_004_xai_on_lean_twin/xai_carry_forward_recommendation.md` |
| OULAD benchmark interpretation | `data/artifacts/experiments/exp_005_public_benchmark_oulad/public_vs_synthetic_interpretation.md` |
| OULAD DDD ablation artifacts (exp_006) | `data/artifacts/experiments/exp_006_oulad_full_ablation/` |
| OULAD DDD XAI artifacts (exp_007) | `data/artifacts/experiments/exp_007_xai_on_oulad/` |
| Faithfulness probe artifacts (exp_008) | `data/artifacts/experiments/exp_008_faithfulness_probe/` |
| OULAD BBB ablation artifacts (exp_009) | `data/artifacts/experiments/exp_009_oulad_ablation_bbb2013j/` |
| OULAD BBB XAI + cross-cohort artifacts (exp_010) | `data/artifacts/experiments/exp_010_xai_on_oulad_bbb2013j/` |
| KU Leuven engagement artifacts (exp_011) | `data/artifacts/experiments/exp_011_kuleuven_engagement/` |
| 3-institution engagement synthesis (exp_012) | `data/artifacts/experiments/exp_012_cross_institution_engagement/cross_institution_engagement.md` |
| Final integrated report | [final_integrated_report.md](final_integrated_report.md) |
| Defense claim guardrails | [core_claims_and_nonclaims.md](core_claims_and_nonclaims.md) |
