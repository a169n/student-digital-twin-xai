# Limitations and Threats to Validity

The methodological design and experimental results described in the
companion documents are bounded by a specific research setting: a synthetic
but schema-controlled dataset, a single-course prototype scope, and a
deferred dependency on a real institutional cohort. This document records
the limitations of that setting honestly and discusses the residual threats
to validity that any dissertation account of the project should preserve
rather than smooth over.

## 1. Synthetic Data Limitations

The experimental evidence is produced exclusively on the synthetic dataset
generated from `generator_v1_3_refined.yaml` against the schema contract
`v1.2`. The relationships between attendance, activity, submission
discipline, performance, mastery, and final outcomes therefore reflect the
generator's design assumptions and tuning rather than the empirical
behavior of any specific learner population. Three implications follow.

First, the predictive numbers reported across the experiments — the
RMSE deltas of `B_lms_plus_mastery` against `B_lms`, the per-week
improvement pattern, the saturated `passed` task — are statements about the
internal structure of the generated dataset. They cannot, on their own,
demonstrate that any equivalent representation would behave the same way on
real institutional records.

Second, the dataset is structurally closer to its own assumptions than to
any institutional reality. For example, weekly aggregates reach
near-perfect monotonic relationships with `final_grade` (Pearson r above
`0.97` for several LMS aggregates), which is rare in real cohorts and is
itself a sign that the generator emphasizes signal clarity over realistic
noise. This is documented in
[docs/experiments/exp_003_mastery_validation.md](../experiments/exp_003_mastery_validation.md)
through the LMS-baseline target-correlation table.

Third, the saturation of the binary `passed` task is a consequence of the
same condition. With cumulative LMS aggregates this strongly aligned with
`final_grade`, every reasonable feature set already lifts pass-classification
performance to ceiling. This means that within the present generator,
classification is not a discriminating benchmark and that the project's
claims rest on the regression target.

The mitigation is not to dismiss the results, but to read them as
internally valid under the controlled setting. The dissertation should
present them as such.

## 2. Internal Realism Versus External Validity

The realism audits in `data/artifacts/reports/` provide an internal check
that the generator's distributions of grades, attendance, activity,
submission behavior, and risk levels are plausible relative to design
assumptions. These audits are useful for catching gross generator
malfunction. They are not, however, a substitute for external validation.
The realism reports verify that the generated data is internally
well-behaved under its own contract; they do not verify that the contract
itself matches the empirical conditions of any specific course or
institution.

Internal validity in this project is therefore strong: experiments are
reproducible, schema-controlled, and leakage-aware. External validity is
explicitly deferred. A dissertation account should be careful not to
present internal realism as external validation, and should state that the
generator parameters are working assumptions rather than empirically
calibrated estimates.

## 3. Redundancy of `overall_mastery`

`overall_mastery` is the single most predictive feature in the lean Twin
representation, but it is also the most redundant with the LMS baseline.
This is documented in [docs/experiments/exp_003_mastery_validation.md](../experiments/exp_003_mastery_validation.md)
and recorded in the metadata of `exp_004_xai_on_lean_twin`:

- Pearson r between `overall_mastery` and `final_grade` is `0.984`.
- Strongest LMS correlate is `avg_assignment_score_to_date` at |r| = `0.993`.
- Drop-column re-training of the lean Twin model increases RMSE by `+0.228`
  when `overall_mastery` is removed.

Two consequences follow. First, part of the predictive improvement
attributed to the mastery block in the synthetic environment is
mathematically very close to the cumulative assignment score; the lean
Twin's advantage over `B_lms` is therefore not a fully independent signal.
Second, in the explanation phase the dominance audit raised an explicit
flag: the top global feature, `activity_score_to_date`, accounts for
`0.648` of the importance share, and `overall_mastery` accounts for
`0.178`. Even though the dominance outcome was `acceptable_with_caveat`
because explanations did not collapse onto a single feature, the
redundancy concern remains. Any dissertation claim about the lean Twin's
distinctive contribution should be qualified accordingly.

This caveat is preserved as a first-class concern in the experiment
metadata under `exp_004_xai_on_lean_twin/experiment_metadata.json` and is
not resolved by the present experiment line.

## 4. Saturation of `passed`

The pass/fail classification target reaches F1 = `1.000` for every feature
set under both splits in `exp_001_baseline` and `exp_002_twin_ablation`.
This is a structural property of the current generator rather than a
modeling success. The implications are explicit. First, `passed` cannot
discriminate between feature sets, so it cannot be used to validate the
Twin representation. Second, `passed` cannot validate the explanation
layer either, because the classifier is essentially trivial under any
reasonable feature set. The experiments therefore correctly designate
`passed` as secondary context rather than as the primary benchmark, and
the project's findings rest on the regression target. A dissertation
account should make this explicit and avoid presenting classification
performance as supporting evidence for representation choice.

## 5. Absence of SHAP in the Current XAI Phase

`exp_004_xai_on_lean_twin` does not produce SHAP explanations. This is a
deliberate scoping decision recorded in the experiment configuration: SHAP
is not part of the current project dependency contract. The explanation
methods used — held-out **permutation importance** with
`neg_root_mean_squared_error` over `15` repeats, plus **one-feature
median-replacement** local perturbations on five deterministically
selected representative cases — are documented sklearn-based methods and
are appropriate for the current research phase, but they are not
equivalent to SHAP.

