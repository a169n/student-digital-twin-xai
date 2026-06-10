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

**(This `exp_005` two-set reading is superseded by the full ablations in §6
(`exp_006`, mixed-to-null on DDD) and §8 (`exp_009`, heterogeneous on BBB); it is
recorded here only as the historical first-look result.)** At the `exp_005` stage,
the OULAD benchmark complicated rather than confirmed the synthetic
carry-forward claim. The lean mastery analogue is slightly worse on the
primary grouped split but better on the secondary temporal-forward split.
This mixed result suggested that mastery-transfer behavior is
context-sensitive. The earlier synthetic experiments remain internally valid
for the controlled generator environment, but the two-set OULAD probe prevented a
stronger claim that the lean mastery advantage had been externally validated.

The bounded `exp_005` conclusion was therefore that OULAD provides a
public-dataset stress test that kept the lean Twin hypothesis plausible but
unresolved externally. It is not evidence that the synthetic dataset is better
than OULAD, and it is not full institutional validation. The full nested
ablations below replace this with the firmer DDD-null / BBB-partial verdict.

## 6. exp_006_oulad_full_ablation — Full OULAD Ablation (DDD 2013J)

### 6.1 What it was designed to test

`exp_006_oulad_full_ablation` extends the OULAD benchmark from the two-set
transfer test of `exp_005` to the full nested A/B/C ablation on real data. The
question is whether the structured ablation that identified a lean Twin
candidate on the synthetic data reproduces on a real, non-circular dataset:
does any Twin feature block deliver a consistent predictive advantage over a
competent LMS-analytics baseline once the deterministic synthetic target is
removed?

### 6.2 Setup

The experiment runs on OULAD module-presentation `DDD` `2013J`: `67,830`
weekly snapshots across `1,938` students, built with the identical
leakage-aware pipeline used on the synthetic data. Six feature-set analogues
are compared — `A_simple_oulad`, `B_lms_oulad`, the per-block extensions, and
`C_twin_oulad` — under both the student-grouped and temporal-forward splits.
Crucially, this phase introduces **fixed-model gradient-boosting reporting**
to neutralize the best-model-per-cell model-flip artifact flagged in
`exp_002`/`exp_005`: the same model is held fixed across splits so that
feature-block deltas are not confounded with model selection.

### 6.3 Key result

The result is a **mixed-to-null** finding. Under the fixed-model comparison,
no Twin feature block improves over the strong `B_lms_oulad` baseline by more
than `1.0` RMSE on either split. The largest single gain is the mastery
analogue on the temporal-forward split (RMSE `9.561` to `9.180`, delta
`-0.381`, roughly a four percent reduction), but the same block is `+0.061`
worse on the student-grouped split. The composite-index block improves the
temporal-forward split modestly (`-0.218`) and is essentially flat on the
grouped split (`+0.008`). The full `C_twin_oulad` analogue is within `±0.025`
RMSE of the baseline on both splits — non-inferior, but not distinctly better.
The minimal `A_simple_oulad` baseline is clearly worse (`+1.207` grouped,
`+4.105` temporal-forward), confirming that the LMS behavioral layer carries
the predictive signal and that the Twin engineering adds little on top of it.

The OULAD task is genuinely predictive, not algebraic: best-model
classification F1 ranges from `0.83` to `0.887` across feature sets and splits
and never reaches `1.000`. This is the direct empirical contrast with the
synthetic environment, where `passed` saturates at F1 `1.000` precisely
because the synthetic `final_grade` is a deterministic, noise-free function of
the same behaviors the features re-aggregate (week-10 reconstruction error
`0.008`, correlation `1.000000`). The synthetic R²≈0.99 and F1=1.000 are
therefore algebraic artifacts, not learnable signal; the real OULAD numbers
are the actual evidence.

### 6.4 Research consequence

