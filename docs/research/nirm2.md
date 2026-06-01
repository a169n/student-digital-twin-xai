# Intelligent Educational Platform with Digital Twin and Explainable AI Integration for Analyzing and Interpreting Students' Learning Achievements

## Abstract

Learning management systems (LMS) record large volumes of educational activity, yet their analytics functions are typically descriptive rather than predictive or explanatory, and they rarely integrate prediction and interpretation into a single teacher-facing tool. This study presents an intelligent educational platform that integrates a **Student Digital Twin** with an **Explainable AI (XAI)** layer to analyze and interpret students' learning achievements. Each student is represented as a dynamic digital twin — a weekly student-state snapshot at the grain of one student per course week — which feeds a leakage-aware predictive engine for final-grade estimation and a model-behavior explanation layer, all surfaced through a teacher-oriented web application backed by a FastAPI service and a local application store. The platform's analytics engine is validated through a disciplined, dependency-driven sequence of five frozen experiments — a baseline feature-set comparison, a structured Twin ablation, a mastery-validation audit, a model-behavior XAI phase, and an external Open University Learning Analytics Dataset (OULAD) public-benchmark stress test. The findings are deliberately bounded: the full Digital Twin representation was *not* justified relative to a stronger LMS baseline, whereas a compact mastery-centered subset improved final-grade prediction on the primary student-grouped split (RMSE 1.894 vs. 2.101) and at early-course weeks, while remaining interpretable with explicit redundancy caveats. The OULAD benchmark complicated rather than confirmed external transfer. The contribution is a methodologically disciplined, teacher-oriented platform that integrates a lean Digital Twin and XAI for analyzing and interpreting learning achievements, rather than a proof of full Digital Twin superiority or an institutional deployment.

## Introduction

Higher-education institutions increasingly instrument their courses through learning management systems that capture attendance, submissions, assessment marks, and fine-grained activity logs. These systems are effective at *recording* what has already happened, but they rarely offer instructors an integrated, forward-looking platform that combines a dynamic student model, predictive analytics, and interpretable explanations in a single decision-support workflow. The result is a structural gap between the data an institution already holds and the early, actionable, and *interpretable* insight a teacher needs to support a student's learning achievements. Recent reviews of student-performance prediction frame the underlying task as supervised learning over academic, behavioral, and LMS-derived variables, and identify weak interpretability and weak integration into teacher workflows as recurring limitations [1][2]. Learning-analytics dashboards partly address visualization, but typically stop at descriptive reporting rather than delivering predictive and explanatory analysis together [3].

A promising conceptual framing for this gap is the *digital twin*: a dynamic, continuously updated virtual representation of a real entity that supports prediction and what-if reasoning rather than static reporting [4]. Applied to education, a student digital twin is not a dashboard but a stateful, time-aware representation of a learner that is updated week by week and can be queried *before* the course ends. To make such a representation useful to a teacher, two further capabilities must be integrated into one platform: a **predictive engine** that estimates learning achievements from the twin state, and an **Explainable AI layer** that interprets those predictions so the teacher understands *which* factors drive a student's estimated outcome. The central scientific question is whether the engineered twin representation genuinely improves prediction beyond a competent LMS analytics layer, and whether any useful twin representation remains interpretable enough for teacher-facing explanation; an explanation layer is valuable only if it preserves the distinction between predictive association and causal mechanism.

The purpose of this study is to design and evaluate an **intelligent educational platform that integrates a Student Digital Twin and Explainable AI for analyzing and interpreting students' learning achievements**. The platform couples a reproducible analytics engine — synthetic LMS-like data generation, weekly twin-snapshot construction, leakage-aware prediction, and model-behavior explanation — with a teacher-oriented web interface served over a documented data flow. Unlike prior work that examines a single representation and reports a single headline result, we explicitly compare a nested hierarchy of feature representations and then decompose, validate, and explain the representation through a chain of five frozen, dependency-driven experiments, each answering a question raised by the previous one, under a strict leakage-aware protocol that isolates internal synthetic validity from external benchmark transfer on the public OULAD dataset. The framework is designed to produce accurate, reproducible, and interpretable insight into learning achievements suitable for both research and teacher-facing decision support, while remaining explicit about the boundaries of what synthetic evidence and model-behavior explanations can claim.

## Literature Review

