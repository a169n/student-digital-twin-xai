# Dissertation Spine Rewrite (update-in-place) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring the 9 stale/partial dissertation documents current through exp_012 so the forward-reading "spine" reflects the public-first honest/mixed evidence base, aligned to the two already-current source-of-truth docs, without restructuring the file set.

**Architecture:** Documentation-only edits (no code, no tests in the pytest sense). One task per document. Every task draws its facts from the **Canonical Findings Ledger** embedded in this plan (extracted verbatim from `docs/dissertation/final_research_conclusions.md`, the verified source of truth) — so numbers never diverge across docs. "Verification" is grep-based: confirm the doc now references exp_006–012 where relevant, contains the correct figures, and no longer carries stale framing (synthetic F1=1.000-as-real, OULAD "complicates/unresolved" as the final word).

**Tech Stack:** Markdown. Tools: Read, Edit, Grep. No Python, no pytest.

**Commit policy:** This repo does NOT auto-commit. Each task ends with a `git add` to stage; the WORKER does NOT run `git commit` (the user commits manually). Commit message lines are shown for the user's convenience.

**Source of truth (do NOT edit except the light-consistency note in Task 10):** `docs/dissertation/final_research_conclusions.md`, `docs/dissertation/defense_summary.md`. Align all stale docs to these.

---

## Canonical Findings Ledger (single source for every task — use these exact figures)

**Synthetic (exp_001–004) — internally valid but on a CIRCULAR target; numbers are artifacts:**
- `final_grade` is a deterministic, noise-free closed-form weighted mean of the same behaviors the features re-aggregate (`services/ml/src/generator/final_results.py:74-84`); week-10 reconstruction error 0.008, corr 1.000000. Hence synthetic R²≈0.99 and `passed` F1=1.000 are ALGEBRAIC ARTIFACTS, not learnable signal. This caveat must lead wherever synthetic numbers appear.
- exp_001: full `C_twin` did NOT reliably beat `B_lms`; worse under temporal-forward.
- exp_002: `B_lms_plus_mastery` only single block improving primary split — RMSE 1.894 vs 2.101 (Δ −0.206); full `C_twin_full` underperforms. Fixed-model re-analysis: mastery ≈ +0.41 RMSE WORSE on temporal-forward; `B_lms_plus_indices` only block improving BOTH splits (≈ −0.066 / −0.068).
- exp_003: `overall_mastery`↔`final_grade` Pearson r 0.984; strongest LMS correlate `avg_assignment_score_to_date` |r| 0.993; removing `overall_mastery` raises RMSE +0.228; improvements at weeks 4–8 (incl. early window 4–6); leakage-safe (≤ snapshot week).
- exp_004: global importance `activity_score_to_date` 0.648, `overall_mastery` 0.178, `avg_assignment_score_to_date` 0.090; dominance audit `acceptable_with_caveat`; avg local mastery share 0.194 < 0.60 threshold; permutation+local median-replacement, 15 repeats, NO SHAP (directional model-behavior, not causal).

**exp_005 (OULAD DDD 2013J, 2-set transfer):** grouped `B_lms_plus_mastery_oulad` 12.724 vs `B_lms_oulad` 12.658 (Δ +0.066, worse); temporal-forward 9.161 vs 9.566 (Δ −0.406, better); classification F1 grouped 0.863/0.861, temporal 0.887/0.884 (NOT 1.000). Framing: "complicates" — but SUPERSEDED by exp_006 (do not let "complicates" be the final OULAD word).

**exp_006 (OULAD DDD 2013J full nested A/B/C ablation, fixed-model GB):** 67830 snapshots, 1938 students. MIXED-TO-NULL: no Twin block beats `B_lms_oulad` by >1.0 RMSE on either split. Mastery temporal 9.561→9.180 (Δ −0.381) but +0.061 grouped; index block temporal −0.218, grouped +0.008; `C_twin_oulad` within ±0.025 both splits; `A_simple_oulad` clearly worse (+1.207 grouped, +4.105 temporal). Classification F1 0.83–0.887, never 1.000 (genuinely predictive, non-circular).

