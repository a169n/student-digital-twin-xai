# Final Research Conclusions

This document records the carefully bounded interpretation of the project's
current contribution that follows from the completed experiments. It
does not claim more than the evidence supports, and it preserves the
caveats that the experiment line itself preserves. It is intended to serve
as the scaffold for a final-conclusions section in the dissertation, with
language that can be lifted directly subject to local stylistic editing.

## 1. The Original Hypothesis Was Not Confirmed in Its Strong Form

The project began under a permissive hypothesis: that a richer, engineered
**Digital Twin representation** of a learner would improve prediction of
end-of-course outcomes beyond what a competent LMS analytics layer
already provides. Under the present synthetic experimental environment,
that hypothesis is not supported in its strong form. In `exp_001_baseline`,
the full Twin set `C_twin` did not reliably outperform the LMS baseline
`B_lms` on the primary student-grouped split, and it deteriorated under
the stricter temporal-forward split. The combined RMSE evidence indicates
that the full Twin representation, as currently engineered, contains
enough redundancy with cumulative LMS aggregates that adding it
wholesale provides no consistent predictive advantage and may even harm
forward-looking generalization.

The dissertation should therefore not claim that the full Digital Twin
outperformed all baselines. The defensible statement is narrower: the full
Twin representation was not justified under the present setup, and the
research direction shifted accordingly toward a structured ablation rather
than toward defending the full representation.

## 2. A Lean Twin Subset Centered on Mastery Improved Prediction

The Twin subgroup ablation in `exp_002_twin_ablation` identified
`B_lms_plus_mastery` as the only single-block extension that produced a
substantive improvement on the LMS baseline under the primary split, with
RMSE `1.894` against `2.101` for `B_lms`, a delta of `-0.206`. No other
single Twin block — trends, indices, or temporal context — produced a
comparable improvement, and the full `C_twin_full` continued to
underperform the LMS baseline. The mastery validation in
`exp_003_mastery_validation` confirmed this finding through diagnostic
checks and through a week-aware protocol that observed improvements at
weeks 4 through 8, including three weeks inside the early-warning window
of weeks 4 through 6.

The defensible statement is that, **within the current synthetic
experimental environment**, a compact Twin subset centered on the mastery
block delivered measurable predictive value over a stronger LMS baseline
on the primary student-grouped split. The advantage is smaller and less
robust under the stricter temporal-forward split, where the candidate is
essentially level with the baseline. The dissertation should report both
sides of this asymmetry.

**Model-stability caveat.** The figures above use a *best-model-per-cell*
protocol, under which the candidate is essentially level with the baseline on
the temporal-forward split; that framing flatters the candidate, because the
`-0.206` RMSE advantage of `B_lms_plus_mastery` is realized only for gradient
boosting on the student-grouped split. A preliminary fixed-model re-analysis —
to be confirmed by the fixed-model ablation table produced in the public-data
phase — indicates that, when the model is held fixed across splits, the mastery
candidate is approximately `+0.41` RMSE *worse* than `B_lms` on the
temporal-forward split, and that `B_lms_plus_indices` (see `exp_002`) is the
only block improving on both splits (≈`-0.066` / ≈`-0.068`). These fixed-model
figures are preliminary until that table exists. Any carry-forward statement
about mastery must therefore be reported with a fixed-model table, not
best-model-per-cell, to avoid a model-selection artifact.

## 3. The Mastery Block Was Validated With Caveats

The mastery validation experiment is what allows the carry-forward
decision to be defended rather than asserted. The diagnostic checks in
`exp_003_mastery_validation` confirmed that mastery features are computed
without future leakage — both `current_topic_mastery` and `overall_mastery`
are constructed strictly from submission scores filtered to
`week_number <= snapshot week` and never read end-of-course outcome
fields — and that the predictive improvement appears in early-week
cutoffs rather than only at end-of-course. The same checks made the
caveat explicit. The Pearson correlation between `overall_mastery` and
`final_grade` reaches `0.984`, the strongest LMS correlate is
`avg_assignment_score_to_date` at `|r| = 0.993`, and removing
`overall_mastery` from the lean Twin model raises RMSE by `+0.228`.

The defensible statement is therefore conditional: the mastery block was
validated as a lean Twin component **with an explicit redundancy caveat**.
The dissertation account should not present mastery as an independent
construct, but as a topic-level aggregation of cumulative score behavior
that, in the present setup, concentrates the predictive signal more
sharply than the wider Twin layer does. Whether this concentration would
survive on a real institutional cohort is an open question.

