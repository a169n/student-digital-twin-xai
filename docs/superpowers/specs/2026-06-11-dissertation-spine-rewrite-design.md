# Dissertation Spine Rewrite (update-in-place) — Design

> **Status:** approved design (2026-06-11). Approach: update-in-place. Next: implementation plan via writing-plans.
> **Commit policy:** NO auto-commits — the user commits manually.

## Goal

Bring the dissertation's stale documents current through exp_012 so the
forward-reading narrative (the "spine") is internally consistent and reflects
the public-first, honest/mixed evidence base — without restructuring the file
set or consolidating into a single document.

The honest, up-to-date narrative ALREADY EXISTS in two documents
(`final_research_conclusions.md`, `defense_summary.md`); the problem is that the
documents a reader/examiner encounters FIRST stop at exp_005 and still present
the synthetic R²≈0.99 / F1=1.000 as if it were a real result. This rewrite
aligns the stale documents to the already-current ones.

## Verified currency map (by actual experiment mentions, 2026-06-11)

**Source of truth (current through exp_012 — do NOT rewrite; align others to these, pull exact numbers from them + artifacts):**
- `docs/dissertation/final_research_conclusions.md` (exp_006/009/011 ×5 each, exp_012 ×3 — incl. §5f)
- `docs/dissertation/defense_summary.md` (full arc incl. exp_012)

**Stale spine documents to update (zero mentions of exp_006–012):**
1. `docs/dissertation/final_integrated_report.md` — main chapter-like report
2. `docs/dissertation/methodological_justification_of_model_and_experiment_design.md` — methods
3. `docs/dissertation/experiment_progression_summary.md` — compact sequence table
4. `docs/dissertation/limitations_and_threats_to_validity.md` — caveats/threats
5. `docs/dissertation/README.md` — index + reading order
6. `docs/dissertation/experimental_results_synthesis.md` — 413-line chronological results narrative (stops at exp_005)

**Partial (small top-up):**
7. `docs/dissertation/core_claims_and_nonclaims.md` — has exp_006/009/011, missing exp_012 only

**Auxiliary (in scope per user decision):**
8. `docs/dissertation/defense_qna.md` — examiner Q&A (stale)
9. `docs/dissertation/figures_and_tables_inventory.md` — artifact/table index (stale)

> NOTE: the earlier Explore-agent map wrongly called `experimental_results_synthesis.md` "current." It is fully stale (verified by reading its tail: §5 = exp_005, ends on the soft "complicates/mixed" framing). It is the single largest addition in this rewrite.

## Canonical findings the stale docs must be aligned to

(Exact numbers to be pulled from the source-of-truth docs + the experiment artifacts during implementation — the plan must cite the artifact, not memory.)

- **Synthetic (exp_001–004):** R²≈0.99 / F1=1.000 are ARTIFACTS of a deterministic circular target (`final_grade` = closed-form weighted mean of the same behaviors the features re-aggregate; week-10 reconstruction error 0.008, corr 1.000000). Must be caveated UPFRONT wherever synthetic numbers appear; never presented as learnable signal.
- **exp_005 (OULAD DDD, 2-set transfer):** grouped `B_lms_plus_mastery_oulad` Δ+0.066 RMSE (worse), temporal_forward Δ−0.406 (better); classification F1 ≈0.86–0.89 (NOT 1.000).
- **exp_006 (OULAD DDD full A/B/C ablation, fixed-model):** mixed-to-null — no Twin block beats `B_lms_oulad` by >1.0 RMSE on either split under a fixed model.
- **exp_009 (OULAD BBB full ablation):** heterogeneous — mastery/`C_twin_oulad` improves on BBB where it did not on DDD; cross-course result is course-specific, not uniform.
- **exp_007 / exp_010 (OULAD XAI):** model-behavior importance is regime-sensitive within a course and partly course-specific across courses (Kendall τ values + Jaccard from the cross_cohort_stability artifacts); explanations lean on near-target/redundant features.
- **exp_008 (synthetic faithfulness probe):** oracle-ordering Kendall τ = 1.000 — a controlled known-ground-truth methods appendix, NOT a headline.
- **exp_011 (KU Leuven engagement-only):** richer engagement neutral, ΔF1 = −0.015.
- **exp_012 (3-institution matched engagement):** ΔF1 neutral-to-modest (fixed-model: temporal_forward ≈0 — KU −0.016 / DDD −0.000 / BBB +0.026; student_group up to +0.072); importance drivers partly transfer, mean Kendall τ = 0.556, verdict `drivers_partly_institution_specific`.

## Per-document changes

### 1. final_integrated_report.md
- Extend the results/methods sections from exp_005 → exp_001–012.
- Add the circular-target caveat UPFRONT where synthetic R²≈0.99 / F1=1.000 appears (currently presented as a dataset property in the "passed classification saturated F1 1.000" section).
- Replace "OULAD complicates / unresolved" with the decisive honest framing: DDD = mixed-to-null full ablation (exp_006); BBB = heterogeneous (exp_009); separate the two cohorts explicitly.
- Add regime-sensitivity (exp_007/010) and the 3-institution engagement robustness (exp_011/012) as CO-EQUAL findings, not afterthoughts.
- Update the abstract and conclusions sections to match (contribution = transfer + explanation-stability + faithfulness probe, NOT accuracy).