Two consequences follow. First, the "share" values reported in the global
importance table are RMSE-increase shares from permutation importance, not
Shapley values; they should not be cited as such. Second, the local
explanations are directional and report which features, when set to the
training median, push the prediction toward or away from the observed
value; they do not provide the additive, locally faithful decomposition
that SHAP offers under its specific assumptions. This is recorded in
[docs/experiments/exp_004_xai_on_lean_twin.md](../experiments/exp_004_xai_on_lean_twin.md):

> These are directional model-behavior explanations, not causal claims.

The dissertation account should reproduce this language and should not
overstate what the present explanation phase establishes.

## 6. Model-Behavior Explanations Versus Causal Explanations

The methods used in `exp_004_xai_on_lean_twin` answer a circumscribed
question: which features, when permuted or replaced, change the model's
predictions, and in which direction? They do not answer the causal
question of which factors actually move the educational outcome. The
distinction matters for a teacher-oriented intervention narrative. A
feature that is influential in the model's predictions is not necessarily
a feature whose modification would improve a learner's outcome, because
the model captures correlation under its training distribution rather than
causal mechanism.

Within the present project, the synthetic generator does encode certain
structural relationships — for example, that lower attendance and lower
submission discipline contribute to lower final outcomes — but the
explanation methods used cannot recover those structural relationships
from the predictions alone, and they would not recover the structural
relationships of any institutional process either. Any future scenario
analysis must therefore be designed as a separate research artifact with
explicit assumptions, not as a direct extrapolation of the present XAI
output.

## 7. Lack of Validation on a Real Institutional Dataset

The project has no real-data validation step. The dissertation cannot
therefore claim that the predictive advantage of the lean Twin replicates
on an institutional cohort, that the explanation behavior remains
teacher-meaningful under real noise, or that the early-warning framing
(improvement at weeks 4–8) survives the absence of synthetic regularity.
This is the dominant external-validity threat. It is acknowledged
consistently in every experiment writeup and is recorded as a residual
limitation in the data-model documentation as well.

## 8. Dependence on Generator Assumptions

The generator under `generator_v1_3_refined.yaml` controls several latent
parameters such as baseline level, motivation level, discipline level,
trajectory type, and topic difficulty. These are deliberately marked as
generation-only fields and are excluded from the model matrix, but they
shape the empirical relationships among the visible features and the
outcomes. Two consequences follow.

First, the apparent strength of any individual feature — including
`activity_score_to_date` and `overall_mastery` — is partly a function of
how the generator combines latent parameters into observed signals.
Recalibrating the generator could legitimately shift the relative
importances reported in the explanation phase. Second, the **shape** of
the predictive advantage of `B_lms_plus_mastery` over `B_lms` is also a
generator-conditioned property: it is what the generator produces, not
what an institutional process necessarily produces.

A dissertation account should therefore present the specific numerical
deltas as evidence about the controlled environment, and the qualitative
finding (that mastery concentrates the Twin layer's useful predictive
signal) as a hypothesis worth re-testing on real data rather than as a
generalized claim.

## 9. Other Repository-Documented Ambiguities

Several smaller ambiguities are already documented in the repository and
should be preserved in the dissertation rather than overwritten.

- The data-model documentation explicitly lists items as still
  provisional, including the exact mathematical formula for `risk_score`,
  the final operational definition of the risk horizon, the calibrated
  threshold cut points after empirical realism checks, and the handling of
  withdrawals and incompletes in weekly heuristic labeling. See
  [docs/data_model/03_targets_and_labels.md](../data_model/03_targets_and_labels.md).
- Composite-index weights, trend-feature scaling, the separation of
  assignment versus quiz categories, and the role of `due_load` are listed
  as open in [docs/data_model/04_feature_definitions.md](../data_model/04_feature_definitions.md).
- The mastery validation records that drop-column tests are run on the
  current best regression model only and therefore expose dependency on a
  single feature without producing a full causal attribution; per-week
  evaluation reuses the student-group split and small per-week test sets,
  which is why the validation interprets the early-week pattern as a whole
  rather than relying on any individual weekly score. See
  [docs/experiments/exp_003_mastery_validation.md](../experiments/exp_003_mastery_validation.md).
- The temporal lineage of mastery is documented from the generator code in
  `services/ml/src/generator/snapshots.py` rather than enforced by an
  automated lineage check. The verification is therefore by code review
  and feature-set conventions, not by an executable invariant.

These ambiguities are part of the honest research state of the project and
should be carried into the dissertation chapter as such.

## 10. Summary

The current results suggest, under the present synthetic experimental
environment, that a lean Twin representation centered on the mastery block
improves prediction beyond a stronger LMS baseline and remains
interpretable in a model-behavior sense. The corresponding limitations are
that the dataset is synthetic, the binary classification task is
saturated, the dominant mastery feature is highly redundant with
cumulative assignment scores, the explanations are model-behavior rather
than causal and do not include SHAP, and no real institutional dataset has
yet been used to test external validity. The dissertation account should
present the contribution within these limits and should not overstate
either predictive superiority or explanatory completeness.