**exp_007 (OULAD DDD XAI):** importance `assessment_submission_rate_due_to_date` 0.28–0.38 (LMS), `overall_mastery_proxy` 0.23–0.43 (co-circular), `is_unregistered_by_week` 0.13–0.20 (exogenous), VLE clickstream 0.02–0.06. Regime-sensitivity (cross-split Kendall τ): `B_lms_oulad` 0.79, `B_lms_plus_mastery_oulad` 0.68, `C_twin_oulad` 0.55 (mean 0.67, none ≥0.90); Jaccard top-5 1.00/1.00/0.67. Model-behavior, not causal.

**exp_008 (synthetic faithfulness probe — methods appendix, NOT headline):** final-week oracle-ordering Kendall τ = 1.0; `activity_score_to_date` share 0.108 (latent-driven proxy); `overall_mastery`↔`avg_assignment_score_to_date` Pearson r 0.994.

**exp_009 (OULAD BBB 2013J full ablation):** 2237 students, 80532 snapshots, richer dated-assessment structure. HETEROGENEOUS: mastery improves temporal-forward Δ −1.026 RMSE (5.284 vs 6.311) — crosses the 1.0 threshold DDD never did; `C_twin_oulad` temporal Δ −0.765; student-grouped every block within 0.087 (null, as DDD); trend & index null on both splits of both courses. F1 0.87–0.93, never 1.000.

**exp_010 (OULAD BBB XAI) + cross-cohort stability:** shared topology (`overall_mastery_proxy`, submission discipline, `is_unregistered_by_week` dominate both courses) but unstable rankings — cross-cohort Kendall τ (DDD vs BBB) 0.32–0.61 (mean 0.52), lower than within-cohort 0.55–0.79 (mean 0.67), none ≥0.90; Jaccard top-5 0.43–1.00.

**exp_011 (KU Leuven 1819, second institution — engagement-only, classification-only PASSED):** 1495 students, 2 courses pooled, weeks 2–15. Mastery ablation CANNOT be built (no scored assessments / continuous grade — itself a cross-institution heterogeneity finding). Engagement predicts PASSED only modestly: F1 0.75–0.76, ROC-AUC 0.65–0.72. Richer `B_engagement` ≈ minimal `A_simple_engagement`: fixed-model F1 Δ −0.015 temporal / +0.000 grouped; ROC-AUC +0.009/+0.041. `cumulative_active_days_to_date` + `cumulative_clicks_to_date` dominate (active-days 0.456 share temporal).

**exp_012 (matched 3-institution engagement-only PASSED: DDD + BBB + KU 1819):** Part A fixed-model GB `B − A` F1: student_group DDD +0.072 / BBB +0.039 / KU +0.000; temporal_forward DDD −0.0003 / KU −0.015 / BBB +0.026 (spread −0.016 to +0.026); ROC-AUC all six cells positive +0.009 to +0.041. Honest reading: a 2-feature engagement baseline (clicks + active-days) is hard to beat. Part B importance-rank stability over 7 shared concepts: mean Kendall τ 0.56 (student_group 0.49, temporal_forward 0.62), below 0.90; most stable KU↔BBB τ 0.714, least KU↔DDD student_group τ 0.238; verdict `drivers_partly_institution_specific`; clicks/active-days are the recurring top drivers, mid/lower ordering only partly transfers. Robustness result, NOT accuracy claim. Synthesis: `docs/experiments/exp_012_oulad_engagement.md`.

