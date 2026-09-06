# A Five-Institution Benchmark for Student-Risk Models, and What It Says About Measuring Explanation Stability

*Anonymous submission — SIDe 2026, Track 1 (Computational Intelligence).*

---

## Abstract

Studies of student-risk models are almost always run on one dataset, and studies of their explanations on one importance estimator. We release a benchmark that removes the first restriction and use it to show why the second one matters. The benchmark covers 63 cohorts from five universities on five learning-management platforms in four countries, 35,529 distinct students, harmonised to one seven-feature schema with adapters and frozen results released. Three findings follow. First, predictability is a property of the institution, not of the task: within-cohort ROC-AUC ranges from 0.845 at the Open University to 0.527 at the University of Zambia, and 19 of 63 cohorts have intervals covering chance, so a single-dataset result describes its dataset. Second, we replicate on this population the finding of Swamy et al. that the choice of explainer dominates the interpretation of a student model, extending it from five MOOC courses and one network to 63 cohorts, five institutions and three model families, and supplying the reference points their design could not: a noise floor of Kendall tau 0.707, an attainable ceiling of 0.338 between two models fitted to disjoint halves of one cohort, and an analytic random baseline. Third, and consequently, we show that a single-estimator stability study reports a conclusion conditional on an undeclared choice: measuring how much a year of retraining costs a feature ranking gives tau 0.238 under permutation importance and 0.520 under SHAP, a spread more than twice the 0.128 effect being measured. We also report two measurement hazards found by auditing our own pipeline — a majority-class F1 that flatters every model, and 72 of 78 same-course transfer pairs sharing students between training and evaluation — and a zero-training baseline that gradient boosting fails to beat in 38 of 63 cohorts.

**Keywords** — benchmark; learning analytics; explainable AI; feature importance; replication; trustworthy AI.

---

## I. Introduction

Two habits shape the empirical literature on student-risk prediction. Models are developed and evaluated on a single dataset, usually one institution's. Explanations are computed with a single importance estimator, usually whichever library the authors reached for. Neither habit is examined, because examining either requires resources most studies do not have: many institutions, or many estimators applied to the same models.

This paper supplies both and reports what they show. It is a resource paper with a measurement result attached, and it is deliberately not a methods paper: we propose no new model, no new explainer, and no new transfer technique. Three of our own candidate methods were tested during this work and discarded when controls showed they did not beat far simpler alternatives; those controls are reported in Section V-D because they bound how the rest should be read.

Contributions:

1. **A public five-institution benchmark** — 63 cohorts, 35,529 distinct students, five platforms, four countries, one harmonised schema, with adapters, cohort definitions and frozen results released (Section III).
2. **The spread of predictability across institutions**, which a single-dataset study cannot observe (Section V-A).
3. **A replication and extension** of the finding that explainer choice dominates the interpretation of a student model [8], on a population five times larger and structurally different, with the floor, ceiling and random baselines that make the numbers interpretable (Section V-B).
4. **A methodological consequence**: single-estimator stability studies report conclusions conditional on an undeclared choice, and we quantify by how much (Section V-C).
5. **Two measurement hazards and a baseline audit** that changed our own conclusions mid-project (Section V-D).

---

## II. Related Work

**Prediction on public LMS data.** Gradient boosting or random forests over weekly activity features, with post-hoc explanations attached, is the standard configuration, and reviews catalogue hundreds of such systems [4]–[6]. The reporting unit is one configuration on one cohort.

**Cross-institution work.** Transfer of student models is well studied: López-Zambrano et al. across 24 Moodle courses [9], [10]; Gardner et al. across four US universities on private data [11]; Schwerter et al. across two universities [12]; Riestra-González et al. across 532 courses at one institution [13]; Jayaprakash et al. ported an early-alert model between partner institutions as early as 2014 [14]. What is missing is not the question but a public artifact: a harmonised, multi-platform corpus another group can run against. That is the gap this benchmark fills.