## 4. The Lean Twin Remained Interpretable Under the Current XAI Phase

In `exp_004_xai_on_lean_twin`, the explanation behavior of the lean Twin
candidate was audited under documented model-behavior methods:
permutation importance with `15` repeats and one-feature median-replacement
local perturbations on five deterministically selected representative
cases. The explanations for `B_lms_plus_mastery` placed
`activity_score_to_date` first by importance share (`0.648`),
`overall_mastery` second (`0.178`), and a tail of LMS-behavior and
performance features below them. The dominance audit returned the outcome
`acceptable_with_caveat` because the average local mastery contribution
share was `0.194`, well below the `0.60` warning threshold, and the
explanations did not collapse onto a single feature.

The defensible statement is that the lean Twin representation remained
**interpretable with caveats** under the current explanation phase. The
caveats are explicit: a single LMS-behavior feature dominated the global
importance ranking, the second-ranked feature was the redundant
`overall_mastery`, and SHAP was not used. The methods used are
directional model-behavior explanations, not causal claims. The
dissertation should reproduce this language and should not claim that the
explanations recover causal mechanism, fully decompose the model's
predictions, or constitute Shapley-value attribution.

## 5. OULAD Complicates External Transfer Rather Than Proving It

`exp_005_public_benchmark_oulad` adds an external public-benchmark stress
test using the local OULAD files under `datasets/oulad`. The benchmark
constructs OULAD weekly snapshots for module-presentation `DDD` `2013J`,
uses a derived `final_weighted_score` target, and compares `B_lms_oulad`
with `B_lms_plus_mastery_oulad`. On the primary student-grouped split, the
mastery analogue is slightly worse than the LMS baseline (RMSE `12.724`
versus `12.658`, delta `+0.066`). On the secondary temporal-forward split,
the direction reverses: the mastery analogue improves RMSE (`9.161` versus
`9.566`, delta `-0.406`).

The defensible statement is that OULAD **complicates** the synthetic
carry-forward claim. It neither confirms a general mastery advantage nor
invalidates the internally validated synthetic result. Instead, it shows
that transfer depends on dataset structure, target semantics, assessment
timing, and missingness. The dissertation should present OULAD as a public
benchmark stress test, not as proof of full external validity and not as a
dataset-quality comparison. Section 5b below extends this evidence with the
full nested ablation, which supersedes the two-set transfer test and yields a
stronger, more decisive statement.

## 5b. The Full OULAD Ablation Confirms No Robust Twin Advantage on Real Data

`exp_006_oulad_full_ablation` extends the OULAD benchmark from the two-set
transfer test of `exp_005` to the full nested A/B/C ablation on real data,
using the identical leakage-aware pipeline (six feature-set analogues,
student-grouped and temporal-forward splits, and a fixed-model gradient
boosting comparison to neutralize the model-flip artifact). The dataset is
OULAD module-presentation `DDD` `2013J`: `67830` weekly snapshots across
`1938` students.

The result is a mixed-to-null finding. Under the fixed-model comparison, no
Twin feature block improves over the strong `B_lms_oulad` baseline by more
than `1.0` RMSE on either split. The largest single gain is the mastery
analogue on the temporal-forward split (RMSE `9.561` to `9.180`, delta
`-0.381`, roughly a four percent reduction), but the same block is `+0.061`
worse on the student-grouped split. The composite-index block improves the
temporal-forward split modestly (`-0.218`) and is essentially flat on the
grouped split (`+0.008`). The full `C_twin_oulad` analogue is within
`±0.025` RMSE of the baseline on both splits: non-inferior, but not
distinctly better. The minimal `A_simple_oulad` baseline is clearly worse
(`+1.207` grouped, `+4.105` temporal-forward), which confirms that the LMS
behavioral layer carries the predictive signal and that the Twin engineering
adds little on top of it.

Crucially, the OULAD task is genuinely predictive, not algebraic. Best-model
classification F1 ranges from `0.83` to `0.887` across feature sets and
splits and never reaches `1.000`. This is the direct empirical contrast with
the synthetic environment, where `passed` saturates at F1 `1.000` precisely
because the synthetic target is a deterministic function of the features
(see Section 1 and the limitations chapter). On the real, non-circular task,
the Twin representation does not earn its added complexity.

The defensible statement is therefore stronger and cleaner than the
`exp_005` "complicates" language: on a real, non-circular dataset, the
engineered Digital Twin feature blocks do **not** deliver a consistent
predictive advantage over a competent LMS-analytics baseline, and the
apparent synthetic advantage of the mastery block did not robustly transfer.
This is an honest negative-to-mixed result on the DDD 2013J cohort. It is one
of two OULAD courses examined; Section 5d reports a second cohort (BBB 2013J)
that qualifies it, showing the result is not uniform across courses.

