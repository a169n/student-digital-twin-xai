# Final Integrated Dissertation Report

## Abstract

This report integrates the completed experimental line of the Student Digital
Twin XAI research prototype into a single dissertation-facing narrative. The
project investigates whether a teacher-oriented student digital twin can
support early academic risk analytics through final grade prediction,
interpretable model behavior, and structured evidence for intervention
reasoning. The evidence base consists of twelve frozen experiments spanning a
synthetic lean-Twin methodological arc, two OULAD cohorts (DDD and BBB 2013J),
and a second institution (KU Leuven), with the detailed per-experiment
manifest given in §5, §6, and §13. A structured comparison with published baselines
(Logistic Regression, Random Forest, Gradient Boosting, and GB + SHAP from the
literature) and commercial platforms is given in §10.

A leading caveat governs the synthetic phase and must be read first. The
synthetic `final_grade` is a **deterministic, noise-free closed-form weighted
mean of the same behaviors the features re-aggregate** (week-10 reconstruction
error `0.008`, correlation `1.000000`). The apparent synthetic R²≈0.99 and the
saturated `passed` F1 = `1.000` are therefore **algebraic artifacts, not
learnable signal**, and the synthetic "mastery win" is an artifact of this
circular target rather than evidence that any Twin representation predicts
better. The substantive empirical evidence rests on the real, non-circular
OULAD and KU Leuven cohorts.

On real data the finding is honest and mixed-to-heterogeneous. The full
Digital Twin representation did not deliver a consistent advantage over a
competent LMS-analytics baseline. On OULAD DDD 2013J (`exp_006`) the full
ablation is mixed-to-null — no Twin block beats the LMS baseline by more than
`1.0` RMSE on either split. On OULAD BBB 2013J (`exp_009`) the mastery block
does improve the temporal-forward split (`-1.026` RMSE) but not the
student-grouped split, the other Twin blocks, or the other course: engineered
Twin value is course- and split-dependent, not robust. The OULAD
classification target is genuinely predictive throughout (best-model F1
`0.83`–`0.93`, never `1.000`). The model-behavior explanations are
interpretable but **regime-sensitive** within a course (Kendall `tau`
`0.55`–`0.79`, mean `0.67`) and partly **course-specific** across courses
(`0.32`–`0.61`, mean `0.52`). A second institution (KU Leuven, `exp_011`),
where the mastery ablation cannot be built at all, and a matched
three-institution engagement synthesis (`exp_012`, mean `tau` ≈ `0.56`) point
the same way: adding feature richness does not robustly help. The resulting
contribution is therefore a reproducible, leakage-aware methodology, an
explanation-stability analysis, an honest mixed/negative real-data finding,
and a cautionary demonstration of synthetic-target circularity — **not** a
proof of Digital Twin accuracy superiority, full external validity, or a
simulation/counterfactual capability.

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

A structural caveat governs the entire synthetic phase and must lead any
reading of its numbers. The synthetic `final_grade` is a **deterministic,
noise-free closed-form weighted mean** of the same behaviors the model's
features re-aggregate (`services/ml/src/generator/final_results.py:74-84`);
at week 10 the features reconstruct the target with maximum absolute error
`0.008` and correlation `1.000000`. The synthetic regression R²≈0.99 and the
saturated `passed` F1 = `1.000` are consequently **algebraic artifacts of a
circular target, not learnable signal**. The synthetic experiments remain
internally valid as a controlled methodological arc, but their apparent
predictive successes — including the "mastery win" — cannot be read as real
capability. The substantive predictive evidence rests on the real OULAD and
KU Leuven cohorts introduced from `exp_005` onward.

The first four experiments use the refined synthetic dataset generated from
`generator_v1_3_refined.yaml`, a student-grouped primary split, a
temporal-forward secondary split where configured, seed `42`, and snapshot
weeks `4..10`. The model families are deliberately simple and defensible:
linear or Ridge-style regression, logistic regression, random forest, and
gradient boosting. The design emphasizes reproducibility, leakage-aware
splitting, train-only preprocessing, and explicit forbidden-column handling
over model complexity.

The fifth and later experiments use separate real-data adapters rather than
the synthetic schema. They are not new generator phases. They are public
benchmark transfer tests that approximate the representation logic on real
data: a two-set OULAD transfer test on module-presentation `DDD` `2013J`
(`exp_005`), full nested A/B/C ablations and model-behavior XAI on two OULAD
cohorts — `DDD 2013J` (`exp_006`/`exp_007`) and `BBB 2013J`
(`exp_009`/`exp_010`) — a controlled faithfulness probe on the synthetic
oracle (`exp_008`), and an engagement-only check on a second institution,
KU Leuven, consolidated into a matched three-institution synthesis
(`exp_011`/`exp_012`).

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

### 4.1 System Architecture