**Explanation stability.** Tiukhova et al. showed with SHAP that importance rankings of student-success models shift across cohorts and years of one programme [7]. Swamy et al. compared five explainers on Bidirectional LSTM models over five MOOCs and concluded that "the choice of explainer is an important decision and is in fact paramount to the interpretation of the predictive results, even more so than the course the model is trained on" [8]. Their conclusion is the one we replicate; we claim neither priority for it nor a contradiction of it. Their design established the ordering structurally — principal-component scatter and per-course heatmaps — but could not put the two sources of variation on a common numeric scale, because their importance vectors have course-specific lengths. A harmonised schema removes that obstacle, which is the extension we contribute. Outside education, Hooker, Mentch and Zhou show permutation importance evaluates a model off its own data manifold and argue a defensible estimate requires refitting [15]; Krishna et al. document disagreement between explanation methods generally [16]; and Verdinelli and Wasserman prove that SHAP and leave-one-covariate-out target genuinely different estimands [17], which we treat as the correct interpretation of part of our result rather than as a competing explanation of it.

---

## III. The Benchmark

### A. Five institutions, five platforms

| Institution | Platform | Country | Cohorts | Students |
|---|---|---|---|---|
| Open University — OULAD [1] | OU VLE | UK | 19 | 30,059 |
| Universidad de Oviedo [13] | Moodle 2.x | Spain | 20 | 3,789 |
| Univ. of KwaZulu-Natal [3] | Moodle | South Africa | 16 | 7,254 |
| KU Leuven [2] | Toledo | Belgium | 6 | 3,951 |
| Univ. of Zambia [18] | Moodle | Zambia | 2 | 117 |
| **Total** | | | **63** | **35,529 distinct** |

A cohort is one course, one academic period, one institution, admitted with at least 50 students and at least 15 in the rarer outcome class. Cohort sizes sum to 45,170, but only 35,529 students are distinct: 21 % appear in more than one cohort, which Section V-D shows is not a bookkeeping detail. Outcome definitions differ across institutions and are perfectly collinear with institution, so no analysis here separates a label effect from an institution effect; OULAD in particular counts withdrawal as failure, which a clickstream predicts almost by construction.

### B. Schema, calendars and corrections

Each adapter emits four weekly counters per student — clicks, active days, content clicks, social clicks — from which seven leakage-safe features are derived identically: four cumulative counters, current-week clicks, active weeks so far, and weeks since last activity. No demographic or assessment feature enters the models; three institutions publish none. Course lengths run from 14 to 46 weeks, so the prediction point is relative: one row per student at week ⌈⅓ × length⌉, repeated at ¼ and ½.

The three Moodle institutions publish no course calendar, so an active span is inferred from the log as the first to the last week in which at least 10 % of enrolled students were active. Building the benchmark surfaced two data defects worth recording for reusers: one release stores its academic years under identical filenames, so a naive loader silently returns the same year three times; and another records a single final examination mark per student with no sitting year, so assigning it to every year in which a student appears leaks a later outcome backwards. Fixing the second cost one cohort, and we report the smaller benchmark rather than the leaked one.

---

## IV. Method

**Models.** A fixed gradient-boosting classifier [19] (200 trees, depth 3, learning rate 0.05) is the primary model, with logistic regression and a random forest as robustness checks. Nothing is tuned per cohort: the object of study is what an ordinary model does.

**Explainers.** Three importance estimators are applied to the same fitted model on the same held-out students: *permutation* importance (three repeats, AUC scoring); *SHAP*, the mean absolute TreeSHAP value per feature [20]; and *drop-column*, refitting without each feature and measuring the AUC lost, which is what [15] argues a defensible estimate requires.

**Agreement.** Kendall tau over the seven features and Jaccard overlap of the top three. Because such numbers are meaningless without bounds, we measure three: a **noise floor** (one fitted model, two permutation seeds), an **attainable ceiling** (two models fitted to disjoint halves of one cohort), and an analytic **random baseline** (expected tau 0.000, expected top-3 Jaccard 0.303).