## 5c. OULAD Explanations Are Interpretable but Regime-Sensitive

`exp_007_xai_on_oulad` applies the same model-behavior explanation methods
used on the synthetic data (held-out permutation importance, model-native
importance, and one-feature local perturbation; no SHAP) to the real OULAD
model, for `B_lms_oulad`, `B_lms_plus_mastery_oulad`, and `C_twin_oulad` under
both splits. Two findings follow.

First, the explanations lean on features that are themselves close to the
target. The dominant feature is `assessment_submission_rate_due_to_date` for
the LMS baseline (importance share `0.28`-`0.38`) and, once mastery is
included, the co-circular `overall_mastery_proxy` (share `0.23`-`0.43`), which
aggregates weighted assessment scores that partly feed the target. The
genuinely exogenous signals — the registration-state flag
`is_unregistered_by_week` (consistently ranked second to fourth, share
`0.13`-`0.20`) and the VLE clickstream features (share `0.02`-`0.06`) — are
present and interpretable but carry modest weight. The honest reading is that
even the explanation partly rests on within-system accounting features rather
than independent behavioral causes, which reinforces rather than offsets the
cautionary message of Section 5b. The defensible teacher-facing statement is
narrow: registration state and engagement activity are the interpretable
exogenous handles, but their contribution to the model is limited.

Second, the explanations are **regime-sensitive**. Comparing the global
importance ranking on the student-grouped split with the temporal-forward
split (`exp_007` stability analysis, Kendall rank correlation over the shared
features), agreement is moderate and below a high-stability threshold for
every feature set: `tau = 0.79` for `B_lms_oulad`, `0.68` for
`B_lms_plus_mastery_oulad`, and `0.55` for `C_twin_oulad` (mean `0.67`, none
reaching `0.90`). Top-5 membership can nonetheless be stable — Jaccard overlap
is `1.00` for the two mastery/twin sets and `0.67` for the LMS baseline —
meaning the same few features dominate across regimes while their relative
priority reorders, and the widest feature set (`C_twin_oulad`) is the least
order-stable. The defensible statement is that *which* features the model
appears to rely on, and in what order, depends on the evaluation scenario.
This extends explanation-stability analysis (Tiukhova et al., 2024) to the
public-benchmark transfer setting and dovetails with the predictive
mixed-to-null result of Section 5b: not only does the Twin representation fail
to win on accuracy, its explanation is not regime-invariant either. These are
model-behavior observations, not causal claims.

## 5d. A Second Cohort (BBB 2013J) Shows Heterogeneous Transfer and Course-Specific Explanations

To test whether the DDD 2013J result is course-specific or robust, `exp_009`
repeats the full nested ablation and `exp_010` repeats the model-behavior XAI on
a second OULAD module-presentation, BBB 2013J (`2237` students, `80532` weekly
snapshots, with a richer dated-assessment structure than DDD). Two findings
follow.

Predictively, the Twin-block value is **heterogeneous, not uniformly null**.
Under the fixed-model comparison on BBB 2013J, the mastery block improves the
temporal-forward split by `-1.026` RMSE (`5.284` versus `6.311`) — crossing the
one-point threshold that no block crossed on DDD — and the full `C_twin_oulad`
improves it by `-0.765`. On the student-grouped split, however, every block
stays within `0.087` RMSE of the baseline (null, as on DDD), and the trend and
composite-index blocks are null on both splits of both courses. Classification
remains genuinely predictive (F1 `0.87`-`0.93`, never `1.000`). The honest
reading is that the DDD null was **partly course-specific**: on a course with
richer assessment structure the mastery block delivers a meaningful gain under
forward-time evaluation, but the advantage does not generalize to the
student-grouped split, to the other Twin blocks, or to the other course. The
defensible cross-course statement is therefore one of heterogeneity — neither
uniform null nor uniform benefit.

