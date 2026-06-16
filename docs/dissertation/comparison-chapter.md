# Chapter 4: Comparison with Existing Methods

## 4.1 Scope and Dimensions of Comparison

Evaluating a system contribution against the literature requires more than a
single accuracy metric. A model that achieves the best F1 on a held-out test
set is not necessarily the most useful system for a practitioner, and a system
that publishes per-student explanations is not necessarily more honest than
one that does not. For this prototype, three dimensions are therefore compared:

| Dimension | What is measured |
|---|---|
| Predictive accuracy | RMSE (regression), F1 and ROC-AUC (classification) |
| Explainability | Whether per-student explanations are produced; what method is used |
| Teacher-facing completeness | Weekly trajectory view; explanation framing accessible to non-ML users; open and reproducible |

Pure accuracy comparison against published benchmarks is problematic because
test sets differ across papers, cohort selection differs, and target
construction differs. Where split details are available, they are reported.
Where they are not, the literature number is included for orientation only,
with an explicit caveat.

All "ours" rows in the table below use the same OULAD DDD 2013J cohort
(1,938 students, 67,830 weekly snapshots), the same student-grouped split
(`test_size = 0.25`, `seed = 42`), and the same feature set (`B_lms_oulad`,
LMS-only features) unless the row specifically labels the mastery feature set.
Source experiment: `exp_005_public_benchmark_oulad`; consolidated in
`exp_013_comparison_baselines`.

---

## 4.2 Quantitative Comparison Table

| Approach | RMSE | F1 | ROC-AUC | Per-student XAI | Teacher UI | Open |
|---|---|---|---|---|---|---|
| Logistic Regression (ours) | — | 0.854 | 0.951 | No | No | Yes |
| Random Forest (ours) | 13.633 | 0.861 | 0.947 | No | No | Yes |
| GB LMS-only (ours) | 12.658 | 0.863 | 0.953 | No | No | Yes |
| **GB + Twin + XAI (this work)** | **12.724** | **0.861** | **0.953** | **Yes (perturbation)** | **Yes** | **Yes** |
| GB + SHAP (Algorithms, 2025) | — | 0.911 | 0.993 | Yes (SHAP) | No | Partial |
| Commercial (EAB Navigate) | unknown | unknown | unknown | Partial | Yes | No |

RMSE is in points on the `final_weighted_score` scale (0–100). F1 and ROC-AUC
are for binary `passed_observed` classification. Logistic Regression does not
produce a regression output and therefore has no RMSE entry.

---

## 4.3 Baseline Model Results

### Logistic Regression

Logistic Regression serves as the standard interpretable classification
baseline. Trained on `B_lms_oulad` (19 LMS features plus 3 indicator columns),
it achieves F1 = 0.854 and ROC-AUC = 0.951 on the held-out student group. This
is a competitive result that underscores the difficulty of beating a
well-tuned linear model on tabular OULAD data, where the dominant predictor —
assessment submission rate — is approximately linear in the log-odds of passing.

No regression target is reported for Logistic Regression as it is a
classification-only model. Ridge regression (`linear_regression` in the
experiment code) achieves RMSE = 14.318 on the same feature set and split,
making it the weakest regression baseline.

### Random Forest

Random Forest achieves RMSE = 13.633 (regression) and F1 = 0.861, ROC-AUC =
0.947 (classification) on the student-grouped split with `B_lms_oulad`. It
outperforms Logistic Regression on F1 by a small margin but underperforms on
ROC-AUC. In the context of the OULAD assessment structure, the Random Forest's
advantage on recall (0.895 vs 0.886) slightly outweighs its lower precision,
but neither difference is practically meaningful.

### Gradient Boosting — LMS-Only

Gradient Boosting on `B_lms_oulad` is the strongest baseline: RMSE = 12.658,
F1 = 0.863, ROC-AUC = 0.953. This is the direct reference point for this
work's lean Twin model. All further accuracy discussion is relative to this
baseline, not to the weaker models.

---

## 4.4 This Work: Gradient Boosting with Twin Features and XAI