**Cohort separations.** Cohort pairs are labelled by what differs: the same course in another year, another course at the same institution, or another institution. All 3,969 ordered pairs are evaluated.

---

## V. Results

### A. Predictability belongs to the institution

| Institution | Cohorts | Within-cohort AUC | Range |
|---|---|---|---|
| OULAD | 19 | 0.845 | 0.709–0.897 |
| UKZN | 16 | 0.667 | 0.536–0.814 |
| KU Leuven | 6 | 0.611 | 0.586–0.653 |
| Oviedo | 20 | 0.606 | 0.384–0.953 |
| Zambia | 2 | 0.527 | 0.455–0.598 |

Nineteen of the 63 cohorts have a within-cohort interval covering 0.5, and one is reliably anti-predictive. A study reporting 0.85 and a study reporting 0.55 may be equally competent and equally correct about their own data. This is the first quantity the benchmark supplies that a single-dataset design cannot.

### B. Reference points for explanation agreement, and a replication

| Reference point | tau | top-3 Jaccard |
|---|---|---|
| Same model, only the permutation seed differs | 0.707 | 0.744 |
| Two models, disjoint halves of one cohort, ranked on the full cohort | 0.338 | 0.487 |
| The same, ranked on a held-out third | 0.198 | 0.415 |
| Independent random rankings | 0.000 | 0.303 |

Two models differing only in which half of one cohort they saw agree at 0.338. That is the most agreement any comparison in this paper can attain, and it is far below what a teacher-facing factor list implicitly promises.

Against those bounds, the estimator comparison. Applied to one fitted model on one set of students, permutation importance and SHAP agree at tau 0.408, permutation and drop-column at 0.258, SHAP and drop-column at 0.123. The qualitative conclusion — that the explainer is a first-order determinant of the resulting factor list — is that of Swamy et al. [8], reproduced here on 63 cohorts across five institutions and three model families rather than five MOOCs and one network.

One arm requires a caveat we report rather than hide. Four of the seven features are cumulative counters of the same behaviour, and removing one leaves near-duplicates behind, so drop-column importance is zero or negative for 3.2 of 7 features on average, against 2.1 for permutation. Its agreement with itself across resamples of one cohort is 0.181 — lower than its agreement with permutation on identical data. On collinear behavioural features, drop-column is not a reliable estimator, and the 0.123 figure should be read as evidence about that estimator in this setting rather than as the headline. The defensible headline figure is the permutation-versus-SHAP agreement of 0.408, which sits above the 0.338 ceiling and is therefore not evidence that the explainer matters more than the training sample.

### C. A single-estimator stability study measures its own estimator

The practical consequence is sharper than the comparison above. Take a question the literature does ask — how much does retraining on the next year's students change a model's feature ranking? — and answer it three times, changing only the estimator:

| Estimator | Agreement between years |
|---|---|
| SHAP | 0.520 |
| Permutation importance | 0.238 |
| Drop-column | degenerate here (§V-B) |

The two reliable estimators differ by 0.282 on the same 78 course-year pairs and the same fitted models. The effect being measured — retraining, against the 0.338 ceiling — is 0.128. The choice of estimator moves the answer by more than twice the size of the phenomenon under study.

A stability study that fixes one estimator therefore reports a number that is as much a property of that choice as of the data, and none that we are aware of declares this. The recommendation is concrete and cheap: report agreement under at least two estimators, and report the ceiling for the design, since without it a tau has no scale.

### D. Three controls that changed our own conclusions

**A zero-training baseline.** Ranking students by cumulative active days — no model, no training, no labels — reaches AUC 0.713 against 0.692 for a locally trained gradient-boosting model, beating it in 38 of 63 cohorts; logistic regression reaches 0.717. At OULAD, where intermediate assessment scores exist, a model using them reaches 0.839 against the rule's 0.757. Behavioural counters carry roughly what a single attendance counter already carries; the value of a model here scales with what it knows beyond attendance.

