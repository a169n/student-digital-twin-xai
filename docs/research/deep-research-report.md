# Methodology for Student Digital Twin Dataset Design

## Executive Summary

We justify the v1 dataset as an **operationalization** of a teacher-facing Student Digital Twin rather than an ad hoc collection of columns. Recent reviews of student-performance prediction consistently group predictors into academic, behavioral or engagement, and contextual families, while recent XAI reviews in education report that academic and behavioral variables remain the dominant inputs for interpretable risk and grade models [1–4]. Canonical public educational datasets reinforce this pattern: OULAD links assessments, student information, registrations, and click interactions, while ASSISTments and KDD Cup data expose prior-correctness, opportunities, hints, and step-level traces [3,9–11]. citeturn6search0turn6search1turn23search3turn14view0turn11search0turn3view10turn9view1

For a v1 research prototype, we therefore recommend a compact two-layer schema: **raw LMS-like tables** plus **weekly `student_twin_snapshots`**, with one row per student per week. The core constructs are academic performance, engagement, discipline, mastery progression, temporal trends, and limited course-internal context. Composite indices and risk labels should be treated as **explicit v1 assumptions**, not validated psychological scales. We also recommend forward-chaining validation, feature-block ablations, fixed random seeds, and explicit ethical constraints for synthetic data, including the exclusion of demographic-sensitive variables unless later evidence justifies them. citeturn3view4turn16view0turn20view0turn21view0turn18view0

## Design Premises

The guiding premise is that a Student Digital Twin should represent a **small set of theoretically meaningful constructs** rather than a large convenience-driven schema. Across recent reviews, student-success models are typically built from combinations of academic records, behavioral traces, and contextual variables, and feature selection remains a major determinant of model quality [1,2,7,8]. A recent XAI review focused on CS and STEM education likewise reports that behavioral and academic-performance data are the most common feature families, and that common targets are course-failure risk and grades [3]. Because teacher-facing interpretation matters, we also align the design with human-centered learning analytics principles that emphasize trust, reliability, and stakeholder relevance [4]. citeturn6search0turn6search1turn20view0turn21view0turn23search3turn14view0

We adopt three explicit assumptions for v1. **Assumption A1:** no institutional real dataset is available, so synthetic data will be used. **Assumption A2:** the prototype targets one programming course with a 10-week weekly structure. **Assumption A3:** demographic-sensitive variables are excluded from v1 unless later evidence shows that they are necessary and ethically justified. These assumptions narrow scope deliberately. Recent work shows that the relationship between LMS interactions and performance depends on course delivery mode and instructional design, so a single-course design is methodologically cleaner for an initial prototype [5,6]. The exclusion of demographic-sensitive variables in v1 is a design choice grounded in risk minimization and human-centered deployment, not a claim that such variables are never predictive. citeturn3view4turn16view0turn14view0turn18view0

## Constructs and Feature Mapping

Public educational datasets provide a practical template for measurable features. OULAD introduced a student-centered multi-table structure linking courses, assessments, student results, registrations, VLE resources, and click interactions, which makes it especially useful for defining raw LMS-like tables [9]. ASSISTments documentation exposes cumulative proficiency variables such as `prior_correct`, `prior_problem_count`, `prior_percent_correct`, and `problem_count`, while the KDD Cup 2010 student-performance datasets expose step-level correctness, opportunities, hints, and durations [10,11]. Together, these sources suggest that a useful educational dataset should separate **raw events** from **derived learner-state indicators** rather than collapsing everything into a single wide table. citeturn11search0turn3view10turn9view1

On that basis, we recommend two v1 layers. The **raw layer** should include `students`, `courses`, `course_topics`, `assignments`, `attendance`, `submissions`, `weekly_activity`, and `final_results`. The **processed layer** should contain `student_twin_snapshots`, with **one row per student per week**. This preserves provenance and keeps the twin interpretable: teachers can inspect both the originating LMS-like evidence and the derived state. Weekly snapshots are preferable to event-level streams in v1 because early-warning research shows that relatively simple, time-dependent LMS representations can offer a good trade-off between predictive performance, portability, and implementation simplicity [5]. For course context, we keep only non-sensitive, course-internal variables such as week number, topic difficulty, assignment type, and due-load; recent work shows that the explanatory power of LMS traces depends on the learning cycle and instructional design, which supports limited context features without expanding into sensitive demographics [6]. citeturn3view4turn16view0turn11search0

## Provisional v1 Definitions

