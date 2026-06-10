# Methodological Justification of Model and Experiment Design

## 1. Overview

The Student Digital Twin XAI prototype investigates whether a Digital Twin
representation of a learner improves the prediction of end-of-course academic
outcomes beyond what a competent LMS analytics layer already provides, and
whether the resulting model behavior remains interpretable enough to support
teacher-oriented decision-making. The methodological design developed across
the experiment sequence is intentionally conservative: simple, well-understood
baselines are established first; richer representations are introduced under
explicit hypotheses; and the explanation layer is added only after a
predictively useful and structurally credible representation has been
identified. This document formalizes the rationale behind the chosen models,
targets, feature sets, splits, evaluation metrics, the use of a synthetic
but schema-controlled dataset, and the later OULAD public-benchmark stress
test.

The argument throughout is bounded by the current research setting. The
experiments operate on a synthetic but structurally constrained dataset
generated under schema `v1.2` using the refined generator configuration
`generator_v1_3_refined.yaml`, with the snapshot grain
`1 row = 1 student × 1 week`. All claims below should therefore be read as
statements about internal methodological validity within this controlled
environment, not as statements about real-institutional generalization.

A further methodological qualification governs the synthetic numbers
specifically. The synthetic `final_grade` is a deterministic, noise-free
closed-form weighted mean of the same behaviors that the features re-aggregate
(`services/ml/src/generator/final_results.py:74-84`; week-10 reconstruction
error `0.008`, correlation `1.000000`). The high synthetic regression fit
(R²≈`0.99`) and the saturated `passed` classification (F1=`1.000`) are therefore
**algebraic artifacts of a circular target**, not learnable signal. This is why
the synthetic experiments are treated strictly as a methods-development and
internal-validity substrate, and why the real-data experiments
(`exp_005`–`exp_012`) carry the empirical weight. The "Digital Twin" here is a
lean, time-aware weekly state representation — not a simulation or
counterfactual engine.

`exp_005_public_benchmark_oulad` adds a separate external benchmark using
OULAD `DDD` `2013J`, but it is treated as transfer stress rather than as full
external validation. The later real-data experiments extend this benchmark into
two distinct OULAD cohorts (`DDD` `2013J` and `BBB` `2013J`, each with its own
full A/B/C ablation) and a second institution (KU Leuven `1819`). These must
never be collapsed into one undifferentiated "OULAD" result, because the two
cohorts behave differently.

## 2. Justification of the Model Stack

### 2.1 Why standard baseline ML models were used

Student-performance prediction in LMS-like environments is a canonical
**tabular supervised-learning problem**. The inputs are scalar summaries of
assessment performance, attendance, engagement, submission discipline, and
course-time context; the outputs are end-of-course grades or pass/fail
decisions. Under such conditions, the methodologically appropriate starting
point is a small, well-understood family of classical estimators rather than
deep architectures, because (i) the feature space is structured rather than
high-dimensional and unstructured, (ii) interpretability is a project
requirement rather than an optional concern, and (iii) classical estimators
expose well-defined inductive biases that allow the comparative behavior of
different feature sets to be attributed to representation rather than to
opaque architectural effects.

The dissertation framing of the project, captured in
`docs/research/model_experiment_design.md`, is consistent with this position
and explicitly motivates a baseline-first evaluation regime under leakage-aware
splitting before any explanation layer is introduced.

### 2.2 Why these exact estimators

Four estimator families are used across the experiments. They are deliberately
chosen to span a controlled interpretability–prediction spectrum and to remain
defensible without elaborate hyperparameter optimization.

| Estimator | Methodological function |
| --- | --- |
| Logistic Regression | Transparent binary-classification reference. Establishes whether the classification task is intrinsically easy before nonlinear models are introduced. |
| Ridge / linear baseline | Transparent regression reference under collinear engineered features. The regression baseline is realized as Ridge regression rather than unpenalized OLS, which is methodologically preferable when cumulative averages, mastery proxies, trends, and composite indices are structurally correlated. |
| Random Forest | Bagged, decorrelated tree ensemble. Provides a strong nonlinear, interaction-capable baseline with limited preprocessing burden, suitable as a default tabular reference. |
| Gradient Boosting | Stage-wise additive tree ensemble. Provides the strongest classical baseline for medium-sized tabular tasks and serves as the reference model for the explanation phase. |