The full ablation supersedes the softer `exp_005` "complicates" language with
a stronger, cleaner statement: on a real, non-circular dataset, the engineered
Digital Twin feature blocks do **not** deliver a consistent predictive
advantage over a competent LMS-analytics baseline, and the apparent synthetic
advantage of the mastery block did not robustly transfer. This is an honest
negative-to-mixed result on the DDD 2013J cohort. It is one of two OULAD
courses examined; `exp_009` (§9) reports a second cohort, BBB 2013J, that
qualifies it and shows the result is not uniform across courses.

## 7. exp_007_xai_on_oulad — OULAD XAI and Regime-Sensitivity (DDD 2013J)

### 7.1 What it was designed to test

`exp_007_xai_on_oulad` applies the model-behavior explanation layer to the
real OULAD model. It asks two questions: which features the OULAD model
appears to rely on, and whether the resulting importance rankings are stable
across evaluation regimes (student-grouped versus temporal-forward).

### 7.2 Setup

The same explanation methods used on the synthetic data are applied here:
held-out permutation importance, model-native importance, and one-feature
local perturbation; no SHAP. Explanations are produced for `B_lms_oulad`,
`B_lms_plus_mastery_oulad`, and `C_twin_oulad` under both splits. Regime
stability is quantified by the Kendall rank correlation (`tau`) of the global
importance ranking between the two splits, together with Jaccard overlap of
the top-5 feature sets.

### 7.3 Key result

The explanations lean on features that are themselves close to the target. The
dominant feature is `assessment_submission_rate_due_to_date` for the LMS
baseline (importance share `0.28`-`0.38`) and, once mastery is included, the
co-circular `overall_mastery_proxy` (share `0.23`-`0.43`), which aggregates
weighted assessment scores that partly feed the target. The genuinely
exogenous signals — the registration-state flag `is_unregistered_by_week`
(consistently ranked second to fourth, share `0.13`-`0.20`) and the VLE
clickstream features (share `0.02`-`0.06`) — are present and interpretable but
carry modest weight.

The explanations are **regime-sensitive**. Comparing the global importance
ranking across the two splits, agreement is moderate and below a
high-stability threshold for every feature set: `tau = 0.79` for `B_lms_oulad`,
`0.68` for `B_lms_plus_mastery_oulad`, and `0.55` for `C_twin_oulad` (mean
`0.67`, none reaching `0.90`). Top-5 membership can nonetheless be stable —
Jaccard overlap is `1.00` for the two mastery/twin sets and `0.67` for the LMS
baseline — meaning the same few features dominate across regimes while their
relative priority reorders, and the widest feature set (`C_twin_oulad`) is the
least order-stable.

### 7.4 Research consequence

*Which* features the model appears to rely on, and in what order, depends on
the evaluation scenario. This extends explanation-stability analysis to the
public-benchmark transfer setting and dovetails with the predictive
mixed-to-null result of §6: not only does the Twin representation fail to win
on accuracy, its explanation is not regime-invariant either. These are
model-behavior observations, not causal claims. The natural next question is
whether the regime-sensitivity and the predictive heterogeneity are
course-specific, which motivates the second-cohort replication in §9–§10.

## 8. exp_008 — Synthetic Faithfulness Probe (Methods Appendix)

### 8.1 What it was designed to test

`exp_008` is a controlled faithfulness probe, not a headline result. It asks
whether the model-behavior explanation machinery recovers a *known* ground
truth when one exists. Because the synthetic generator defines `final_grade`
as a closed-form weighted mean of behaviors, the final course week provides an
oracle ordering of feature importance against which the explanation method can
be checked.

### 8.2 Setup

At the final course week, the generator's weight ordering is treated as the
oracle. Permutation importance is compared against this oracle by Kendall
`tau`. The probe also inspects how proxy correlation and redundancy distort
importance away from the underlying latent drivers.

### 8.3 Key result

