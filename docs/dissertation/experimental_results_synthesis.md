# Experimental Results Synthesis

This document integrates the results of the completed experiments into a
chronological narrative. Each experiment is described in terms of the question
it was designed to answer, the setup it employed, the headline result it
produced, and the consequence that result had for the next experiment in the
sequence. The combined narrative explains how the project moved from an open
question about full Digital Twin superiority to a validated lean Twin
representation with an interpretable explanation layer, followed by an
external public-benchmark stress test on OULAD.

The first four experiments operate on schema `v1.2`, on the refined synthetic
dataset produced by `generator_v1_3_refined.yaml`, with primary target
`final_grade`, secondary context target `passed`, primary student-grouped
split (`test_size = 0.25`, `seed = 42`), and a snapshot filter restricted to
weeks `4..10`. The primary headline numbers below reproduce the values
recorded in the per-experiment writeups under `docs/experiments/` and in the
`experiment_metadata.json` artifacts under
`data/artifacts/experiments/<experiment_id>/`. `exp_005_public_benchmark_oulad`
is separate: it uses the local OULAD CSV files under `datasets/oulad`, an
external adapter schema `external_oulad_adapter_v1`, primary target
`final_weighted_score`, and secondary target `passed_observed`.

## 1. exp_001_baseline — Baseline Feature-Set Comparison

### 1.1 What it was designed to test

`exp_001_baseline` establishes the first reproducible modeling baseline for
the refined dataset by comparing three nested feature sets — `A_simple`,
`B_lms`, and `C_twin` — across a small stack of classical estimators. The
hypothesis is whether the full Digital Twin representation improves
`final_grade` prediction over an LMS-style baseline, or whether the
engineered Twin layer mostly duplicates information already present in
cumulative LMS aggregates.

### 1.2 Setup

Both classification (logistic regression, random forest, gradient boosting)
and regression (linear regression / Ridge, random forest, gradient boosting)
families are trained for each feature set under the primary student-grouped
split and the secondary temporal-forward split. The supervised targets are
`final_grade` (primary) and `passed` (secondary context). `risk_level` is
explicitly excluded.

### 1.3 Key result

On the primary student-grouped split, the best regression RMSE values were:

| Feature set | Best RMSE | Best model |
| --- | ---: | --- |
| `A_simple` | 2.673 | gradient boosting |
| `B_lms` | 2.101 | gradient boosting |
| `C_twin` | 2.149 | random forest |

Under the stricter temporal-forward split, the gap widened in favor of the
LMS baseline:

| Feature set | Best RMSE | Best model |
| --- | ---: | --- |
| `A_simple` | 2.210 | linear regression |
| `B_lms` | 2.270 | linear regression |
| `C_twin` | 2.937 | linear regression |

For `passed`, all three feature sets reached F1 = `1.000` under both splits.
The classification target was therefore saturated and could not discriminate
between representations.

### 1.4 Research consequence

The headline finding is negative but useful: the full Twin representation did
not reliably outperform the LMS baseline, and it degraded under the stricter
forward split. The methodologically correct response is to test which
**subgroups** of the Twin layer add marginal value beyond `B_lms`, rather
than to discard the Twin representation wholesale or to re-tune models. The
project's research direction therefore shifts from "is the full Twin justified?"
to "which Twin subgroup, if any, is justified?" This shift is documented in
[exp_001_vs_exp_002_comparison.md](../experiments/exp_001_vs_exp_002_comparison.md)
and motivates the immediate follow-up experiment.

## 2. exp_002_twin_ablation — Twin Subgroup Ablation

### 2.1 What it was designed to test

`exp_002_twin_ablation` decomposes the Twin layer into semantically coherent
blocks and asks which of them, individually or in compact combination,
improve on `B_lms`. The hypothesis is that the full Twin set is partly
redundant, and that a smaller subset may retain any useful Twin signal with
less collinearity.