This stack is small enough to be reasoned about exhaustively, broad enough to
expose where additional engineered structure either helps or fails to help,
and aligned with the implementation under
`services/ml/src/experiments/`. The interpretability anchor is provided by the
linear/logistic family; the predictive ceiling is approximated by the ensemble
family. No deeper or specialized estimator is introduced because the central
research question concerns the **representation** rather than the predictor.

## 3. Justification of Target Choices

### 3.1 Why `final_grade` is the primary target

`final_grade` is treated as the primary supervised target across the first
four synthetic experiments. The motivation is informational. A continuous numeric grade
preserves both rank order and distance between students; a thresholded
pass/fail label collapses those distinctions into a single boundary decision.
Within a teacher-oriented analytics context, the magnitude of distance from
adequacy is itself a meaningful signal: it differentiates a student who is
marginally below threshold from one who is far below it, and it differentiates
high-performing students from one another. Predicting `final_grade` therefore
provides the richer benchmark for evaluating whether richer representations
add genuine information.

The data-model contract in `docs/data_model/03_targets_and_labels.md` reflects
this decision explicitly, designating `final_grade` as the primary regression
target while noting that it must not be used as a snapshot-time feature and
must be joined onto weekly snapshots only after temporally clean snapshot
construction.

### 3.2 Why `passed` is treated as a secondary context target

`passed` is reported throughout the experiment sequence, but only as
secondary context. The decisive observation, documented across the synthetic
experiments, is that the binary task is essentially saturated on the current
synthetic dataset: best F1 reaches `1.000` for every feature set under both
splits in `exp_001_baseline` and `exp_002_twin_ablation`. A target that
approaches ceiling performance under multiple feature sets and models cannot
discriminate between representations and therefore cannot serve as the central
benchmark for evaluating whether the Twin layer adds value. `passed` remains
useful for operational reporting and as a reference to early-warning framing,
but methodologically it is too coarse and currently too easy to drive
representation choice.

### 3.3 Why `risk_level` is intentionally excluded as a supervised target

`risk_level` is excluded from supervised training as a matter of methodological
necessity rather than convenience. It is a teacher-facing categorical concern
label derived from the continuous heuristic `risk_score`, which is itself a
monotonic combination of the same weekly twin features that serve as model
inputs. Training a model against `risk_level` would therefore amount to
teaching the predictor to reproduce a hand-designed rule system over its own
inputs rather than to predict an external empirical outcome. The construction
and consequences of that decision are documented under
`docs/data_model/03_targets_and_labels.md`, which explicitly classifies
`risk_level` as a heuristic teacher-facing label rather than ML ground truth in
schema `v1.2`. The exclusion is enforced operationally by the experiment
runners through forbidden-column lists.

The combined target hierarchy — `final_grade` as the primary supervised
outcome, `passed` as secondary context, and `risk_level` as a teacher-facing
heuristic that remains outside the supervised label space — is therefore
internally coherent and is preserved consistently across the experiment line.

## 4. Justification of Feature-Set Comparison

### 4.1 Why feature-set comparison was the chosen evaluation lens

The central research question of the project is not whether a single
high-capacity model can fit the synthetic data; under the current generator,
multiple models can do so. The central question is whether the engineered
**Digital Twin representation** carries information that is not already
present in a strong LMS analytics layer, and which subcomponents of the Twin
representation, if any, are responsible for that information. This is a
representation question, not a model-tuning question. Feature-set comparison
is the methodologically appropriate lens for representation questions because
it isolates the contribution of representation by holding the model family,
split, target, and metric constant.

### 4.2 Why the progression `A_simple` → `B_lms` → `C_twin` was appropriate