At the final week, the importance ranking recovers the generator's weight
ordering exactly: Kendall `tau = 1.0`. The probe simultaneously illustrates
the distortions: `activity_score_to_date` takes an importance share of `0.108`
as a latent-driven proxy rather than a direct cause, and `overall_mastery` is
redundant with `avg_assignment_score_to_date` at Pearson `r = 0.994`. The
probe therefore confirms that the method is faithful to ground truth when
ground truth is known, while documenting how proxy structure and redundancy
shape the importance picture.

### 8.4 Research consequence

This is a **methods appendix**, not primary evidence. It validates the
explanation method's faithfulness on a controlled oracle and characterizes the
proxy/redundancy effects that complicate interpretation on real data. It does
not add to the predictive claims, which rest on the real OULAD and KU Leuven
cohorts; the synthetic oracle exists only because the synthetic target is
deterministic and circular.

## 9. exp_009_oulad_full_ablation_bbb — Second-Cohort Ablation (BBB 2013J)

### 9.1 What it was designed to test

`exp_009` repeats the full nested ablation on a second OULAD
module-presentation, BBB 2013J, to test whether the DDD 2013J mixed-to-null
result is course-specific or robust across courses.

### 9.2 Setup

BBB 2013J comprises `2,237` students and `80,532` weekly snapshots, with a
richer dated-assessment structure than DDD. The feature sets, splits,
leakage-aware pipeline, and fixed-model gradient-boosting reporting are
identical to `exp_006`, so the two cohorts are directly comparable.

### 9.3 Key result

The Twin-block value is **heterogeneous, not uniformly null**. Under the
fixed-model comparison on BBB 2013J, the mastery block improves the
temporal-forward split by `-1.026` RMSE (`5.284` versus `6.311`) — crossing
the one-point threshold that no block crossed on DDD — and the full
`C_twin_oulad` improves it by `-0.765`. On the student-grouped split, however,
every block stays within `0.087` RMSE of the baseline (null, as on DDD), and
the trend and composite-index blocks are null on both splits of both courses.
Classification remains genuinely predictive (F1 `0.87`-`0.93`, never `1.000`).

### 9.4 Research consequence

The DDD null was **partly course-specific**: on a course with richer
assessment structure the mastery block delivers a meaningful gain under
forward-time evaluation, but the advantage does not generalize to the
student-grouped split, to the other Twin blocks, or to the other course. The
defensible cross-course statement is therefore one of heterogeneity — neither
uniform null nor uniform benefit. This motivates a cross-cohort
explanation-stability analysis (§10) to see whether the model's "why" is also
course-dependent.

## 10. exp_010_xai_on_oulad_bbb — BBB XAI and Cross-Cohort Stability

### 10.1 What it was designed to test

`exp_010` repeats the model-behavior XAI on BBB 2013J and adds a cross-cohort
explanation-stability comparison: are the importance rankings shared between
the two OULAD courses, or are they course-specific?

### 10.2 Setup

The same permutation/native/local methods (no SHAP) are applied to the BBB
2013J model under both splits. Cross-cohort stability is quantified by the
Kendall `tau` of the importance rankings of DDD versus BBB, per feature set and
split, together with top-5 Jaccard overlap.

### 10.3 Key result

The importance topology is qualitatively **shared** across the two courses —
`overall_mastery_proxy`, assessment-submission discipline, and the
`is_unregistered_by_week` withdrawal flag dominate on both — but the rankings
are **not stable**. The cross-cohort agreement (Kendall `tau` of DDD versus
BBB) is `0.32`-`0.61` (mean `0.52`), lower than the within-cohort cross-split
agreement of §7 (`0.55`-`0.79`, mean `0.67`), and no cell reaches a
high-stability threshold; top-5 membership overlaps only partially (Jaccard
`0.43`-`1.00`).

### 10.4 Research consequence

