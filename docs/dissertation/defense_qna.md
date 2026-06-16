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

The early two-set OULAD probe (`exp_005`) showed mixed transfer evidence: on the
primary student-grouped split the mastery analogue was slightly worse than the
OULAD LMS baseline (`+0.066` RMSE), while on the secondary temporal-forward split
it improved RMSE by `-0.406`. That `exp_005` "complicates" reading is **superseded**
by the full nested ablations: on DDD 2013J (`exp_006`) the verdict is mixed-to-null
(no Twin block beats `B_lms_oulad` by more than `1.0` RMSE on either split), and on
BBB 2013J (`exp_009`) it is heterogeneous (mastery crosses the threshold on the
temporal-forward split, `-1.026` RMSE, but is null on the student-grouped split).
The current OULAD verdict is therefore heterogeneous-DDD-null/BBB-partial, not
"complicates": engineered Twin value is course- and split-dependent. It does not
confirm full external validity, and it does not invalidate the controlled synthetic
finding.

## What are the current limitations?

The main limitations are synthetic-data dependence, no local institutional
validation, saturation of the synthetic `passed` target, redundancy of
`overall_mastery`, non-causal XAI methods, absence of SHAP, and heterogeneous
OULAD transfer evidence (DDD-null, BBB-partial). Intervention and scenario
analysis remain future work and should not be presented as validated outcomes of
the current experiment line.

## What is the most defensible final claim?

The defensible claim is that the repository implements a disciplined
teacher-oriented Student Digital Twin + XAI research prototype, identifies a
lean mastery-centered Twin subset as the best internal candidate under the
current synthetic setup, validates and explains it with caveats, and records a
heterogeneous real-data result across three institutions — DDD-null and
BBB-partial under the full ablation, with importance drivers that transfer only
partially (mean Kendall `tau` ≈ `0.56`). The honest external verdict is that
feature-richness does not robustly help, not that transfer is "unresolved".

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

It is split- and model-dependent. The `-0.206` synthetic win holds for gradient
boosting on the student-grouped split only. The fixed-model ablation tables from
the public-data phase confirm the real-data picture is mixed/conditional, not
"the twin wins": on DDD 2013J (`exp_006`) no Twin block beats `B_lms_oulad` by
more than `1.0` RMSE on either split (mixed-to-null), and on BBB 2013J (`exp_009`)
mastery helps only on the temporal-forward split (`-1.026` RMSE) and is null on
the student-grouped split. We report fixed-model tables for exactly this reason
and frame the real-data finding as a heterogeneous, split-dependent result, not
"the twin wins."

## Isn't your synthetic accuracy meaningless given the circular target?

Yes, and that is exactly the point of the chapter, not a flaw we are hiding.
Synthetic `final_grade` is a deterministic, noise-free closed-form weighted mean
of the same behaviors the features re-aggregate
(`services/ml/src/generator/final_results.py:74-84`), with week-10 reconstruction
error `0.008` and correlation `1.000000`. So the synthetic `R²≈0.99` and `passed`
F1 `1.000` are algebraic artifacts, not learnable signal, and no empirical
learning claim rests on them. The evidence is the real OULAD data, where the same
pipeline yields classification F1 `0.83`–`0.93` and never `1.000`. That gap — a
perfect synthetic score collapsing to a genuinely predictive but imperfect real
score — is itself the demonstration that the synthetic "mastery advantage" was
manufactured by the circular target. We use the synthetic case only as a
controlled faithfulness probe with known ground truth (`exp_008`), not as a
performance result.

## Does the Twin actually help on real data?

It is heterogeneous, not uniform — that is the honest two-cohort finding, and we
deliberately treat OULAD as two distinct ablations rather than one. On DDD 2013J
(`exp_006`, `67830` snapshots, `1938` students), under a fixed-model gradient
boosting comparison, no Twin block beats the strong `B_lms_oulad` baseline by more
than `1.0` RMSE on either split: the best move is mastery on temporal-forward
(`9.561` → `9.180`, `-0.381`) but `+0.061` worse on the student-grouped split —
essentially null. On BBB 2013J (`exp_009`, `80532` snapshots, `2237` students,
richer dated-assessment structure), the mastery block does cross that threshold on
temporal-forward, `-1.026` RMSE (`6.311` → `5.284`), with `C_twin_oulad` at
`-0.765`; but on the student-grouped split every block stays within `0.087`
(null, as on DDD), and the trend and index blocks are null on both splits of both
courses. So engineered Twin value is course- and split-dependent: it can help when
the assessment structure is rich and the evaluation is forward-in-time, but it
does not generalize across splits, blocks, or courses. This is model-behavior on
two OULAD cohorts, not a causal or universal claim.

## Are the explanations stable across evaluation conditions?