The feature hierarchy used in `exp_001_baseline` is nested and
hypothesis-driven. `A_simple` captures a minimal academic baseline using score
averages and attendance; `B_lms` adds activity, time on platform, submission
discipline, and explicit missingness indicators that approximate a realistic
LMS analytics layer; `C_twin` adds trend features, mastery proxies, composite
indices, and limited course-time context to instantiate the full Digital Twin
hypothesis. The hierarchy mirrors the canonical decomposition used in the
educational-analytics literature into academic performance, behavioral signals
derived from online systems, and engineered state representations, and it
makes the central research question concrete: does the Twin representation add
value beyond what a competent LMS analytics baseline already captures?

### 4.3 Why a Twin subgroup ablation was needed

`exp_001_baseline` revealed that the full `C_twin` representation did not
reliably outperform `B_lms`: under the primary student-grouped split,
`C_twin` produced a slightly higher RMSE than `B_lms` (`2.149` vs `2.101`),
and under the temporal-forward split the gap widened in favor of `B_lms`
(`2.270` vs `2.937`). The methodologically correct response to this finding
is not to discard the Twin representation wholesale, nor to re-tune models, but
to test whether semantically coherent **subgroups** of the Twin layer add
marginal value to the LMS baseline.

`exp_002_twin_ablation` therefore evaluates `B_lms` plus single-block
extensions — trends, mastery, composite indices, temporal context — and one
compact combination, against `C_twin_full` as the upper-bound reference. This
decomposition is consistent with the standard role of ablation in machine
learning: to estimate the marginal contribution of components inside a larger
system. In project terms, it converts the negative baseline finding into a
structured representation diagnostic rather than an inconclusive failure.

### 4.4 Why `B_lms_plus_mastery` emerged as a lean Twin candidate

Among the ablation sets, `B_lms_plus_mastery` produced the lowest RMSE on the
primary split (`1.894`, a delta of `-0.206` versus `B_lms`) and the smallest
deviation from the LMS baseline under the stricter temporal-forward split.
Under the same primary split, the full `C_twin_full` representation produced
a higher RMSE than the LMS baseline. The mastery block therefore concentrates
the predictive signal that the wider Twin representation otherwise dilutes,
and it does so with only two additional features. On these grounds — and on
these grounds alone within the current synthetic environment —
`B_lms_plus_mastery` was carried forward as the lean Twin candidate.

`exp_003_mastery_validation` then subjects this carry-forward to four
diagnostic checks (target-correlation analysis, redundancy with LMS features,
drop-column re-training, and permutation importance) and to a week-aware
protocol that examines whether the mastery improvement appears in early-week
cutoffs. The candidate retains its predictive advantage and improves on the
baseline at weeks 4–8, supporting the early-warning framing that the project
is ultimately designed to enable. The diagnostics also flag a known caveat —
`overall_mastery` is highly redundant with `avg_assignment_score_to_date`
(|r| = 0.993) and dominates the drop-column test — which is preserved as an
explicit caveat rather than smoothed over.

## 5. Justification of Splitting Strategy

### 5.1 Why row-random splitting is rejected

The grain of the modeling unit is `1 student × 1 week`. Under that grain, a
single learner contributes many rows to the dataset, and later rows are
temporally downstream of earlier rows for the same learner. A row-random split
therefore violates two assumptions simultaneously: the rows are not
identically distributed across the train/test boundary because the same
learner appears on both sides, and they are not temporally independent
because future weeks of a held-in student carry information that should not be
available at prediction time. Under those conditions, row-random validation
systematically underestimates generalization error and inflates apparent
performance. Row-random splitting is therefore explicitly rejected by the
experimental design.

### 5.2 Why student-grouped splitting is the primary split

The primary split across the synthetic experiments is grouped by `student_id` with
a held-out fraction of `0.25` and a fixed seed of `42`. This split prevents
the same learner from appearing in both the training and test partitions and
therefore yields a defensible estimate of generalization to **new students**.
Student-grouped splitting is the minimum requirement for any fair evaluation
in this setting; it is the regime under which the headline RMSE comparisons
between feature sets are reported.

The OULAD benchmark keeps the same principle by grouping on OULAD
`id_student`, while using the OULAD-derived `final_weighted_score` target
instead of the synthetic `final_grade`.

### 5.3 Why temporal-forward splitting is used as a secondary split

