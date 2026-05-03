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
<!-- experiment-registry:end -->

## Comparison Notes

`exp_002_twin_ablation` exists because `exp_001_baseline` showed that the full
Twin representation was not automatically better than the LMS baseline. The
next experiment therefore tests Twin subgroups rather than adding XAI on top of
an unexamined full feature set.

See [exp_001_vs_exp_002_comparison.md](exp_001_vs_exp_002_comparison.md) for
the compact comparison summary.
