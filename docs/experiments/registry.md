# Experiment Registry

This registry is the canonical index of versioned experiment records. It is
maintained as a concise research history, not as a full MLOps system.

## Lifecycle Rules

- Use a new experiment ID when changing dataset version, schema version,
  feature-set definition, target, split strategy, or model family in a way that
  changes interpretation.
- Preserve previous artifact folders. Do not silently overwrite old results.
- Keep `risk_level` out of supervised training unless the schema and research
  framing are explicitly revised.
- Treat `final_grade` as the primary supervised target for current experiments.

## Registry

<!-- experiment-registry:start -->
| ID | Title | Status | Schema | Dataset / config | Primary target | Artifacts | Doc | Conclusion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| exp_001_baseline | Baseline feature-set comparison | completed | v1.2 | generator_v1_3_refined.yaml | final_grade | [exp_001_baseline](../../data/artifacts/experiments/exp_001_baseline) | [exp_001_baseline.md](exp_001_baseline.md) | `C_twin` did not reliably outperform `B_lms`; Twin redundancy requires ablation. |
| exp_002_twin_ablation | Twin subgroup ablation | completed | v1.2 | generator_v1_3_refined.yaml | final_grade | [exp_002_twin_ablation](../../data/artifacts/experiments/exp_002_twin_ablation) | [exp_002_twin_ablation.md](exp_002_twin_ablation.md) | Carry forward `B_lms_plus_mastery`; full Twin justified: False. |
| exp_003_mastery_validation | Mastery validation | completed | v1.2 | generator_v1_3_refined.yaml | final_grade | [exp_003_mastery_validation](../../data/artifacts/experiments/exp_003_mastery_validation) | [exp_003_mastery_validation.md](exp_003_mastery_validation.md) | Carry `B_lms_plus_mastery` into XAI as the lean Twin candidate. It improves on `B_lms` overall and in at least one early-week cutoff, supporting the early-warning story. |
| exp_004_xai_on_lean_twin | XAI on lean Twin | completed | v1.2 | generator_v1_3_refined.yaml | final_grade | [exp_004_xai_on_lean_twin](../../data/artifacts/experiments/exp_004_xai_on_lean_twin) | [exp_004_xai_on_lean_twin.md](exp_004_xai_on_lean_twin.md) | Carry `B_lms_plus_mastery` forward for dissertation XAI with an `overall_mastery` redundancy caveat; explanations remain teacher-meaningful and do not collapse into one feature. |
| exp_005_public_benchmark_oulad | Public OULAD benchmark for lean Twin transfer | completed | external_oulad_adapter_v1 | OULAD DDD 2013J | final_weighted_score | [exp_005_public_benchmark_oulad](../../data/artifacts/experiments/exp_005_public_benchmark_oulad) | [exp_005_public_benchmark_oulad.md](exp_005_public_benchmark_oulad.md) | `B_lms_plus_mastery_oulad` did not improve the primary OULAD grouped split, but improved a secondary temporal-forward split. |
| exp_006_oulad_full_ablation | Full nested A/B/C ablation on OULAD (DDD 2013J) | completed | external_oulad_adapter_v1 | OULAD DDD 2013J | final_weighted_score | [exp_006_oulad_full_ablation](../../data/artifacts/experiments/exp_006_oulad_full_ablation) | [exp_006_oulad_full_ablation.md](exp_006_oulad_full_ablation.md) | `C_twin_oulad` was approximately level with `B_lms_oulad` on OULAD. |
| exp_007_xai_on_oulad | OULAD model-behavior XAI: feature importance and concentration (DDD 2013J) | completed | external_oulad_adapter_v1 | OULAD DDD 2013J | final_weighted_score | [exp_007_xai_on_oulad](../../data/artifacts/experiments/exp_007_xai_on_oulad) | [exp_007_xai_on_oulad.md](exp_007_xai_on_oulad.md) | Model-behavior explanations for OULAD DDD 2013J; top driver(s) on temporal_forward: assessment_submission_rate_due_to_date, overall_mastery_proxy. |
| exp_008_faithfulness_probe | Controlled XAI faithfulness probe on synthetic generator oracle | completed | v1.2 | generator_v1_3_refined.yaml | final_grade | [exp_008_faithfulness_probe](../../data/artifacts/experiments/exp_008_faithfulness_probe) | [exp_008_faithfulness_probe.md](exp_008_faithfulness_probe.md) | Oracle-ordering Kendall tau = 1.000 |
| exp_009_oulad_ablation_bbb2013j | Second-cohort full A/B/C ablation on OULAD (BBB 2013J) | completed | external_oulad_adapter_v1 | OULAD BBB 2013J | final_weighted_score | [exp_009_oulad_ablation_bbb2013j](../../data/artifacts/experiments/exp_009_oulad_ablation_bbb2013j) | [exp_009_oulad_ablation_bbb2013j.md](exp_009_oulad_ablation_bbb2013j.md) | `C_twin_oulad` improved over `B_lms_oulad` on OULAD. |
| exp_010_xai_on_oulad_bbb2013j | Second-cohort OULAD model-behavior XAI (BBB 2013J) | completed | external_oulad_adapter_v1 | OULAD BBB 2013J | final_weighted_score | [exp_010_xai_on_oulad_bbb2013j](../../data/artifacts/experiments/exp_010_xai_on_oulad_bbb2013j) | [exp_010_xai_on_oulad_bbb2013j.md](exp_010_xai_on_oulad_bbb2013j.md) | Model-behavior explanations for OULAD DDD 2013J; top driver(s) on temporal_forward: cumulative_submitted_weight_to_date, overall_mastery_proxy. |
<!-- experiment-registry:end -->

## Comparison Notes

`exp_002_twin_ablation` exists because `exp_001_baseline` showed that the full
Twin representation was not automatically better than the LMS baseline. The
next experiment therefore tests Twin subgroups rather than adding XAI on top of
an unexamined full feature set.

See [exp_001_vs_exp_002_comparison.md](exp_001_vs_exp_002_comparison.md) for
the compact comparison summary.
