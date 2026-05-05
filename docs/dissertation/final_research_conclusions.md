# Final Research Conclusions

This document records the carefully bounded interpretation of the project's
current contribution that follows from the four completed experiments. It
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

## 5. The Resulting Contribution Is a Lean Twin + XAI Research Prototype

The project's resulting contribution, on the basis of the four
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
- a versioned experiment governance layer with frozen configurations,
  metadata, machine-readable artifacts, per-experiment writeups, and a
  cumulative registry.

Within these scaffolds, the substantive empirical contribution is the
identification and validation of `B_lms_plus_mastery` as a compact Twin
representation that predicts end-of-course outcomes more accurately than
a stronger LMS baseline on the primary split, while remaining
interpretable under documented permutation and local-perturbation
methods. The project is therefore positioned as a research prototype that
demonstrates **how to study** Digital Twin + XAI for academic risk
analytics under disciplined methodological constraints, rather than as a
proof that any specific full Twin formulation is superior.

## 6. What This Conclusion Does Not Claim

For dissertation rigor, it is important to be explicit about the claims
the present evidence does **not** support.

- The conclusions do not claim that any Digital Twin representation
  outperforms a competent LMS analytics baseline in general. The current
  evidence is that the **full** Twin representation did not, and that a
  **lean** Twin centered on mastery did, **on the primary split, in the
  synthetic environment**.
- The conclusions do not claim that the explanation methods used recover
  causal mechanism. They are directional model-behavior explanations.
- The conclusions do not claim external validity. The dataset is
  synthetic and no institutional cohort has been used for validation.
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

## 7. Carry-Forward Statement for the Dissertation

The dissertation can therefore carry forward the following statement as
the bounded conclusion of the current research phase:

> Under the present synthetic experimental environment, the full Digital
> Twin representation was not justified relative to a stronger LMS
> baseline. A compact Twin subset centered on the mastery block,
> `B_lms_plus_mastery`, delivered measurable predictive value over the
> LMS baseline on the primary student-grouped split and improved the
> baseline at early-course weeks. Mastery was validated as a lean Twin
> component with an explicit redundancy caveat for `overall_mastery`. The
> resulting model-behavior explanations remained teacher-meaningful and
> did not collapse onto a single feature, with the redundancy and
> dominance caveats preserved as part of the conclusion. The
> contribution is therefore a teacher-oriented, lean Twin + XAI research
> prototype with a documented methodological pipeline, rather than a
> proof of full Digital Twin superiority or an institutional validation.

This statement is consistent with every experiment artifact in the
repository and overstates none of them.