**Overall honest arc (the spine's thesis):** Synthetic "mastery win" = circular-target artifact → real OULAD is heterogeneous (DDD null exp_006, BBB partial exp_009) → explanations regime-sensitive + course-specific (exp_007/010) → second institution KU Leuven + 3-institution engagement (exp_011/012) confirm feature-richness does not robustly help. **Contribution = reproducible leakage-aware methodology + explanation-stability analysis + honest mixed/negative real-data finding + a cautionary synthetic-circularity demonstration. NOT accuracy, NOT Digital-Twin superiority, NOT a simulation engine.**

**Cross-cutting guardrails (every doc):** (1) synthetic R²≈0.99/F1=1.000 = artifact, never learnable signal; (2) "Digital Twin" = lean time-aware weekly state representation, NOT simulation/counterfactual; (3) contribution = transfer + explanation-stability + faithfulness probe, NOT accuracy; (4) always pair best-per-cell with fixed-model; never headline the model-flip win; (5) disclose OULAD partial target circularity (assessment-score feeds `final_weighted_score`); lean on clickstream + classification; (6) OULAD = TWO distinct ablations (DDD null, BBB heterogeneous), never one undifferentiated "OULAD".

---

## File / task map

| Task | File | Action |
|---|---|---|
| 1 | `docs/dissertation/experimental_results_synthesis.md` | Add exp_006–012 chronological sections; update §6–§7 closing arc |
| 2 | `docs/dissertation/final_integrated_report.md` | Extend report through exp_012; upfront synthetic caveat; DDD/BBB split; co-equal regime + exp_012 findings; fix abstract/conclusions |
| 3 | `docs/dissertation/methodological_justification_of_model_and_experiment_design.md` | Extend methods through exp_006–012 (ablation/fixed-model, XAI+stability, engagement matched design) |
| 4 | `docs/dissertation/limitations_and_threats_to_validity.md` | OULAD heterogeneity; new regime-sensitivity/course-specificity subsection; external validity exp_011/012 |
| 5 | `docs/dissertation/experiment_progression_summary.md` | Add exp_006–012 rows + citation references |
| 6 | `docs/dissertation/core_claims_and_nonclaims.md` | Add exp_012 claim/non-claim (top-up only) |
| 7 | `docs/dissertation/defense_qna.md` | Add Q&A for exp_006–012 |
| 8 | `docs/dissertation/figures_and_tables_inventory.md` | Add exp_006–012 artifacts/tables/figures |
| 9 | `docs/dissertation/README.md` | Update inventory + reading order + currency (do LAST) |
| 10 | (cross-doc) | Final consistency sweep |

**Every task, before editing:** Read the target doc IN FULL to match its existing structure, heading style, and tone. Use ONLY figures from the Canonical Findings Ledger above (or, if a needed number is not in the ledger, read it from the cited experiment artifact and note that). Apply the cross-cutting guardrails. Do NOT invent numbers.

---

## Task 1: experimental_results_synthesis.md — add exp_006–012 sections

**Files:** Modify `docs/dissertation/experimental_results_synthesis.md` (currently ends at §7, exp_005).

- [ ] **Step 1: Read the target doc in full** to learn its per-experiment template (each experiment has subsections: "What it was designed to test" / "Setup" / "Key result" / "Research consequence") and its §6 "Trajectory" and §7 "Why XAI…" closing sections.

- [ ] **Step 2: Append new experiment sections after §5 (exp_005)**, following the SAME per-experiment template, for: exp_006 (DDD full ablation), exp_007 (DDD XAI + regime-sensitivity), exp_008 (faithfulness probe — methods appendix), exp_009 (BBB ablation, heterogeneous), exp_010 (BBB XAI + cross-cohort stability), exp_011 (KU Leuven engagement-only), exp_012 (3-institution synthesis). Use the exact figures from the Ledger for each. Renumber/insert cleanly (e.g. §5 stays exp_005, add §5.1…§5.7 or §6…§12 matching the doc's numbering convention — match what the doc already does).

- [ ] **Step 3: Rewrite the §6 "Trajectory" and §7 closing** so the arc runs through exp_012 (not ending on exp_005 "complicates/unresolved"). The new closing must state the honest arc from the Ledger's "Overall honest arc" paragraph: circular-artifact → heterogeneous real data → regime/course-specific explanations → cross-institution feature-richness does not robustly help; contribution = methodology + honest finding.

- [ ] **Step 4: Verify**

Run: `grep -c "exp_006\|exp_009\|exp_011\|exp_012" docs/dissertation/experimental_results_synthesis.md` → expect ≥ 4.
Run: `grep -n "complicates rather than" docs/dissertation/experimental_results_synthesis.md` → the exp_005 "complicates" wording may remain in the exp_005 section, but confirm the DOC's final/closing section no longer ends on "unresolved/complicates" as the last word (read the new §closing).
Run: `grep -n "0.5556\|0.56\|drivers_partly_institution_specific\|-1.026\|mixed-to-null" docs/dissertation/experimental_results_synthesis.md` → confirm exp_012 mean-τ, exp_009 BBB delta, and exp_006 framing are present.

- [ ] **Step 5: Stage (no commit)**

```bash
git add docs/dissertation/experimental_results_synthesis.md
# user commits: docs(dissertation): extend results synthesis through exp_012
```

---

## Task 2: final_integrated_report.md — extend main report through exp_012

**Files:** Modify `docs/dissertation/final_integrated_report.md` (~355 lines, ends at exp_005).

- [ ] **Step 1: Read the target doc in full**; locate the abstract/intro, the results sections (esp. the synthetic "passed classification saturated F1 1.000" section and the exp_005 "OULAD complicates" section), and the conclusions.

- [ ] **Step 2: Add the synthetic circular-target caveat UPFRONT** wherever the synthetic R²≈0.99 / F1=1.000 appears, using the Ledger's synthetic-circularity wording (deterministic noise-free target; reconstruction error 0.008; artifacts not learnable signal). The F1=1.000 must never read as a real capability.

- [ ] **Step 3: Extend the results section from exp_005 → exp_006–012.** Split OULAD into two distinct ablations: DDD 2013J (exp_006, mixed-to-null) and BBB 2013J (exp_009, heterogeneous, mastery temporal −1.026). Add exp_007/010 regime-sensitivity + cross-cohort (τ 0.55–0.79 within, 0.32–0.61 cross) and exp_011/012 engagement robustness (ΔF1 −0.015; mean τ 0.56) as CO-EQUAL findings. Use Ledger figures.

- [ ] **Step 4: Replace "OULAD complicates / unresolved"** as the report's external-evidence verdict with the decisive honest framing (DDD null, BBB heterogeneous; feature-richness not robust across 3 cohorts/2 institutions).

- [ ] **Step 5: Update the abstract and conclusions** to match: contribution = methodology + explanation-stability + honest mixed/negative finding + cautionary circularity demonstration; NOT accuracy, NOT Twin superiority, NOT simulation.

- [ ] **Step 6: Verify**

Run: `grep -c "exp_006\|exp_009\|exp_011\|exp_012" docs/dissertation/final_integrated_report.md` → ≥ 4.
Run: `grep -n "artifact\|deterministic\|circular" docs/dissertation/final_integrated_report.md` → confirm the synthetic caveat is present near the F1=1.000 mention.
Run: `grep -n "BBB 2013J\|DDD 2013J" docs/dissertation/final_integrated_report.md` → confirm both cohorts named distinctly.

- [ ] **Step 7: Stage (no commit)**

```bash
git add docs/dissertation/final_integrated_report.md
# user commits: docs(dissertation): extend integrated report through exp_012, lead with synthetic-circularity caveat
```

---

## Task 3: methodological_justification_of_model_and_experiment_design.md — extend methods

**Files:** Modify `docs/dissertation/methodological_justification_of_model_and_experiment_design.md` (~365 lines, methods stop at exp_005).

- [ ] **Step 1: Read the target doc in full**; locate the experiment-sequence/methods section and the XAI methods section (currently exp_004 "teacher-meaningful").

- [ ] **Step 2: Extend the experiment-sequence/methods** through: exp_006/009 — full nested A/B/C ablation methodology, fixed-model reporting (why: neutralize the model-flip artifact), OULAD feature-mapping (adapter analogues); exp_007/010 — OULAD XAI runner (permutation + native + local, no SHAP) and the cross-cohort/cross-split explanation-stability methodology (Kendall τ / Jaccard top-k); exp_008 — controlled faithfulness probe (final-week known-ground-truth oracle); exp_011/012 — engagement-only matched design (shared dataset-agnostic core), the concept-alignment map, and cross-institution τ. Use Ledger figures where a result is cited.

- [ ] **Step 3: Update the XAI methods subsection** to incorporate the regime-sensitivity finding (importance rankings are not regime-invariant; τ values from exp_007/010) — methods justification for why stability is measured.

- [ ] **Step 4: Verify**

Run: `grep -c "exp_006\|exp_009\|exp_011\|exp_012" docs/dissertation/methodological_justification_of_model_and_experiment_design.md` → ≥ 4.
Run: `grep -n "fixed-model\|Kendall\|concept-alignment\|cross-cohort\|faithfulness" docs/dissertation/methodological_justification_of_model_and_experiment_design.md` → confirm the new methodology terms appear.

- [ ] **Step 5: Stage (no commit)**

```bash
git add docs/dissertation/methodological_justification_of_model_and_experiment_design.md
# user commits: docs(dissertation): extend methodology through exp_006-012
```

---

## Task 4: limitations_and_threats_to_validity.md — heterogeneity, regime-sensitivity, external validity

**Files:** Modify `docs/dissertation/limitations_and_threats_to_validity.md` (~262 lines).

- [ ] **Step 1: Read the target doc in full**; locate the OULAD-limitations section (currently exp_005 only) and the external-validity threat section.

- [ ] **Step 2: Update the OULAD limitation** to integrate exp_006 (DDD null) + exp_009 (BBB heterogeneous) — replace the exp_005-only "mixed" framing with the two-cohort heterogeneity (Ledger figures). Keep/strengthen the OULAD partial-target-circularity disclosure (assessment-score feeds `final_weighted_score`).

- [ ] **Step 3: Add a new subsection** "Explanation Regime-Sensitivity and Course/Institution-Specificity" with the τ/Jaccard values: within-course cross-split τ 0.55–0.79 (mean 0.67), cross-course τ 0.32–0.61 (mean 0.52), cross-institution engagement mean τ 0.56 — none reaching 0.90. Frame as a threat to the stability/usefulness of explanations across regimes.

- [ ] **Step 4: Extend the external-validity threat** to include KU Leuven (exp_011, second institution, engagement-only — mastery cannot even be built) and exp_012 (3-institution engagement: richer features do not robustly help). State the partiality honestly (engagement task ≠ OULAD assessment task).

- [ ] **Step 5: Verify**

Run: `grep -c "exp_006\|exp_009\|exp_011\|exp_012" docs/dissertation/limitations_and_threats_to_validity.md` → ≥ 4.
Run: `grep -n "regime-sensitiv\|0.52\|0.67\|course-specific\|KU Leuven" docs/dissertation/limitations_and_threats_to_validity.md` → confirm the new subsection + external-validity additions.

- [ ] **Step 6: Stage (no commit)**

```bash
git add docs/dissertation/limitations_and_threats_to_validity.md
# user commits: docs(dissertation): add regime-sensitivity + multi-cohort/institution limitations
```

---

## Task 5: experiment_progression_summary.md — sequence table + citations

**Files:** Modify `docs/dissertation/experiment_progression_summary.md` (~110 lines, table stops at exp_005).

- [ ] **Step 1: Read the target doc in full**; locate the sequence table (the per-experiment rows) and the "citation-friendly references" section.

- [ ] **Step 2: Add table rows** for exp_006, exp_007, exp_008, exp_009, exp_010, exp_011, exp_012 matching the existing columns, with honest one-line outcomes/tags from the Ledger (exp_006 `mixed-to-null` DDD; exp_007 `regime-sensitive XAI`; exp_008 `faithfulness probe τ=1.0 appendix`; exp_009 `heterogeneous` BBB mastery −1.026; exp_010 `cross-cohort τ 0.32–0.61`; exp_011 `engagement-neutral` ΔF1 −0.015; exp_012 `3-institution robustness, partial transfer τ 0.56`). Replace any soft "complicates" tag for exp_005 context with a pointer that exp_006 supersedes it.

- [ ] **Step 3: Extend the citation-friendly references** to include the doc + artifact paths for exp_006/007/008/009/010/011/012 (e.g. `docs/experiments/exp_006_oulad_full_ablation.md`, `docs/experiments/exp_012_oulad_engagement.md`, `data/artifacts/experiments/exp_012_cross_institution_engagement/`).

- [ ] **Step 4: Verify**

Run: `grep -c "exp_006\|exp_009\|exp_011\|exp_012" docs/dissertation/experiment_progression_summary.md` → ≥ 4.
Run: `grep -n "exp_012_oulad_engagement\|cross_institution_engagement" docs/dissertation/experiment_progression_summary.md` → confirm citation paths added.

- [ ] **Step 5: Stage (no commit)**

```bash
git add docs/dissertation/experiment_progression_summary.md
# user commits: docs(dissertation): add exp_006-012 to progression summary + citations
```

---

## Task 6: core_claims_and_nonclaims.md — exp_012 top-up

**Files:** Modify `docs/dissertation/core_claims_and_nonclaims.md` (~109 lines; has exp_006/009/011, missing exp_012).

- [ ] **Step 1: Read the target doc in full**; locate the "claims" and "cannot make" lists and the existing exp_011/engagement entries.

- [ ] **Step 2: Add the exp_012 entries** consistent with the existing style: a CLAIM that, across three matched institutions, a minimal 2-feature engagement baseline is hard to beat and importance drivers transfer only partially (mean τ 0.56) — a robustness finding; and a NON-CLAIM that this is an accuracy win or a causal/like-for-like institutional replication. Keep it to ~2–4 bullet lines (top-up, not a section).

- [ ] **Step 3: Verify**

Run: `grep -c "exp_012" docs/dissertation/core_claims_and_nonclaims.md` → ≥ 1.
Run: `grep -n "robustness\|partly\|0.56\|drivers_partly" docs/dissertation/core_claims_and_nonclaims.md` → confirm the framing is present.

- [ ] **Step 4: Stage (no commit)**

```bash
git add docs/dissertation/core_claims_and_nonclaims.md
# user commits: docs(dissertation): add exp_012 cross-institution robustness claim/non-claim
```

---

## Task 7: defense_qna.md — Q&A for exp_006–012

**Files:** Modify `docs/dissertation/defense_qna.md` (~104 lines, stale).

- [ ] **Step 1: Read the target doc in full** AND read `docs/dissertation/defense_summary.md` (source of truth, has the exp_012 Q&A) to match phrasing/format.

- [ ] **Step 2: Add Q&A entries** in the file's existing format for the examiner's likely questions: (a) "Isn't your synthetic accuracy meaningless given the circular target?" (yes — that's why real OULAD F1 0.83–0.93 is the evidence); (b) "Does the Twin help on real data?" (heterogeneous — DDD null exp_006, BBB partial exp_009 mastery −1.026); (c) "Are the explanations stable?" (regime-sensitive τ 0.55–0.79 within, 0.32–0.61 cross-course); (d) "Does it hold beyond one institution?" (KU Leuven exp_011 + 3-institution exp_012: feature-richness does not robustly help, mean τ 0.56). Align answers to the Ledger + defense_summary.md; do not contradict them.

- [ ] **Step 3: Verify**

Run: `grep -c "exp_006\|exp_009\|exp_011\|exp_012" docs/dissertation/defense_qna.md` → ≥ 3.
Run: `grep -n "circular\|heterogeneous\|regime\|institution" docs/dissertation/defense_qna.md` → confirm the four themes are covered.

- [ ] **Step 4: Stage (no commit)**

```bash
git add docs/dissertation/defense_qna.md
# user commits: docs(dissertation): add exp_006-012 defense Q&A
```

---

## Task 8: figures_and_tables_inventory.md — artifact index through exp_012

**Files:** Modify `docs/dissertation/figures_and_tables_inventory.md` (~183 lines, stale).

- [ ] **Step 1: Read the target doc in full** to learn its inventory format (how figures/tables/artifacts are listed and pathed).

- [ ] **Step 2: Add inventory entries** for exp_006–012 outputs, matching the format: exp_006/009 ablation tables (incl. fixed-model tables), exp_007/010 XAI importance + concentration + `cross_cohort_stability`, exp_008 faithfulness probe, exp_011 engagement results + `engagement_importance.csv`, exp_012 `cross_institution_engagement.{json,md}` + per-cohort engagement artifacts. Use the real repo paths under `data/artifacts/experiments/...` and `docs/experiments/...`.

- [ ] **Step 3: Verify**

Run: `grep -c "exp_006\|exp_009\|exp_011\|exp_012" docs/dissertation/figures_and_tables_inventory.md` → ≥ 4.
Run: `grep -n "cross_institution_engagement\|cross_cohort_stability\|engagement_importance" docs/dissertation/figures_and_tables_inventory.md` → confirm the new artifacts are indexed.

- [ ] **Step 4: Stage (no commit)**

```bash
git add docs/dissertation/figures_and_tables_inventory.md
# user commits: docs(dissertation): index exp_006-012 figures/tables/artifacts
```

---

## Task 9: README.md — inventory + reading order + currency (DO LAST)

**Files:** Modify `docs/dissertation/README.md` (~75 lines).

- [ ] **Step 1: Read the target doc in full** AND confirm Tasks 1–8 are complete (this task indexes their results). Locate the experiment inventory, the recommended reading order, and the per-doc currency descriptions.

- [ ] **Step 2: Update the experiment inventory** to list exp_001–012 (currently exp_001–005).

- [ ] **Step 3: Update the recommended reading order** so the now-current spine flows: intro/report (final_integrated_report) → results (experimental_results_synthesis) → methods (methodological_justification) → limitations → conclusions (final_research_conclusions) → claims (core_claims_and_nonclaims) → defense (defense_summary, defense_qna) → appendices (figures inventory, progression summary). The goal: a reader reaches the decisive exp_006–012 evidence BEFORE the conclusions.

- [ ] **Step 4: Refresh per-doc currency descriptions** so none describes a doc as stopping at exp_005.

- [ ] **Step 5: Verify**

Run: `grep -c "exp_006\|exp_009\|exp_011\|exp_012" docs/dissertation/README.md` → ≥ 1 (inventory mentions recent experiments).
Run: `grep -n "exp_005" docs/dissertation/README.md` → confirm exp_005 is no longer described as the latest/last experiment.

- [ ] **Step 6: Stage (no commit)**

```bash
git add docs/dissertation/README.md
# user commits: docs(dissertation): update README inventory + reading order through exp_012
```

---

## Task 10: Cross-doc consistency sweep

**Files:** Read-only sweep across `docs/dissertation/`; small fixes only if a contradiction is found.

- [ ] **Step 1: Stale-framing sweep.** Run:
`grep -rn "F1 .1.000\|F1=1.000\|R².0.99\|complicates the\|unresolved external\|stress test that keeps" docs/dissertation/`
For each hit, confirm it is now correctly caveated (synthetic F1=1.000 must read as artifact; OULAD "complicates" must not be a doc's final verdict). Fix any uncaveated stale framing in place.

- [ ] **Step 2: Number-consistency sweep.** Spot-check that the key recurring figures match the Ledger across docs: exp_009 mastery `-1.026`; exp_012 mean τ `0.56`; exp_007 cross-split τ `0.55`–`0.79`; exp_006 "no block >1.0 RMSE". Run:
`grep -rn "1.026\|0.56\|0.55.*0.79\|mixed-to-null" docs/dissertation/` and confirm no divergent values (e.g. a doc saying mean τ 0.66 for exp_012).

- [ ] **Step 3: Guardrail sweep.** Confirm no doc claims Digital-Twin accuracy superiority, a simulation/counterfactual capability, or causal XAI. Run:
`grep -rn "outperform\|simulation\|counterfactual\|causal" docs/dissertation/` and verify each is either negated/caveated or absent. Fix contradictions.

- [ ] **Step 4: Light-consistency note on source-of-truth docs.** If (and only if) a Task 1–9 edit introduced a statement that contradicts `final_research_conclusions.md` or `defense_summary.md`, fix the STALE doc to match the source of truth (do not rewrite the source-of-truth docs).

- [ ] **Step 5: Stage any fixes (no commit)**

```bash
git add docs/dissertation/
# user commits: docs(dissertation): cross-doc consistency sweep for exp_006-012 spine
```

---

## Self-review notes

- **Spec coverage:** spec §1 (final_integrated_report) → Task 2; §2 (methodological_justification) → Task 3; §3 (experiment_progression_summary) → Task 5; §4 (limitations) → Task 4; §5 (README) → Task 9; §6 (experimental_results_synthesis) → Task 1; §7 (core_claims top-up) → Task 6; §8 (defense_qna) → Task 7; §9 (figures inventory) → Task 8; light-consistency pass + verification → Task 10. All 9 docs + the consistency/guardrail checks covered.
- **No placeholders:** every task specifies the exact target sections, the exact figures (Ledger), the framing rules, and concrete verification greps. Prose is authored per-doc by the implementer to match each doc's voice — this is appropriate delegation for a documentation rewrite, not a placeholder, because the WHAT (content, numbers, framing) and the HOW-to-verify are fully specified.
- **Consistency:** all numeric facts derive from one Ledger (extracted verbatim from `final_research_conclusions.md`), so cross-doc divergence is structurally prevented; Task 10 sweeps for any residual drift.
- **Ordering:** README (Task 9) is last because it indexes the now-current docs; the consistency sweep (Task 10) is the final gate. Tasks 1–8 are mutually independent (different files) and subagent-parallel-safe, though executed sequentially with review.
- **No code/tests:** documentation-only; "verification" is grep-based, intentionally (no pytest applies).