The secondary split, used in `exp_001_baseline`, `exp_002_twin_ablation`, and
`exp_003_mastery_validation`, is temporal-forward with held-out students.
Under this regime, training is restricted to early-course weeks while testing
is performed on later-course weeks for students who do not appear in
training. This composite split addresses two distinct generalization
questions simultaneously: it avoids training on a learner's own future
(temporal leakage) and on the learner's own identity (identity leakage). It
is therefore the more demanding regime and is appropriate for assessing the
plausibility of an early-warning use case, where the operational expectation
is that the model will be applied to unseen learners earlier than the latest
data it was trained on.

The asymmetry between the two splits is itself diagnostic. A representation
that performs well under the primary split but degrades under the secondary
split is exploiting structure that is stable across a learner's snapshots but
less transferable to a forward-looking scenario. In the experiment line, the
full Twin set in `exp_001_baseline` exhibits exactly this pattern, which
strengthens the case for ablation rather than for further full-Twin tuning.

## 6. Justification of Evaluation Metrics

The evaluation protocol is task-aligned and multi-metric rather than
single-score. For regression — the primary modeling task — the project reports
**MAE**, **RMSE**, and **R²**. MAE summarizes average absolute deviation in
target units and is robust to outliers; RMSE penalizes larger misses more
heavily while remaining in the units of the target and is therefore the
primary headline metric in cross-feature-set comparisons; R² reports the
proportion of variance explained and provides a normalized reference that is
comparable across splits. Reporting all three keeps the comparison balanced
between robustness, sensitivity to large errors, and overall fit.

For classification — the secondary context task — the project reports
**accuracy**, **precision**, **recall**, **F1**, and **ROC-AUC**. Accuracy is
retained as a descriptive baseline; precision, recall, and F1 capture the
operational threshold-dependent behavior of the classifier; ROC-AUC provides
a threshold-independent ranking measure. This combination is conventional and
allows the saturation of `passed` on the current dataset to be reported
without ambiguity: when both F1 and ROC-AUC reach `1.000` across feature sets
and splits, the binary task offers no representational discrimination, which
is documented honestly rather than overlooked.

The metrics are reported per feature set, per model, and per split rather than
as global winners, in line with reproducibility-oriented reporting norms. The
multi-metric, multi-split presentation is what allows the asymmetric behavior
of the full Twin representation across primary and secondary splits to be
read as a substantive finding rather than an artifact.

## 7. Justification of the Synthetic but Schema-Controlled Dataset

The decision to operate on a synthetic dataset is bounded by the research
phase and stated explicitly. The argument has three parts.

First, the project is positioned as a research prototype rather than as a
deployment study. Its objective is to investigate **methodological viability**
of a Digital Twin + XAI approach to teacher-oriented academic risk analytics
under controlled conditions, not to validate the approach against a specific
institution. For methodological investigation, a synthetic but structurally
realistic dataset is a defensible substrate because it permits explicit
control over schema, leakage, missingness handling, and the relationships
among educational signals.

Second, the dataset is **schema-controlled** rather than ad hoc. It is
generated against the versioned contract `schema_v1.2`, validated against
that contract, and audited for realism through the reports in
`data/artifacts/reports/`. The data-model documentation under
`docs/data_model/` formalizes scope, entities, dictionary, targets, features,
and assumptions. This means the dataset is reproducible, auditable, and
versioned in the same way that the experiments themselves are, rather than
opportunistically assembled.

Third, the synthetic setting is an enabler of **internal validity**, not a
substitute for external validity. Because the generator parameters are
explicit, the experiments can isolate questions that would be difficult to
isolate on institutional data — for example, whether the Twin layer's
predictive value is concentrated in a single block, or whether mastery is
informationally distinct from cumulative score averages. The corresponding
limitation, that the experiments cannot establish generalization to real
institutional data, is acknowledged consistently across the experiment writeups
and is discussed in detail in
[limitations_and_threats_to_validity.md](limitations_and_threats_to_validity.md).
The OULAD benchmark partially addresses transfer plausibility, but because it
uses a public dataset and a derived target, it remains a transfer stress test
rather than institutional validation — even after it is extended to two OULAD
cohorts and a second institution (Section 8). A further methodological caveat
applies to OULAD specifically: the derived `final_weighted_score` target is
partly assessment-driven, so the assessment-score features are partially
co-circular with it. The real-data analysis therefore deliberately leans on the
clickstream signals and on the classification task, where the target is
genuinely external to the features.