### 2.2 Setup

The feature sets are `B_lms` (baseline), `B_lms_plus_trends`,
`B_lms_plus_mastery`, `B_lms_plus_indices`, `B_lms_plus_temporal`,
`B_lms_plus_trends_mastery` (compact combination), and `C_twin_full` (upper
reference). Models, splits, targets, seed, and snapshot filter are unchanged
from `exp_001_baseline` to keep the ablation strictly comparable.

### 2.3 Key result

On the primary student-grouped split, ranked by best RMSE:

| Feature set | Best RMSE | Δ vs `B_lms` |
| --- | ---: | ---: |
| `B_lms_plus_mastery` | 1.894 | -0.206 |
| `B_lms_plus_trends_mastery` | 1.973 | -0.127 |
| `B_lms_plus_indices` | 2.035 | -0.066 |
| `B_lms_plus_temporal` | 2.078 | -0.023 |
| `B_lms_plus_trends` | 2.096 | -0.005 |
| `B_lms` | 2.101 |  +0.000 |
| `C_twin_full` | 2.149 | +0.049 |

Under the temporal-forward split, the picture is less favorable to
mastery-augmented sets: `B_lms_plus_mastery` is essentially level with
`B_lms` (`+0.006`), `B_lms_plus_indices` mildly improves (`-0.068`), and
`C_twin_full` deteriorates (`+0.667`). The classification task remains
saturated for `passed`.

### 2.4 Research consequence

The mastery block is the only single-block extension that produces a
substantive improvement on the primary split, and the full Twin set remains
unjustified relative to the LMS baseline. The lean Twin recommendation
recorded in
`data/artifacts/experiments/exp_002_twin_ablation/lean_twin_recommendation.md`
is to carry `B_lms_plus_mastery` forward and to mark the full `C_twin` as
not justified under the present setup. The next research question becomes
whether the mastery block is a genuine signal carrier or a near-direct
proxy for `final_grade` that would compromise the lean Twin's interpretability
in the explanation phase.

## 3. exp_003_mastery_validation — Mastery Validation

### 3.1 What it was designed to test

`exp_003_mastery_validation` audits the mastery block before any explanation
layer is added on top of it. The objective is to determine whether mastery
adds genuine signal beyond `B_lms` or whether it acts as a direct proxy for
`final_grade`. The validation comprises overall regression headlines, per-week
delta analysis, mastery-vs-target correlation analysis, mastery-vs-LMS
redundancy analysis, drop-column re-training, and permutation importance.

### 3.2 Setup

The compared feature sets are `B_lms` (baseline) and `B_lms_plus_mastery`
(candidate), with `B_lms_plus_trends_mastery` and `C_twin_full` retained as
optional context. The week-aware protocol fits a model independently per week
in `[4, 5, 6, 7, 8, 9, 10]` under the same student-grouped split, and a week
is considered improved when `candidate_rmse - baseline_rmse < -0.05`.
"Early weeks" are defined as weeks `<= 6`.

### 3.3 Key result

The headline regression result reproduces the ablation finding: on the
primary split, `B_lms_plus_mastery` reaches RMSE `1.894` versus `2.101` for
`B_lms`, a delta of `-0.206`. Under the temporal-forward split, the candidate
is essentially level with the baseline (`+0.006`), confirming the asymmetry
already observed.

The week-aware protocol shows that the candidate improves on the baseline at
weeks `[4, 5, 6, 7, 8]` and is essentially level at weeks `[9, 10]`. Three
of the five improving weeks fall inside the early-week window, supporting the
early-warning framing.

The diagnostic checks expose the redundancy structure clearly:

| Mastery feature | Pearson r vs `final_grade` | Strongest LMS correlate (|r|) |
| --- | ---: | --- |
| `current_topic_mastery` | 0.935 | `avg_quiz_score_to_date` (0.934) |
| `overall_mastery` | 0.984 | `avg_assignment_score_to_date` (0.993) |