Explanatorily, the importance topology is qualitatively **shared** across the
two courses — `overall_mastery_proxy`, assessment-submission discipline, and
the `is_unregistered_by_week` withdrawal flag dominate on both — but the
rankings are **not stable**. The cross-cohort agreement of the importance
rankings (Kendall `tau` of DDD versus BBB, per feature set and split) is
`0.32`-`0.61` (mean `0.52`), lower than the within-cohort cross-split agreement
of Section 5c (`0.55`-`0.79`, mean `0.67`), and no cell reaches a high-stability
threshold; top-5 membership overlaps only partially (Jaccard `0.43`-`1.00`). So
the model's "why" is not only regime-sensitive within a course but also partly
course-specific across courses. This cross-cohort extension of the
explanation-stability analysis tightens the cautionary message: both the
feature-group predictive value and the explanations that accompany it depend on
the course and the evaluation scenario. These remain model-behavior
observations, not causal claims, and the evidence still spans only two courses
from a single institution (OULAD).

## 6. The Resulting Contribution Is a Methodology + an Honest Real-Data Finding

The project's resulting contribution, on the basis of the ten
experiments, is best framed as a **teacher-oriented, lean Twin + XAI
research prototype**. The contribution is methodological and structural,
not a demonstration of full Digital Twin superiority and not an
institutional validation. Specifically, the project produces:

- a versioned data-model contract under schema `v1.2`, separating raw
  LMS-like data, processed twin snapshots, and end-of-course outcomes;
- a synthetic but schema-controlled dataset generator with realism
  audits;
- a leakage-aware modeling pipeline with student-grouped and
  temporal-forward splits, train-only imputation and scaling, and
  forbidden-column enforcement;
- a hypothesis-driven feature hierarchy and a structured ablation that
  identifies a lean Twin candidate;
- a documented mastery validation step with explicit redundancy and
  per-week diagnostics;
- a model-behavior explanation phase with global permutation importance
  and local perturbation explanations on a representative case set;
- a public OULAD benchmark adapter and a full nested A/B/C ablation on real
  data (`exp_006`) with documented feature mapping, fixed-model reporting,
  and an honest mixed-to-null transfer result;
- a real-data model-behavior explanation phase on OULAD (`exp_007`) plus an
  explanation-stability analysis showing the importance rankings are
  regime-sensitive (Kendall `tau` `0.55`-`0.79` across splits);
- a controlled synthetic faithfulness probe (`exp_008`) on known ground truth:
  at the final course week, importance recovers the generator's weight ordering
  (Kendall `tau` `1.0`), while illustrating how proxy correlation and redundancy
  shape importance (`activity_score_to_date` share `0.108` as a latent-driven
  proxy; `overall_mastery` redundant with `avg_assignment_score_to_date` at
  Pearson `r` `0.994`) — a methods appendix, not primary evidence;
- a second-cohort replication on OULAD BBB 2013J (`exp_009` ablation, `exp_010`
  XAI) plus a cross-cohort explanation-stability analysis, showing that
  Twin-block value is heterogeneous across courses (mastery improves BBB
  temporal-forward by `-1.026` RMSE but not DDD) and that importance rankings
  are partly course-specific (cross-cohort Kendall `tau` `0.32`-`0.61`,
  mean `0.52`);
- a versioned experiment governance layer with frozen configurations,
  metadata, machine-readable artifacts, per-experiment writeups, and a
  cumulative registry.

Within these scaffolds, the substantive empirical contribution is **not** a
demonstration that the Twin representation predicts better. On the synthetic
data, `B_lms_plus_mastery` appeared to outperform the LMS baseline, but that
apparent gain is an artifact of a deterministic, circular target (Section 1).
On real, non-circular OULAD data the picture is **heterogeneous across
courses**: on DDD 2013J (`exp_006`) no Twin block delivers a consistent
advantage over a competent LMS baseline, whereas on BBB 2013J (`exp_009`) the
mastery block does improve the forward-time split — but the advantage does not
hold on the student-grouped split, on the other Twin blocks, or on the other
course. The honest empirical finding is therefore that **engineered Twin
representation value is course- and split-dependent, not a robust improvement**:
representation richness that looks valuable under synthetic conditions transfers
to real data only narrowly and inconsistently.

The substantive contribution is consequently **methodological and
cautionary**. The project (i) supplies a reproducible, leakage-aware protocol
for constructing, ablating, and explaining weekly student-state
representations; (ii) demonstrates, through the synthetic-to-OULAD contrast,
how a circular target can manufacture an apparent feature-group advantage that
disappears or fragments on genuine data — a concrete cautionary case for the
Digital-Twin-in-education literature; and (iii) contributes an
explanation-stability analysis (`exp_007`, `exp_010`) showing that, on real
data, the model's importance rankings are regime-sensitive within a course
(mean Kendall `tau` `0.67`) and partly course-specific across courses (mean
`0.52`), none reaching `0.90` — so the explanation's "why" is not invariant to
the evaluation scenario or the course, a positive methodological result that
sits on top of the honest predictive finding. The project is thus
positioned as a research prototype that demonstrates **how to study** — and
how to avoid fooling oneself about — Digital Twin + XAI for academic risk
analytics, rather than as a proof that any Twin formulation is superior.