The prototype is implemented as a monorepo with two independently runnable
services. The machine learning service (`services/ml/`) is a Python package
containing the OULAD data adapter, the feature engineering pipeline, the
experiment runner, the model training code, and the perturbation-based XAI
module. All experiment outputs are versioned JSON and CSV artifacts written to
`data/artifacts/experiments/<experiment_id>/`. The web application
(`apps/web/`) is a Next.js server-side-rendered frontend that reads those
frozen artifacts at request time and serves teacher-facing views.

The data flow is: raw OULAD CSV files → OULAD adapter (`oulad_adapter.py`) →
weekly snapshot table (one row per student per week) → feature engineering →
trained Gradient Boosting model → prediction and perturbation-based explanation
artifacts → JSON payload consumed by the web app at runtime. The web layer
performs no ML computation; it is a pure read-only view over pre-computed
artifacts. This separation means that the experimental results are reproducible
independently of the web frontend, and the frontend can be tested without
retraining the model.

The demo payload loaded by the web app is a sample of approximately 150
students from the OULAD DDD 2013J cohort, drawn from the `exp_005` snapshot
table. The full cohort (1,938 students, 67,830 weekly snapshots) is not shipped
with the repository due to file size; the OULAD raw files and the snapshot
builder allow full reconstruction.

### 4.2 Teacher-Facing Interface

The web application provides two primary views for teachers.

The **cohort dashboard** (`/dashboard`) shows a sortable, filterable table of
all students in the loaded payload. Each row displays predicted final grade,
pass-risk badge (high / medium / low), current week, and key LMS signals. The
table supports filtering by risk level, enabling a teacher to quickly identify
students in the high-risk group across the full cohort without examining each
student individually.

The **student detail page** (`/students/[studentId]`) provides the full
per-student picture. Nine summary cards show the predicted grade, actual grade,
risk score, mastery, activity, attendance, assignment and quiz averages, and the
3-week score trend. A timeline chart plots the weekly trajectory of predictions,
mastery, activity, and risk over all available weeks. A scrollable weekly
snapshot table gives the raw weekly values. Below the timeline, the
explanation panel shows per-student model-behavior factors: which signals raise
and which lower the prediction for the student's current week, alongside a
teacher-readable summary sentence.

The explanation panel carries an explicit XAI limitation notice with three
points: that the factors describe model behaviour, not causes; that the score
should not be the sole basis for a student intervention; and that rankings can
shift across time periods and cohorts. This framing directly addresses the
research gap identified in the literature review — that published academic work
adds explanations without documenting how teachers may misinterpret them.

The interface is built with shadcn/ui components and Tailwind CSS. It requires
no external authentication or database: all data is loaded from local JSON files
at server render time, making it deployable in a research or demonstration
context without infrastructure dependencies.

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

The external phase then deepens the transfer test rather than ending on
`exp_005`. `exp_006` runs the full nested A/B/C ablation on OULAD DDD 2013J with
fixed-model reporting; `exp_007` explains that model and measures
regime-sensitivity; `exp_008` is a controlled synthetic faithfulness probe on
the deterministic oracle. `exp_009` repeats the full ablation on a second OULAD
cohort, BBB 2013J, and `exp_010` adds the cross-cohort explanation-stability
comparison. `exp_011` extends to a second institution (KU Leuven,
engagement-only), and `exp_012` consolidates a matched three-institution
engagement robustness comparison. The dependency chain therefore runs synthetic
lean-Twin validation → real-data ablation → real-data explanation-stability →
cross-institution engagement robustness.

This design avoids an unsupported move from full Twin construction directly to
explanation. The full representation was tested first, found unjustified, and
then decomposed. XAI was introduced only after the lean candidate had been
validated with caveats. Throughout, the controlling interpretation is the
honest, course- and regime-dependent real-data finding, not the
circular-target synthetic carry-forward.

## 6. Experiment Sequence

### 6.1 exp_001_baseline

The first experiment compares `A_simple`, `B_lms`, and `C_twin` on the
synthetic dataset. On the primary student-grouped split, `B_lms` reached RMSE
`2.101`, while the full `C_twin` reached RMSE `2.149`. On the temporal-forward
split, `B_lms` reached RMSE `2.270`, while `C_twin` deteriorated to RMSE
`2.937`. The `passed` classification task saturated and reached F1 `1.000`
for all feature sets under both splits.

The F1 `1.000` must be read with the circular-target caveat from Section 3 and
must never be reported as a real capability. It is an **algebraic artifact**:
the synthetic `final_grade` (and therefore the thresholded `passed`) is a
**deterministic, noise-free** function of the same behaviors the features
re-aggregate (week-10 reconstruction error `0.008`, correlation `1.000000`).
The saturated classifier is recovering a closed-form identity, not learning a
predictive signal. The same caveat applies to the synthetic regression
R²≈0.99 reported throughout the synthetic arc.

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