Student-performance prediction has become an active sub-field of educational data mining, and recent systematic reviews establish its scope, conventions, and recurring variable families. Alalawi, Athauda, and Chiong survey machine learning for student-performance prediction and confirm that the field is dominated by *tabular* supervised learning, while interpretability and actionability remain underdeveloped relative to raw predictive accuracy [1]. Yağcı reports that classical machine-learning algorithms predict academic performance from prior assessment and engagement features with competitive accuracy, reinforcing the tabular framing of the task [2]. Complementing prediction, learning-analytics research shows that teacher- and learner-facing dashboards improve awareness but often remain descriptive, motivating platforms that fold prediction and explanation into the same actionable interface [3]. These results justify framing the task as tabular regression on a continuous achievement target and treating interpretability and platform integration as first-class requirements.

A second strand concerns the *digital-twin* paradigm. Recent surveys describe a digital twin as a dynamic, bidirectionally linked virtual representation of a physical entity that supports monitoring, prediction, and what-if reasoning, and they trace its diffusion from manufacturing into data-rich service domains [4]. This study adapts the general concept to education by representing each learner as a weekly student-state snapshot rather than a static record, so the twin can be queried before the course ends.

A third strand concerns the *model families* appropriate to LMS-derived prediction, which is a tabular problem on medium-sized structured data. Recent benchmark studies show that gradient-boosted and other tree ensembles remain difficult to beat on typical tabular data, and that deep architectures do not consistently outperform them at this scale [5][6]. This evidence justifies a conservative stack of a regularized linear baseline, random forests, and gradient boosting rather than deep models, and it motivates careful baseline comparison before any richer representation is accepted.

A fourth strand concerns *explainability*, treated here as an integrated platform component rather than a decorative add-on. In education specifically, Khosravi et al. argue that explanations must be designed for stakeholders such as teachers and learners, not only for model developers, and they map the explanation dimensions relevant to educational decision support [7]. Broad XAI surveys catalogue post-hoc methods — including feature-importance and local perturbation techniques such as permutation importance, LIME, and SHAP — and stress the persistent distinction between describing *model behavior* and recovering *causal mechanism* [8][9]. We adopt model-behavior explanations and preserve that distinction explicitly.

A fifth strand concerns *evaluation discipline and reproducibility*. Kapoor and Narayanan document that data leakage is a widespread cause of over-optimistic, irreproducible results in machine-learning-based science, and they recommend grouped or temporal evaluation, train-only preprocessing, and transparent reporting [10]. We therefore adopt student-grouped and temporal-forward splits with train-only preprocessing and forbidden-column enforcement, and we bind every result to a frozen experiment artifact. For external transfer we use the public OULAD dataset, a large anonymized record of LMS activity and outcomes across module-presentations [11]. Despite this body of work, an integrated educational platform that constructs, ablates, validates, *and* explains a lean student digital twin under a single leakage-aware protocol — and surfaces the result to teachers through a reproducible data flow with a public-benchmark stress test — remains absent. This study addresses that gap.

## Methodology

### 3.1 Platform Architecture and Data Flow

The platform is a modular monorepo organized around five components: a **web application** (Next.js) providing the teacher-facing interface; an **API service** (FastAPI) exposing domain read endpoints; a local **application store** (SQLite) holding generated persistence; an **ML/analytics service** (Python) for data generation, experiments, inference, and explainability; and a **contracts package** holding the versioned schema shared across services. The runtime data flow is deterministic and traceable: the ML service generates synthetic LMS-like data and weekly Twin snapshots; frozen experiments write evidence under `data/artifacts/experiments/`; an export script reshapes that evidence into a deterministic research payload; the API importer loads the payload into a SQLite application store; FastAPI serves teacher-facing dashboard, student, Twin, prediction, explanation, and research-evidence endpoints; and the Next.js client consumes those endpoints at runtime. This projection neither rewrites the active schema (`schema_v1.2`) nor reruns prior experiments, so the interface always reflects frozen, auditable evidence. The teacher-facing UI presents cohort dashboards, a student list, per-student Twin views, final-grade predictions, and explanation panels. Consistent with its research-prototype scope, the current platform is read-only and intentionally excludes authentication and roles, live LMS integration, online retraining, and production deployment hardening; these are documented as out of scope.

### 3.2 Data Collection

