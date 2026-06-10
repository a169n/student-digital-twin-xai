# exp_012_oulad_engagement: Three-institution engagement-only PASSED synthesis (OULAD DDD 2013J, OULAD BBB 2013J, KU Leuven 1819)

> **CROSS-INSTITUTION SYNTHESIS — ENGAGEMENT-ONLY — CLASSIFICATION ONLY (PASSED)**
>
> This is the synthesis record for exp_012. It combines the two matched OULAD
> per-cohort runs (DDD 2013J, BBB 2013J) with the KU Leuven exp_011 run into a
> single three-institution engagement-only robustness check. Only binary PASSED
> classification is reported. Regression is intentionally omitted (engagement-only
> matched design); `final_grade = float(passed)` is a structural placeholder.
> Cross-institution importance comparison uses permutation-importance RANKS, not
> magnitudes, because social CLICKS (OULAD) and forum POSTS (KU Leuven) are
> incommensurable units.

## Objective

Run a matched engagement-only PASSED-classification comparison across three
institution cohorts — OULAD DDD 2013J, OULAD BBB 2013J, and KU Leuven 1819 — to
answer the next-step question raised by exp_011: does richer engagement
(B_engagement) consistently improve PASSED prediction over the minimal
click/active-days baseline (A_simple_engagement), and do the permutation-importance
drivers of PASSED prediction transfer across institutions? This is an honest
robustness check, not a best-predictor claim: the engagement-only constraint is a
deliberate matched design imposed by KU Leuven's lack of assessment-score data, so
the mastery/Twin feature blocks from exp_005/exp_006/exp_009 are excluded by
construction. Part A reports the fixed-model (gradient_boosting) B-minus-A delta on
both split strategies; Part B reports cross-institution importance-rank stability.

## Matched feature sets

The two OULAD cohorts use a single OULAD feature pair; KU Leuven uses the exp_011
pair. The OULAD columns carry the `_oulad` suffix in the pipeline but encode the
same concepts.

### Baseline — `A_simple_engagement` / `A_simple_engagement_oulad`

Minimal two-feature engagement baseline: cumulative click volume + cumulative
active days, plus a leakage-safe has-activity indicator.

- KU Leuven: `cumulative_clicks_to_date`, `cumulative_active_days_to_date` (indicator `has_activity_to_date`)
- OULAD: `cumulative_clicks_to_date`, `cumulative_active_days_to_date` (indicator `has_vle_activity_to_date`)

### Candidate — `B_engagement` / `B_engagement_oulad`

Richer multi-dimensional engagement set: total clicks, active days, current-week
clicks, content-type click split, content focus ratio, forum/social activity,
temporal course progress, and the raw week counter.

- KU Leuven: `cumulative_clicks_to_date`, `cumulative_active_days_to_date`, `cumulative_sessions_to_date`, `cumulative_content_clicks_to_date`, `current_week_clicks`, `avg_session_clicks_to_date`, `content_click_ratio_to_date`, `cumulative_forum_posts_to_date`, `days_since_course_start`, `week_number`
- OULAD: `cumulative_clicks_to_date`, `cumulative_active_days_to_date`, `current_week_clicks`, `cumulative_content_clicks_to_date`, `cumulative_social_clicks_to_date`, `content_click_ratio_to_date`, `week_number`

### Shared concept set (Part B alignment)

Seven concepts present in both institutions are aligned for the rank-stability
comparison: `total_clicks`, `active_days`, `current_clicks`, `content_clicks`,
`content_ratio`, `forum_engagement` (= OULAD social CLICKS vs KU forum POSTS),
`week`.

### KU-only excluded concepts

Three KU Leuven concepts have no OULAD analog and are dropped from Part B:
`cumulative_sessions_to_date`, `avg_session_clicks_to_date`,
`days_since_course_start`. OULAD VLE logs are daily, not session-resolved, so
session-level features cannot be reconstructed.

## Part A — Engagement delta (fixed model = `gradient_boosting`)