Two further caveats bound this "win". First, the entire comparison sits on the
circular synthetic target (Section 3): the mastery block's apparent advantage
is realized against an algebraically reconstructable outcome, so it is not
evidence of real predictive value. Second, the headline figures use a
best-model-per-cell protocol that flatters the candidate. A fixed-model
re-analysis — holding gradient boosting fixed across splits, as later
formalized in the OULAD phase — indicates the mastery candidate is
approximately `+0.41` RMSE *worse* than `B_lms` on the temporal-forward split,
and that `B_lms_plus_indices` is the only block improving both splits
(≈ `-0.066` / `-0.068`). Any carry-forward statement about mastery must
therefore be paired with a fixed-model reading, not best-model-per-cell.

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
Classification performance is nearly level between the two feature sets (F1
`0.863`/`0.861` grouped, `0.887`/`0.884` temporal-forward) — and, crucially,
nowhere near the saturated synthetic F1 `1.000`, because the OULAD target is
genuinely predictive rather than a closed-form identity.

The consequence is not external confirmation. The two-set transfer test alone
returns a mixed signal. This is the starting point, not the final word: the
full nested ablation in `exp_006` (§6.6) supersedes the two-set test and
yields the decisive statement, and a second OULAD cohort (`exp_009`, §6.8)
shows the result is not uniform across courses. A partial-target-circularity
note carries forward from here: OULAD's `final_weighted_score` is itself
partly fed by assessment scores, so the regression results lean on
within-system accounting; the classification target and the VLE clickstream
features are the cleaner, more exogenous evidence.

### 6.6 exp_006_oulad_full_ablation — Full OULAD Ablation (DDD 2013J)

`exp_006` extends the OULAD benchmark from the two-set transfer test to the
**full nested A/B/C ablation** on real data, using the identical leakage-aware
pipeline. The dataset is OULAD module-presentation `DDD 2013J`: `67,830`
weekly snapshots across `1,938` students. This phase introduces **fixed-model
gradient-boosting reporting** — the same model held fixed across splits — to
neutralize the best-model-per-cell model-flip artifact flagged in `exp_002`
and `exp_005`, so feature-block deltas are not confounded with model selection.

The result is a **mixed-to-null** finding. Under the fixed-model comparison,
no Twin feature block improves over the strong `B_lms_oulad` baseline by more
than `1.0` RMSE on either split. The largest single gain is the mastery
analogue on the temporal-forward split (RMSE `9.561` to `9.180`, delta
`-0.381`), but the same block is `+0.061` worse on the student-grouped split.
The composite-index block improves the temporal-forward split modestly
(`-0.218`) and is essentially flat on the grouped split (`+0.008`). The full
`C_twin_oulad` analogue is within `±0.025` RMSE of the baseline on both splits:
non-inferior, but not distinctly better. The minimal `A_simple_oulad` baseline
is clearly worse (`+1.207` grouped, `+4.105` temporal-forward), confirming that
the LMS behavioral layer carries the predictive signal and that the Twin
engineering adds little on top of it. Best-model classification F1 ranges from
`0.83` to `0.887` across feature sets and splits and never reaches `1.000` —
the direct empirical contrast with the synthetic, circular target.

The consequence is the decisive, honest statement: on a real, non-circular
dataset, the engineered Digital Twin feature blocks do **not** deliver a
consistent predictive advantage over a competent LMS-analytics baseline, and
the apparent synthetic advantage of the mastery block did not robustly
transfer. This is one of two OULAD cohorts; §6.8 qualifies it.

### 6.7 exp_007_xai_on_oulad — OULAD XAI and Regime-Sensitivity (DDD 2013J)

`exp_007` applies the same model-behavior explanation methods (held-out
permutation importance, model-native importance, one-feature local
perturbation; no SHAP) to the real OULAD `DDD 2013J` model, for `B_lms_oulad`,
`B_lms_plus_mastery_oulad`, and `C_twin_oulad` under both splits. Two findings
follow, as a co-equal contribution alongside the predictive result.

First, the explanations lean on features close to the target. The dominant
feature is `assessment_submission_rate_due_to_date` for the LMS baseline
(importance share `0.28`-`0.38`) and, once mastery is included, the co-circular
`overall_mastery_proxy` (share `0.23`-`0.43`). The genuinely exogenous signals
— the registration-state flag `is_unregistered_by_week` (share `0.13`-`0.20`)
and the VLE clickstream features (share `0.02`-`0.06`) — are interpretable but
carry modest weight. Even the explanation partly rests on within-system
accounting features rather than independent behavioral causes.

Second, the explanations are **regime-sensitive**. The Kendall rank
correlation of the global importance ranking between the student-grouped and
temporal-forward splits is moderate and below a high-stability threshold for
every feature set: `tau = 0.79` for `B_lms_oulad`, `0.68` for
`B_lms_plus_mastery_oulad`, and `0.55` for `C_twin_oulad` (mean `0.67`, none
reaching `0.90`). Top-5 Jaccard overlap is `1.00`/`1.00`/`0.67`: the same few
features dominate across regimes while their relative priority reorders, and
the widest feature set is the least order-stable. *Which* features the model
appears to rely on, and in what order, depends on the evaluation scenario.
These are model-behavior observations, not causal claims.