## 7. What This Conclusion Does Not Claim

For dissertation rigor, it is important to be explicit about the claims
the present evidence does **not** support.

- The conclusions do not claim that any Digital Twin representation
  outperforms a competent LMS analytics baseline in a course- and
  split-independent way. A lean mastery subset appeared to win **in the
  synthetic environment** (circular target) and did improve one split of one
  real course (BBB 2013J, `exp_009`), but not the other split, the other Twin
  blocks, or the other course (DDD 2013J, `exp_006`). The defensible claim is
  heterogeneity, not a robust advantage.
- The conclusions do not claim that the explanation methods used recover
  causal mechanism. They are directional model-behavior explanations.
- The conclusions do not claim full external validity. The main development
  dataset is synthetic; the real-data evidence spans two OULAD
  module-presentations (`DDD` `2013J`, `BBB` `2013J`) from a single
  institution, across which the Twin-block value and the explanations are
  heterogeneous. No independent institution has been used, so external
  validity beyond OULAD is not established.
- The conclusions do not claim that `passed` is a useful target for
  representation choice in the present setting; it is saturated.
- The conclusions do not claim that the predictive advantage of the lean
  Twin is fully independent of cumulative score behavior.
  `overall_mastery` is highly redundant with `avg_assignment_score_to_date`,
  and the dissertation should preserve that caveat.
- The conclusions do not claim that scenario analysis or intervention
  recommendations follow from the present XAI phase. The intervention
  framing is part of the project's broader scope but is not yet validated
  against any of these experiments.
- The conclusions do not claim that the synthetic predictive scores
  (R²≈0.99, F1=1.000) reflect learnable signal. The synthetic `final_grade`
  is a deterministic, noise-free function of the model's own features
  (`services/ml/src/generator/final_results.py:74-84`; week-10 max absolute
  reconstruction error 0.008), so those scores are algebraic artifacts. The
  empirical claims rest on real OULAD data, where the same pipeline yields
  best-model F1 0.83-0.887 on DDD 2013J and 0.87-0.93 on BBB 2013J, never
  1.000.

## 8. Carry-Forward Statement for the Dissertation

The dissertation can therefore carry forward the following statement as
the bounded conclusion of the current research phase:

> Under the synthetic experimental environment, a compact Twin subset
> centered on the mastery block (`B_lms_plus_mastery`) appeared to improve
> end-of-course prediction over a stronger LMS baseline and to remain
> interpretable under documented model-behavior explanations. That apparent
> predictive gain is, however, an artifact of a deterministic, circular
> synthetic target. When the identical leakage-aware pipeline was applied to
> real, non-circular OULAD data — first as a two-set transfer test
> (`exp_005`) and then as a full nested A/B/C ablation with fixed-model
> reporting across two cohorts — the result is **heterogeneous**. On DDD 2013J
> (`exp_006`, `67830` snapshots, `1938` students) no Twin block beat the LMS
> baseline by more than `1.0` RMSE on either split; on BBB 2013J (`exp_009`,
> `80532` snapshots, `2237` students) the mastery block improved the
> temporal-forward split by `-1.026` RMSE but not the student-grouped split,
> and the trend and index blocks were null on both courses. The OULAD
> classification target was genuinely predictive throughout (best-model F1
> `0.83`–`0.93`, never `1.000`). The accompanying explanations (`exp_007`,
> `exp_010`) are regime-sensitive within a course (Kendall `tau` `0.55`–`0.79`)
> and partly course-specific across courses (`0.32`–`0.61`). The contribution
> is therefore a reproducible, leakage-aware methodology for constructing,
> ablating, and explaining weekly student-state representations, together with
> an honest finding that engineered Twin value and its explanations are course-
> and split-dependent rather than robust, and a cautionary demonstration that a
> circular synthetic target can manufacture an apparent representation
> advantage that fragments on genuine data. It is not a proof of Digital Twin
> superiority, and its external evidence spans two OULAD courses from one
> institution.

This statement is consistent with every experiment artifact in the
repository and overstates none of them.

The defense-ready version of this conclusion is summarized separately in
[defense_summary.md](defense_summary.md) and guarded by
[core_claims_and_nonclaims.md](core_claims_and_nonclaims.md).