## 8. Justification of the Explanation Phase and the Real-Data Extension

The synthetic experiment line (Sections 4–6) establishes a lean Twin candidate
under internal-validity conditions. Because that candidate's apparent advantage
rests on a circular target (Section 1), the methodological burden then shifts
to two things: explaining model behavior in a disciplined, non-causal way, and
re-running the entire protocol on real, non-circular data. This section
justifies the design of the explanation phase (`exp_004`, `exp_007`, `exp_010`)
and of the real-data extension (`exp_005`, `exp_006`, `exp_009`, `exp_011`,
`exp_012`), including the controlled faithfulness probe (`exp_008`).

### 8.1 Why the explanation phase uses permutation and local perturbation, not SHAP

The explanation phase is deliberately built from held-out permutation
importance, model-native importance, and one-feature local perturbation rather
than from SHAP or other attribution libraries. The rationale is a
dependency-contract choice: permutation and single-feature perturbation are
model-agnostic, require no additional approximation machinery, and produce
**directional model-behavior** statements that are easy to bound and reproduce
under a frozen pipeline. On the synthetic candidate, `exp_004` reports global
permutation importance with median-replacement local perturbation over a
representative case set (15 repeats), and the resulting dominance audit is
recorded as `acceptable_with_caveat` (average local mastery share `0.194`, below
the `0.60` concentration threshold). Throughout, the explanations are framed as
statements about how the fitted model uses its inputs, **not** as causal
mechanism — a guardrail that is preserved verbatim into the real-data XAI runs.

### 8.2 Why importance is reported as regime-sensitive, and why stability is measured

A single ranked importance table, reported once, would invite the reader to
treat "the model's reasons" as a fixed property of the representation. The
real-data XAI runs (`exp_007` on DDD, `exp_010` on BBB) show that this would be
methodologically misleading: importance rankings are **regime-sensitive**. The
same feature set produces materially different orderings depending on the split
and the course. This finding is what justifies adding an explicit
**explanation-stability methodology** rather than reporting importance once.

Stability is quantified with two complementary, library-free metrics computed
over the importance vectors of two regimes: **Kendall τ** (tau-b, over the
shared features, robust to ties) for full-ordering agreement, and **Jaccard
top-k** overlap for agreement on the leading drivers. The metrics are applied at
two scopes. *Cross-split* (within-course) stability compares the
student-grouped and temporal-forward importance orderings inside one course;
across DDD feature sets this yields τ `0.55`–`0.79` (mean `0.67`, none reaching
`0.90`) with Jaccard top-5 `0.67`–`1.00`. *Cross-cohort* stability compares the
same feature set across the two OULAD courses (DDD vs BBB); this is lower, τ
`0.32`–`0.61` (mean `0.52`), confirming that the "why" is partly
course-specific. Reporting these explicitly is a positive methodological result
that sits on top of the predictive finding: it tells a teacher-facing audience
that an explanation valid in one regime should not be assumed valid in another.

### 8.3 Why the real-data ablation is a full nested A/B/C ablation with fixed-model reporting

`exp_005` was a two-set transfer test (`B_lms_oulad` vs
`B_lms_plus_mastery_oulad`). To put the synthetic representation question on the
same footing as the synthetic ablation, `exp_006` (DDD) and `exp_009` (BBB)
re-run the **full nested A/B/C ablation** on OULAD: `A_simple_oulad` →
`B_lms_oulad` → single Twin-block extensions → `C_twin_oulad`. This requires an
**OULAD feature-mapping** layer — adapter analogues of the synthetic feature
blocks (an assessment/mastery proxy, submission-discipline and missingness
analogues, VLE clickstream activity, registration-status handles, and
course-time context) — so that "the mastery block" or "the index block" means
the same *kind* of thing on real data as it did on synthetic data, even though
the underlying columns differ.

