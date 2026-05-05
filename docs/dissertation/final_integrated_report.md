# Final Integrated Dissertation Report

## Abstract

This report integrates the completed experimental line of the Student Digital
Twin XAI research prototype into a single dissertation-facing narrative. The
project investigates whether a teacher-oriented student digital twin can
support early academic risk analytics through final grade prediction,
interpretable model behavior, and structured evidence for intervention
reasoning. The evidence base consists of five frozen experiments:
`exp_001_baseline`, `exp_002_twin_ablation`,
`exp_003_mastery_validation`, `exp_004_xai_on_lean_twin`, and
`exp_005_public_benchmark_oulad`.

The strongest conclusion is bounded. The full Digital Twin representation did
not outperform the stronger LMS baseline under the present setup and was not
carried forward. A lean Twin subset, `B_lms_plus_mastery`, improved final
grade prediction on the primary synthetic student-grouped split and improved
the LMS baseline across several early weekly snapshots. This subset was
validated with a clear redundancy caveat because `overall_mastery` is highly
correlated with cumulative LMS performance. The XAI phase showed that the
lean representation remains interpretable under permutation importance and
local perturbation explanations, but these explanations are model-behavior
descriptions rather than causal explanations. The OULAD public benchmark
provided mixed external evidence: the mastery analogue did not improve the
primary grouped OULAD split, but it did improve the secondary
temporal-forward split. The resulting contribution is therefore a disciplined
teacher-oriented lean Twin + XAI research prototype, not a proof of full
Digital Twin superiority or full external validity.

## 1. Introduction

Learning management systems record large amounts of educational activity, but
their common analytics functions are often descriptive rather than predictive
or explanatory. Teachers may see attendance, submissions, marks, and activity
logs, but still lack an integrated view of a student's evolving academic
state, the likely end-of-course outcome, and the model-behavior factors behind
that estimate. This repository explores that gap through a research prototype
based on Student Digital Twin and Explainable AI concepts.

The central object is the student as a dynamic digital twin. In the current
repository, this object is represented through weekly student-state snapshots
at the grain `1 row = 1 student x 1 week`. The prototype is not designed as a
full LMS, a student information system, or a production intervention platform.
It is an analytics and decision-support layer intended to help instructors
identify risk, understand model behavior, and reason about possible
interventions under explicitly documented assumptions.

The experimental line does not attempt to make the system look complete. It
tests the representation itself. The core research question is whether a
student Twin representation adds defensible value over a competent LMS-style
baseline, and whether any useful Twin representation remains interpretable
enough for teacher-facing explanation.

## 2. Research Problem and Motivation

The research problem can be stated as follows: how can a teacher-oriented
educational analytics prototype represent a student's evolving learning state
in a way that supports prediction and explanation without overclaiming causal
or external validity?

This problem matters because early-warning systems require more than a final
risk flag. A teacher needs to know why a student appears at risk, whether the
signal is coming from performance, activity, attendance, submission discipline,
or mastery state, and how stable the evidence is. A Digital Twin framing is
useful only if it captures dynamic student state rather than repackaging a
static dashboard. An XAI layer is useful only if it explains model behavior in
a form that preserves the distinction between predictive association and
causal mechanism.

The repository therefore treats three distinctions as methodologically
important:

- LMS baseline features versus engineered Twin features.
- Internal synthetic validation versus public external benchmark evidence.
- Model-behavior explanation versus causal explanation.

These distinctions shape the experiment sequence and the final dissertation
claim.

## 3. Methodological Design

The project follows a research-first design. The data model and schema
contracts provide the source of truth, followed by code implementation, tests,
and generated artifacts. The canonical data-model documentation is maintained
under `docs/data_model/`, and the active synthetic experiment schema is
`schema_v1.2` under `packages/contracts/schema_versions/`.

