# Dissertation Synthesis

This directory consolidates the existing experimental line of the
**Student Digital Twin XAI** research prototype into a coherent academic
synthesis suitable for dissertation preparation. It does not introduce new
experiments, alter prior conclusions, or modify experiment artifacts. Its sole
purpose is to integrate the existing repository evidence into a structure that
can be lifted into a dissertation chapter or appendix with minimal adaptation.

The canonical evidence base is the four completed experiments:

- `exp_001_baseline` — baseline feature-set comparison
- `exp_002_twin_ablation` — Twin subgroup ablation
- `exp_003_mastery_validation` — mastery-block validation
- `exp_004_xai_on_lean_twin` — XAI on the lean Twin candidate

The supporting documentation includes the data-model contracts under
`docs/data_model/`, the experiment logbook under `docs/experiments/`, the
existing methodological brief in `docs/research/model_experiment_design.md`,
and the ML service documentation in `services/ml/README.md`.

## Document Index

| Document | Purpose |
| --- | --- |
| [methodological_justification_of_model_and_experiment_design.md](methodological_justification_of_model_and_experiment_design.md) | Formal methods narrative covering models, targets, feature sets, splits, metrics, and the role of synthetic data. |
| [experimental_results_synthesis.md](experimental_results_synthesis.md) | Integrated chronological synthesis of the four experiments, their setups, and their results. |
| [experiment_progression_summary.md](experiment_progression_summary.md) | Compact tabular summary of the experiment sequence and research consequences. |
| [limitations_and_threats_to_validity.md](limitations_and_threats_to_validity.md) | Honest, academically toned discussion of synthetic-data limits, redundancy, saturation, and explanation scope. |
| [final_research_conclusions.md](final_research_conclusions.md) | Carefully bounded interpretation of the current contribution and the resulting research stance. |
| [figures_and_tables_inventory.md](figures_and_tables_inventory.md) | Inventory of reusable result tables, artifact files, and candidate figures. |

## Reading Order

For a dissertation reader unfamiliar with the project, the recommended order is:

1. [methodological_justification_of_model_and_experiment_design.md](methodological_justification_of_model_and_experiment_design.md)
2. [experimental_results_synthesis.md](experimental_results_synthesis.md)
3. [experiment_progression_summary.md](experiment_progression_summary.md)
4. [limitations_and_threats_to_validity.md](limitations_and_threats_to_validity.md)
5. [final_research_conclusions.md](final_research_conclusions.md)
6. [figures_and_tables_inventory.md](figures_and_tables_inventory.md)

## Scope and Stance

This synthesis is grounded strictly in the present repository state. Where the
repository contains residual ambiguity — for example, the redundancy of
`overall_mastery`, the saturation of `passed`, or the absence of SHAP in the
current explanation phase — that ambiguity is reproduced explicitly rather than
smoothed away. The documents here intentionally avoid causal claims and avoid
asserting external validity beyond the synthetic experimental environment.

The output of this synthesis should be read as **dissertation source material**,
not as a finished dissertation chapter. The narrative is academically toned and
internally consistent, but final adaptation, citation completion, and rhetorical
polishing remain a separate editorial step.