### 6.8 exp_009_oulad_full_ablation_bbb — Second-Cohort Ablation (BBB 2013J)

`exp_009` repeats the full nested ablation on a second, distinct OULAD
module-presentation, **BBB 2013J** (`2,237` students, `80,532` weekly
snapshots, with a richer dated-assessment structure than DDD), under the
identical pipeline and fixed-model reporting. OULAD must be read as two
distinct cohorts — DDD 2013J and BBB 2013J — not one undifferentiated
benchmark.

The Twin-block value is **heterogeneous, not uniformly null**. Under the
fixed-model comparison on BBB 2013J, the mastery block improves the
temporal-forward split by `-1.026` RMSE (`5.284` versus `6.311`) — crossing
the one-point threshold that no block crossed on DDD — and the full
`C_twin_oulad` improves it by `-0.765`. On the student-grouped split, however,
every block stays within `0.087` RMSE of the baseline (null, as on DDD), and
the trend and composite-index blocks are null on both splits of both courses.
Classification remains genuinely predictive (F1 `0.87`-`0.93`, never `1.000`).

The consequence is heterogeneity: the DDD null was **partly course-specific**.
On a course with richer assessment structure the mastery block delivers a
meaningful gain under forward-time evaluation, but the advantage does not
generalize to the student-grouped split, the other Twin blocks, or the other
course. The defensible cross-course statement is neither uniform null nor
uniform benefit — engineered Twin value is course- and split-dependent.

### 6.9 exp_010_xai_on_oulad_bbb — BBB XAI and Cross-Cohort Stability

`exp_010` repeats the model-behavior XAI on BBB 2013J and adds a cross-cohort
explanation-stability comparison. The importance topology is qualitatively
**shared** across the two courses — `overall_mastery_proxy`,
assessment-submission discipline, and the `is_unregistered_by_week` withdrawal
flag dominate both — but the rankings are **not stable**. The cross-cohort
agreement (Kendall `tau` of DDD versus BBB, per feature set and split) is
`0.32`-`0.61` (mean `0.52`), lower than the within-cohort cross-split agreement
of §6.7 (`0.55`-`0.79`, mean `0.67`); no cell reaches a high-stability
threshold, and top-5 membership overlaps only partially (Jaccard `0.43`-`1.00`).
The model's "why" is not only regime-sensitive within a course but also partly
course-specific across courses — a co-equal cautionary finding alongside the
predictive heterogeneity. The controlled synthetic faithfulness probe that
licenses these known-ground-truth stability readings is recorded separately as
a methods appendix in §6.10.

### 6.10 exp_008 — Synthetic Faithfulness Probe (Methods Appendix)

`exp_008` is a controlled faithfulness probe, not a headline result, recorded
here as a methods appendix. Because the synthetic generator defines
`final_grade` as a closed-form weighted mean, the final course week provides an
**oracle ordering** of feature importance. At that week the permutation
importance recovers the generator's weight ordering exactly (Kendall
`tau = 1.0`), confirming the explanation method is faithful to ground truth
when ground truth is known. The probe simultaneously documents the distortions
that complicate real-data interpretation: `activity_score_to_date` takes a
`0.108` importance share as a latent-driven proxy, and `overall_mastery` is
redundant with `avg_assignment_score_to_date` at Pearson `r = 0.994`. The
oracle exists only because the synthetic target is deterministic and circular;
the probe adds no predictive claim.

### 6.11 exp_011 — Second Institution (KU Leuven), Engagement-Only

`exp_011` adds a second institution, the KU Leuven de-identified
learning-analytics dataset (Tiukhova et al., 2026, CC-BY-4.0), to extend
external validity beyond OULAD. The integration itself surfaces a structural
finding: KU Leuven exposes raw clickstream, forum activity, and course
structure, but **no intermediate scored assessments and no continuous grade** —
only a binary `PASSED` outcome and categorical exam-session buckets. The
project's central mastery/assessment ablation therefore **cannot be reproduced
on KU Leuven at all**; the question "does the mastery block help?" is
unanswerable here because the data to construct it does not exist. This is
itself a cross-institution heterogeneity result.

What KU Leuven supports is an **engagement-only, classification-only** check on
year 1819 (two courses pooled, `1,495` students, weeks `2`–`15`, leakage-safe
cumulative-to-date features). Engagement predicts passing only **modestly** —
best-model F1 `0.75`-`0.76`, ROC-AUC `0.65`-`0.72` — far below the
assessment-driven OULAD numbers, as expected when no assessment signal is
available. The **richer** engagement set `B_engagement` is essentially level
with the minimal `A_simple_engagement`: fixed-model F1 delta `-0.015` on the
temporal-forward split and `+0.000` on the student-grouped split, with a small
ROC-AUC gain (`+0.009`/`+0.041`). Permutation importance shows the signal is
carried by basic engagement volume — `cumulative_active_days_to_date` and
`cumulative_clicks_to_date` dominate (the former takes a `0.456` share on the
temporal-forward split) — while forum participation and temporal position
contribute little. Across three real cohorts spanning two institutions, adding
a richer engineered representation does not robustly beat a simpler baseline.