The model's "why" is not only regime-sensitive within a course but also partly
course-specific across courses. This cross-cohort extension of the
explanation-stability analysis tightens the cautionary message: both the
feature-group predictive value and the explanations that accompany it depend on
the course and the evaluation scenario. These remain model-behavior
observations, not causal claims, and the evidence still spans only two courses
from a single institution (OULAD), which motivates a second-institution check
in §11.

## 11. exp_011 — Second Institution (KU Leuven), Engagement-Only

### 11.1 What it was designed to test

`exp_011` adds a second institution, the KU Leuven de-identified
learning-analytics dataset, to extend external validity beyond OULAD. It asks
whether the project's representation-richness question survives a change of
institution, and whether weekly engagement features predict `PASSED`.

### 11.2 Setup

The integration itself surfaces a structural finding: KU Leuven exposes raw
clickstream, forum activity, and course structure, but **no intermediate
scored assessments and no continuous grade** — only a binary `PASSED` outcome
and categorical exam-session buckets. The mastery/assessment ablation
therefore **cannot be reproduced on KU Leuven at all**; the question "does the
mastery block help?" is unanswerable here because the data to construct it does
not exist. This is itself a cross-institution heterogeneity result. What KU
Leuven supports is an **engagement-only, classification-only** check on year
1819 (two courses pooled, `1,495` students, weeks `2`–`15`, leakage-safe
cumulative-to-date features under both splits): does a richer engagement
representation (`B_engagement`) beat a minimal one (`A_simple_engagement`)?

### 11.3 Key result

Engagement predicts passing only **modestly** — best-model F1 `0.75`-`0.76`,
ROC-AUC `0.65`-`0.72` — far below the assessment-driven OULAD numbers, as
expected when no assessment signal is available (the two are different tasks
and not directly comparable). The **richer** engagement set `B_engagement` is
essentially level with the minimal `A_simple_engagement`: fixed-model F1 delta
`-0.015` on the temporal-forward split and `+0.000` on the student-grouped
split, with a small ROC-AUC gain of `+0.009`/`+0.041`. Permutation importance
shows the signal is carried by basic engagement volume —
`cumulative_active_days_to_date` and `cumulative_clicks_to_date` dominate both
splits (the former takes a `0.456` share on the temporal-forward split) —
while forum participation and temporal position contribute little.

### 11.4 Research consequence

The cross-institution statement is consistent with the OULAD finding and
strengthens it: across three real cohorts spanning two institutions, adding a
richer engineered feature representation does not robustly beat a simpler
baseline. The honest limitation is that the cross-institution comparison is
necessarily partial (KU Leuven cannot test mastery, and its engagement task is
weaker and distinct from the OULAD assessment task), so this is evidence about
the robustness of feature-richness claims, not a like-for-like institutional
replication. This motivates a single matched three-institution synthesis (§12).

## 12. exp_012 — Cross-Institution Engagement Robustness (Three Institutions)

### 12.1 What it was designed to test

`exp_012` consolidates the cross-institution evidence into a single **matched**
comparison: an engagement-only, classification-only `PASSED` comparison across
OULAD DDD 2013J, OULAD BBB 2013J, and KU Leuven 1819 at once, under an
identical two-feature design. The matched constraint is imposed by KU Leuven's
lack of assessment-score data: the mastery/Twin blocks are excluded by
construction so the three institutions are directly comparable. It asks whether
a richer engagement representation consistently beats a minimal two-feature
baseline, and whether the importance drivers of `PASSED` transfer across
institutions.

### 12.2 Setup

The minimal baseline is `A_simple_engagement` (cumulative clicks + cumulative
active days); the richer set is `B_engagement`. Part A reports the fixed-model
(gradient boosting) `B − A` F1 delta on both splits across all three cohorts.
Part B aligns permutation-importance rankings onto seven shared engagement
concepts and compares them pairwise across institutions by Kendall `tau`. The
full synthesis is in `docs/experiments/exp_012_oulad_engagement.md`.