No — they are regime-sensitive, and we report that as a finding rather than
suppress it. Within a single course (`exp_007` on DDD), the permutation-importance
rankings differ between the student-grouped and temporal-forward splits: Kendall
`tau` is `0.79` / `0.68` / `0.55` for `B_lms_oulad` /
`B_lms_plus_mastery_oulad` / `C_twin_oulad` (mean `0.67`, none reaching `0.90`),
even though top-5 membership can stay stable (Jaccard up to `1.0`) while the order
reorders. Across courses (`exp_010`, DDD vs BBB) the rankings are even less stable
— cross-cohort Kendall `tau` `0.32`–`0.61` (mean `0.52`), below the within-cohort
`0.55`–`0.79` — though the topology is shared (`overall_mastery_proxy`,
submission discipline, and `is_unregistered_by_week` dominate both courses). The
model's "why" is therefore not invariant to the evaluation scenario or the course;
this extends explanation-stability work (Tiukhova et al., 2024) to the transfer
setting and is a directional model-behavior result, not a causal one.

## Does anything hold beyond a single institution?

We checked a second institution and then a matched three-institution comparison,
and the consistent answer is that adding feature richness does not robustly help.
KU Leuven (`exp_011`, Tiukhova et al. 2026; `1495` students) has no scored
assessments and no continuous grade, so the mastery ablation literally cannot be
built there — the research question itself is institution-dependent. On its
engagement-only classification of `PASSED`, engagement predicts passing only
modestly (F1 `0.75`–`0.76`, ROC-AUC `0.65`–`0.72`), and a richer engagement
representation does not beat a minimal two-feature one (fixed-model F1 delta
`-0.015` temporal / `+0.000` grouped). `exp_012` then folds DDD, BBB, and KU
Leuven into one matched, engagement-only `PASSED` comparison: a two-feature
baseline (cumulative clicks + cumulative active-days) is hard to beat (`B − A` F1
positive only on the student_group split — DDD `+0.072`, BBB `+0.039`, KU `+0.000`
— and flat-to-negative on temporal-forward), and the importance drivers transfer
only partially (mean Kendall `tau` ≈ `0.56`, verdict
`drivers_partly_institution_specific`, most stable KU↔BBB `0.71`, least KU↔DDD
`0.24`). This is a robustness statement about gradient-boosting behavior, not an
accuracy win or a like-for-like institutional replication.

## The literature benchmark (Algorithms 2025) achieves ROC-AUC 0.993 and you get 0.953 — isn't your system just weaker?

Yes on classification accuracy, and we say so openly. The comparison is included
in §10 of the final report and is not hidden. Three caveats limit how much weight
to place on the gap. First, the published target is binary dropout, not the
weighted assessment score regression used here — the targets are not identical.
Second, the exact cohort and split construction in that paper are not fully
specified; a non-student-grouped split on OULAD weekly snapshots can inflate
ROC-AUC substantially, because the same student's rows appear in both train and
test. Third, that paper does not provide a teacher interface or document how
explanations are communicated to non-ML users.

The more important answer is that accuracy superiority is not the claimed
contribution. The contribution is: (i) a complete, open, end-to-end prototype
from raw OULAD data to per-student teacher-facing explanations; (ii) an honest
negative result — adding mastery features over a strong LMS baseline did not
help (Δ RMSE +0.066, Δ F1 −0.002 on the student-grouped split) — which most
published papers in this area omit; (iii) an explanation-stability analysis with
documented regime-sensitivity. A master's dissertation does not need to set a new
benchmark; it needs to make a defensible methodological contribution.

## Why does the system have a teacher UI if the model accuracy is not better than a simple baseline?

The UI is not justified by accuracy superiority — it is justified by the absence
of comparable open, teacher-facing academic tools. Published papers in this space
release model metrics, not systems. Commercial platforms (EAB Navigate, Civitas
Learning) have teacher dashboards but are closed, undocumented as to their models,
and do not communicate explanation limitations. The interface built here provides
a weekly trajectory view, per-student XAI panel, and — critically — an explicit
limitation notice telling teachers that the factors shown describe model behaviour,
not causes, and should not be the sole basis for intervention. No published
academic paper in the literature review provides an equivalent. That design
decision directly addresses the third research gap identified in the literature:
that existing XAI papers add explanations without addressing how teachers may
misinterpret them.

## Why add an XAI disclaimer to the UI rather than just describing the limitation in the dissertation?

A dissertation section that notes "our explanations are not causal" while the UI
says "this factor is driving the student's outcome" is internally inconsistent.
The disclaimer in the UI (`XaiDisclaimer` component in `explanation-panel.tsx`)
makes the same three points as the methodology: the factors describe model
behaviour, not causes; they should not be the sole basis for intervention; and
their ranking can shift across time periods and cohorts. This consistency between
the written claim and the deployed interface is itself part of the contribution —
it is what distinguishes "system contribution" from "model contribution plus
optional visualisation". The component is minimal (12 lines), non-intrusive, and
directly grounded in the regime-sensitivity finding of `exp_007`.