The primary development corpus is a synthetic but structurally realistic LMS-like dataset governed by a versioned data contract (`schema_v1.2`) and produced by a reproducible generator (`generator_v1_3_refined.yaml`, seed `42`). The dataset models one programming course over a ten-week structure with weekly topics, assignments, quizzes, attendance, activity logs, and a final result, organized into three conceptual layers: raw LMS-like tables; processed *student twin snapshots* at the grain `1 row = 1 student × 1 week`; and prediction and explanation artifacts. After restricting snapshots to the early-warning window (weeks `4..10`), the synthetic modeling table contains **798 rows across 114 students**, with primary target `final_grade` (mean `62.41`, SD `20.62`) and secondary label `passed` (positive rate `0.781`); the cohort spans four behavioral trajectory archetypes — *stable-high* (26 students), *declining* (33), *improving* (30), and *consistently-at-risk* (25). To separate internal from external validity, a strictly held-out **public benchmark** is used only at the transfer stage and is never used to tune the synthetic pipeline: the OULAD module-presentation `DDD 2013J` is adapted into weekly rows (`1 student-presentation × 1 week`, weeks `4..38`), yielding **67,830 rows across 1,938 students**. Its derived target `final_weighted_score` is computed from assessment weights and student assessment scores and is documented as comparable but not identical to the synthetic `final_grade`, while `passed_observed` maps OULAD `Pass`/`Distinction` to positive and `Fail`/`Withdrawn` to negative.

### 3.3 Digital Twin Feature Representation

Features are organized as a **nested, hypothesis-driven hierarchy** so the contribution of the Twin layer can be isolated (Table 1). All mastery features are constructed strictly from submission scores filtered to `week_number ≤ snapshot week` and never read end-of-course outcomes, ensuring temporal causality. For OULAD, an analogous `B_lms_oulad` / `B_lms_plus_mastery_oulad` pair is built from assessment-structure mastery proxies (due-to-date weighted mastery, assessment-cluster and assessment-type mastery, and coverage context).

**Table 1.** Nested feature-set hierarchy and ablation blocks.

| Feature set | Contents | Methodological role |
|---|---|---|
| `A_simple` | minimal teacher-visible academic signals | performance floor |
| `B_lms` | + cumulative performance, attendance, submission discipline, activity/engagement | strong non-Twin baseline |
| `C_twin` | + short-term trends, mastery, composite indices, temporal context | full Twin hypothesis |
| Ablation blocks | `B_lms` + one of {trends, mastery, indices, temporal} and {trends + mastery} | per-block marginal value |

### 3.4 Predictive Model Development

The platform's analytics engine is validated through five experiments run as a single dependency-driven arc, each freezing its configuration, metadata, and artifacts:

- **`exp_001_baseline`** — compares `A_simple`, `B_lms`, and `C_twin` to test whether the full Twin representation improves over simpler baselines.
- **`exp_002_twin_ablation`** — decomposes the Twin layer to identify which subgroup, if any, adds value beyond `B_lms`.
- **`exp_003_mastery_validation`** — audits the selected mastery block for genuine signal versus proxy redundancy, with per-week, correlation, drop-column, and temporal-lineage diagnostics.
- **`exp_004_xai_on_lean_twin`** — explains the validated lean candidate and tests whether model behavior collapses onto a single feature.
- **`exp_005_public_benchmark_oulad`** — stress-tests whether the lean mastery-centered representation logic transfers to OULAD.

The model stack is deliberately conservative and interpretable. Regression uses a regularized linear baseline (the config label `linear_regression` resolves to **Ridge**, preferable under correlated features), `RandomForestRegressor`, and `GradientBoostingRegressor`. Classification uses `LogisticRegression`, `RandomForestClassifier`, and `GradientBoostingClassifier`. The supervised targets are `final_grade` (primary) and `passed` (secondary context); the teacher-facing heuristic `risk_level` is **excluded** as a training target to avoid the tautology of supervising a model on a hand-designed rule derived from the same snapshot features. Evaluation uses a primary **student-grouped split** (`GroupShuffleSplit`, `test_size = 0.25`, seed `42`) and a secondary **temporal-forward split** (train on early weeks, test on later weeks, with held-out students), preventing both identity and future leakage [10]. Preprocessing is train-only: median imputation with missingness indicators, and standardization applied to linear models only; forbidden columns (identifiers, end-of-course outcomes, heuristic risk fields, predicted-outcome columns, and generation-only latent variables) are enforced out of the model matrix.

### 3.5 Explainable AI Integration

Explainability is integrated as a core platform capability, applied only after a predictively useful and structurally credible representation has been identified. Global explanations use held-out **permutation importance** (15 repeats on negative RMSE) supplemented by tree-native importance; local explanations use **one-feature-at-a-time replacement with the training median** on five deterministically selected representative cases (`strong_performer`, `at_risk`, `improving_trajectory`, `declining_trajectory`, `borderline_medium`) [9]. A dedicated dominance audit checks whether explanations collapse onto a single feature. SHAP is intentionally not used, as it lies outside the current dependency contract; consequently, all explanations are reported as **directional model-behavior descriptions, not causal claims** [8], and are surfaced to teachers through per-student explanation panels so that a predicted achievement can be interpreted in terms of its contributing factors.