The primary supervised target in the synthetic experiments is `final_grade`.
The secondary context target is `passed`. The teacher-facing `risk_level`
label remains important for the digital twin and monitoring narrative, but it
is not used as a supervised training target in the experiment line. This
choice avoids training directly on a heuristic label generated from the same
synthetic assumptions the model is meant to evaluate.

The first four experiments use the refined synthetic dataset generated from
`generator_v1_3_refined.yaml`, a student-grouped primary split, a
temporal-forward secondary split where configured, seed `42`, and snapshot
weeks `4..10`. The model families are deliberately simple and defensible:
linear or Ridge-style regression, logistic regression, random forest, and
gradient boosting. The design emphasizes reproducibility, leakage-aware
splitting, train-only preprocessing, and explicit forbidden-column handling
over model complexity.

The fifth experiment uses a separate OULAD adapter rather than the synthetic
schema. It is not a new generator phase. It is a public benchmark stress test
that approximates the representation logic on OULAD module-presentation
`DDD` `2013J`.

## 4. Data and Schema Design

The synthetic data model separates the educational analytics pipeline into
three conceptual layers.

The first layer is raw LMS-like data: students, course structure, assignments,
attendance, submissions, activity, and final outcomes. The second layer is the
processed student twin snapshot table, where each row records one student's
state at one course week. The third layer consists of prediction and
explanation artifacts, including model metrics, feature importances, local
case explanations, and experiment metadata.

This separation is central to the Digital Twin framing. The snapshot table is
not simply a report. It is a time-aware student-state representation that can
be filtered by week and used for prediction before the end of the course. The
current synthetic scope is intentionally narrow: one course, a 10-week
structure, weekly topics, assignments, quizzes, attendance, activity, and
final result.

The OULAD benchmark uses a different data source and target semantics. It
builds weekly rows for one module-presentation, uses weeks `4..38`, and
derives `final_weighted_score` from OULAD assessment weights and student
assessment scores. This target is comparable to `final_grade` only at the
level of broad predictive task framing; it is not identical to the synthetic
target.

## 5. Experimental Design

The experiment sequence is dependency-driven. Each experiment answers a
specific question raised by the previous result.

`exp_001_baseline` asks whether the full Digital Twin feature set improves
over simpler baselines. `exp_002_twin_ablation` asks which Twin subgroup, if
any, adds value beyond the stronger LMS baseline. `exp_003_mastery_validation`
audits whether the selected mastery block is useful without being an
unacceptable proxy for the final outcome. `exp_004_xai_on_lean_twin` explains
the validated lean representation and checks whether model behavior collapses
onto a single feature. `exp_005_public_benchmark_oulad` stress-tests whether
the lean mastery-centered representation logic transfers to a public dataset.

This design avoids an unsupported move from full Twin construction directly to
explanation. The full representation was tested first, found unjustified, and
then decomposed. XAI was introduced only after the lean candidate had been
validated with caveats.

## 6. Experiment Sequence

### 6.1 exp_001_baseline

The first experiment compares `A_simple`, `B_lms`, and `C_twin` on the
synthetic dataset. On the primary student-grouped split, `B_lms` reached RMSE
`2.101`, while the full `C_twin` reached RMSE `2.149`. On the temporal-forward
split, `B_lms` reached RMSE `2.270`, while `C_twin` deteriorated to RMSE
`2.937`. The `passed` classification task saturated and reached F1 `1.000`
for all feature sets under both splits.

The research consequence is negative but useful: the full Twin representation
was not justified under the present setup. The appropriate next step was not
to claim full Twin superiority, but to decompose the Twin layer.

### 6.2 exp_002_twin_ablation

The second experiment compares the LMS baseline with individual Twin blocks:
trends, mastery, indices, temporal context, a compact trends-plus-mastery
combination, and the full Twin reference. On the primary split,
`B_lms_plus_mastery` reached RMSE `1.894`, improving over `B_lms` by `-0.206`.
The full `C_twin_full` reached RMSE `2.149`, remaining worse than `B_lms`.

