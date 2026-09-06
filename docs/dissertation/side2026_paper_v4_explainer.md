# The Explainer Matters More Than the Data: Instability of Feature Rankings in Student-Risk Models Across Five Institutions

*Anonymous submission — SIDe 2026, Track 1 (Computational Intelligence).*

---

## Abstract

Early-warning systems in education increasingly show teachers not only a risk score but the features that produced it. We ask what that list of features is a property of. On a public benchmark of 63 student cohorts from five universities, five learning-management platforms and four countries, covering 35,529 distinct students, we separate three things that can change a model's feature ranking and measure each on one scale: the explanation method, the training sample, and the institution. Changing the explanation method costs the most. Applied to the *same fitted model on the same students*, permutation importance and SHAP agree at Kendall tau 0.408, permutation and drop-column at 0.258, and SHAP and drop-column at 0.123. For comparison, two models trained on disjoint halves of one cohort agree at 0.338, the same model retrained on the next year's students agrees at 0.210, and a model imported from another institution agrees at 0.034, against a random-ranking expectation of 0.000. A teacher's factor list is therefore shaped more by the library the developer chose than by which students the model was trained on. Predictive accuracy behaves entirely differently across the same comparisons: moving to another institution retains 51 % of the model's above-chance discrimination while the explanation retains 10 % of its attainable agreement. We report the benchmark, the three-way separation, and two controls that shaped the design — a zero-training baseline that a gradient-boosting model fails to beat in 38 of 63 cohorts, and a contamination audit showing that 72 of 78 same-course transfer pairs share students between training and evaluation. Adapters, cohort definitions and frozen results are released.

**Keywords** — explainable AI; learning analytics; feature importance; SHAP; model portability; trustworthy AI; benchmark.

---

## I. Introduction

A student-risk model that outputs only a number is hard to act on, so deployed systems increasingly attach an explanation: the three or five features that most influenced this student's score. The teacher is expected to read that list as a statement about the student — this one is at risk *because* of low forum participation, that one *because* of a long gap since the last login.

For the list to mean that, it has to be a property of the students and their behaviour. It is not obvious that it is. The ranking is produced by a chain — these students, this training sample, this model class, this importance estimator — and any link in the chain could be doing the work.

We separate three of those links and measure each on one scale, using a benchmark assembled for the purpose:

1. **The explanation method**, holding model and data fixed.
2. **The training sample**, holding method and institution fixed: two models fitted to disjoint halves of one cohort, and models retrained on the next year's students.
3. **The institution**, holding method fixed: a model imported from a different university on a different platform.

Our contributions:

- **A public five-institution benchmark** — 63 cohorts, 35,529 distinct students, five LMS platforms, four countries, with adapters and frozen results released (Section III).
- **The three-way separation** of explanation instability, on a single comparable scale with a measured floor, a measured attainable ceiling, and an analytic random baseline (Sections V-A to V-C).
- **The ordering it reveals**: explainer choice destabilises the ranking more than the training sample does (Section V-D).
- **The contrast with accuracy**, which degrades along the same ladder at a fifth of the rate (Section V-A).
- **Two controls that changed our own conclusions** and are reported rather than removed: a zero-training baseline, and a train/test contamination audit (Section V-E).

---

## II. Related Work

**Explanations in learning analytics.** Attaching SHAP or permutation importance to a student-success model is now standard practice, and reviews catalogue hundreds of such systems [4]–[6]. The explanation is normally presented as a finding about students rather than as an estimate with its own error.

**Explanation stability.** Tiukhova et al. showed with SHAP that importance rankings of student-success models shift across cohorts and academic years of one programme [7], establishing that the ranking is not fixed over time. We extend that in two directions they did not take: comparing a *transferred* model's ranking against what a *locally trained* model would say, and comparing *different estimators* on one model. Outside education, Hooker, Mentch and Zhou show that permutation importance evaluates the model off its own data manifold and argue that a defensible estimate requires refitting [8] — the drop-column estimator we adopt as a third arm. Krishna et al. document broad disagreement between explanation methods in general machine learning [9]; whether that disagreement is large or small *relative to the other sources of variation* in a deployed education setting has not been measured, and that comparison is what this paper supplies.

**Portability.** Cross-course and cross-institution transfer of student models is well studied: López-Zambrano et al. across 24 Moodle courses [10], [11]; Gardner et al. across four US universities on private data [12]; Schwerter et al. across two universities [13]; Riestra-González et al. across 532 courses at one institution [14]; Jayaprakash et al. ported an early-alert model between partner institutions as early as 2014 [15]. We use the transfer ladder from this literature as an instrument rather than as a subject: it supplies the widest of our three separations and the accuracy comparison that gives the explanation result its scale.

