# Limitations and Threats to Validity

The methodological design and experimental results described in the
companion documents are bounded by a specific research setting: a synthetic
but schema-controlled dataset with a deterministic, circular target, a
single-course prototype scope, external public benchmarks spanning two
OULAD courses (DDD 2013J, BBB 2013J) and a partial engagement-only check on
a second institution (KU Leuven), and a deferred dependency on a fully
local institutional cohort and teacher workflow. This document records
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
near-perfect relationships with `final_grade` (Pearson r
above `0.97` for several LMS aggregates). This is **not merely "signal clarity"**:
`final_grade` is a deterministic, noise-free closed-form weighted mean
(`0.55*assignment_avg + 0.25*quiz_avg + 0.10*attendance_rate*100 + 0.10*on_time_rate*100`,
`services/ml/src/generator/final_results.py:74-84`) of the very behaviors the
features re-aggregate. The target is therefore an algebraic function of the
inputs (week-10 max absolute reconstruction error 0.008, correlation 1.000000),
so the synthetic predictive scores cannot, even in principle, demonstrate learnable
educational signal. This is why the primary empirical evidence in this work is
the real OULAD dataset and the synthetic data is retained only as a controlled
faithfulness probe (`exp_008`). This is documented in
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

The OULAD public-dataset stress test adds external evidence, but it does
not erase this limitation, and it is now best read as **two distinct
ablations on two courses rather than one undifferentiated "OULAD" result**.
The two-set transfer test of `exp_005_public_benchmark_oulad` (DDD `2013J`)
was superseded by the full nested A/B/C ablation of
`exp_006_oulad_full_ablation` on the same cohort (`67830` weekly snapshots,
`1938` students, fixed-model gradient boosting to neutralize the
model-flip artifact). On DDD 2013J the result is **mixed-to-null**: no
Twin feature block improves over the strong `B_lms_oulad` baseline by more
than `1.0` RMSE on either split. The largest single gain is the mastery
analogue on the temporal-forward split (`9.561` to `9.180`, delta
`-0.381`), but the same block is `+0.061` worse on the student-grouped
split; the full `C_twin_oulad` stays within `±0.025` RMSE of the baseline
on both splits; and the minimal `A_simple_oulad` is clearly worse
(`+1.207` grouped, `+4.105` temporal-forward), confirming that the LMS
behavioral layer carries the signal.

A second cohort, BBB 2013J (`exp_009`, `2237` students, `80532` weekly
snapshots, with a richer dated-assessment structure), shows that this null
is **partly course-specific** rather than uniform. Under the fixed-model
comparison the mastery block improves the temporal-forward split by
`-1.026` RMSE (`5.284` versus `6.311`) — crossing the one-point threshold
that no block crossed on DDD — and the full `C_twin_oulad` improves it by
`-0.765`. On the student-grouped split, however, every block stays within
`0.087` RMSE of the baseline (null, as on DDD), and the trend and
composite-index blocks are null on both splits of both courses. The
defensible cross-course statement is therefore one of **heterogeneity**:
neither uniform null nor uniform benefit, with the Twin advantage
appearing only under forward-time evaluation on the course with richer
assessment structure. This complicates and qualifies external transfer
rather than proving it.

A partial-target-circularity disclosure applies to the OULAD evidence as
well, though it is far milder than the synthetic case. The derived
`final_weighted_score` regression target is built from assessment scores,
and the mastery analogue (`overall_mastery_proxy`) aggregates weighted
assessment scores that partly feed that target, so the regression numbers
should not be read as fully independent of within-system accounting. This
is why the OULAD evidence in this work leans on the genuinely exogenous
signals — VLE clickstream engagement and the registration-state flag — and
on the **classification** target, which is genuinely predictive and
non-circular: best-model F1 ranges from `0.83` to `0.93` across feature
sets, splits, and both courses and never reaches `1.000`, in direct
contrast to the saturated synthetic `passed` task (Section 4).

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

## 7. Explanation Regime-Sensitivity and Course/Institution-Specificity

A distinct threat concerns the **stability and therefore the usefulness of
the explanations** across evaluation regimes, courses, and institutions. A
teacher-facing explanation is only actionable if the features it surfaces,
and their relative priority, are reasonably consistent across the
scenarios under which the model is used. The OULAD explanation-stability
analyses show that this consistency is at best moderate and never reaches a
high-stability bar.

Within a single course (DDD 2013J, `exp_007`), comparing the global
importance ranking on the student-grouped split with the temporal-forward
split yields Kendall rank correlations of `0.55`-`0.79` (mean `0.67`)
across the three feature sets — moderate, and below a `0.90` high-stability
threshold for every set; the widest feature set, `C_twin_oulad`, is the
least order-stable (`tau = 0.55`). Across courses (DDD versus BBB 2013J,
`exp_010`), agreement is **lower still**: cross-cohort Kendall `tau` of
`0.32`-`0.61` (mean `0.52`), with top-5 membership overlapping only
partially (Jaccard `0.43`-`1.00`). Extending to a second institution, the
matched three-institution engagement comparison (`exp_012`) finds a mean
cross-institution importance-rank Kendall `tau` of `0.56` over seven shared
engagement concepts (student-grouped mean `0.49`, temporal-forward mean
`0.62`), again well below `0.90`; the most stable pair is KU↔BBB
(`tau = 0.714`) and the least is KU↔DDD on the student-grouped split
(`tau = 0.238`).