Drop-column re-training shows that removing `overall_mastery` increases RMSE
by `+0.228`, while removing `current_topic_mastery` increases RMSE by only
`+0.036`. Permutation importance places `overall_mastery` as the largest
single contributor to predictive performance.

Temporal lineage is verified by inspection of
`services/ml/src/generator/snapshots.py`: both mastery features are computed
strictly from submission scores filtered to `week_number <= snapshot week`
and never read end-of-course outcome fields.

### 3.4 Research consequence

The mastery block is validated as a lean Twin component, but with an explicit
caveat: `overall_mastery` is highly redundant with cumulative assignment
scores and dominates the candidate model's behavior. The carry-forward
recommendation is therefore `carry_forward` of `B_lms_plus_mastery` with
documented redundancy, captured in
`data/artifacts/experiments/exp_003_mastery_validation/mastery_carry_forward_recommendation.md`.
This decision determines that the explanation phase will be performed on the
lean Twin candidate rather than on the full Twin set, and that the
`overall_mastery` redundancy must be audited in any subsequent XAI step.

## 4. exp_004_xai_on_lean_twin — XAI on the Lean Twin

### 4.1 What it was designed to test

`exp_004_xai_on_lean_twin` introduces the explanation layer only after a
predictively useful and structurally credible representation has been
identified. It explains the validated lean Twin candidate
`B_lms_plus_mastery` and decides whether its predictive behavior is
interpretable and teacher-meaningful, or whether the explanations collapse
onto a single dominating mastery feature.

### 4.2 Setup

The reference model is gradient boosting under the primary student-grouped
split, with `B_lms` as the reference baseline and `B_lms_plus_mastery` as
the lean Twin set. Explanations are produced through two model-behavior
methods rather than through SHAP. Global explanations use held-out
**permutation importance** on `neg_root_mean_squared_error` with
`permutation_repeats = 15`, supplemented by tree-native importance where
available. Local explanations use **one-feature-at-a-time replacement with
the training median**, applied to five deterministically selected
representative cases (`strong_performer`, `at_risk`, `improving_trajectory`,
`declining_trajectory`, `borderline_medium`).

SHAP is not used in this phase. The fallback reason is recorded explicitly
in the experiment configuration: SHAP is not part of the current project
dependency contract. The methods are therefore documented as **directional
model-behavior explanations, not causal claims**.

A dedicated `overall_mastery` dominance audit is performed against
configurable thresholds to detect collapse onto a single feature.

### 4.3 Key result

Predictive behavior is consistent with the validation experiment:

| Configuration | RMSE | MAE | R² |
| --- | ---: | ---: | ---: |
| `B_lms` | 2.101 | 1.681 | 0.990 |
| `B_lms_plus_mastery` | 1.894 | 1.510 | 0.992 |
| `B_lms_plus_mastery` without `overall_mastery` | 2.122 | 1.686 | 0.990 |

The lean Twin advantage versus the LMS baseline is `-0.206` RMSE; the cost
of removing `overall_mastery` is `+0.228` RMSE.

Global explanations on `B_lms_plus_mastery` rank `activity_score_to_date`
first (importance share `0.648`), `overall_mastery` second (share `0.178`),
and `avg_assignment_score_to_date` third (share `0.090`). The remaining
features — including `time_spent_to_date`, `on_time_submission_rate_to_date`,
`attendance_rate_to_date`, `avg_quiz_score_to_date`, and
`current_topic_mastery` — appear at lower but non-negligible shares. The
baseline-versus-lean comparison shows that the lean Twin top-five replaces
`avg_quiz_score_to_date` and `attendance_rate_to_date` from the LMS top-five
with `overall_mastery` and `time_spent_to_date`, indicating that mastery
enters the explanation as one factor among several rather than as a
total-information substitute.