### 6.12 exp_012 — Cross-Institution Engagement Robustness (Three Institutions)

`exp_012` consolidates the cross-institution evidence into a single **matched**
comparison: an engagement-only, classification-only `PASSED` comparison across
OULAD DDD 2013J, OULAD BBB 2013J, and KU Leuven 1819 at once, under an
identical two-feature design (the mastery/Twin blocks are excluded by
construction, since KU Leuven cannot build them, so the three institutions are
directly comparable).

Part A is **neutral-to-modest with a split asymmetry**. The richer engagement
set never decisively wins or loses on F1. The positive fixed-model `B − A` F1
deltas concentrate on the `student_group` split — DDD `+0.072`, BBB `+0.039`,
KU `+0.000` — while the stricter, early-warning-relevant `temporal_forward`
split is essentially flat to slightly negative: DDD `-0.0003`, KU `-0.015`,
BBB `+0.026` (full spread `-0.016` to `+0.026`). ROC-AUC rises slightly more
consistently (all six cells positive, `+0.009` to `+0.041`). The honest reading
is the opposite of an accuracy win: a two-feature engagement baseline (clicks +
active-days) is hard to beat.

Part B is **partial transfer**. Aligning permutation-importance rankings onto
seven shared engagement concepts and comparing pairwise yields a mean Kendall
`tau` of `0.56` (student_group mean `0.49`, temporal_forward mean `0.62`), well
below the `0.90` "stable everywhere" bar; the most stable pair is KU↔BBB
(`tau = 0.714`) and the least is KU↔DDD on student_group (`tau = 0.238`). The
verdict is `drivers_partly_institution_specific`: clicks and active-days recur
as the top drivers across all three institutions and both splits, but the
relative ordering of the mid- and lower-ranked concepts only partially
transfers. This is a robustness result about gradient-boosting model behavior,
not an accuracy claim and not causal evidence.

## 7. Results and Interpretation

The completed experiments support a bounded interpretation.

First, the synthetic "successes" are artifacts of a circular target and must
not be read as real capability. The synthetic `final_grade` is a
deterministic, noise-free closed-form function of the same behaviors the
features re-aggregate (week-10 reconstruction error `0.008`, correlation
`1.000000`), so the synthetic R²≈0.99, the saturated `passed` F1 `1.000`, and
the apparent "mastery win" are algebraic artifacts. The synthetic arc is a
controlled, cautionary methodological demonstration, not evidence that any Twin
formulation predicts better.

Second, on real, non-circular data the full Digital Twin did not deliver a
consistent advantage over a competent LMS baseline, and the result is
**heterogeneous across cohorts**. On OULAD DDD 2013J (`exp_006`) the full
ablation is mixed-to-null — no Twin block beats the LMS baseline by more than
`1.0` RMSE on either split, and the minimal `A_simple_oulad` is clearly worse
(`+1.207` grouped, `+4.105` temporal-forward), showing the LMS layer carries
the signal. On OULAD BBB 2013J (`exp_009`) the mastery block improves the
temporal-forward split by `-1.026` RMSE but not the student-grouped split, the
other Twin blocks, or the other course. Engineered Twin value is therefore
course- and split-dependent, not a robust improvement. The OULAD
classification target is genuinely predictive throughout (best-model F1
`0.83`-`0.93`, never `1.000`), which is exactly what makes the real-data
result trustworthy where the synthetic one is not.

Third, the explanation phase is meaningful but its outputs are not invariant.
On synthetic data the lean model did not collapse onto a single feature, but
global importance was dominated by `activity_score_to_date` and
`overall_mastery` remained redundant with cumulative assessment performance.
On real OULAD data the explanations are **regime-sensitive** within a course
(Kendall `tau` `0.55`-`0.79`, mean `0.67`) and partly **course-specific**
across courses (`0.32`-`0.61`, mean `0.52`), none reaching `0.90`. The
faithfulness probe (`exp_008`) confirms the method recovers a known oracle
ordering exactly (`tau = 1.0`) when ground truth exists, licensing these
stability statements as method-faithful observations.

Fourth, the cross-institution evidence points the same way. A second
institution (KU Leuven, `exp_011`) cannot even support the mastery ablation,
and on its engagement-only task a richer engagement set does not beat a
minimal one (fixed-model F1 delta `-0.015`/`+0.000`). The matched
three-institution synthesis (`exp_012`) confirms a two-feature engagement
baseline is hard to beat (richer features add neutral-to-modest F1, ≈0 on the
stricter temporal-forward split) and that importance drivers transfer only
partially (mean `tau` ≈ `0.56`). Across three real cohorts and two institutions
the recurring result is that **adding feature richness does not robustly help**.

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

