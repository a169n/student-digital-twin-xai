# Research Internship Report — Scientific Research Proposal

---

## Part 1: Research Proposal

**Title:** A Student Digital Twin with Explainable AI for Teacher-Oriented Academic Risk Analytics

---

### 1. Subject Area and Problem Identification

This research sits at the intersection of educational data mining, learning analytics, and explainable artificial intelligence (XAI). Existing Learning Management System (LMS) analytics tools aggregate student activity into static dashboards that reflect past behavior rather than modeling a student's evolving academic state. As a result, educators receive retrospective summaries instead of timely, interpretable signals suited to early intervention. The core problem is: *how can a student's dynamic academic state be represented in a way that is both predictively useful and transparently explainable to a non-technical teacher?*

---

### 2. Theoretical Background

The theoretical foundation draws from three bodies of literature. First, student-performance prediction research consistently identifies academic performance, behavioral engagement, and mastery progression as the most informative feature families for predicting course outcomes. Second, the Digital Twin paradigm — originally developed in engineering — offers a model for maintaining a continuously updated virtual representation of a real-world entity; applied to education, this translates to weekly learner-state snapshots constructed from observable LMS data. Third, recent XAI reviews in STEM education confirm that permutation-based and perturbation-based explanation methods can produce teacher-meaningful feature attributions for grade and risk models. Human-centered learning analytics principles further require that such systems prioritize stakeholder trust, transparency, and actionability over predictive complexity.

---

### 3. Research Problem Definition

Current LMS-based analytics lack a structured, time-aware learner-state representation that supports both accurate prediction of final academic outcomes and interpretable, teacher-facing explanations. Three research questions guide the investigation:

1. Does a Student Digital Twin representation improve prediction of end-of-course grades beyond a standard LMS analytics baseline?
2. Which feature groups within the Twin representation contribute most to predictive gains, and is a compact subset sufficient?
3. Can the selected model's predictions be explained in a form that remains meaningful for teacher decision-making across course weeks?

---

### 4. Research Methods

The study follows a structured experimental sequence. A synthetic dataset — organized at the grain of one observation per student per week — is generated to simulate a 10-week programming course. Six feature groups are constructed: academic performance, engagement, discipline, mastery progression, temporal trends, and course-internal context. Predictive models are evaluated under two validation strategies: a student-grouped split (to assess within-cohort generalization) and a temporal-forward split (to assess early-warning utility). Feature-block ablations systematically compare a minimal performance baseline, a full LMS feature set, and a full Digital Twin representation, ultimately identifying a compact Twin subset centered on mastery progression as the best-performing configuration. The primary evaluation metric is Root Mean Squared Error (RMSE) of the predicted final grade. For explainability, permutation importance and local perturbation-based explanations are applied to identify which features drive individual predictions. An external validation is conducted on a publicly available real-world dataset — the Open University Learning Analytics Dataset (OULAD) — to stress-test the generalizability of the proposed representation.

---

### 5. Ethical Considerations

Several ethical constraints are addressed by design. The research uses entirely synthetic data, removing direct privacy risks, though synthetic generation may still reproduce structural biases and this is documented as a limitation. All demographic-sensitive variables — such as ethnicity, socioeconomic status, and gender — are excluded as a deliberate risk-minimization measure. The system is framed strictly as decision support for teachers, not as an automated judgment tool; the XAI layer is intended to preserve human agency. Explanation outputs are presented as directional model-behavior descriptions, not causal claims, to prevent misuse in high-stakes academic decisions.

---

### 6. Project Scope and Timing

| Phase | Activity | Timeline |
|---|---|---|
| 1 | Data schema design, synthetic generation, realism audit | Weeks 1–2 |
| 2 | Baseline modeling and feature-block ablation | Weeks 3–5 |
| 3 | Mastery block validation and XAI explanation phase | Weeks 6–8 |
| 4 | External benchmark on public real-world dataset | Weeks 9–10 |
| 5 | Synthesis, dissertation write-up, and dissemination | Weeks 11–12 |