The dominance audit returns the outcome `acceptable_with_caveat`. The
single flag raised is that the top global feature accounts for `0.648` of
the importance share. The average local mastery contribution share across
the five representative cases is `0.194`, which sits below the configured
warning threshold of `0.60`. The five local cases are summarized as
teacher-meaningful — four of them feature mastery as part of the
student-state story, and one (`improving_trajectory`) is mostly LMS-behavior
and performance driven.

### 4.4 Research consequence

The lean Twin candidate is carried forward for dissertation XAI with an
`overall_mastery` redundancy caveat. Explanations remain teacher-meaningful
and do not collapse onto a single feature. The decision is recorded as
`carry_forward_with_caveat` in
`data/artifacts/experiments/exp_004_xai_on_lean_twin/xai_carry_forward_recommendation.md`.
The two structural caveats — that the top feature dominates global
importance share, and that `overall_mastery` is known from
`exp_003_mastery_validation` to be highly redundant with LMS aggregates —
are preserved as explicit caveats in the dissertation narrative rather than
treated as resolved.

## 5. exp_005_public_benchmark_oulad — Public OULAD Benchmark

### 5.1 What it was designed to test

`exp_005_public_benchmark_oulad` is an external representation-transfer
benchmark. It does not compare the synthetic dataset against OULAD as if
datasets were competing models. Instead, it asks whether the same
representation logic can be approximated on OULAD and whether the lean
mastery analogue improves over a strong OULAD LMS-style baseline.

### 5.2 Setup

The benchmark uses only the seven local OULAD files in `datasets/oulad`:
`assessments.csv`, `courses.csv`, `studentInfo.csv`,
`studentRegistration.csv`, `studentVle.csv`, `vle.csv`, and
`studentAssessment.csv`. The configured subset is module-presentation
`DDD` `2013J`, selected to keep the benchmark aligned with the current
one-course scope while retaining a sufficiently large cohort and observed
exam score rows.

The adapter builds weekly rows at the grain
`1 student-course presentation x 1 week`, using weeks `4..38`. The resulting
modeling table has `67,830` snapshot rows and `1,938` students. The primary
target is the derived `final_weighted_score`, computed from
`assessments.weight` and `studentAssessment.score`; it is not treated as
identical to the synthetic `final_grade`. The secondary label
`passed_observed` maps OULAD `Pass` and `Distinction` to positive and
`Fail` and `Withdrawn` to negative.

The compared feature sets are:

- `B_lms_oulad`: cumulative assessment performance, submission discipline,
  VLE activity intensity/category features, course progression, and
  registration state;
- `B_lms_plus_mastery_oulad`: the same baseline plus assessment-structure
  mastery proxies such as due-to-date weighted mastery, current assessment
  cluster mastery, assessment-type mastery, and coverage context.

The benchmark uses the same model-family discipline as the earlier phases:
Ridge/linear baseline, random forest, and gradient boosting for regression,
with logistic regression, random forest, and gradient boosting for the
secondary classification task. The primary split is grouped by `id_student`;
the secondary split is temporal-forward with held-out students.

### 5.3 Key result

On the primary student-grouped split, the lean mastery analogue does not
improve over the OULAD LMS baseline:

| Feature set | Best RMSE | Best model | Δ vs `B_lms_oulad` |
| --- | ---: | --- | ---: |
| `B_lms_oulad` | 12.658 | gradient boosting | +0.000 |
| `B_lms_plus_mastery_oulad` | 12.724 | gradient boosting | +0.066 |

On the secondary temporal-forward split, the direction reverses:

| Feature set | Best RMSE | Best model | Δ vs `B_lms_oulad` |
| --- | ---: | --- | ---: |
| `B_lms_oulad` | 9.566 | gradient boosting | +0.000 |
| `B_lms_plus_mastery_oulad` | 9.161 | gradient boosting | -0.406 |