The real-data benchmark is best understood as a transfer test across **two
distinct OULAD cohorts and a second institution**, not one undifferentiated
"OULAD" check. OULAD uses public data with different assessment design,
missingness, module timing, and outcome semantics; the benchmark asks whether
the representation idea transfers and whether the engineered blocks improve a
competent LMS baseline. A partial-target-circularity disclosure applies: OULAD's
derived `final_weighted_score` is partly fed by assessment scores, so the
regression results lean somewhat on within-system accounting — the cleaner,
more exogenous evidence is the genuinely predictive classification target and
the VLE clickstream features.

The verdict is decisive and honest rather than "unresolved". The two-set
transfer test (`exp_005`) is only the starting point; the full nested
ablations supersede it. On **DDD 2013J** (`exp_006`) the result is
**mixed-to-null** — no Twin block beats the LMS baseline by more than `1.0`
RMSE on either split. On **BBB 2013J** (`exp_009`) the result is
**heterogeneous** — the mastery block improves the temporal-forward split by
`-1.026` RMSE but nothing else, on no other split, block, or course. The
accompanying explanations are regime-sensitive within a course (`tau`
`0.55`-`0.79`) and partly course-specific across courses (`0.32`-`0.61`). A
second institution (KU Leuven, `exp_011`) — where the mastery ablation cannot
even be built — and the matched three-institution engagement synthesis
(`exp_012`, mean `tau` ≈ `0.56`) extend the same finding. Across three cohorts
and two institutions, **engineered feature-richness does not robustly improve
prediction**, and the value of both the representation and its explanations is
course- and regime-dependent. This is the project's external-evidence verdict:
not a complication to be resolved later, but a clear honest mixed/negative
result.

## 10. Comparison with Published Methods and Baselines

### 10.1 Dimensions of Comparison

Accuracy alone is insufficient as a comparison axis for a system contribution.
Three dimensions are compared: predictive accuracy (RMSE for regression,
F1 and ROC-AUC for pass/fail classification), explainability (whether
per-student explanations are produced and by what method), and
teacher-facing completeness (weekly trajectory view, explanation framing,
openness and reproducibility).

All "ours" rows use OULAD DDD 2013J, the `B_lms_oulad` feature set, and the
student-grouped split (`test_size = 0.25`, `seed = 42`). Numbers are from
`exp_005_public_benchmark_oulad`, consolidated in `exp_013_comparison_baselines`.
RMSE is on the `final_weighted_score` scale (0–100); F1 and ROC-AUC are for
binary `passed_observed`.

| Approach | RMSE | F1 | ROC-AUC | Per-student XAI | Teacher UI | Open |
|---|---|---|---|---|---|---|
| Logistic Regression (ours) | — | 0.854 | 0.951 | No | No | Yes |
| Random Forest (ours) | 13.633 | 0.861 | 0.947 | No | No | Yes |
| GB LMS-only (ours, `exp_005`) | 12.658 | 0.863 | 0.953 | No | No | Yes |
| **GB + Twin + XAI (this work)** | **12.724** | **0.861** | **0.953** | **Yes (perturbation)** | **Yes** | **Yes** |
| GB + SHAP (Algorithms, 2025) | — | 0.911 | 0.993 | Yes (SHAP) | No | Partial |
| Commercial (EAB Navigate) | unknown | unknown | unknown | Partial | Yes | No |

### 10.2 Baseline Model Results

Logistic Regression on `B_lms_oulad` achieves F1 = 0.854 and ROC-AUC = 0.951
on the held-out student group. This is competitive, reflecting that the dominant
predictive signal — assessment submission rate — is approximately linear in the
log-odds of passing. Ridge regression (labeled `linear_regression`) achieves
RMSE = 14.318, the weakest regression baseline.

Random Forest achieves RMSE = 13.633 (regression) and F1 = 0.861, ROC-AUC = 0.947
(classification). The slight F1 gain over Logistic Regression is not practically
meaningful. Gradient Boosting on `B_lms_oulad` is the strongest baseline: RMSE = 12.658,
F1 = 0.863, ROC-AUC = 0.953. All accuracy comparisons for this work are relative
to this baseline.

### 10.3 This Work versus Published Benchmarks

The core system trains Gradient Boosting on `B_lms_plus_mastery_oulad`, adding
six mastery-proxy features to the LMS set. On the student-grouped split: RMSE = 12.724
(delta **+0.066** versus LMS-only), F1 = 0.861 (delta −0.002). Adding mastery
features did not improve accuracy on this cohort under this split. This is the
honest negative result central to the contribution.