The decisive methodological choice in `exp_006`/`exp_009` is **fixed-model
reporting**. In the synthetic ablation, allowing the best estimator per cell to
be selected can flatter a candidate feature set: a block can appear to "win"
simply because, in its cell, a different model happened to be the per-cell best
(a model-flip artifact). To neutralize this, the OULAD ablation fixes a single
estimator (Gradient Boosting) across every feature set and split, so any
remaining RMSE difference is attributable to representation alone. Wherever a
best-per-cell number is shown, it is paired with the fixed-model number, and the
fixed-model number is the one that carries the argument — the model-flip win is
never headlined. Under fixed-model reporting the result is honest and
**heterogeneous across the two cohorts**: on DDD (`exp_006`; `67830` snapshots,
`1938` students) no Twin block beats `B_lms_oulad` by more than `1.0` RMSE on
either split (mixed-to-null); on BBB (`exp_009`; `80532` snapshots, `2237`
students) the mastery block does improve the temporal-forward split by `-1.026`
RMSE — crossing the `1.0` threshold DDD never did — but not the student-grouped
split, and the trend and index blocks remain null on both courses. The
classification target stays genuinely predictive throughout (best-model F1
`0.83`–`0.93`, never `1.000`), which is the methodological point of moving to
real data.

### 8.4 Why a controlled faithfulness probe was added

The explanation-stability analysis tells us *whether* the importance ordering is
reproducible, but not *whether* it is faithful to a known generative truth.
Because real-data ground truth is unobservable, `exp_008` constructs a
controlled **faithfulness probe** on the synthetic generator, whose feature
weights are known. The probe restricts attention to the **final course week**,
the one point at which the to-date features equal the generator's closed-form
inputs, and compares the measured importance ordering against the known oracle
weight ordering. The measured ordering recovers the oracle ordering exactly
(Kendall τ = `1.0`), while the same probe illustrates how proxy correlation and
redundancy distort importance away from the structural weights
(`activity_score_to_date` carries share `0.108` as a latent-driven proxy;
`overall_mastery` is redundant with `avg_assignment_score_to_date` at Pearson
`r` `0.994`). This is positioned as a **methods appendix**, not as headline
evidence: it validates that the permutation machinery can recover a known
ordering when one exists, and it makes the redundancy caveat concrete.

### 8.5 Why the second institution uses a matched engagement-only design

Generalization beyond one institution requires a second institution, but a
second institution rarely exposes the same signals. KU Leuven `1819`
(`exp_011`; `1495` students, two pooled courses, weeks `2`–`15`) has **no scored
assessments or continuous grade**, so the mastery ablation cannot be
reconstructed at all — itself a cross-institution heterogeneity finding about
what data institutions actually share. To make any comparison defensible, the
design is therefore **matched on engagement only**: a single, dataset-agnostic
**engagement-benchmark core** is run identically on OULAD and on KU Leuven, with
classification (`PASSED`) as the only shared target. On KU Leuven, engagement
predicts passing only modestly (F1 `0.75`–`0.76`, ROC-AUC `0.65`–`0.72`), and a
richer `B_engagement` set does not beat a minimal `A_simple_engagement` one
under fixed-model reporting (F1 Δ `-0.015` temporal / `+0.000` grouped), with
`cumulative_active_days_to_date` and `cumulative_clicks_to_date` dominating.

`exp_012` then runs this matched engagement core across **three institutions**
(OULAD DDD + BBB + KU Leuven) under identical fixed-model conditions. Comparing
importance across institutions whose features are *named* differently requires a
**concept-alignment map**: each institution's raw engagement columns are mapped
onto a small set of shared engagement concepts (clicks, active days, session
regularity, and so on), so that a **cross-institution Kendall τ** can be
computed over the shared-concept ordering. The result is a robustness finding,
not an accuracy claim: a two-feature click/active-days baseline is hard to beat
(richer-set `B − A` F1 spread `-0.016` to `+0.026` on the strict temporal split,
all six ROC-AUC cells positive), and the importance drivers transfer only
partially (mean Kendall τ ≈ `0.56`, verdict `drivers_partly_institution_specific`,
with clicks/active-days the recurring leading concepts and the mid/lower
ordering only partly shared). This matched design is what lets the project state
honestly that **feature-richness does not robustly help across cohorts and
institutions**, without overclaiming a like-for-like institutional replication.