### 12.3 Key result

Part A is **neutral-to-modest with a split asymmetry**. The richer engagement
set never decisively wins or loses on F1. The positive deltas concentrate on
the `student_group` split — DDD `+0.072`, BBB `+0.039`, KU `+0.000` — while the
stricter, early-warning-relevant `temporal_forward` split is essentially flat
to slightly negative: DDD `-0.0003`, KU `-0.015`, and only modestly positive on
BBB (`+0.026`). The full `temporal_forward` spread is therefore `-0.016` to
`+0.026`. ROC-AUC rises slightly more consistently (all six cells positive,
`+0.009` to `+0.041`). The honest reading is the opposite of an accuracy win:
**a two-feature engagement baseline is hard to beat**, and the dominant
`PASSED` signal is already captured by cumulative clicks plus active days.

Part B is **partial transfer**. Aligning the seven shared engagement concepts
and comparing pairwise yields a mean Kendall `tau` of `0.56` (student_group
mean `0.49`, temporal_forward mean `0.62`), well below the `0.90` "stable
everywhere" bar; the most stable pair is KU↔BBB (`tau = 0.714`) and the least
is KU↔DDD on student_group (`tau = 0.238`). The verdict is
`drivers_partly_institution_specific`: `cumulative_active_days_to_date` and
`cumulative_clicks_to_date` recur as the top drivers across all three
institutions and both splits (with the `#1` driver flipping between active-days
and clicks by cohort and split), but the relative ordering of the mid- and
lower-ranked concepts only partially transfers.

### 12.4 Research consequence

The result is a **robustness result, not an accuracy claim**: across three
independent institutions, a minimal two-feature engagement baseline is hard to
beat, and richer engagement features add neutral-to-modest F1 — positive mostly
on the `student_group` split and approximately zero on the stricter
`temporal_forward` early-warning split. The importance drivers transfer only
partially (mean `tau` ≈ `0.56`): broad drivers recur, but the full ordering is
partly institution-specific. This is a statement about gradient-boosting model
behavior, not causal evidence, and it closes the cross-institution arc
consistent with the project's broader honest, mixed-result posture: adding
feature richness does not robustly improve prediction.

## 13. Trajectory: From Circular Synthetic Artifact to Honest Real-Data Finding

The synthetic experiments (`exp_001`–`exp_004`) form a clean internal
methodological arc. `exp_001_baseline` finds that the full Twin representation
does not reliably beat the LMS baseline; `exp_002_twin_ablation` identifies
mastery as the only single-block extension that substantively improves
`B_lms` on the primary split; `exp_003_mastery_validation` audits and
carries forward the mastery block with an explicit redundancy caveat; and
`exp_004_xai_on_lean_twin` explains the lean candidate and finds the
explanations teacher-meaningful and not collapsed onto a single feature. The
crucial reframing, however, is that this apparent "mastery win" is an
**artifact of a circular target**: the synthetic `final_grade` is a
deterministic, noise-free weighted mean of the same behaviors the features
re-aggregate (week-10 reconstruction error `0.008`, correlation `1.000000`),
so the synthetic R²≈0.99 and `passed` F1=1.000 are algebraic artifacts, not
learnable signal. The synthetic arc is therefore best read as a controlled,
cautionary demonstration of how a circular target can manufacture an apparent
representation advantage — not as evidence that any Twin formulation predicts
better.

When the identical leakage-aware pipeline is applied to real, non-circular
data, that apparent advantage **does not robustly transfer**. On OULAD — which
must be read as **two distinct cohorts**, not one undifferentiated benchmark —
the picture is heterogeneous. On DDD 2013J (`exp_006`) the full ablation is
mixed-to-null: no Twin block beats the LMS baseline by more than `1.0` RMSE on
either split, and the minimal `A_simple_oulad` is clearly worse, showing the
LMS layer already carries the signal. On BBB 2013J (`exp_009`), a course with
richer assessment structure, the mastery block does improve the
temporal-forward split by `-1.026` RMSE — but the gain does not hold on the
student-grouped split, on the other Twin blocks, or on the other course. The
honest empirical finding is that engineered Twin value is **course- and
split-dependent, not a robust improvement**. Throughout, the OULAD
classification target is genuinely predictive (best-model F1 `0.83`–`0.93`,
never `1.000`), which is exactly what makes the real-data result trustworthy
where the synthetic one is not.