The XAI layer from `exp_007` applies permutation importance and local
median-replacement to the GB model. The dominant factor is
`assessment_submission_rate_due_to_date` (importance share 0.381); genuinely
exogenous signals (`is_unregistered_by_week`, VLE clickstream) carry interpretable
but secondary weight. Importance rankings are regime-sensitive: Kendall tau between
student-grouped and temporal-forward splits is 0.55–0.79 — none reaching 0.90 —
so explanations describe model behaviour under a particular evaluation scenario,
not stable causal rankings. Per-student explanations are surfaced in the teacher
UI alongside weekly trajectory charts.

The published reference benchmark is López de la Rosa et al. (Algorithms, 2025),
which reports ROC-AUC = 0.993 and F1 = 0.911 using gradient boosting with SHAP
on OULAD dropout prediction (doi: 10.3390/a18100662). Three caveats limit direct
comparison. First, their target is binary dropout, not the weighted assessment
score regression used here. Second, the exact cohort selection and split strategy
are not reported in sufficient detail to confirm student-grouped evaluation;
a non-student-grouped split can inflate classification metrics substantially.
Third, no teacher UI or documented explanation framing for non-ML users is provided.
Taking the published number at face value: the literature's best classification
result (AUC 0.993) outperforms this work (AUC 0.953). This is expected and is
not a weakness of the contribution — the contribution is an end-to-end prototype
with honest evaluation, not a superior classifier.

### 10.4 Commercial Platforms

EAB Navigate, Civitas Learning, and Brightspace Insights offer teacher-facing
risk-scoring dashboards. None publishes model evaluation details, test-set
construction, or underlying feature engineering. Accuracy comparison is impossible.
Where explanations exist, they are framed as opaque "contributing factors" without
documented limitations. This work differs on three points: it is fully open and
reproducible, it documents regime-sensitivity of the XAI rankings, and it frames
explanations explicitly as model-behaviour descriptions rather than causal
intervention recommendations. The teacher interface built here — with weekly
trajectory, per-student XAI panel, and explicit XAI limitation notice — has no
published academic equivalent.

### 10.5 Summary

The accuracy of this work is comparable to standard baselines and below the
published best on OULAD. The mastery (Twin) features did not improve over the
LMS-only baseline on the primary split. The most defensible comparative claim is
not accuracy superiority but a different combination: a complete, open,
reproducible end-to-end prototype; documented honest negative result; and a
teacher UI with explicit XAI caveats that no published academic paper in this
area provides. Detailed experiment code, data artifacts, and comparison numbers
are in `exp_013_comparison_baselines` and `docs/dissertation/comparison-chapter.md`.

## 11. Limitations and Threats to Validity

The main development evidence is synthetic, and on a **circular target**. The
synthetic `final_grade` is a deterministic, noise-free closed-form weighted
mean of the same behaviors the features re-aggregate (week-10 reconstruction
error `0.008`, correlation `1.000000`). The synthetic R²≈0.99 and the saturated
`passed` F1 `1.000` are algebraic artifacts, not learnable signal, and the
synthetic "mastery win" is an artifact of this circularity. The synthetic phase
is internally valid as a controlled methodological arc but carries no
predictive external validity; the substantive evidence rests on real data.

The `passed` target is saturated in the synthetic experiments precisely because
of that circularity. It cannot be used to discriminate between representations,
so on synthetic data regression on `final_grade` (itself circular) is the only
meaningful synthetic comparison, and the real OULAD classification target (F1
`0.83`-`0.93`, never `1.000`) is the trustworthy predictive evidence.

The mastery block is useful but redundant. `overall_mastery` is close to
cumulative LMS performance and to `final_grade`. This is a structural caveat,
not a minor reporting detail.

The XAI methods are not causal and are not SHAP. Their outputs should be
described as directional model-behavior explanations.

The real-data evidence is public and valuable but partial. It spans two OULAD
module-presentations (`DDD 2013J`, `BBB 2013J`) and a second institution
(KU Leuven), with adapted targets. The OULAD result is heterogeneous across
cohorts (DDD null, BBB partial), and the KU Leuven check is engagement-only
and classification-only — it cannot test mastery and its task differs from
OULAD. The cross-institution evidence therefore supports the narrower claim
that feature-richness does not robustly help; it is not a like-for-like
institutional replication of the Twin ablation. OULAD's
`final_weighted_score` is also partly fed by assessment scores (partial target
circularity), so the regression results lean somewhat on within-system
accounting.

Explanations are not invariant across regimes or courses. Importance rankings
are regime-sensitive within a course (Kendall `tau` `0.55`-`0.79`, mean `0.67`)
and partly course-specific across courses (`0.32`-`0.61`, mean `0.52`), with
cross-institution engagement drivers transferring only partially (mean `tau` ≈
`0.56`); none reach `0.90`. The stability of teacher-facing explanations across
deployment regimes is therefore itself a documented limitation.