## 9. Reproducibility and Experiment Governance

The methodological choices above are operationalized through versioned
experiment artifacts. Each experiment has a frozen YAML configuration in
`services/ml/configs/experiments/`, a dedicated artifact folder under
`data/artifacts/experiments/<experiment_id>/`, a machine-readable
`experiment_metadata.json`, a per-experiment Markdown summary in
`docs/experiments/`, and a row in `docs/experiments/registry.md`. This
governance discipline is methodologically meaningful rather than merely
operational: it ensures that every claim made in the dissertation can be
bound to a specific experiment ID, configuration file, split definition, and
artifact set, and that prior experiments are preserved unchanged when the
research direction shifts.

The seed is fixed at `42` across all experiments. Snapshot filtering is
applied uniformly with `min_week = 4` to avoid the early-course window in
which several score-based aggregates are legitimately undefined. Forbidden
columns — identifiers, end-of-course outcomes used as features, the
heuristic `risk_score`, `risk_level`, the snapshot-level
`predicted_final_grade`, and generation-only latent variables — are excluded
from the model matrix to prevent label and identity leakage. Train-only
imputation and feature scaling for linear models are enforced through the
shared experiment-runner pipeline.

## 10. Summary

The methodological design reflected in the experiment sequence is conservative,
hypothesis-driven, and reproducibility-aware. Standard baseline ML models are
appropriate because the prediction problem is tabular and interpretability is
a research requirement; the four-estimator stack spans the necessary
interpretability–prediction spectrum without overfitting to an arbitrary
estimator choice. `final_grade` is the primary target because it preserves
information that `passed` collapses; `passed` is secondary because it
saturates on the current dataset; `risk_level` is excluded because it is a
heuristic over the same features used as model inputs. The nested feature
hierarchy from `A_simple` through `B_lms` to `C_twin` makes the
representation question concrete; the subsequent ablation refines it into a
component-level diagnostic; the mastery validation tests the carry-forward
candidate against redundancy and target-leakage concerns; and the explanation
phase is performed only on the validated lean candidate. Crucially, the
synthetic gain is then re-examined as an artifact of a circular target rather
than accepted as a result. The explanation phase itself is built from
permutation and local-perturbation methods (no SHAP, by dependency-contract
choice) and is reported with an explicit explanation-stability analysis —
Kendall τ and Jaccard top-k, computed cross-split and cross-cohort — precisely
because the importance rankings turn out to be regime-sensitive rather than
invariant (within-course τ `0.55`–`0.79`, cross-course `0.32`–`0.61`,
cross-institution `0.56`). The real-data extension then re-runs the full nested
A/B/C ablation under fixed-model reporting on two distinct OULAD cohorts
(`exp_006` DDD, mixed-to-null; `exp_009` BBB, heterogeneous with mastery
`-1.026` RMSE on the temporal split) to neutralize the model-flip artifact, adds
a controlled faithfulness probe against a known oracle ordering (`exp_008`), and
finally tests a matched engagement-only design across a second institution and
three cohorts (`exp_011`, `exp_012`) through a concept-alignment map. Across all
of this the evidence is heterogeneous rather than a clean transfer confirmation.
Student-grouped and temporal-forward splits, rather than row-random splits, are
necessary consequences of the snapshot grain. The reported metrics (RMSE, MAE,
R² for regression; accuracy, precision, recall, F1, ROC-AUC for classification)
provide the multi-metric, multi-split evidence base that the experimental
claims rest on, and the real-data classification F1 (`0.83`–`0.93`, never
`1.000`) is the non-circular counterpart to the saturated synthetic F1. The
synthetic but schema-controlled dataset is a defensible substrate for
methodological investigation — and a cautionary circularity demonstration —
under explicit external-validity caveats. Together these choices form a coherent
methods chapter from which a dissertation account of the experimental line
through `exp_012` can be written without substantive revision.