The honest reading is that the same few features tend to dominate across
regimes — submission discipline, the `overall_mastery_proxy`, the
registration-state flag, and, in the engagement setting, cumulative clicks
and active days — so the broad story is recurrent. But the **relative
ordering** of features is regime-sensitive within a course, partly
course-specific across courses, and only partly institution-transferable.
None of the measured agreements reaches `0.90`. This is a threat to
validity for any narrative that treats a single importance ranking as a
stable, transferable account of "what matters." It must be carried into the
dissertation as a limitation on the explanation layer's generalizability,
not smoothed over. These remain model-behavior observations under the
project's permutation-importance methods, not causal claims, and they
describe how the gradient-boosting model's attributed importances move
across regimes rather than which factors actually move educational
outcomes.

## 8. Public Benchmark Is Not Institutional Validation

The project now includes a public OULAD benchmark across two courses and a
partial check on a second institution, but it still has no full validation
on a local institutional cohort. OULAD is valuable because it stress-tests
the representation logic on a public dataset with different assessment
design, missingness, and outcome semantics. It does not provide
institution-specific validation of the teacher workflow, intervention
context, local LMS event semantics, or local grading policy.

The second-institution evidence is genuinely useful but **partial by
construction**. `exp_011` adds the KU Leuven de-identified
learning-analytics dataset (year 1819, two courses pooled, `1495` students,
weeks `2`-`15`). Its integration surfaces a structural cross-institution
finding: KU Leuven exposes raw clickstream, forum activity, and course
structure but **no intermediate scored assessments and no continuous
grade** — only a binary `PASSED` outcome — so the project's central
mastery/assessment ablation **cannot be built on KU Leuven at all**. The
question "does the mastery block help?" is simply not answerable there.
What KU Leuven supports is an engagement-only, classification-only check,
on which engagement predicts passing only modestly (best-model F1
`0.75`-`0.76`, ROC-AUC `0.65`-`0.72`) and a richer engagement
representation is essentially level with a minimal one (fixed-model F1
delta `-0.015` temporal-forward, `+0.000` student-grouped).

The matched three-institution synthesis `exp_012` consolidates this:
across OULAD DDD 2013J, OULAD BBB 2013J, and KU Leuven 1819 under an
identical two-feature engagement design, a richer engagement set adds only
neutral-to-modest F1 over a minimal cumulative-clicks-plus-active-days
baseline — positive mostly on the student-grouped split (up to `+0.072`)
and approximately zero on the stricter temporal-forward early-warning split
(spread `-0.016` to `+0.026`, e.g. DDD `-0.0003`, KU `-0.015`). The honest
reading is that **richer engineered feature richness does not robustly
help** across three real cohorts and two institutions.

Two honesty constraints bound how much this external evidence can carry.
First, the cross-institution comparison is necessarily **partial**: KU
Leuven cannot test the mastery/Twin ablation at all, and its engagement
task is weaker than and **distinct from** the OULAD assessment task, so
this is evidence about the robustness of feature-richness claims, not a
like-for-like institutional replication of the Twin ablation. Second,
the dissertation therefore cannot claim that the predictive advantage of
the lean Twin replicates on an institutional cohort, that the explanation
behavior remains teacher-meaningful under real classroom noise, or that the
early-warning framing survives outside the synthetic generator. The correct
claim is narrower: external transfer was tested across two OULAD courses
(heterogeneous) and a partial engagement-only check on a second institution
(feature-richness does not robustly help), producing honest mixed-to-null
evidence rather than full external validity. This remains a dominant
external-validity threat.

## 9. Dependence on Generator Assumptions

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

## 10. Other Repository-Documented Ambiguities

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

## 11. Summary

Under the present synthetic experimental environment, a lean Twin
representation centered on the mastery block appeared to improve prediction
beyond a stronger LMS baseline and remained interpretable in a
model-behavior sense — but that apparent gain is an artifact of a
deterministic, circular synthetic target, not learnable signal. The
corresponding limitations are that the main development dataset is
synthetic with a circular target, the binary classification task is
saturated there, the dominant mastery feature is highly redundant with
cumulative assignment scores, and the explanations are model-behavior
rather than causal and do not include SHAP. On real, non-circular data the
evidence is honestly mixed rather than a validation: across two OULAD
courses the Twin value is heterogeneous (null on DDD 2013J, partial on BBB
2013J with mastery temporal-forward `-1.026` RMSE), the explanations are
regime-sensitive within a course (Kendall `tau` `0.55`-`0.79`, mean `0.67`)
and partly course-specific across courses (`0.32`-`0.61`, mean `0.52`), and
a second institution (KU Leuven, `exp_011`/`exp_012`, engagement-only)
confirms that feature-richness does not robustly help (cross-institution
importance-rank mean `tau` `0.56`). None of the measured explanation
agreements reaches `0.90`. The dissertation account should present the
contribution within these limits and should not overstate either predictive
superiority or explanatory completeness.

For defense packaging, these limitations should be treated as guardrails, not
as afterthoughts. The demo and final report should explicitly distinguish
synthetic internal evidence (a circular-target artifact), OULAD
public-benchmark transfer evidence (two cohorts, heterogeneous),
cross-institution engagement robustness evidence (KU Leuven, partial),
model-behavior explanation, and causal intervention reasoning — and should
never present the "Digital Twin" as a simulation or counterfactual engine
rather than the lean, time-aware weekly state representation it is.