Change in fixed-model PASSED-classification metrics when moving from the
simple-engagement baseline (A) to the richer engagement candidate (B). Delta is
B minus A. Absolute F1 values are the fixed-model values from each per-cohort run.

| Institution | Split | A F1 | B F1 | ΔF1 | A ROC-AUC | B ROC-AUC | ΔROC-AUC |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| OULAD DDD 2013J | temporal_forward | 0.7896 | 0.7892 | -0.0003 | 0.8929 | 0.9137 | +0.0208 |
| OULAD DDD 2013J | student_group | 0.7340 | 0.8058 | +0.0718 | 0.8602 | 0.8997 | +0.0396 |
| OULAD BBB 2013J | temporal_forward | 0.7873 | 0.8131 | +0.0258 | 0.8746 | 0.8983 | +0.0237 |
| OULAD BBB 2013J | student_group | 0.7727 | 0.8120 | +0.0393 | 0.8499 | 0.8843 | +0.0344 |
| KU Leuven 1819 | temporal_forward | 0.7567 | 0.7411 | -0.0155 | 0.6927 | 0.7020 | +0.0093 |
| KU Leuven 1819 | student_group | 0.7536 | 0.7537 | +0.0001 | 0.6598 | 0.7005 | +0.0407 |

**Honest reading.** Richer engagement is neutral-to-modest across all three
institutions: it never decisively wins or loses. The dominant PASSED signal is
already captured by the minimal click/active-days baseline. The larger positive
ΔF1 values appear on the `student_group` split (DDD +0.072, BBB +0.039, KU
+0.000), while the stricter `temporal_forward` split — the early-warning-relevant
one, where the model trains on early weeks and predicts forward — is essentially
flat to slightly negative on two of three cohorts (DDD -0.000, KU -0.015) and only
modestly positive on BBB (+0.026). ROC-AUC moves up slightly more consistently
than F1 (all six cells positive, +0.009 to +0.041), indicating the richer set
improves ranking/calibration more than the thresholded F1. None of this supports a
claim that engagement richness is a strong predictor; it supports the opposite — a
two-feature engagement baseline is hard to beat.

## Part B — Importance-rank stability across institutions

Permutation-importance rankings (gradient_boosting, ROC-AUC scoring, n_repeats=15)
aligned onto the seven shared engagement concepts, then compared pairwise. Kendall
τ is over aligned concepts; Jaccard is over the top-5 concepts.

| Split | Pair | Kendall τ | Jaccard@5 | n_shared |
| --- | --- | ---: | ---: | ---: |
| student_group | KU_Leuven vs OULAD_BBB | 0.7143 | 0.6667 | 7 |
| student_group | KU_Leuven vs OULAD_DDD | 0.2381 | 0.4286 | 7 |
| student_group | OULAD_BBB vs OULAD_DDD | 0.5238 | 0.6667 | 7 |
| temporal_forward | KU_Leuven vs OULAD_BBB | 0.7143 | 0.6667 | 7 |
| temporal_forward | KU_Leuven vs OULAD_DDD | 0.5238 | 0.6667 | 7 |
| temporal_forward | OULAD_BBB vs OULAD_DDD | 0.6190 | 0.6667 | 7 |

- Mean Kendall τ (student_group): 0.4921
- Mean Kendall τ (temporal_forward): 0.6190
- **Mean Kendall τ (all pairs, all splits): 0.5556**
- all_stable (τ ≥ 0.90 everywhere): false
- **Verdict: `drivers_partly_institution_specific`**

**Interpretation.** The top drivers — cumulative active-days and cumulative clicks
(plus current-week clicks) — recur as the leading concepts across all three
institutions and both splits. But the full rank ordering only PARTIALLY transfers:
mean τ ≈ 0.556, well below the 0.90 "stable everywhere" bar, and one pair
(KU_Leuven vs OULAD_DDD on student_group) drops to τ ≈ 0.238. The relative
ordering of the mid- and lower-ranked concepts (content clicks, content ratio,
forum/social, week) shifts between cohorts. This is a statement about MODEL
BEHAVIOUR — how the gradient-boosting model distributes learned reliance over its
inputs — not a causal claim about what drives student outcomes across institutions.