### 2. methodological_justification_of_model_and_experiment_design.md
- Extend the experiment-sequence/methods sections through exp_006/009 (full nested A/B/C ablation + fixed-model reporting + OULAD feature-mapping), exp_007/010 (OULAD XAI runner + cross-cohort stability methodology: Kendall τ / Jaccard), exp_008 (controlled faithfulness probe), exp_011/012 (engagement-only matched design + concept-alignment map + cross-institution τ).
- Update the XAI methods section (currently exp_004 "teacher-meaningful") to incorporate the regime-sensitivity finding.

### 3. experiment_progression_summary.md
- Add exp_006–012 rows to the sequence table with honest outcome tags (e.g. exp_006 `mixed-to-null`, exp_009 `heterogeneous`, exp_011 `engagement-neutral`, exp_012 `robustness/partial-transfer`).
- Extend the citation-friendly references section to include exp_006/008/009/010/011/012 doc + artifact paths.

### 4. limitations_and_threats_to_validity.md
- Update the OULAD limitation (currently exp_005 only) to integrate exp_006 (DDD null) + exp_009 (BBB heterogeneous).
- Add a dedicated subsection "Explanation Regime-Sensitivity and Course/Institution-Specificity" with the τ/Jaccard values from exp_007/010 (within/cross-course) and exp_012 (cross-institution, mean τ 0.556).
- Extend the external-validity threat to include the KU Leuven second institution (exp_011) and the 3-institution engagement check (exp_012): even a simpler engagement representation does not transfer robustly.

### 5. README.md
- Update the experiment inventory to include exp_006–012.
- Update the recommended reading order so the now-current spine flows evidence → limitations → conclusions (so a reader reaches decisive evidence before conclusions).
- Refresh per-document currency descriptions.

### 6. experimental_results_synthesis.md
- Add new chronological sections for exp_006 (DDD full ablation), exp_007 (DDD XAI), exp_008 (faithfulness probe), exp_009 (BBB ablation), exp_010 (BBB XAI + cross-cohort stability), exp_011 (KU Leuven engagement), exp_012 (3-institution synthesis) — following the existing per-experiment template (designed-to-test / setup / key result / research consequence).
- Replace the §6–§7 "trajectory" closing framing (which currently ends at exp_005 "complicates/unresolved") with the updated arc through exp_012.

### 7. core_claims_and_nonclaims.md
- Top-up only: add the exp_012 cross-institution robustness claim/non-claim (engagement richness does not robustly help across 3 institutions; drivers partly institution-specific — a robustness finding, not an accuracy claim). Everything else is already current.

### 8. defense_qna.md
- Add Q&A entries covering exp_006–012: the DDD-null vs BBB-heterogeneous distinction, regime-sensitive explanations, the 3-institution engagement robustness, and the synthetic-circularity question (align to the entries already in `defense_summary.md`).

### 9. figures_and_tables_inventory.md
- Update the artifact/figure/table index to include exp_006–012 outputs (ablation tables, fixed-model tables, XAI importance + concentration, cross_cohort_stability, exp_012 cross_institution_engagement, engagement_importance CSVs).

## Cross-cutting guardrails (carry into every edited doc)
- Synthetic R²≈0.99 / F1=1.000 = circular-target ARTIFACT, never "learnable signal."
- "Digital Twin" = a lean, time-aware weekly state representation, NOT a simulation/counterfactual engine.
- Contribution rests on transfer + explanation-stability + a known-ground-truth faithfulness probe — NOT accuracy.
- Always report the fixed-model view alongside best-per-cell; never headline the model-flip win.
- Disclose the OULAD partial target circularity (assessment-score features feed `final_weighted_score`); lean interpretation on clickstream + classification.
- OULAD is TWO distinct ablations (DDD exp_006 null, BBB exp_009 heterogeneous), never one undifferentiated "OULAD."

## Light consistency pass (NOT a rewrite)
- Touch the two source-of-truth docs (`final_research_conclusions.md`, `defense_summary.md`) ONLY if an updated stale doc would otherwise contradict them; no structural rewrites of the current docs.

## Out of scope
- No consolidation into a single thesis document; the 9-file structure stays.
- No aggressive de-duplication (the redundancy / SHAP-not-causal caveats may remain repeated across docs); only fix outright contradictions.
- No new experiments; no changes to code or experiment artifacts (the only code already touched — the exp_010 cohort-label fix — is a separate, completed debt).

## Verification (acceptance criteria)
- Every quantitative figure added traces to a named experiment artifact or to `final_research_conclusions.md` / `defense_summary.md` (no invented or memory-sourced numbers).
- A final consistency check: no edited document contradicts `core_claims_and_nonclaims.md` or the source-of-truth docs (especially on the synthetic-circularity non-claim, the "Digital Twin ≠ simulation" framing, and accuracy-vs-robustness).
- No remaining occurrence of the stale "OULAD complicates / unresolved / F1=1.000-as-real" framing in any spine document.
- `grep` confirms each of the 6 core docs now references exp_006–012 where relevant; README reading order points to current docs.