The core system trains Gradient Boosting on `B_lms_plus_mastery_oulad`, which
extends the LMS feature set with a lean mastery analogue block: six additional
features derived from OULAD's dated assessment structure (due-to-date weighted
mastery, TMA/CMA/exam mastery aggregates, assessment coverage context, and a
current-cluster mastery proxy).

**Regression result:** RMSE = 12.724 on the student-grouped split. This is
0.066 RMSE points *worse* than the LMS-only Gradient Boosting baseline. The
difference is within noise but directionally negative: adding mastery features
to the LMS baseline did not help on this cohort under this split strategy.

**Classification result:** F1 = 0.861, ROC-AUC = 0.953 — essentially identical
to the LMS-only baseline (F1 delta = −0.002, ROC-AUC delta = 0.000).

This is the honest negative result of this work. The mastery feature block,
which showed a modest advantage on certain weeks of the controlled synthetic
experiments (`exp_002`), did not transfer to OULAD DDD 2013J under the primary
student-grouped evaluation. A secondary temporal-forward split shows a weaker
signal: the mastery analogue improves RMSE by −0.406 on temporal-forward, but
this split is less reliable for generalisation claims because it conflates
student-group and temporal effects. The multi-cohort picture (`exp_006`, `exp_009`)
further complicates the result: on OULAD BBB 2013J the mastery block beats the
LMS baseline by −1.026 RMSE on temporal-forward but remains null on
student-grouped. The cross-cohort pattern is therefore heterogeneous — neither
a consistent null nor a consistent benefit.

The XAI layer (permutation importance and local median-replacement explanation,
`exp_007`) is applied to the GB model on `B_lms_oulad`. The dominant feature is
`assessment_submission_rate_due_to_date` (importance share 0.381); three
genuinely exogenous signals — `is_unregistered_by_week`, `cumulative_clicks_to_date`,
and VLE category aggregates — carry interpretable but secondary weight. Importance
rankings are regime-sensitive: Kendall tau between student-grouped and
temporal-forward splits is 0.55–0.79 (none ≥ 0.90), meaning the explanations
must be framed as describing model behaviour under a particular evaluation
scenario, not as stable causal rankings.

Per-student explanations are surfaced in the teacher-facing interface, showing
each student's feature-level contribution to the predicted grade and pass-risk
score, alongside the weekly trajectory view.

---

## 4.5 Published Literature Benchmarks (Tier 2)

The following results are taken directly from published papers. They are
included for orientation, not for direct comparison: the papers use different
OULAD cohorts, different target definitions, and in some cases different
train/test splits.

### Modular GB + SHAP Pipeline (Algorithms, 2025)

López de la Rosa et al. (2025) report a gradient boosting pipeline with SHAP
explanations on OULAD dropout prediction, achieving ROC-AUC = 0.993 and F1 =
0.911 (doi: 10.3390/a18100662). The paper uses SHAP for both global feature
importance and per-student local explanations, includes governance-ready
subgroup reporting, and is substantially more accurate than the baselines in
this work.

Three important caveats apply. First, the target in López de la Rosa et al. is
dropout (binary), not the weighted assessment score regression used here — the
two targets are not directly comparable. Second, the exact OULAD cohort and
split strategy are not reported in sufficient detail to establish whether the
test set is student-grouped or not; a non-student-grouped split on OULAD can
inflate classification metrics substantially because the same student's weeks
appear in both train and test. Third, the paper does not provide a teacher UI
or document how explanations are communicated to non-ML users.

Taking the published number at face value: the literature's best classification
result (AUC 0.993) substantially outperforms this work (AUC 0.953). This is
expected and is not presented as a problem. The contribution of this work is
not a better classifier; it is an end-to-end prototype with honest evaluation
and a teacher interface.

### LSTM on OULAD (Atlantis Press)

An earlier deep learning benchmark reports accuracy = 83.4% and precision =
82.2% on OULAD dropout prediction using LSTM. This is comparable to the
Logistic Regression baseline in this work (accuracy = 86.7%), which suggests
that LSTM does not provide a clear advantage on OULAD weekly sequences over
well-calibrated classical models. LSTM interpretability is also substantially
harder to surface in a teacher interface without additional post-hoc methods.