The recommended v1 feature set follows six constructs. **Academic performance** is represented by assignment, quiz, and exam signals and by cumulative means. **Engagement** is represented by attendance, login frequency, materials accessed, and time spent. **Discipline** is represented by missed assignments, late submissions, and the on-time submission rate. **Mastery progression** is approximated at the topic level using recent correctness on topic-linked quizzes and assignments. **Temporal trends** capture short-window changes in score, activity, and attendance. **Contextual factors** are limited to course-internal signals such as topic difficulty and assessment load. This choice is consistent with recent feature-selection work showing that behavioral characteristics are highly informative and that feature engineering materially affects predictive performance [7,8]. It is also aligned with public datasets and applied LMS studies that use engagement patterns, time spent, progress tracking, assignment marks, and examination signals as practical predictors [9–11,15,17]. citeturn20view0turn21view0turn11search0turn3view10turn9view1turn14view3turn17view0

We therefore define the following **provisional v1 composite indicators** as transparent, teacher-readable assumptions rather than validated psychometric scales:

1. `engagement_index = 0.40·attendance_rate_to_date + 0.30·normalized(activity_score_to_date) + 0.30·on_time_submission_rate_to_date`
2. `performance_index = 0.50·normalized(avg_assignment_score_to_date) + 0.30·normalized(avg_quiz_score_to_date) + 0.20·overall_mastery`
3. `discipline_index = 0.50·on_time_submission_rate_to_date + 0.30·(1 − normalized(late_submissions_to_date)) + 0.20·(1 − normalized(missed_assignments_to_date))`
4. `risk_score = 0.30·(1 − performance_index) + 0.25·(1 − engagement_index) + 0.20·(1 − discipline_index) + 0.15·normalized(missed_assignments_to_date) + 0.10·negative_trend_penalty`

A practical v1 mapping is `risk_level ∈ {low, medium, high}` using dataset-specific thresholds, for example `<0.40`, `0.40–0.69`, and `≥0.70`; these thresholds should be recalibrated after observing synthetic distributions. For synthetic target derivation, we recommend `final_grade` as a weighted end-of-course outcome derived from assessments, quizzes, attendance or completion, and any final assessment; `passed` is then derived from the course pass threshold. This keeps `risk_level` as the **primary target** and `final_grade` as the **secondary target** while preserving a coherent teacher-facing interpretation [3,14,15]. citeturn23search3turn24view2turn14view3

## Validation and Ablation Design

Feature usefulness should be tested empirically rather than assumed. We recommend three validation layers. First, validate **schema and realism**: expected row counts, key uniqueness, permissible ranges, and distributional checks for grades, lateness, activity, and risk labels. Second, validate **predictive utility** with forward-chaining evaluation by week: at week *t*, train or score using only information available by week *t*, then predict `final_grade` and `risk_level`. Third, validate **interpretability and feature usefulness** through ablation and explanation-stability analysis. This is consistent with recent work on feature selection in student-performance prediction and with recent XAI work that evaluates explanation stability under changing contexts [5,7,8,16]. citeturn3view4turn20view0turn21view0turn25search0

The ablation plan should remain compact:

1. **Performance-only baseline:** scores and quiz features only.
2. **Add the engagement block:** attendance and LMS activity.
3. **Add the discipline block:** lateness, missed work, on-time rate.
4. **Add the mastery block:** topic-level mastery features.
5. **Add the temporal block:** recent trend features.
6. **Raw features vs. derived indices:** compare raw LMS variables against twin indices and against the combined set.
7. **Context on/context off:** add week number, topic difficulty, and due-load to test whether limited context improves calibration.

Model comparison can begin with transparent baselines such as logistic regression and decision trees, followed by tree ensembles. For `risk_level` we recommend macro-F1, balanced accuracy, and calibration; for `final_grade`, MAE and RMSE. For XAI, we recommend checking whether the top global features remain reasonably stable across folds or weeks, following recent work that uses SHAP not only for explanation but also for feature-stability analysis under changing learning contexts [16]. citeturn25search0

## Reproducibility and Ethical Notes

Because v1 uses synthetic data, reproducibility must be designed in from the start. We recommend versioned schema contracts, fixed random seeds, configuration-controlled generation, and release of generation assumptions alongside the dataset. Synthetic educational data are methodologically defensible when real institutional data are unavailable, but they must be **validated rather than assumed** to be safe or realistic. Recent work on synthetic student data shows that correlation analysis, density comparison, heatmaps, and dimensionality checks can be used to assess whether generated data preserve useful structure [12]. citeturn3view6

