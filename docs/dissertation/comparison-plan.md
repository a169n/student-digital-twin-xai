# Comparison Plan: Existing Methods vs. This Work

## Purpose

A dissertation comparing this system to existing approaches requires a structured comparison chapter. This document defines what to compare, against what baselines, and on which dimensions.

---

## Comparison Dimensions

Pure accuracy comparison is insufficient — it misses the core contribution of this work. Three dimensions must be covered:

| Dimension | What to measure |
|---|---|
| Predictive accuracy | RMSE (regression), F1 / ROC-AUC (classification) |
| Explainability | Does the method produce per-student explanations? What type? |
| Teacher-facing completeness | Weekly trajectory, UI, explanation framing for non-ML users |

---

## Baselines to Implement

All baselines must be trained on the **same OULAD DDD 2013J student-grouped split** used in exp_005 / the demo payload. This is the only way to make accuracy comparisons honest.

### Tier 1 — Standard ML baselines (must implement)

| Model | Task | Why include |
|---|---|---|
| Logistic Regression | Pass/fail classification | Standard interpretable baseline; often beats complex models |
| Random Forest | Both regression + classification | Common OULAD benchmark in literature |
| Gradient Boosting (no Twin features, LMS only) | Both | Direct comparison to our lean model — already partially done in exp_005 |

### Tier 2 — Published results from literature (cite, do not reimplement)

Take accuracy numbers from papers that used the same OULAD DDD 2013J cohort and report them in a comparison table with a footnote that test splits may differ. This is standard academic practice.

| Source | Model | Reported metric |
|---|---|---|
| Algorithms 2025 (doi:10.3390/a18100662) | GB + SHAP pipeline | AUC 0.993, F1 0.911 |
| OULAD MOOC paper (Atlantis Press) | LSTM | Accuracy 83.4%, Precision 82.2% |

### Tier 3 — Commercial platforms (qualitative only)

EAB Navigate, Civitas Learning, Brightspace Insights. No access to their models. Describe qualitatively: what they show to teachers, whether explanations exist, whether the system is open.

---

## Comparison Table Structure (for dissertation chapter)

All "ours" rows: OULAD DDD 2013J, B_lms_oulad feature set, student_group split (test_size=0.25, seed=42).
Source: exp_005_public_benchmark_oulad. Consolidated in exp_013_comparison_baselines.

| Approach | RMSE | F1 | ROC-AUC | Per-student XAI | Teacher UI | Open / reproducible |
|---|---|---|---|---|---|---|
| Logistic Regression (ours) | — | 0.854 | 0.951 | No | No | Yes |
| Random Forest (ours) | 13.633 | 0.861 | 0.947 | No | No | Yes |
| GB LMS-only (ours, exp_005) | 12.658 | 0.863 | 0.953 | No | No | Yes |
| **GB + Twin + XAI (this work)** | 12.724 | 0.861 | 0.953 | Yes (perturbation) | Yes | Yes |
| GB + SHAP (literature, 2025) | — | 0.911 | 0.993 | Yes (SHAP) | No | Partial |
| Commercial (EAB Navigate) | unknown | unknown | unknown | Partial | Yes | No |

Notes on the filled rows:
- RMSE for regression target `final_weighted_score` (range 0–100); F1 and ROC-AUC for binary `passed_observed`.
- Logistic Regression: classification only (no regression equivalent).
- "GB + Twin" uses B_lms_plus_mastery_oulad (LMS + mastery proxy features); XAI via permutation importance + local perturbation (exp_007).
- GB + SHAP (literature): test split details differ; not directly comparable but included for orientation.
- The mastery (Twin) features did **not** improve RMSE over LMS-only baseline on this split (delta +0.066 RMSE). This is the honest negative result.

---

## Honest Framing

The comparison must not overclaim. Likely outcomes:

- **Accuracy**: Our model will be roughly comparable to published GB results, not clearly better. This is expected and should be stated openly.
- **XAI**: Our approach uses perturbation, not SHAP. It is less established but avoids SHAP's known instability on small samples. This trade-off should be explained.
- **Teacher UI**: No other published academic work has a comparable end-to-end teacher interface. This is the clearest differentiator.
- **Negative result**: The mastery features did not beat the LMS-only baseline on the student-grouped split. This is the most academically valuable finding to highlight, not hide.

---

## What Still Needs to Be Done

- [x] Train Logistic Regression on OULAD DDD 2013J, same split as exp_005 — already in exp_005 (F1=0.854, ROC-AUC=0.951)
- [x] Train Random Forest on OULAD DDD 2013J, same split as exp_005 — already in exp_005 (RMSE=13.633, F1=0.861, ROC-AUC=0.947)
- [x] Collect metrics and fill the comparison table — done, see exp_013_comparison_baselines
- [ ] Write the comparison chapter citing literature numbers for Tier 2
- [ ] Add qualitative section on commercial platforms