**A majority-class metric.** Our first implementation computed F1 with the default positive label, which is *passing*. Every configuration looked healthy while losing, on the class an alerting system acts upon, to a rule that alerts everyone. The check costs one line: print the trivial rule beside every score [21].

**Contamination.** 72 of 78 same-course pairs and 324 of 916 other-course pairs share students between training and evaluation, up to 94 % of the target cohort; cross-institution pairs are clean at under 1.5 %. Uncorrected, same-course transfer appears to *beat* within-cohort performance. Any evaluation of this shape must report per-pair overlap.

### E. Sensitivity

Repeating the analysis at ¼ and ½ of course length changes every level and no ordering: cross-institution explanation agreement is 0.038, 0.034 and 0.029 at the three cutoffs, and accuracy rises with the later cutoff.

---

## VI. Discussion and Limitations

The benchmark's value is in what it makes cheap. Any group can now run a proposed model, representation or explainer against 63 cohorts from five platforms and report the same reference points we do. That is a modest contribution and a real one: the field's recurring difficulty, visible in Section V-A, is that results describe datasets, and the only remedy is more datasets in one place.

The measurement result is a caution rather than a discovery. Swamy et al. established that the explainer dominates [8]; we confirm it on a different and larger population and add the bounds that let a reader judge magnitude. Section V-C is the part we believe is new and the part practitioners should act on: a stability number without a declared estimator and a measured ceiling is not interpretable, and the literature currently reports such numbers routinely.

**Limitations.** Seven behavioural features are strongly correlated, which is exactly the setting in which importance is least identifiable, and in which drop-column degenerates; richer feature sets may behave differently and we cannot test that where assessment data is unpublished. Three estimators are not exhaustive. Outcome semantics differ across institutions and are collinear with institution. Course calendars for three institutions are inferred rather than published. Zambia contributes two small cohorts whose intervals cover chance. Bootstrap intervals resample pairs that share target cohorts and are narrower than fully clustered intervals; the estimator spread in Section V-C is reported without a significance test and rests on 78 pairs from six course families. Everything here is correlational, and Section V-B is an argument against reading any of these rankings causally.

---

## VII. Conclusion

We release a benchmark of 63 student cohorts from five universities, five platforms and four countries, harmonised to one schema, with adapters and frozen results. On it, within-cohort predictability ranges from 0.845 to 0.527, so a single-dataset result is a statement about that dataset. We reproduce, on this population, the finding that the choice of importance estimator dominates a student model's explanation, and we supply the noise floor, attainable ceiling and random baseline that such numbers require to be interpretable. The consequence we would most like read is narrow: asking how stable an explanation is, with one estimator and no ceiling, produces an answer that moves by more than the effect under study when the estimator changes. Reporting two estimators and a ceiling costs one additional run and makes the answer mean something.

---

## References