The explanation layer follows the same trajectory from "interpretable" to
"interpretable but unstable". On DDD (`exp_007`) the importance rankings are
**regime-sensitive** across splits (Kendall `tau` `0.55`–`0.79`, mean `0.67`,
none reaching `0.90`); on BBB versus DDD (`exp_010`) they are also partly
**course-specific** (cross-cohort `tau` `0.32`–`0.61`, mean `0.52`). The
controlled faithfulness probe (`exp_008`) confirms the method recovers a known
oracle ordering exactly (`tau = 1.0`) when ground truth exists, which is what
licenses these stability statements as method-faithful observations rather than
noise.

Extending beyond OULAD, the second institution (KU Leuven, `exp_011`) cannot
even support the mastery ablation — its very absence of scored assessments is a
cross-institution heterogeneity finding — and on the engagement-only task a
richer engagement representation does not beat a minimal one (fixed-model F1
delta `-0.015`/`+0.000`). The matched three-institution synthesis (`exp_012`)
confirms the pattern decisively: across DDD, BBB, and KU Leuven, a two-feature
engagement baseline (clicks + active-days) is hard to beat (richer features add
neutral-to-modest F1, ≈0 on the stricter temporal-forward split), and the
importance drivers transfer only partially (mean Kendall `tau` `0.56`,
`drivers_partly_institution_specific`). Across three real cohorts and two
institutions, the recurring result is that **adding feature richness does not
robustly help**.

The project's contribution, accordingly, is **methodological and cautionary,
not a demonstration of accuracy, Digital Twin superiority, or simulation**. The
"Digital Twin" here is a lean, time-aware weekly student-state representation,
not a simulation or counterfactual engine. The substantive contributions are:
(i) a reproducible, leakage-aware protocol for constructing, ablating, and
explaining weekly student-state representations, reported with fixed-model
comparisons to neutralize model-selection artifacts; (ii) an
explanation-stability analysis showing that, on real data, importance rankings
are regime-sensitive within a course and partly course-specific across courses;
(iii) a cautionary synthetic-circularity demonstration of how a deterministic
target can manufacture an apparent feature-group advantage that fragments on
genuine data; and (iv) an honest mixed/negative real-data finding across two
OULAD cohorts and a second institution. The arc therefore does not end on an
"unresolved/complicates" verdict: it ends on a clear, defensible statement that
engineered feature richness does not robustly improve prediction on real data,
and that the value of both the representation and its explanations is course-
and regime-dependent.

## 14. Why XAI Was Introduced Only After Lean Validation

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

`exp_005`–`exp_012` are not additional synthetic validation steps in that
chain. They are the external phase appended after the synthetic XAI work to
test whether the representation logic remains plausible outside the
generator-controlled setting: a two-set OULAD transfer test (`exp_005`),
full nested ablations and model-behavior XAI on two OULAD cohorts (`exp_006`/
`exp_007` on DDD 2013J, `exp_009`/`exp_010` on BBB 2013J), a controlled
faithfulness probe (`exp_008`), and an engagement-only check on a second
institution consolidated into a matched three-institution synthesis
(`exp_011`/`exp_012`). The dependency chain therefore runs synthetic
lean-Twin validation → real-data ablation → real-data explanation-stability →
cross-institution engagement robustness, and the controlling interpretation
is the honest, course- and regime-dependent finding stated in §13, not the
synthetic carry-forward.