The temporal-forward split is more cautious. `B_lms_plus_mastery` was nearly
level with `B_lms`, with delta `+0.006`. This means the mastery block was the
best internal candidate on the primary split, but its forward-transfer
advantage was not established.

### 6.3 exp_003_mastery_validation

The third experiment validates the mastery block before explanation. It
confirms the primary RMSE advantage of `B_lms_plus_mastery` and examines
weekly behavior, correlations, redundancy, drop-column effects, and temporal
lineage.

The candidate improves over the baseline at weeks `4`, `5`, `6`, `7`, and
`8`, with early-week improvements in weeks `4..6`. However, the validation
also finds that `overall_mastery` is highly redundant with LMS aggregates:
its Pearson correlation with `final_grade` is `0.984`, and its strongest LMS
correlate is `avg_assignment_score_to_date` at `|r| = 0.993`. Dropping
`overall_mastery` increases RMSE by `+0.228`.

The consequence is a carry-forward decision with caveat. Mastery is a
defensible lean Twin component in this controlled environment, but the
dissertation must not present it as an independent construct separate from
cumulative score behavior.

### 6.4 exp_004_xai_on_lean_twin

The fourth experiment applies XAI to the lean candidate using permutation
importance and one-feature median-replacement local perturbations. SHAP is not
used because it is not part of the current dependency contract.

The lean model reaches RMSE `1.894` compared with `2.101` for `B_lms`. The top
global feature is `activity_score_to_date`, with importance share `0.648`.
`overall_mastery` ranks second, with share `0.178`. The average local mastery
contribution share across the five representative cases is `0.194`. The
dominance audit outcome is `acceptable_with_caveat`.

The consequence is that the lean Twin remains teacher-meaningful under the
current XAI phase, but only as a model-behavior explanation. It is not causal,
not SHAP-based, and not free from dominance and redundancy caveats.

### 6.5 exp_005_public_benchmark_oulad

The fifth experiment maps the representation logic to OULAD. It compares
`B_lms_oulad` against `B_lms_plus_mastery_oulad` using the derived
`final_weighted_score` target and secondary `passed_observed` label.

On the primary student-grouped split, the mastery analogue is slightly worse:
RMSE `12.724` versus `12.658`, delta `+0.066`. On the temporal-forward split,
the direction reverses: RMSE `9.161` versus `9.566`, delta `-0.406`.
Classification performance is nearly level between the two feature sets.

The consequence is not external confirmation. OULAD complicates the internal
synthetic finding and keeps transfer unresolved. It supports the conclusion
that representation behavior is context-sensitive and should be re-tested on
additional real or institutional datasets.

## 7. Results and Interpretation

The completed experiments support a bounded interpretation.

First, the full Digital Twin did not outperform the LMS baseline. This matters
because it prevents the dissertation from making a broad claim about richer
Twin representations being automatically better. Under the present setup,
adding all engineered Twin features increased redundancy and did not improve
the central metric.

Second, the useful signal was concentrated in a lean mastery-centered subset.
The mastery block improved the primary synthetic regression comparison and
showed early-week gains, which supports the early-warning framing. However,
the advantage is conditional on the synthetic environment and is much less
robust under the temporal-forward synthetic split.

Third, the explanation phase was meaningful but limited. The lean model did
not collapse onto a single mastery feature, and the local cases are
interpretable as teacher-facing student-state examples. At the same time,
global importance is dominated by `activity_score_to_date`, and
`overall_mastery` remains redundant with cumulative assessment performance.

Fourth, external benchmark evidence is mixed. OULAD does not invalidate the
synthetic result, because the internal experiments remain valid under their
own controlled assumptions. It also does not validate the result externally,
because the primary OULAD split did not improve.

## 8. Explainability Phase

Explainability is part of the core research framing, but the present phase is
careful about what kind of explanation it provides. The methods used in
`exp_004_xai_on_lean_twin` describe model behavior. Permutation importance
measures how much held-out RMSE changes when a feature is permuted. Local
median replacement measures how a prediction changes when one feature is
replaced by the training median.