Ethically, synthetic data are not a privacy silver bullet. Synthetic generation can still preserve sensitive relationships from source data, can amplify existing biases, and always creates a privacy–fidelity trade-off that must be documented [13]. We therefore recommend that v1 avoid demographic-sensitive predictors, document intended users and actions, and state explicitly that the system is **decision support for teachers** rather than automated judgment. Human-centered reviews in learning analytics emphasize stakeholder agency, trustworthiness, and end-user relevance; these principles are directly applicable to a teacher-facing Student Digital Twin with XAI [4]. citeturn18view0turn14view0

## Experimental Pipeline

The accompanying `.docx` already embeds the pipeline image as a PNG. If the diagram needs to be revised later, the Mermaid specification below can be rendered again and reinserted into the Word file.

```mermaid
flowchart LR
    A[Schema contract and assumptions] --> B[Raw LMS-like generation]
    B --> C[Weekly aggregation]
    C --> D[Student twin snapshots]
    D --> E[Baseline models]
    E --> F[XAI explanations]
    F --> G[Ablation and validation]
    G --> H[Teacher-facing interpretation]
```

## Appendix

### Construct-to-feature mapping

The table below operationalizes the six constructs in a way that is consistent with recent reviews, public datasets, and interpretable teacher-facing analytics [1–11,15–17]. citeturn6search0turn6search1turn23search3turn11search0turn3view10turn9view1turn14view3turn17view0turn25search0

| Construct | Candidate raw LMS-like features | Candidate derived twin features | Why retained in v1 |
|---|---|---|---|
| Academic performance | `assignment_score`, `quiz_score`, `exam_score`, assessment type/weight | `avg_assignment_score_to_date`, `avg_quiz_score_to_date`, `predicted_final_grade` | Core predictor family; teacher-actionable and easy to explain |
| Engagement | `attendance`, `login_count`, `materials_opened`, `time_spent_minutes` | `attendance_rate_to_date`, `activity_score_to_date`, `engagement_index` | Common LMS-trace predictors for early warning |
| Discipline | `submitted`, `submitted_on_time`, `days_late`, missed work | `on_time_submission_rate_to_date`, `late_submissions_to_date`, `discipline_index` | Operationalizes task compliance in intervention-friendly terms |
| Mastery progression | `topic_id`, item correctness, `prior_correct`, opportunity, hints | `current_topic_mastery`, `overall_mastery` | Inspired by ASSISTments/KDD skill-opportunity logic; approximates knowledge state without full knowledge tracing |
| Temporal trends | `week_no`, dated interactions, dated submissions | `score_trend_last_3_weeks`, `activity_trend_last_3_weeks`, `attendance_trend_last_3_weeks` | Early-warning value depends on change over time |
| Contextual factors | `week_no`, `topic_difficulty`, `assignment_type`, `due_load` | context tags or normalized load indicators | Keep limited and course-internal in v1; sensitive context excluded by assumption |

## Recommended Next Steps

1. Freeze `schema_v1.0` and the field-level data dictionary before any data generation.
2. Implement the synthetic generator with raw LMS-like tables and weekly `student_twin_snapshots`.
3. Add schema-aware validation and descriptive realism checks.
4. Train week-by-week baseline models and run the planned ablations.
5. Add SHAP-based global and local explanations only after the baseline feature blocks are validated.

## References

Recent sources were prioritized where possible. Older sources are retained only when they are canonical public dataset references.

