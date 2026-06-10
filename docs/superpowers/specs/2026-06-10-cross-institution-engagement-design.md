# exp_012 — Matched Engagement-Only PASSED Classification Across Three Institutions

> **Status:** approved design (2026-06-10). Next: implementation plan via writing-plans.
> **Commit policy:** NO auto-commits — the user commits manually.

## Goal

Make exp_011's three-institution claim genuinely apples-to-apples. exp_011 ran an
engagement-only PASSED classification on KU Leuven (1819) and found richer
engagement features neutral over a minimal baseline (ΔF1 = −0.015). Its declared
next step is to compare that A→B engagement delta — and the importance rankings —
against OULAD. But the existing OULAD experiments (exp_005/006/009) use richer
blocks built on **assessment-score** features, while KU Leuven is **clickstream-only**.
The feature universes do not match, so a direct comparison is not valid.

exp_012 closes that gap by running a **matched engagement-only** PASSED
classification on OULAD (DDD 2013J and BBB 2013J) using feature sets that mirror
KU Leuven's, then a cross-institution analysis over the shared engagement concept
set.

This is a **robustness check, not a win-hunt.** OULAD will likely echo a
mixed/null A→B delta; that cross-institution consistency is the contribution.

## Scope decision (resolved)

Chosen approach: **true matched engagement-only OULAD run** (the most rigorous of
three options considered). Rejected alternatives:
- *Lean aggregation of existing results* — the OULAD "richer block" delta is not
  engagement-only, so the comparison would be soft.
- *Quantitative on hand-mapped concepts from existing results* — same feature
  mismatch; importance comparison would rest on differently-constructed features.

## Common task and constraint

- **Task:** binary PASSED classification only. No regression (KU Leuven has no
  numeric grade; matched design drops it for OULAD too).
- **OULAD target:** `passed_observed` (from `studentInfo.final_result`, Pass and
  Distinction → passed) — already constructed by the adapter.
- **Splits:** both `student_group` and `temporal_forward`. Report best-per-cell
  **and** fixed-model (`gradient_boosting`) tables to neutralize model-flip.
- **Importance:** permutation importance, `n_repeats=15`, scored on ROC-AUC,
  mirroring exp_011.

## Components

### 1. OULAD engagement-only feature sets (`oulad_adapter.py`)

Mirror KU Leuven's `A_simple_engagement` / `B_engagement`:

- `A_simple_engagement_oulad`: `cumulative_clicks_to_date`,
  `cumulative_active_days_to_date`; indicator `has_vle_activity_to_date`.
- `B_engagement_oulad`: the above + `current_week_clicks`,
  `cumulative_content_clicks_to_date`,
  `cumulative_social_clicks_to_date` (forum/social analog),
  `content_click_ratio_to_date`, `week_number`.

**New adapter column:** `cumulative_active_days_to_date` — count of distinct
VLE-active days up to and including the current week, leakage-safe (to-date only,
no global statistics). Added because active-days is KU Leuven's #1
temporal-forward driver and is trivially derivable from `studentVle` dates.

`content_click_ratio_to_date` = `cumulative_content_clicks_to_date` /
`cumulative_clicks_to_date` (0 when denominator is 0), if not already present.

**Documented omission:** OULAD VLE logs are daily-granular and have no within-day
*session* boundaries, so KU Leuven's `cumulative_sessions_to_date` and
`avg_session_clicks_to_date` have no OULAD analog and are intentionally excluded
from the matched set. The shared universe is the intersection of buildable
concepts.

### 2. exp_012 config + run

**Methodology-match requirement.** KU Leuven's PASSED metrics AND permutation
importance (exp_011) are produced by one runner,
`run_engagement_benchmark_kuleuven.py`: engagement-only, binary PASSED, both
splits, best-per-cell + fixed-model `gradient_boosting`, permutation importance
scored on ROC-AUC. OULAD's benchmark runner (`run_public_benchmark_oulad.py`)
produces regression metrics, and the OULAD XAI runner produces *regression*
permutation importance — neither matches KU Leuven's PASSED-classification
importance format. To make Part B genuinely apples-to-apples, OULAD must be run
through the **same** classification+importance code path as KU Leuven.

