# Dissertation Synthesis

This directory consolidates the existing experimental line of the
**Student Digital Twin XAI** research prototype into a coherent academic
synthesis suitable for dissertation preparation. It does not alter prior
conclusions or modify experiment artifacts. Its purpose is to integrate the
existing repository evidence into a structure that can be lifted into a
dissertation chapter or appendix with minimal adaptation.

The canonical evidence base is the five completed experiments:

- `exp_001_baseline` — baseline feature-set comparison
- `exp_002_twin_ablation` — Twin subgroup ablation
- `exp_003_mastery_validation` — mastery-block validation
- `exp_004_xai_on_lean_twin` — XAI on the lean Twin candidate
- `exp_005_public_benchmark_oulad` — public OULAD transfer benchmark

The supporting documentation includes the data-model contracts under
`docs/data_model/`, the experiment logbook under `docs/experiments/`, the
existing methodological brief in `docs/research/model_experiment_design.md`,
and the ML service documentation in `services/ml/README.md`.

This directory now also contains the final packaging layer for dissertation
writing and oral defense: one integrated report, a defense summary pack, and a
curated set of figures and tables generated from the frozen experiment
artifacts.

## Document Index

| Document | Purpose |
| --- | --- |
| [final_integrated_report.md](final_integrated_report.md) | Single chapter-like report integrating the complete experiment line, including OULAD, into the final bounded dissertation narrative. |
| [methodological_justification_of_model_and_experiment_design.md](methodological_justification_of_model_and_experiment_design.md) | Formal methods narrative covering models, targets, feature sets, splits, metrics, and the role of synthetic data. |
| [experimental_results_synthesis.md](experimental_results_synthesis.md) | Integrated chronological synthesis of the experiment sequence, its setups, and its results. |
| [experiment_progression_summary.md](experiment_progression_summary.md) | Compact tabular summary of the experiment sequence and research consequences. |
| [limitations_and_threats_to_validity.md](limitations_and_threats_to_validity.md) | Honest, academically toned discussion of synthetic-data limits, redundancy, saturation, and explanation scope. |
| [final_research_conclusions.md](final_research_conclusions.md) | Carefully bounded interpretation of the current contribution and the resulting research stance. |
| [figures_and_tables_inventory.md](figures_and_tables_inventory.md) | Inventory of reusable result tables, artifact files, generated figures, and generated tables. |
| [defense_summary.md](defense_summary.md) | Concise oral-defense summary of the problem, method, evidence, result, and contribution. |
| [defense_qna.md](defense_qna.md) | Compact answers to likely supervisor and defense questions. |
| [core_claims_and_nonclaims.md](core_claims_and_nonclaims.md) | Explicit guardrails for what the dissertation can and cannot claim. |

## Reading Order

For a dissertation reader unfamiliar with the project, the recommended order is:

1. [final_integrated_report.md](final_integrated_report.md)
2. [methodological_justification_of_model_and_experiment_design.md](methodological_justification_of_model_and_experiment_design.md)
3. [experimental_results_synthesis.md](experimental_results_synthesis.md)
4. [experiment_progression_summary.md](experiment_progression_summary.md)
5. [limitations_and_threats_to_validity.md](limitations_and_threats_to_validity.md)
6. [final_research_conclusions.md](final_research_conclusions.md)
7. [figures_and_tables_inventory.md](figures_and_tables_inventory.md)
8. [core_claims_and_nonclaims.md](core_claims_and_nonclaims.md)

## Scope and Stance

This synthesis is grounded strictly in the present repository state. Where the
repository contains residual ambiguity — for example, the redundancy of
`overall_mastery`, the saturation of `passed`, the absence of SHAP in the
current explanation phase, or the mixed OULAD transfer benchmark — that
ambiguity is reproduced explicitly rather than smoothed away. The documents
here intentionally avoid causal claims and avoid asserting full external
validity.

The output of this synthesis should be read as **dissertation source material**,
not as a finished dissertation chapter. The narrative is academically toned and
internally consistent, but final adaptation, citation completion, and rhetorical
polishing remain a separate editorial step.

## Defense Demo

The repository includes a minimal read-only web route at `/research-demo`.
The route is backed by frozen experiment artifacts and is intended for defense
explanation, not live training or production analytics.