1. Xiao, W., Ji, P., & Hu, J. 2022. *A survey on educational data mining methods used for predicting students’ performance*. *Engineering Reports*, 4, e12482. URL: `https://onlinelibrary.wiley.com/doi/full/10.1002/eng2.12482` citeturn6search0
2. Albreiki, B., Zaki, N., & Alashwal, H. 2021. *A Systematic Literature Review of Student’ Performance Prediction Using Machine Learning Techniques*. *Education Sciences*, 11(9), 552. URL: `https://www.mdpi.com/2227-7102/11/9/552` citeturn6search8
3. Choi, W.-C., Lam, C.-T., Pang, P. C.-I., & Mendes, A. J. 2025. *A Systematic Literature Review of Explainable Artificial Intelligence (XAI) for Interpreting Student Performance Prediction in Computer Science and STEM Education*. *Proceedings of the 30th ACM Conference on Innovation and Technology in Computer Science Education*, 221–227. URL: `https://doi.org/10.1145/3724363.3729027` citeturn23search9turn23search3
4. Alfredo, R., Echeverria, V., Jin, Y., Yan, L., Swiecki, Z., Gašević, D., & Martinez-Maldonado, R. 2024. *Human-centred learning analytics and AI in education: A systematic literature review*. *Computers and Education: Artificial Intelligence*, 6, 100215. URL: `https://doi.org/10.1016/j.caeai.2024.100215` citeturn14view0
5. Santos, R. M., & Henriques, R. 2023. *Accurate, timely, and portable: Course-agnostic early prediction of student performance from LMS logs*. *Computers and Education: Artificial Intelligence*, 5, 100175. URL: `https://doi.org/10.1016/j.caeai.2023.100175` citeturn3view4
6. Hernández-García, Á., Cuenca-Enrique, C., Del-Río-Carazo, L., & Iglesias-Pradas, S. 2024. *Exploring the relationship between LMS interactions and academic performance: A Learning Cycle approach*. *Computers in Human Behavior*, 155, 108183. URL: `https://doi.org/10.1016/j.chb.2024.108183` citeturn16view0
7. Yu, S., Cai, Y., Pan, B., & Leung, M.-F. 2024. *Semi-Supervised Feature Selection of Educational Data Mining for Student Performance Analysis*. *Electronics*, 13(3), 659. URL: `https://doi.org/10.3390/electronics13030659` citeturn20view0
8. Hemdanou, A. L., Sefian, M. L., Achtoun, Y., & Tahiri, I. 2024. *Comparative analysis of feature selection and extraction methods for student performance prediction across different machine learning models*. *Computers and Education: Artificial Intelligence*, 7, 100301. URL: `https://doi.org/10.1016/j.caeai.2024.100301` citeturn21view0
9. Kuzilek, J., Hlosta, M., & Zdrahal, Z. 2017. *Open University Learning Analytics dataset*. *Scientific Data*, 4, 170171. URL: `https://www.nature.com/articles/sdata2017171` citeturn11search0
10. ASSISTmentsData. n.d. *An Explanation on how to interpret our data sets*. URL: `https://sites.google.com/site/assistmentsdata/an-explanation-on-how-to-interpret-our-data-sets` citeturn3view10
11. Association for Computing Machinery SIGKDD. 2010. *KDD Cup 2010: Student performance evaluation — Data*. URL: `https://kdd.org/kdd-cup/view/kdd-cup-2010-student-performance-evaluation/Data` citeturn9view1
12. Farhood, H., Joudah, I., Beheshti, A., & Muller, S. 2024. *Advancing student outcome predictions through generative adversarial networks*. *Computers and Education: Artificial Intelligence*, 7, 100293. URL: `https://doi.org/10.1016/j.caeai.2024.100293` citeturn3view6
13. Shanley, D., Hogenboom, J., Lysen, F., Wee, L., Gomes, A. L., Dekker, A., & Meacham, D. 2024. *Getting real about synthetic data ethics*. *EMBO Reports*, 25, 2152–2155. URL: `https://doi.org/10.1038/s44319-024-00101-0` citeturn18view0
14. Islam, M. M., Sojib, F. H., Mihad, M. F. H., Hasan, M., & Rahman, M. 2025. *The integration of explainable AI in Educational Data Mining for student academic performance prediction and support system*. *Telematics and Informatics Reports*, 18, 100203. URL: `https://doi.org/10.1016/j.teler.2025.100203` citeturn24view0
15. Ghimire, S., Abdulla, S., Joseph, L. P., Prasad, S., Murphy, A., Devi, A., Barua, P. D., Deo, R. C., Acharya, R., & Yaseen, Z. M. 2024. *Explainable artificial intelligence-machine learning models to estimate overall scores in tertiary preparatory general science course*. *Computers and Education: Artificial Intelligence*, 7, 100331. URL: `https://doi.org/10.1016/j.caeai.2024.100331` citeturn14view3
16. Tiukhova, E., Vemuri, P., López Flores, N., Islind, A. S., Óskarsdóttir, M., Poelmans, S., Baesens, B., & Snoeck, M. 2024. *Explainable Learning Analytics: Assessing the stability of student success prediction models by means of explainable AI*. *Decision Support Systems*, 182, 114229. URL: `https://doi.org/10.1016/j.dss.2024.114229` citeturn25search0
17. Lam, P. X., Mai, P. Q. H., Nguyen, Q. H., Pham, T., Nguyen, T. H. H., & Nguyen, T. H. 2024. *Enhancing educational evaluation through predictive student assessment modeling*. *Computers and Education: Artificial Intelligence*, 6, 100244. URL: `https://doi.org/10.1016/j.caeai.2024.100244` citeturn17view0