### 3.6 Evaluation Metrics

- Regression: **MAE**, **RMSE** (primary decision metric, in target units), and **R²**.
- Classification: **Precision**, **Recall**, **F1-score**, **ROC-AUC**, and accuracy (descriptive).
- Per-week RMSE deltas to assess early-warning behavior (weeks `4..10`, early window `≤ 6`).
- Diagnostic measures: Pearson correlation of features with the target, mastery-vs-LMS redundancy correlations, and drop-column RMSE effects.
- Confusion-matrix and feature-importance reporting per feature set, per model, per split.

### 3.7 Tools and Libraries

ML/analytics service: Python with scikit-learn (model families, splitters, metrics, permutation importance), pandas and NumPy (data handling), PyArrow (snapshot storage), Pydantic and PyYAML (schema contracts and frozen configs), and pytest (pipeline and metadata tests). Platform layer: FastAPI (API service), SQLite (application store), and Next.js with React and TypeScript (teacher-facing web application). Every experiment is bound to an experiment ID, a frozen YAML config, an `experiment_metadata.json` record, machine-readable CSV/JSON result artifacts, and a per-experiment Markdown summary, in line with reproducibility and leakage-avoidance guidance [10].

## Results

The five-experiment line that powers the platform's analytics engine supports a bounded but consistent interpretation, summarized by primary student-grouped RMSE unless otherwise stated.

**Internal synthetic comparison (`exp_001_baseline`, `exp_002_twin_ablation`).** The full Twin set did not beat the LMS baseline on the primary split and degraded sharply under the temporal-forward split, while a structured ablation showed that only the mastery block produced a substantive gain over `B_lms` (Table 2). Under the temporal-forward split the mastery advantage was not established (Δ `+0.006`, essentially level); `A_simple`, `B_lms`, and `C_twin` reached RMSE `2.210`, `2.270`, and `2.937` respectively, and the `passed` task saturated at F1 = `1.000` for every feature set under both splits. The correct response was therefore to decompose the Twin layer and carry forward only the mastery block, not the full representation.

**Table 2.** Internal synthetic comparison — best regression RMSE on the primary student-grouped split (lower is better; identical setup across `exp_001_baseline` and `exp_002_twin_ablation`).

| Feature set | Primary RMSE | Δ vs `B_lms` |
|---|---:|---:|
| `B_lms_plus_mastery` (lean Twin) | 1.894 | −0.206 |
| `B_lms_plus_trends_mastery` | 1.973 | −0.127 |
| `B_lms_plus_indices` | 2.035 | −0.066 |
| `B_lms_plus_temporal` | 2.078 | −0.023 |
| `B_lms_plus_trends` | 2.096 | −0.005 |
| `B_lms` (baseline) | 2.101 | +0.000 |
| `C_twin` (full Twin) | 2.149 | +0.049 |
| `A_simple` | 2.673 | +0.572 |

**Mastery validated with a redundancy caveat (`exp_003_mastery_validation`).** The lean candidate improved on the baseline at weeks `4–8` (three inside the early-warning window `≤ 6`) and was level at weeks `9–10`, supporting the early-detection framing. However, `overall_mastery` is highly redundant with cumulative assessment performance — it correlates with `final_grade` at Pearson `r = 0.984` and with `avg_assignment_score_to_date` at `|r| = 0.993`, and it is the dominant single contributor (drop-column ΔRMSE `+0.228`, versus only `+0.036` for `current_topic_mastery`). Mastery is therefore a defensible lean component but must be reported as a topic-level aggregation of cumulative score behavior, not an independent construct.

**Lean Twin remained interpretable (`exp_004_xai_on_lean_twin`).** Explaining the lean candidate (RMSE `1.894`, MAE `1.510`, R² `0.992`, versus `2.101` / `1.681` / `0.990` for `B_lms`; removing `overall_mastery` returns it to `2.122` / `1.686` / `0.990`), global permutation importance ranked `activity_score_to_date` first (importance share `0.648`), `overall_mastery` second (`0.178`), and `avg_assignment_score_to_date` third (`0.090`). The dominance audit returned `acceptable_with_caveat`: the average local mastery contribution share across the five representative cases was `0.194`, well below the `0.60` warning threshold, and the explanations did not collapse onto a single feature.

