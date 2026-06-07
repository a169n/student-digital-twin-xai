# Defense Q&A

## Why not use `risk_level` as the supervised target?

`risk_level` is a teacher-facing heuristic label in the current data model. In
the synthetic dataset, training directly on it would teach the model to
replicate a generated rule rather than learn from an educational outcome.
Using `final_grade` as the primary target is more defensible because it is the
end-of-course outcome the risk framing is meant to anticipate. `passed` is kept
as secondary context, but it saturates in the synthetic experiments and cannot
discriminate between feature sets.

## Why use synthetic data?

The project begins with synthetic data because the repository is a research
prototype without an approved institutional cohort. Synthetic data allows the
schema, snapshot grain, leakage controls, feature hierarchy, and experiment
governance to be developed safely and reproducibly. The dissertation should
not claim that synthetic evidence provides full external validity. It provides
controlled internal evidence that must be re-tested on real institutional data.

## Why did the full Twin fail?

The full Twin did not fail as a software object; it failed as a predictive
representation under the current experimental setup. In `exp_001`, `C_twin`
did not improve over the stronger LMS baseline and deteriorated on the
temporal-forward split. The likely explanation is redundancy: adding all trend,
mastery, index, and temporal features wholesale introduced overlapping signals
without reliable marginal value. This is why the next experiment decomposed
the Twin layer instead of defending the full set.

## Why is the project still legitimately about Digital Twin + XAI?

A Digital Twin is not defined by the largest possible feature set. The project
still models students as time-aware weekly states and tests which student-state
components are defensible. The outcome of the experiment line is a lean Twin
representation, not no Twin representation. XAI remains central because the
validated lean representation is explained through global and local
model-behavior methods for teacher interpretation.

## Why was `B_lms_plus_mastery` carried forward?

`B_lms_plus_mastery` was the only single Twin block that produced a substantive
primary-split improvement over `B_lms` in the ablation experiment. It reduced
RMSE from `2.101` to `1.894` and then passed a validation phase showing
early-week improvements and no direct future-outcome leakage in the feature
lineage. It was carried forward with an explicit caveat: `overall_mastery` is
highly redundant with `avg_assignment_score_to_date`.

## Why was SHAP not used?

SHAP was not part of the current project dependency contract for these
experiments. The XAI phase therefore used documented sklearn-compatible
methods: held-out permutation importance and one-feature median-replacement
local perturbations. The dissertation should describe these as directional
model-behavior explanations, not as SHAP values, Shapley decompositions, or
causal explanations.

## What did the OULAD benchmark show?

OULAD showed mixed transfer evidence. On the primary student-grouped split,
the mastery analogue was slightly worse than the OULAD LMS baseline
(`+0.066` RMSE). On the secondary temporal-forward split, it improved RMSE by
`-0.406`. This complicates the synthetic carry-forward claim. It does not
confirm full external validity, and it does not invalidate the controlled
synthetic finding.

## What are the current limitations?

The main limitations are synthetic-data dependence, no local institutional
validation, saturation of the synthetic `passed` target, redundancy of
`overall_mastery`, non-causal XAI methods, absence of SHAP, and mixed OULAD
transfer evidence. Intervention and scenario analysis remain future work and
should not be presented as validated outcomes of the current experiment line.

## What is the most defensible final claim?

The defensible claim is that the repository implements a disciplined
teacher-oriented Student Digital Twin + XAI research prototype, identifies a
lean mastery-centered Twin subset as the best internal candidate under the
current synthetic setup, validates and explains it with caveats, and records a
mixed OULAD benchmark that leaves external transfer unresolved.

## Isn't your synthetic `final_grade` just a deterministic function of your own features, so the high accuracy is meaningless?

Yes, and we state this explicitly. `final_grade` is a closed-form weighted mean
of assignment, quiz, attendance, and on-time behavior with no noise term
(`services/ml/src/generator/final_results.py:74-84`); week-10 reconstruction max
absolute error is 0.008. That is precisely why we do not base any empirical
learning claim on synthetic accuracy. Synthetic data is used only as a controlled
faithfulness probe with known ground truth (`exp_008`). The empirical claims rest
on real OULAD data, where the same pipeline yields F1 0.86-0.89 (not 1.000),
which is itself direct evidence that the perfect synthetic scores were a
generator artifact.

## You claim mastery features help - but does that survive a fair comparison?

It is split- and model-dependent. The `-0.206` win holds for gradient boosting
on the student-grouped split only; a preliminary fixed-model re-analysis (to be
confirmed by the fixed-model ablation table produced in the public-data phase)
indicates mastery is approximately `+0.41` worse on the temporal-forward split,
and that only `B_lms_plus_indices` improves on both splits. We report fixed-model
tables for this reason and frame the
real-data finding as a mixed/conditional result, not "the twin wins."