[1] J. Kuzilek, M. Hlosta, and Z. Zdrahal, "Open University Learning Analytics dataset," *Scientific Data*, vol. 4, art. 170171, 2017, doi: 10.1038/sdata.2017.171.
[2] E. Tiukhova, D. Van Landuyt, B. Baesens, and M. Snoeck, "Open data, private learners: a de-identified student activity and performance dataset for learning analytics," *Scientific Data*, vol. 13, art. 548, 2026, doi: 10.1038/s41597-026-06821-3.
[3] R. Raghavjee, P. R. Subramaniam, and I. Govender, "Anonymized dataset of Information Systems and Technology students at a South African university for learning analytics," *Data*, vol. 11, no. 1, art. 1, 2026, doi: 10.3390/data11010001.
[4] A. Bettahi, F.-Z. Belouadha, and H. Harroud, "A modular and explainable machine learning pipeline for student dropout prediction in higher education," *Algorithms*, vol. 18, no. 10, art. 662, 2025, doi: 10.3390/a18100662.
[5] S. Boujmiraz, H. Darhmaoui, and A. Drissi el Maliani, "Predicting student performance: a comprehensive review of machine learning, deep learning, and explainable AI approaches," *Computers and Education: Artificial Intelligence*, vol. 10, art. 100548, 2026, doi: 10.1016/j.caeai.2026.100548.
[6] R. Guevara-Reyes, I. Ortiz-Garcés, R. Andrade, F. Cox-Riquetti, and W. Villegas-Ch, "Machine learning models for academic performance prediction: interpretability and application in educational decision-making," *Frontiers in Education*, vol. 10, art. 1632315, 2025, doi: 10.3389/feduc.2025.1632315.
[7] E. Tiukhova et al., "Explainable learning analytics: assessing the stability of student success prediction models by means of explainable AI," *Decision Support Systems*, vol. 182, art. 114229, 2024, doi: 10.1016/j.dss.2024.114229.
[8] V. Swamy, B. Radmehr, N. Krco, M. Marras, and T. Käser, "Evaluating the explainers: black-box explainable machine learning for student success prediction in MOOCs," in *Proc. 15th Int. Conf. Educational Data Mining (EDM)*, 2022, doi: 10.5281/zenodo.6852964.
[9] J. López-Zambrano, J. A. Lara, and C. Romero, "Towards portability of models for predicting students' final performance in university courses starting from Moodle logs," *Applied Sciences*, vol. 10, no. 1, art. 354, 2020, doi: 10.3390/app10010354.
[10] J. López-Zambrano, J. A. Lara, and C. Romero, "Improving the portability of predicting students' performance models by using ontologies," *Journal of Computing in Higher Education*, vol. 34, pp. 1–19, 2022, doi: 10.1007/s12528-021-09273-3.
[11] J. Gardner, R. Yu, Q. Nguyen, C. Brooks, and R. Kizilcec, "Cross-institutional transfer learning for educational models: implications for model performance, fairness, and equity," in *Proc. ACM Conf. Fairness, Accountability, and Transparency (FAccT)*, 2023.
[12] J. Schwerter et al., "Cross-course generalizability of SRL-aligned predictive models using digital learning traces," arXiv:2604.22812, 2026.
[13] M. Riestra-González, M. del P. Paule-Ruíz, and F. Ortin, "Massive LMS log data analysis for the early prediction of course-agnostic student performance," *Computers & Education*, vol. 163, art. 104108, 2021, doi: 10.1016/j.compedu.2020.104108.
[14] S. M. Jayaprakash, E. W. Moody, E. J. M. Lauría, J. R. Regan, and J. D. Baron, "Early alert of academically at-risk students: an open source analytics initiative," *Journal of Learning Analytics*, vol. 1, no. 1, pp. 6–47, 2014, doi: 10.18608/jla.2014.11.3.
[15] G. Hooker, L. Mentch, and S. Zhou, "Unrestricted permutation forces extrapolation: variable importance requires at least one more model, or there is no free variable importance," *Statistics and Computing*, vol. 31, art. 82, 2021, doi: 10.1007/s11222-021-10057-z.
[16] S. Krishna et al., "The disagreement problem in explainable machine learning: a practitioner's perspective," arXiv:2202.01602, 2022.
[17] I. Verdinelli and L. Wasserman, "Feature importance: a closer look at Shapley values and LOCO," *Statistical Science*, vol. 39, no. 4, 2024, doi: 10.1214/24-STS937.
[18] L. Phiri, "A multi-source dataset for CS1 failure prediction in a sub-Saharan African context," Zenodo, 2026, doi: 10.5281/zenodo.21292883.
[19] J. H. Friedman, "Greedy function approximation: a gradient boosting machine," *Annals of Statistics*, vol. 29, no. 5, pp. 1189–1232, 2001.
[20] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2017.
[21] N. Bosch and L. Paquette, "Metrics for discrete student models: chance levels, comparisons, and use cases," *Journal of Learning Analytics*, vol. 5, no. 2, pp. 86–104, 2018, doi: 10.18608/jla.2018.52.6.