---

## 4.6 Commercial Platforms (Tier 3)

Three commercial platforms offer teacher-facing student analytics with
some form of predictive or risk-scoring capability: **EAB Navigate**,
**Civitas Learning**, and **Brightspace Insights**. None of these platforms
publishes model evaluation details, test-set construction, or the feature
engineering underlying their risk scores. Comparison on accuracy is therefore
not possible.

On the explainability and teacher-UI dimensions, the commercial platforms
provide risk flags and recommended interventions, but the basis for those
recommendations is opaque to the teacher. The explanations, where they exist,
are typically framed as "contributing factors" derived from rule-based heuristics
or undisclosed model internals, not as per-student model-behaviour descriptions
with documented limitations.

This work differs from commercial platforms in three ways: it is fully open
and reproducible, it documents where its XAI method fails to achieve
regime-invariant rankings, and it frames explanations explicitly as
model-behaviour descriptions rather than causal intervention recommendations.

---

## 4.7 Discussion

### Accuracy

This work does not improve over the current published literature on pass/fail
classification accuracy. The best classification result (ROC-AUC = 0.953) is
below the published benchmark of 0.993, and the mastery features did not
improve over the LMS-only baseline. These facts are stated openly. A
master's-level research prototype is not expected to set a new benchmark; it
is expected to make a methodologically defensible contribution.

The more substantive accuracy finding is the honest negative result: adding a
lean mastery analogue to the LMS feature set did not help on the primary
student-grouped split on DDD 2013J. This result — null on both RMSE and F1
under the stricter evaluation — is itself a contribution, because it documents
a failure mode that most published papers in this area omit. The common
practice of reporting only the best-performing configuration on a single split
creates a literature where mastery or engagement enrichments appear to
universally help; the heterogeneous two-cohort result here challenges that
interpretation.

### Explainability

This work uses perturbation-based importance (permutation importance and local
median replacement) rather than SHAP. This choice has a specific justification:
SHAP values on small within-student test subsets exhibit known instability
because the marginal contribution computation requires approximating a
conditional expectation that is poorly estimated with fewer than ~50 samples
per student-week. The perturbation method used here is less sophisticated and
produces noisier global rankings, but it is interpretable on the same
individual prediction row used by the teacher interface without requiring a
background dataset assumption.

The limitation is the regime-sensitivity finding (`exp_007`): importance
rankings differ across evaluation scenarios, which means they cannot be
presented as stable causal orderings. The teacher UI should frame them — and
does frame them — as "this is how the model weights each signal to make this
prediction", not as "this is why the student is at risk".

### Teacher-Facing Interface

No published academic paper in the reviewed literature provides a
comparable end-to-end teacher interface: weekly trajectory charts, pass-risk
classification with XAI explanation, grade regression with feature
contributions, and a cohort-level table with filtering by risk level, all on
real OULAD data. Commercial platforms have interfaces but are closed. This is
the clearest and most defensible contribution of this work.

---

## 4.8 Summary

| Dimension | This work vs. literature |
|---|---|
| Classification accuracy | Below published best (AUC 0.953 vs 0.993); comparable to standard baselines |
| Mastery features vs. LMS-only | Null on primary split (Δ RMSE +0.066, Δ F1 −0.002); heterogeneous across cohorts |
| XAI method | Perturbation-based; less precise than SHAP but applicable without background-set assumption |
| Teacher UI | Unique in the academic literature; commercial equivalents are closed |
| Honest negative result | Documented and central to the contribution; not hidden |
| Reproducibility | Fully open; all experiments are versioned YAML + JSON artifacts |

The contribution of this dissertation is not an accuracy improvement. It is a
governed, leakage-aware, end-to-end prototype that implements the full cycle
from raw OULAD data to teacher-facing weekly explanations, evaluated honestly
with explicit documentation of where the engineered Twin features fail to
deliver benefit — a result type that is systematically underrepresented in the
educational analytics literature.