## Top drivers per institution / split (top-3 by permutation importance)

Compact view of the leading drivers from each per-cohort importance CSV (candidate
feature set, gradient_boosting). Active-days and clicks dominate everywhere.

| Institution | Split | #1 | #2 | #3 |
| --- | --- | --- | --- | --- |
| OULAD DDD 2013J | student_group | cumulative_active_days (59.4%) | current_week_clicks (20.4%) | cumulative_clicks (10.7%) |
| OULAD DDD 2013J | temporal_forward | cumulative_active_days (46.0%) | current_week_clicks (35.8%) | cumulative_clicks (11.9%) |
| OULAD BBB 2013J | student_group | cumulative_clicks (45.2%) | cumulative_active_days (22.6%) | current_week_clicks (15.8%) |
| OULAD BBB 2013J | temporal_forward | current_week_clicks (38.5%) | cumulative_active_days (23.6%) | cumulative_clicks (21.9%) |
| KU Leuven 1819 | student_group | cumulative_clicks (17.5%) | cumulative_active_days (15.9%) | cumulative_sessions (14.8%) |
| KU Leuven 1819 | temporal_forward | cumulative_active_days (45.6%) | cumulative_clicks (13.0%) | current_week_clicks (10.0%) |

(Shares are over positive importances. KU Leuven's `cumulative_sessions_to_date`
is a KU-only concept excluded from the Part B shared-concept alignment.)

## Caveats

- **Forum/social proxy mismatch.** `forum_engagement` maps to social CLICKS in
  OULAD (`cumulative_social_clicks_to_date`) but to forum POSTS in KU Leuven
  (`cumulative_forum_posts_to_date`). Different units; Part B compares RANKS, not
  magnitudes, to avoid comparing incommensurable quantities.
- **No OULAD sessions.** OULAD VLE logs are daily, not session-resolved, so
  session counts and average session clicks (present on KU Leuven) cannot be
  reconstructed; those KU-only concepts are excluded from the shared-concept
  alignment.
- **Both splits reported.** Each per-cohort headline conclusion keys off only its
  primary split, but both `student_group` and `temporal_forward` are reported here
  for completeness. Cross-split disagreement within a cohort is expected and is not
  itself evidence of cross-institution instability.
- **Engagement-only is a deliberate matched constraint**, not a best-predictor
  claim. The mastery/assessment-score feature blocks from exp_005/exp_006/exp_009
  are intentionally excluded so the three institutions are directly comparable.
- **Model behaviour, not causality.** Part B importances describe a
  gradient-boosting model's learned input-output mapping, not the causal factors
  driving student outcomes.

## Artifact paths

- Cross-institution synthesis JSON: `data/artifacts/experiments/exp_012_cross_institution_engagement/cross_institution_engagement.json`
- Cross-institution synthesis MD: `data/artifacts/experiments/exp_012_cross_institution_engagement/cross_institution_engagement.md`
- OULAD DDD 2013J cohort: `data/artifacts/experiments/exp_012_oulad_engagement_ddd2013j/` (doc: [exp_012_oulad_engagement_ddd2013j.md](exp_012_oulad_engagement_ddd2013j.md))
- OULAD BBB 2013J cohort: `data/artifacts/experiments/exp_012_oulad_engagement_bbb2013j/` (doc: [exp_012_oulad_engagement_bbb2013j.md](exp_012_oulad_engagement_bbb2013j.md))
- KU Leuven 1819 cohort (exp_011): `data/artifacts/experiments/exp_011_kuleuven_engagement/` (doc: [exp_011_kuleuven_engagement.md](exp_011_kuleuven_engagement.md))

## Next step

Optionally fold this three-institution synthesis into the dissertation's
cross-institution robustness section (Task 7): the engagement-richness delta is
neutral-to-modest (and flat on the early-warning temporal_forward split), and the
permutation-importance drivers of PASSED prediction transfer only partially across
institutions (mean Kendall τ ≈ 0.556, `drivers_partly_institution_specific`), with
active-days and clicks the stable leading concepts everywhere.