**Architecture:** extract the dataset-agnostic core of the KU Leuven engagement
runner (split building, classification train/score, permutation importance,
best/fixed-model diagnostics, markdown rendering) into a shared module
`engagement_benchmark.py`. The existing KU Leuven runner becomes a thin entry
point that builds KU snapshots (`ku_leuven_adapter`) and calls the core
(behavior-preserving — exp_011 outputs must reproduce). A new thin OULAD entry
point builds OULAD snapshots (`oulad_adapter`) and calls the **same** core.

- Config `services/ml/configs/experiments/exp_012_oulad_engagement_<cohort>.yaml`
  per cohort (DDD 2013J, BBB 2013J), declaring the two engagement feature sets,
  classification-only, both splits, fixed-model `gradient_boosting`, permutation
  importance.
- Run once for DDD 2013J and once for BBB 2013J. Separate artifact dirs; do not
  overwrite existing experiments.

### 3. Cross-institution analysis (`analyze_cross_institution_engagement.py`)

Mirrors `analyze_cross_cohort_stability.py`; reuses `stability.kendall_tau` /
`stability.jaccard_topk`. Reads existing results JSONs (OULAD exp_012 DDD + BBB,
KU Leuven exp_011) — no model re-training.

- **Part A — A→B engagement delta.** Table of ΔF1 and ΔROC-AUC
  (`B_engagement` − `A_simple_engagement`) for the fixed model, per split, across
  all three institutions. Honest verdict: consistently neutral / mixed / helpful.
- **Part B — importance stability.** Over the shared engagement concept set, an
  explicit concept-alignment map renames cohort-specific columns to canonical
  concept names (e.g. OULAD `cumulative_social_clicks_to_date` ↔ KU Leuven
  `cumulative_forum_posts_to_date` → `forum_engagement`). Then pairwise
  Kendall τ + Jaccard@k between institutions, per split, over the aligned
  concepts. Verdict: are top drivers (clicks / active-days) stable across
  institutions, or institution-specific.
- Writes `<artifact>/cross_institution_engagement.{json,md}` and a registry-style
  doc under `docs/experiments/`.

### 4. Dissertation write-up

Fold the cross-institution robustness finding into
`docs/dissertation/final_research_conclusions.md` and `defense_summary.md`:
the engagement→PASSED signal is dominated by a minimal click/active-days baseline
across three independent institutions; richer engagement adds little; this is a
robustness result, not an accuracy claim.

## Testing (TDD — failing test first, per project convention)

- `test_oulad_engagement.py`: new adapter column `cumulative_active_days_to_date`
  present and monotone non-decreasing within a student; engagement feature sets
  load with the expected columns; `content_click_ratio_to_date` in [0, 1].
- exp_012 config loads and declares both engagement feature sets, classification
  only.
- `test_cross_institution_engagement.py`: concept-alignment map produces a shared
  universe; delta aggregation correct on a fixture; Kendall τ over aligned
  concepts well-defined (identical rankings → 1.0).

## Concept-alignment map (canonical names)

| Canonical concept | OULAD column | KU Leuven column |
|---|---|---|
| total_clicks | cumulative_clicks_to_date | cumulative_clicks_to_date |
| current_clicks | current_week_clicks | current_week_clicks |
| content_clicks | cumulative_content_clicks_to_date | cumulative_content_clicks_to_date |
| forum_engagement | cumulative_social_clicks_to_date | cumulative_forum_posts_to_date |
| content_ratio | content_click_ratio_to_date | content_click_ratio_to_date |
| active_days | cumulative_active_days_to_date | cumulative_active_days_to_date |
| week | week_number | week_number |

KU-only (no OULAD analog, excluded from Part B): `cumulative_sessions_to_date`,
`avg_session_clicks_to_date`, `days_since_course_start`. Their exclusion is
reported, not silent.

## Out of scope

- No SHAP (project decision stands).
- No regression on OULAD engagement sets (matched-design constraint).
- No new KU Leuven cohort unless the data trivially supports it (decide during
  planning).
- No synthetic-data involvement.

## Risks

- `cumulative_social_clicks_to_date` (clicks on forum) vs KU
  `cumulative_forum_posts_to_date` (post count) are related but not identical
  units; Part B compares **ranks**, not magnitudes, which tolerates the unit
  difference — but the caveat must be stated in the report.
- OULAD engagement-only classification may be weaker than the assessment-laden
  blocks; that is expected and on-message (engagement-only is the deliberate
  constraint, matching KU Leuven).
