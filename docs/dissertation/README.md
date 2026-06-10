# Dissertation Synthesis

This directory consolidates the existing experimental line of the
**Student Digital Twin XAI** research prototype into a coherent academic
synthesis suitable for dissertation preparation. It does not alter prior
conclusions or modify experiment artifacts. Its purpose is to integrate the
existing repository evidence into a structure that can be lifted into a
dissertation chapter or appendix with minimal adaptation.

The canonical evidence base is the twelve completed experiments. The first
group is synthetic (internally valid but on a **circular target**, so its
near-perfect numbers are algebraic artifacts, not learnable signal); the second
group carries the decisive real-data and cross-institution evidence:

- `exp_001_baseline` — baseline feature-set comparison (synthetic)
- `exp_002_twin_ablation` — Twin subgroup ablation (synthetic)
- `exp_003_mastery_validation` — mastery-block validation (synthetic)
- `exp_004_xai_on_lean_twin` — XAI on the lean Twin candidate (synthetic)
- `exp_005_public_benchmark_oulad` — public OULAD (DDD 2013J) 2-set transfer benchmark
- `exp_006_oulad_full_ablation` — OULAD DDD 2013J full nested A/B/C ablation; fixed-model, **mixed-to-null** (no Twin block beats the LMS baseline by >1.0 RMSE)
- `exp_007_oulad_xai` — OULAD DDD XAI; importance rankings **regime-sensitive** (cross-split Kendall τ 0.55–0.79, none ≥0.90)
- `exp_008_faithfulness_probe` — controlled synthetic **faithfulness probe** (final-week oracle τ = 1.0; methods appendix, not a headline)
- `exp_009_oulad_bbb_ablation` — OULAD BBB 2013J full ablation; **heterogeneous** (mastery improves temporal-forward Δ −1.026 RMSE, crossing the threshold DDD never did)
- `exp_010_oulad_bbb_xai` — OULAD BBB XAI + **cross-cohort stability** (DDD vs BBB Kendall τ 0.32–0.61, lower than within-cohort)
- `exp_011_ku_leuven_engagement` — KU Leuven 1819, second institution, **engagement-only** classification (mastery ablation cannot even be built)
- `exp_012_oulad_engagement` — matched **3-institution engagement** robustness (DDD + BBB + KU; feature-richness does not robustly help, importance mean τ 0.56)

The supporting documentation includes the data-model contracts under
`docs/data_model/`, the experiment logbook under `docs/experiments/`, the
existing methodological brief in `docs/research/model_experiment_design.md`,
and the ML service documentation in `services/ml/README.md`.

This directory now also contains the final packaging layer for dissertation
writing and oral defense: one integrated report, a defense summary pack, and a
curated set of figures and tables generated from the frozen experiment
artifacts.

## Document Index

All documents are current through `exp_012`.

| Document | Purpose |
| --- | --- |
| [final_integrated_report.md](final_integrated_report.md) | Single chapter-like report integrating the complete exp_001–012 line — synthetic circularity caveat upfront, OULAD split into DDD (exp_006, null) and BBB (exp_009, heterogeneous), regime-sensitivity and 3-institution engagement as co-equal findings — into the final bounded dissertation narrative. |
| [methodological_justification_of_model_and_experiment_design.md](methodological_justification_of_model_and_experiment_design.md) | Formal methods narrative covering models, targets, feature sets, splits, metrics, the role of synthetic data, and — through exp_006–012 — full nested A/B/C ablation with fixed-model reporting, the OULAD XAI runner with cross-cohort/cross-split stability methodology, the faithfulness probe, and the matched engagement design. |
| [experimental_results_synthesis.md](experimental_results_synthesis.md) | Integrated chronological synthesis of the full exp_001–012 sequence, its setups, and its results, closing on the honest mixed/negative real-data arc. |
| [experiment_progression_summary.md](experiment_progression_summary.md) | Compact tabular summary of the exp_001–012 sequence, research consequences, and citation-friendly artifact references. |
| [limitations_and_threats_to_validity.md](limitations_and_threats_to_validity.md) | Honest, academically toned discussion of synthetic-data limits, redundancy, saturation, OULAD two-cohort heterogeneity, explanation regime-sensitivity/course-specificity, and cross-institution external validity (exp_011/012). |
| [final_research_conclusions.md](final_research_conclusions.md) | Carefully bounded interpretation of the current contribution and the resulting research stance, reflecting the complete exp_001–012 evidence base (source of truth). |
| [figures_and_tables_inventory.md](figures_and_tables_inventory.md) | Inventory of reusable result tables, artifact files, generated figures, and generated tables, indexed through the exp_006–012 outputs. |
| [defense_summary.md](defense_summary.md) | Concise oral-defense summary of the problem, method, evidence, result, and contribution, current through exp_012. |
| [defense_qna.md](defense_qna.md) | Compact answers to likely supervisor and defense questions, covering the synthetic-circularity, real-data heterogeneity, explanation-stability, and cross-institution themes through exp_012. |
| [core_claims_and_nonclaims.md](core_claims_and_nonclaims.md) | Explicit guardrails for what the dissertation can and cannot claim, including the exp_012 cross-institution robustness claim/non-claim. |

## Reading Order

For a dissertation reader unfamiliar with the project, the recommended order
puts the decisive exp_006–012 evidence (results, methods, limitations) **before**
the conclusions and claims, so the bounded stance is reached only after the
honest real-data and cross-institution findings:

1. [final_integrated_report.md](final_integrated_report.md) — the integrated narrative
2. [experimental_results_synthesis.md](experimental_results_synthesis.md) — the chronological evidence through exp_012
3. [methodological_justification_of_model_and_experiment_design.md](methodological_justification_of_model_and_experiment_design.md) — how the evidence was produced
4. [limitations_and_threats_to_validity.md](limitations_and_threats_to_validity.md) — heterogeneity, regime-sensitivity, external validity
5. [final_research_conclusions.md](final_research_conclusions.md) — the bounded interpretation
6. [core_claims_and_nonclaims.md](core_claims_and_nonclaims.md) — the explicit guardrails
7. [defense_summary.md](defense_summary.md) — the oral-defense summary
8. [defense_qna.md](defense_qna.md) — anticipated defense questions
9. [figures_and_tables_inventory.md](figures_and_tables_inventory.md) — appendix: artifacts, figures, tables
10. [experiment_progression_summary.md](experiment_progression_summary.md) — appendix: compact sequence table + citations

## Scope and Stance

This synthesis is grounded strictly in the present repository state. Where the
repository contains residual ambiguity — for example, the circular synthetic
target (whose near-perfect numbers are algebraic artifacts), the absence of SHAP
in the current explanation phase, the heterogeneous OULAD real-data evidence (DDD
null, BBB partial), the regime-sensitivity and course-specificity of the
explanations, or the only-partial transfer of importance drivers across three
institutions — that ambiguity is reproduced explicitly rather than smoothed away.
The documents here intentionally avoid causal claims and avoid asserting full
external validity.

The output of this synthesis should be read as **dissertation source material**,
not as a finished dissertation chapter. The narrative is academically toned and
internally consistent, but final adaptation, citation completion, and rhetorical
polishing remain a separate editorial step.

## Defense Demo

The repository includes a minimal read-only web route at `/research-demo`.
The route is backed by frozen experiment artifacts and is intended for defense
explanation, not live training or production analytics.