Finally, intervention and scenario analysis remain future work. The current
experiment line supports prediction and model-behavior explanation; it does
not validate intervention recommendations, and the "Digital Twin" here is a
lean, time-aware weekly student-state representation, not a simulation or
counterfactual engine.

## 12. Final Conclusions

The final conclusion is deliberately bounded and honest. Within the synthetic
environment, a compact mastery-centered Twin subset, `B_lms_plus_mastery`,
*appeared* to improve final grade prediction and to remain interpretable. But
that apparent gain is an **artifact of a deterministic, circular target**: the
synthetic `final_grade` is a noise-free closed-form weighted mean of the same
behaviors the features re-aggregate (week-10 reconstruction error `0.008`,
correlation `1.000000`), so the synthetic R²≈0.99 and `passed` F1 `1.000` are
algebraic artifacts. The synthetic arc therefore contributes a controlled,
cautionary demonstration of how a circular target can manufacture an apparent
representation advantage — not evidence that any Twin formulation predicts
better.

When the identical leakage-aware pipeline is applied to real, non-circular
data, that advantage does not robustly transfer, and the picture is
**heterogeneous across cohorts**. On OULAD DDD 2013J (`exp_006`,
`67,830` snapshots, `1,938` students) the full ablation is mixed-to-null: no
Twin block beats the LMS baseline by more than `1.0` RMSE on either split, and
the minimal `A_simple_oulad` is clearly worse, so the LMS layer already carries
the signal. On OULAD BBB 2013J (`exp_009`, `80,532` snapshots, `2,237`
students) the mastery block improves the temporal-forward split by `-1.026`
RMSE — but not the student-grouped split, the other Twin blocks, or the other
course. The OULAD classification target is genuinely predictive throughout
(best-model F1 `0.83`-`0.93`, never `1.000`). The accompanying explanations
(`exp_007`, `exp_010`) are regime-sensitive within a course (Kendall `tau`
`0.55`-`0.79`) and partly course-specific across courses (`0.32`-`0.61`). A
second institution (KU Leuven, `exp_011`) cannot even build the mastery
ablation and shows a richer engagement set does not beat a minimal one
(fixed-model F1 delta `-0.015`/`+0.000`), and the matched three-institution
synthesis (`exp_012`, mean `tau` ≈ `0.56`) confirms a two-feature engagement
baseline is hard to beat. Across three real cohorts and two institutions,
adding feature richness does not robustly help.

The most defensible dissertation statement is therefore that the project's
contribution is **methodological and cautionary, not an accuracy or
Digital-Twin-superiority claim**. It supplies (i) a reproducible, leakage-aware
protocol for constructing, ablating, and explaining weekly student-state
representations, reported with fixed-model comparisons to neutralize
model-selection artifacts; (ii) an explanation-stability analysis showing that,
on real data, importance rankings are regime-sensitive within a course and
partly course-specific across courses; (iii) a cautionary
synthetic-circularity demonstration; and (iv) an honest mixed/negative
real-data finding across two OULAD cohorts and a second institution. The
"Digital Twin" here is a lean, time-aware weekly student-state representation,
not a simulation or counterfactual engine. External validation across more
institutions and causal intervention reasoning remain future work.

## 13. Canonical Evidence References

- [exp_001_baseline](../experiments/exp_001_baseline.md)
- [exp_002_twin_ablation](../experiments/exp_002_twin_ablation.md)
- [exp_003_mastery_validation](../experiments/exp_003_mastery_validation.md)
- [exp_004_xai_on_lean_twin](../experiments/exp_004_xai_on_lean_twin.md)
- [exp_005_public_benchmark_oulad](../experiments/exp_005_public_benchmark_oulad.md)
- [exp_006_oulad_full_ablation (DDD 2013J)](../experiments/exp_006_oulad_full_ablation.md)
- [exp_007_xai_on_oulad (DDD 2013J)](../experiments/exp_007_xai_on_oulad.md)
- [exp_008_faithfulness_probe (methods appendix)](../experiments/exp_008_faithfulness_probe.md)
- [exp_009_oulad_ablation_bbb2013j (BBB 2013J)](../experiments/exp_009_oulad_ablation_bbb2013j.md)
- [exp_010_xai_on_oulad_bbb2013j (BBB 2013J)](../experiments/exp_010_xai_on_oulad_bbb2013j.md)
- [exp_011_kuleuven_engagement](../experiments/exp_011_kuleuven_engagement.md)
- [exp_012_oulad_engagement (3-institution synthesis)](../experiments/exp_012_oulad_engagement.md)
- [exp_013_comparison_baselines](../../data/artifacts/experiments/exp_013_comparison_baselines/exp_013_comparison_baselines_results.json)
- [Comparison chapter (standalone)](comparison-chapter.md)
- [Experiment progression summary](experiment_progression_summary.md)
- [Experimental results synthesis](experimental_results_synthesis.md)
- [Limitations and threats to validity](limitations_and_threats_to_validity.md)
- [Final research conclusions](final_research_conclusions.md)