These methods help answer a teacher-facing interpretation question: which
observed student-state factors appear to drive the model's prediction? They do
not answer a causal intervention question: what would happen to the student's
outcome if the teacher changed one of those factors? The dissertation should
therefore use the explanation outputs as interpretive support, not as causal
evidence.

The five local cases - strong performer, at risk, improving trajectory,
declining trajectory, and borderline medium - show that mastery participates
in several student-state stories while one case remains mostly LMS behavior
and performance driven. This supports the claim that the explanation layer is
teacher-meaningful under the current setup, with caveats preserved.

## 9. External Benchmark Discussion

The OULAD benchmark is best understood as a transfer stress test. It uses a
public dataset with different assessment design, missingness, module timing,
and outcome semantics. The benchmark does not compare the custom synthetic
dataset against OULAD as if one dataset were better. It asks whether a similar
representation idea can be approximated on OULAD and whether the mastery-like
block improves the OULAD LMS baseline.

The answer is mixed. The primary grouped split does not improve, while the
secondary temporal-forward split does. The dissertation should preserve this
tension. A fair conclusion is that OULAD complicates the internal claim and
prevents full external-validation language. It also keeps the lean Twin
hypothesis plausible enough to justify future testing on additional public or
institutional datasets.

## 10. Limitations and Threats to Validity

The main development evidence is synthetic. Its relationships among
attendance, activity, submissions, mastery, and final grade reflect generator
assumptions. This limits external validity.

The `passed` target is saturated in the synthetic experiments. It cannot be
used to discriminate between representations, so regression on `final_grade`
is the meaningful target for representation choice.

The mastery block is useful but redundant. `overall_mastery` is close to
cumulative LMS performance and to `final_grade`. This is a structural caveat,
not a minor reporting detail.

The XAI methods are not causal and are not SHAP. Their outputs should be
described as directional model-behavior explanations.

The OULAD benchmark is public and valuable, but it is not institutional
validation. It uses one module-presentation and an adapted target. Its mixed
result means transfer remains unresolved.

Finally, intervention and scenario analysis remain future work. The current
experiment line supports prediction and model-behavior explanation; it does
not validate intervention recommendations.

## 11. Final Conclusions

The final conclusion is deliberately bounded. Under the present synthetic
experimental environment, the full Digital Twin representation was not
justified relative to the stronger LMS baseline. A compact mastery-centered
Twin subset, `B_lms_plus_mastery`, was the best internal candidate: it improved
final grade prediction on the primary synthetic split, improved the baseline
across several early weeks, and remained interpretable under the current XAI
phase. This candidate carries explicit caveats about redundancy,
feature-dominance, synthetic-data dependence, and non-causal explanation.

The OULAD benchmark adds an important external check. It does not confirm a
general mastery advantage, because the primary grouped OULAD split slightly
favors the LMS baseline. It does not invalidate the internal finding either,
because the temporal-forward OULAD split favors the mastery analogue and the
datasets have different structure and target semantics. The most defensible
dissertation statement is therefore that the project demonstrates a disciplined
method for constructing, testing, validating, and explaining a lean Student
Digital Twin representation for teacher-oriented academic analytics, while
leaving external validation and causal intervention reasoning as future work.

## 12. Canonical Evidence References

- [exp_001_baseline](../experiments/exp_001_baseline.md)
- [exp_002_twin_ablation](../experiments/exp_002_twin_ablation.md)
- [exp_003_mastery_validation](../experiments/exp_003_mastery_validation.md)
- [exp_004_xai_on_lean_twin](../experiments/exp_004_xai_on_lean_twin.md)
- [exp_005_public_benchmark_oulad](../experiments/exp_005_public_benchmark_oulad.md)
- [Experiment progression summary](experiment_progression_summary.md)
- [Experimental results synthesis](experimental_results_synthesis.md)
- [Limitations and threats to validity](limitations_and_threats_to_validity.md)
- [Final research conclusions](final_research_conclusions.md)