The expected output is a teacher-oriented lean Twin and XAI research prototype with reproducible artifacts and a bounded set of empirical conclusions suitable for a master's dissertation defense.

---

## Part 2: Data Collection Methods, Sources, Volume, and Characteristics

---

### 1. Data Collection Methods

The research employed two data collection methods:

**Method 1 — Controlled Synthetic Data Generation (Primary)**
Because no real institutional student dataset was available, a structured synthetic dataset was generated algorithmically. Data was not collected from real students but was designed to simulate realistic LMS-like learning behavior. Each synthetic student was assigned hidden generation parameters — including baseline academic level, motivation, discipline, and overall trajectory type — to produce structurally plausible variation across the cohort. After generation, realism audits were conducted to verify that grade distributions, activity patterns, correlation structures, and risk-label proportions matched expected educational behavior.

**Method 2 — Secondary Use of a Public Archival Dataset (External Benchmark)**
The Open University Learning Analytics Dataset (OULAD) — a publicly available real-world dataset from the UK — was used for external validation. A single module-presentation subset was selected to test whether the representation logic developed on synthetic data transferred to a real student cohort.

---

### 2. Data Sources

| Source | Type | Purpose |
|---|---|---|
| Custom synthetic generator | Primary, synthetic | Main modeling and all internal experiments |
| OULAD — Open University, UK | Secondary, real-world archival | External generalizability stress-test |

---

### 3. Volume of Data Collected

**Synthetic dataset:**

| Parameter | Value |
|---|---|
| Total students in cohort | 114 |
| Course duration | 10 weeks |
| Modeling observations (weeks 4–10) | 798 rows |
| Raw source tables | 8 tables |
| Processed weekly snapshot table | 1 table (1 row = 1 student × 1 week) |

**Student trajectory distribution (synthetic):**

| Trajectory type | Students | Observations |
|---|---|---|
| Stable high performer | 26 | 182 |
| Declining | 33 | 231 |
| Improving | 30 | 210 |
| Consistently at risk | 25 | 175 |

**OULAD benchmark:** one module-presentation subset covering weeks 4 through 38.

---

### 4. Data Characteristics and Parameters

**Prediction targets:**

| Variable | Type | Statistics |
|---|---|---|
| Final grade | Continuous (regression target) | Mean: 62.41, Std: 20.62, range 0–100 |
| Passed | Binary (classification target) | 78.1% positive rate |
| Risk level | Categorical heuristic label (Low / Medium / High) | Teacher-facing indicator, not used as ML target |

**Feature structure — 18 features across 6 blocks:**

| Block | Description |
|---|---|
| Academic performance | Cumulative assignment and quiz score averages; recent score trend |
| LMS engagement | Cumulative platform activity score; total time spent; recent activity trend |
| Attendance | Cumulative attendance rate; recent attendance trend |
| Submission discipline | On-time submission rate; count of missed and late assignments |
| Mastery progression | Topic-level mastery estimate; overall running mastery proxy |
| Composite indices | Weighted engagement, performance, and discipline index; continuous risk score |

**Top predictive features — Pearson correlation with final grade:**

| Feature | r |
|---|---|
| Performance index (weighted composite) | 0.986 |
| Overall mastery proxy | 0.984 |
| Cumulative activity score | 0.983 |
| Average assignment score to date | 0.982 |
| Average quiz score to date | 0.978 |

**Data quality notes:**
- High inter-feature collinearity was detected between mastery and score-based features (r up to 0.993), documented as a redundancy caveat throughout the experiments.
- Early-course observations contain structural missing values for assessment scores, as no graded items exist yet; these are handled via explicit presence indicators rather than imputation.
- A strict anti-leakage policy was enforced: every weekly feature was computed exclusively from data observable up to that week, with no access to future submissions or end-of-course outcomes.