The secondary classification target is nearly level between feature sets:
on the grouped split F1 is `0.863` for `B_lms_oulad` and `0.861` for
`B_lms_plus_mastery_oulad`; on the temporal-forward split F1 is `0.887`
and `0.884`, respectively.

### 5.4 Research consequence

The OULAD benchmark complicates rather than confirms the synthetic
carry-forward claim. The lean mastery analogue is slightly worse on the
primary grouped split but better on the secondary temporal-forward split.
This mixed result suggests that mastery-transfer behavior is
context-sensitive. The earlier synthetic experiments remain internally valid
for the controlled generator environment, but the OULAD benchmark prevents a
stronger claim that the lean mastery advantage has been externally validated.

The correct dissertation conclusion is therefore bounded: OULAD provides a
public-dataset stress test that keeps the lean Twin hypothesis plausible but
unresolved externally. It is not evidence that the synthetic dataset is better
than OULAD, and it is not full institutional validation.

## 6. Trajectory From Full Twin to Lean Twin

The first four experiments form a single methodological arc. `exp_001_baseline`
poses the open question of whether the full Twin representation improves on
the LMS baseline, and finds that it does not under the present setup.
`exp_002_twin_ablation` decomposes the Twin layer into blocks and identifies
mastery as the only single-block extension that substantively improves on
`B_lms` on the primary split, while confirming that the full Twin
representation remains unjustified. `exp_003_mastery_validation` audits the
mastery block against target-correlation, redundancy, drop-column, and
per-week criteria and validates the carry-forward with an explicit
redundancy caveat. `exp_004_xai_on_lean_twin` explains the validated lean
candidate using documented permutation and local perturbation methods and
finds that the explanations are teacher-meaningful and do not collapse onto
a single feature.

The progression is therefore not from a successful full Twin to a refined
full Twin. It is from an unjustified full Twin to a **validated lean Twin
representation**: `B_lms` augmented by the mastery block. The direction of
the project, accordingly, is not to defend full Twin superiority but to
present a smaller, structurally credible Twin that delivers measurable
predictive value over a stronger LMS baseline while remaining interpretable.

`exp_005_public_benchmark_oulad` extends this arc by testing whether the
representation logic transfers to a public benchmark. The result is mixed:
primary grouped performance does not improve, while secondary temporal-forward
performance does. That means the lean Twin candidate remains defensible as an
internally validated representation, but external transfer remains an open
empirical question.

For final dissertation packaging, this internal-versus-external distinction is
the controlling interpretation. The first four experiments support a bounded
internal conclusion about `B_lms_plus_mastery`; the fifth experiment adds a
public stress test that complicates transfer and prevents a stronger
external-validity claim.

## 7. Why XAI Was Introduced Only After Lean Validation

The explanation phase was deliberately deferred until a representation had
been identified that could be explained meaningfully. Producing explanations
on top of the full Twin set in `exp_001_baseline` would have invested
interpretive effort in a representation that did not improve on the LMS
baseline; producing explanations on `B_lms_plus_mastery` immediately after
`exp_002_twin_ablation` would have ignored the redundancy concern between
`overall_mastery` and `avg_assignment_score_to_date`. The sequence
ablation → mastery validation → XAI ensures that the explanation layer is
applied to a representation whose predictive value, internal redundancy
profile, and temporal lineage are all documented in advance. This ordering
is reflected in the explicit `parent_experiment` metadata recorded in each
experiment's configuration:

- `exp_002_twin_ablation` → parent `exp_001_baseline`
- `exp_003_mastery_validation` → parent `exp_002_twin_ablation`
- `exp_004_xai_on_lean_twin` → parent `exp_003_mastery_validation`

The dissertation narrative inherits this same dependency chain.

`exp_005_public_benchmark_oulad` is not an additional synthetic validation
step in that chain. It is the external benchmark appended after the XAI phase
to test whether the representation logic remains plausible outside the
generator-controlled setting.