---

## III. Data, Schema and Task

### A. Five institutions, five platforms

| Institution | Platform | Country | Cohorts | Students |
|---|---|---|---|---|
| Open University — OULAD [1] | OU VLE | UK | 19 | 30,059 |
| Universidad de Oviedo [14] | Moodle 2.x | Spain | 20 | 3,789 |
| Univ. of KwaZulu-Natal [3] | Moodle | South Africa | 16 | 7,254 |
| KU Leuven [2] | Toledo | Belgium | 6 | 3,951 |
| Univ. of Zambia [16] | Moodle | Zambia | 2 | 117 |
| **Total** | | | **63** | **35,529 distinct** |

Cohort sizes sum to 45,170; 21 % of students appear in more than one cohort, which Section V-E shows is not a bookkeeping detail. A cohort is one course, one academic period, one institution, admitted with at least 50 students and 15 in the rarer class. Outcome definitions differ by institution and are perfectly collinear with it, so no analysis here separates a label effect from an institution effect.

### B. Schema and task

Four weekly counters per student — clicks, active days, content clicks, social clicks — yield seven leakage-safe features: four cumulative counters, current-week clicks, active weeks so far, and weeks since last activity. No demographic or assessment feature enters the model; three of the five institutions publish none. Course lengths run from 14 to 46 weeks, so the prediction point is relative: one row per student at week ⌈⅓ × length⌉, repeated at ¼ and ½. The three Moodle institutions publish no course calendar, so an active span is inferred from the log.

---

## IV. Method

### A. The three separations

**Explainer.** One model, fitted once per cohort on two thirds of its students; three importance rankings computed on the held-out third. *Permutation* importance (three repeats, AUC scoring) is the ladder's estimator; *SHAP* is the mean absolute TreeSHAP value per feature [18]; *drop-column* refits the model without each feature and measures the AUC lost, which is what [8] argues a defensible estimate requires.

**Training sample.** Two models fitted to disjoint halves of one cohort and ranked on common data — the attainable ceiling, since nothing differs but the sample. Also the same course in the following year.

**Institution.** A model fitted at one institution, ranked on a target cohort at another, against what a model trained on that target would say.

### B. Metrics and reference points

Agreement is Kendall tau over the seven features and the Jaccard overlap of the top three, so every comparison sits on one scale. Three reference points bound it: a **noise floor**, two rankings of one fitted model differing only in the permutation seed; the **attainable ceiling** above; and an analytic **random baseline** — expected tau 0.000 and expected top-3 Jaccard 0.303 by a hypergeometric argument.

### C. Models

A fixed gradient-boosting classifier [17] (200 trees, depth 3, learning rate 0.05) is the object of study, with logistic regression and random forest as robustness checks. Nothing is tuned per cohort; the question is what an ordinary model does. Accuracy is ROC-AUC, with 5-fold stratified cross-validation within a cohort.

---

## V. Results

### A. Accuracy transfers; the explanation does not

| Separation | ROC-AUC | Explanation agreement (tau) |
|---|---|---|
| Within cohort | 0.691 | ceiling 0.338 (§V-B) |
| Same course, next year | 0.656 | 0.210 |
| Other course, same institution | 0.651 | 0.077 |
| Other institution | 0.597 | 0.034 |

Pairs sharing students between training and evaluation are excluded (§V-E). Put on one scale, moving to another institution leaves the model 51 % of its above-chance discrimination — (0.597 − 0.5) / (0.691 − 0.5) — and 10 % of its attainable explanation agreement, 0.034 of 0.338. The two properties degrade at rates that differ fivefold.

### B. The ceiling: rankings are unstable before anything moves

| Reference point | tau | top-3 Jaccard |
|---|---|---|
| Same model, reseeded (noise floor) | 0.707 | 0.744 |
| Two half-models, ranked on the full cohort | 0.338 | 0.487 |
| Two half-models, ranked on a held-out third | 0.198 | 0.415 |
| Independent random rankings | 0.000 | 0.303 |

Nothing differs between the two half-models but which students they saw. We report the ceiling under two scoring regimes and use the more generous one throughout. Ranking both half-models on the full cohort (0.338) matches how the transfer ladder scores every model and is therefore the comparable figure; scoring them on a held-out third instead is stricter but measures agreement on less data, and gives 0.198. Every ratio in this paper is computed against 0.338, which understates the instability rather than overstating it. The noise floor of 0.707 confirms this is not estimator variance: the same fitted model, re-seeded, is far more self-consistent than two models fitted to halves of one cohort.

### C. The explainer matters more than the data

Applied to one fitted model, on one set of students:

| Pair of explanation methods | tau | top-3 Jaccard |
|---|---|---|
| Permutation vs SHAP | 0.408 | 0.552 |
| Permutation vs drop-column | 0.258 | 0.431 |
| SHAP vs drop-column | **0.123** | 0.389 |

Two standard estimators applied to identical inputs agree at 0.123. That is below the 0.210 achieved by a model retrained on an entirely different year's students, and far below the 0.338 ceiling. The disagreement is not one institution's quirk: the SHAP-versus-drop-column pair ranges only from 0.090 to 0.185 across the five institutions.

### D. The ordering

Ranked by how much each change costs the feature list:

1. **Switching the explanation method** — down to 0.123.
2. **Retraining on another year's students** — 0.210.
3. **Retraining on a disjoint half of the same cohort** — 0.338, the ceiling.
4. **Importing from another institution** — 0.034, the largest single drop, but reached only after the ceiling has already removed two thirds of the available agreement.

The list a teacher sees is therefore determined first by a library choice made once by a developer, and only then by anything about the students. This inverts how such lists are presented and, we argue, how they should be governed: a deployed system should report which estimator produced its explanation and what that choice costs, in the way it already reports a model's accuracy.

### E. Two controls that changed our own conclusions

**A zero-training baseline.** Ranking students by cumulative active days — no model, no training, no labels — reaches AUC 0.713 against 0.692 for a locally trained gradient-boosting model and 0.717 for logistic regression, and beats gradient boosting in 38 of 63 cohorts. This does not bear on the explanation result, but it bounds what the underlying models are: ordinary and unremarkable, which is the condition under which the explanation question is worth asking at all. It also disciplines the reading of Section V-A, since a model that barely beats a sort cannot support strong claims about what its features mean.

**Contamination.** 72 of 78 same-course pairs and 324 of 916 other-course pairs share students between training and evaluation, up to 94 % of the target cohort; cross-institution pairs are clean at under 1.5 %. Uncorrected, same-course transfer appears to *beat* within-cohort performance. Table V-A uses clean pairs only.

### F. Sensitivity

Repeating the ladder at ¼ and ½ of course length leaves the ordering unchanged: cross-institution explanation agreement is 0.038, 0.034 and 0.029 at the three cutoffs, while accuracy rises with the later cutoff.

---

## VI. Discussion and Limitations

The practical consequence is narrow and concrete. A system that shows a teacher "the top three risk factors for this student" is showing an artifact of three choices, of which the students are the least influential. Two developers building the same system on the same data, one reaching for SHAP and the other for a refit-based importance, would put substantially different factor lists in front of the same teacher. Until an explanation is reported together with the estimator that produced it and some measure of its stability, it is not evidence a teacher can act on.

We do not claim the underlying models are useless, nor that explanation is hopeless. Section V-B shows agreement well above chance: there is a signal, it is simply much weaker than the presentation implies. Nor do we claim SHAP is wrong and drop-column right; we claim that the choice is consequential and currently invisible.

**Limitations.** Seven behavioural features are strongly correlated, which is exactly the setting in which importance is least identifiable — richer, less collinear feature sets may behave better, and we cannot test that on the three institutions that publish no assessment data. The three estimators are not exhaustive. Outcome semantics differ across institutions and are collinear with institution. Course calendars for the three Moodle institutions are inferred rather than published. Zambia contributes two small cohorts whose intervals cover chance, and 19 of the 63 cohorts have within-cohort intervals covering 0.5. Bootstrap intervals resample pairs that share target cohorts and are therefore narrower than a fully clustered interval would be. Everything here is correlational: none of these rankings is a causal account of failure, and Section V is an argument against reading them that way.

---

## VII. Conclusion

On 63 cohorts from five universities, the feature ranking a student-risk model produces depends more on which importance estimator was chosen than on which students the model was trained on. SHAP and drop-column importance, applied to the same fitted model on the same students, agree at Kendall tau 0.123 — below the 0.210 of a model retrained on a different year's cohort, and far below the 0.338 that two models fitted to disjoint halves of one cohort achieve. Predictive accuracy over the same comparisons is far more robust, retaining 51 % of its above-chance discrimination across institutions where the explanation retains 10 %.

The recommendation follows directly. Report the estimator alongside the explanation, and report the agreement between at least two estimators as routinely as accuracy is reported. We release the benchmark, five institution adapters and all frozen results so that the measurement takes one command.

---

## References