**OULAD complicated external transfer (`exp_005_public_benchmark_oulad`).** On the public benchmark the mastery analogue was slightly worse on the primary grouped split but better on the temporal-forward split (Table 3); secondary classification was nearly level (grouped F1 `0.861` vs. `0.863`; temporal-forward `0.884` vs. `0.887`). OULAD therefore neither confirms a general mastery advantage nor invalidates the internally validated synthetic result; transfer depends on dataset structure, assessment timing, and missingness.

**Table 3.** OULAD external benchmark — best RMSE by split (`exp_005_public_benchmark_oulad`; module-presentation `DDD 2013J`; best model gradient boosting in all cells).

| Feature set | Primary (grouped) RMSE | Temporal-forward RMSE |
|---|---:|---:|
| `B_lms_oulad` | 12.658 | 9.566 |
| `B_lms_plus_mastery_oulad` | 12.724 | 9.161 |
| Δ vs `B_lms_oulad` | +0.066 | −0.406 |

**Summary.** The study delivers an intelligent educational platform that integrates a Student Digital Twin and an Explainable AI layer to analyze and interpret learning achievements through a reproducible, teacher-facing data flow. Its analytics engine is grounded in disciplined evidence: under the present synthetic environment, the full Digital Twin was not justified relative to a stronger LMS baseline, a compact mastery-centered subset (`B_lms_plus_mastery`) delivered measurable predictive value on the primary split and at early weeks, the lean representation stayed interpretable under documented model-behavior methods with redundancy and dominance caveats preserved, and the OULAD benchmark complicated external transfer. The contribution is therefore a methodologically disciplined platform integrating a lean Twin and XAI for academic-achievement analytics — not a proof of full Digital Twin superiority, and not an institutional validation. Authenticated multi-user access, live LMS integration, and validated intervention/scenario simulation remain future work, to be validated before any causal or recommendation claim is made.

## References

[1] K. Alalawi, R. Athauda, and R. Chiong, "Contextualizing the current state of research on the use of machine learning for student performance prediction: a systematic literature review," *Engineering Reports*, vol. 5, no. 12, art. e12699, 2023.

[2] M. Yağcı, "Educational data mining: prediction of students' academic performance using machine learning algorithms," *Smart Learning Environments*, vol. 9, no. 1, art. 11, 2022.

[3] T. Susnjak, G. S. Ramaswami, and A. Mathrani, "Learning analytics dashboard: a tool for providing actionable insights to learners," *International Journal of Educational Technology in Higher Education*, vol. 19, no. 1, art. 12, 2022.

[4] S. Mihai, M. Yaqoob, D. V. Hung, W. Davis, P. Towakel, M. Raza, M. Karamanoglu, B. Barn, D. Shetve, R. V. Prasad, H. Venkataraman, R. Trestian, and H. X. Nguyen, "Digital twins: a survey on enabling technologies, challenges, trends and future prospects," *IEEE Communications Surveys & Tutorials*, vol. 24, no. 4, pp. 2255–2291, 2022.

[5] R. Shwartz-Ziv and A. Armon, "Tabular data: deep learning is not all you need," *Information Fusion*, vol. 81, pp. 84–90, 2022.

[6] L. Grinsztajn, E. Oyallon, and G. Varoquaux, "Why do tree-based models still outperform deep learning on typical tabular data?" in *Proc. 36th Conf. Neural Information Processing Systems (NeurIPS), Datasets and Benchmarks Track*, 2022.

[7] H. Khosravi, S. B. Shum, G. Chen, C. Conati, Y.-S. Tsai, J. Kay, S. Knight, R. Martinez-Maldonado, S. Sadiq, and D. Gašević, "Explainable artificial intelligence in education," *Computers and Education: Artificial Intelligence*, vol. 3, art. 100074, 2022.

[8] S. Ali, T. Abuhmed, S. El-Sappagh, K. Muhammad, J. M. Alonso-Moral, R. Confalonieri, R. Guidotti, J. Del Ser, N. Díaz-Rodríguez, and F. Herrera, "Explainable artificial intelligence (XAI): what we know and what is left to attain trustworthy artificial intelligence," *Information Fusion*, vol. 99, art. 101805, 2023.

[9] C. Molnar, *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable*, 2nd ed., 2022. [Online]. Available: https://christophm.github.io/interpretable-ml-book/

[10] S. Kapoor and A. Narayanan, "Leakage and the reproducibility crisis in machine-learning-based science," *Patterns*, vol. 4, no. 9, art. 100804, 2023.

[11] J. Kuzilek, M. Hlosta, and Z. Zdrahal, "Open University Learning Analytics dataset," *Scientific Data*, vol. 4, art. 170171, 2017.