[1] J. Kuzilek, M. Hlosta, and Z. Zdrahal, "Open University Learning Analytics dataset," *Scientific Data*, vol. 4, art. 170171, 2017, doi: 10.1038/sdata.2017.171.
[2] E. Tiukhova, D. Van Landuyt, B. Baesens, and M. Snoeck, "Open data, private learners: a de-identified student activity and performance dataset for learning analytics," *Scientific Data*, vol. 13, art. 548, 2026, doi: 10.1038/s41597-026-06821-3.
[3] R. Raghavjee, P. R. Subramaniam, and I. Govender, "Anonymized dataset of Information Systems and Technology students at a South African university for learning analytics," *Data*, vol. 11, no. 1, art. 1, 2026, doi: 10.3390/data11010001.
[4] A. Bettahi, F.-Z. Belouadha, and H. Harroud, "A modular and explainable machine learning pipeline for student dropout prediction in higher education," *Algorithms*, vol. 18, no. 10, art. 662, 2025, doi: 10.3390/a18100662.
[5] S. Boujmiraz, H. Darhmaoui, and A. Drissi el Maliani, "Predicting student performance: a comprehensive review of machine learning, deep learning, and explainable AI approaches," *Computers and Education: Artificial Intelligence*, vol. 10, art. 100548, 2026, doi: 10.1016/j.caeai.2026.100548.
[6] R. Guevara-Reyes, I. Ortiz-Garcés, R. Andrade, F. Cox-Riquetti, and W. Villegas-Ch, "Machine learning models for academic performance prediction: interpretability and application in educational decision-making," *Frontiers in Education*, vol. 10, art. 1632315, 2025, doi: 10.3389/feduc.2025.1632315.
[7] E. Tiukhova et al., "Explainable learning analytics: assessing the stability of student success prediction models by means of explainable AI," *Decision Support Systems*, vol. 182, art. 114229, 2024, doi: 10.1016/j.dss.2024.114229.
[8] G. Hooker, L. Mentch, and S. Zhou, "Unrestricted permutation forces extrapolation: variable importance requires at least one more model, or there is no free variable importance," *Statistics and Computing*, vol. 31, art. 82, 2021, doi: 10.1007/s11222-021-10057-z.
[9] S. Krishna et al., "The disagreement problem in explainable machine learning: a practitioner's perspective," arXiv:2202.01602, 2022.
[10] J. López-Zambrano, J. A. Lara, and C. Romero, "Towards portability of models for predicting students' final performance in university courses starting from Moodle logs," *Applied Sciences*, vol. 10, no. 1, art. 354, 2020, doi: 10.3390/app10010354.
[11] J. López-Zambrano, J. A. Lara, and C. Romero, "Improving the portability of predicting students' performance models by using ontologies," *Journal of Computing in Higher Education*, vol. 34, pp. 1–19, 2022, doi: 10.1007/s12528-021-09273-3.
[12] J. Gardner, R. Yu, Q. Nguyen, C. Brooks, and R. Kizilcec, "Cross-institutional transfer learning for educational models: implications for model performance, fairness, and equity," in *Proc. ACM Conf. Fairness, Accountability, and Transparency (FAccT)*, 2023.
[13] J. Schwerter et al., "Cross-course generalizability of SRL-aligned predictive models using digital learning traces," arXiv:2604.22812, 2026.
[14] M. Riestra-González, M. del P. Paule-Ruíz, and F. Ortin, "Massive LMS log data analysis for the early prediction of course-agnostic student performance," *Computers & Education*, vol. 163, art. 104108, 2021, doi: 10.1016/j.compedu.2020.104108.
[15] S. M. Jayaprakash, E. W. Moody, E. J. M. Lauría, J. R. Regan, and J. D. Baron, "Early alert of academically at-risk students: an open source analytics initiative," *Journal of Learning Analytics*, vol. 1, no. 1, pp. 6–47, 2014, doi: 10.18608/jla.2014.11.3.
[16] L. Phiri, "A multi-source dataset for CS1 failure prediction in a sub-Saharan African context," Zenodo, 2026, doi: 10.5281/zenodo.21292883.
[17] J. H. Friedman, "Greedy function approximation: a gradient boosting machine," *Annals of Statistics*, vol. 29, no. 5, pp. 1189–1232, 2001.
[18] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2017.
[19] N. Bosch and L. Paquette, "Metrics for discrete student models: chance levels, comparisons, and use cases," *Journal of Learning Analytics*, vol. 5, no. 2, pp. 86–104, 2018, doi: 10.18608/jla.2018.52.6.

---

*ARCHIVED 2026-09-06. Version 4, built on an ordering claim (explainer 0.123 < retraining 0.210) that round-4 review dissolved: rescaling both into one evaluation protocol gives 0.123 vs 0.123. Swamy et al. (EDM 2022) also own the qualitative claim. Superseded by the resource-and-replication version.*
