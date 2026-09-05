# What Transfers and What Does Not: Predictions, Thresholds and Explanations of Early-Warning Models Across Five Institutions

*Anonymous submission — SIDe 2026, Track 1 (Computational Intelligence). Draft v1.0, 2026-09-05. Results from `data/artifacts/experiments/exp_014_transfer_ladder/f33/`.*

---

## Abstract

Early-warning models that flag students at risk of failing a course are almost always trained and evaluated inside a single course, so nothing is known about what survives when the same model is applied elsewhere. We assemble a public transfer benchmark of 64 real cohorts from five institutions on five learning-management platforms - the Open University (19 module-presentations), Universidad de Oviedo (20 courses), the University of KwaZulu-Natal (16 course-years), KU Leuven (6 course-years) and the University of Zambia (3 course-years) - covering 45,236 students under one seven-feature engagement schema and a relative early-warning cutoff at one third of each course. Three model families are evaluated over all 4,096 ordered cohort pairs along a transfer-distance ladder: within cohort, the same course in another year, another course at the same institution, and another institution. Three properties degrade at three different rates. Discrimination falls from ROC-AUC 0.746 within cohort to 0.616 across institutions. The fixed decision threshold fails much harder: F1 at 0.5 drops from 0.809 to 0.507, because cohort pass rates span 0.21 to 0.95. Re-expressing each feature as a percentile within the target cohort, an unsupervised transform requiring no target labels, restores cross-institution F1 to 0.639 uniformly across model families and recovers 0.089 AUC for a linear model; a regression of per-pair loss on measured distribution shift shows it works by removing sensitivity to platform click scale, and that it leaves prevalence shift untouched. Explanations do not transfer at all: permutation-importance rankings of a transferred model agree with locally trained rankings at Kendall tau 0.03 over 3,034 cross-institution pairs, and the transform that repairs predictions does not repair them. Two controls close the obvious objections. Enriching the feature set with intermediate assessment scores raises within-cohort AUC from 0.858 to 0.902 without shrinking the transfer gap, and excluding withdrawn students leaves the signal intact at 0.793. Code, cohort definitions and frozen results are released.

**Keywords** - learning analytics; early warning; model portability; transfer; explainable AI; trustworthy AI; distribution shift.

---

## I. Introduction

Predicting which students will fail a course from their activity in a learning-management system (LMS) is among the most replicated tasks in learning analytics. On the Open University Learning Analytics Dataset alone, dozens of papers report classifiers above 0.90 ROC-AUC with post-hoc explanations attached [4]–[6]. Almost all share one experimental unit: train and test on a held-out split of the *same* course presentation.

That is not how such a model is used. An institution that adopts an early-warning system trains it on the cohorts it already has and applies it to the cohort it is teaching now, to courses that did not exist when the model was built, and — if the system is a product — at other institutions whose platform records activity on a different scale. Three separate things could break in that move: the model's ability to rank students, the threshold that turns a score into an alert, and the explanation a teacher is shown. The literature treats the first and ignores the other two.

Evidence on the first is thin and contradictory. Studies inside one Moodle installation found decision-tree models transfer only between structurally similar courses [7], [8]. A study across four US universities found zero-shot transfer can match locally trained models [9]; a 2026 study across three courses at two universities found substantial degradation when base rates differ, and that linear models transfer better than tree ensembles [10]. None of these uses public data, none exceeds four institutions, none tests a fix that needs no target labels, and none asks whether the explanation survives.

Part of the reason is scarcity. A 2026 census that hand-coded 1,125 LAK, EDM and AIED papers from 2020–2024 and extracted 172 datasets found that, of the 130 publicly available ones, only four carry timestamped per-student activity, a course outcome, and a key joining them [11]. Meanwhile the largest cross-course study in the field — 26 MOOCs and 145,714 students — publishes its code and withholds its data [12]. Benchmarks of this kind exist; they are not reproducible.

This paper contributes:

1. **A public five-institution transfer benchmark.** 64 cohorts, 45,236 students, five LMS platforms, four countries, built from five open datasets [1]–[3], [13], [14] through one canonical engagement schema and one relative-time cutoff (Section III).
2. **A transfer-distance ladder** — D0 within cohort, D1 same course another year, D2 another course at the same institution, D3 another institution — evaluated for all 4,096 ordered cohort pairs, with two pooled-source settings (Section IV).
3. **Separated failure modes.** Discrimination, threshold calibration, and explanation agreement degrade at different rates; the threshold fails first and the explanation fails hardest (Section V).
4. **A label-free fix and its mechanism.** A within-cohort percentile representation recovers part of the cross-institution loss; a regression of loss on measured distribution shift shows it works by removing sensitivity to platform click scale (Section V-D).
5. **Two controls that close the obvious objections**: feature richness does not govern transferability, and the result is not an artefact of labelling withdrawal as failure (Section V-E).

The contribution is not a new algorithm. It is a reproducible answer to a deployment question the literature leaves open, and a fix that costs one line of preprocessing.

---

## II. Related Work

**Prediction and explanation on public LMS data.** Gradient boosting or random forests over weekly features, with SHAP attached, is the standard configuration; recent work reports up to 0.99 AUC on dropout [4], and reviews catalogue hundreds of such models [5], [6]. The reporting unit is one configuration on one cohort, which says nothing about transfer.

**Portability.** López-Zambrano, Lara and Romero studied 24 Moodle courses at one university and found decision-tree models port only when courses are grouped by degree or by similar activity usage [7]; a follow-up replaced low-level log attributes with an ontology of actions and improved portability [8]. Gardner et al. [9] transferred across four US universities under data-sharing constraints, reporting that zero-shot transfer approaches local performance without harming fairness — on harmonised institutional data that is not public. Schwerter et al. [10] found performance and calibration degrade across institutions with different at-risk base rates, and that Elastic Net transfers better than tree ensembles. Riestra-González et al. [13] predicted course-agnostic performance across 532 Moodle courses at one university. In MOOCs, Swamy, Marras and Käser [12] used meta-transfer over 26 courses to warm-start new ones. The fixes proposed across this line are course grouping, semantic attributes, or meta-learning; a within-cohort rescaling of the features themselves has not been tested, and no study spans five institutions with public data.

**Explanation stability.** Tiukhova et al. [15] showed with SHAP that feature importances of student-success models shift across cohorts of one KU Leuven programme, and argued that stable factors are the actionable ones. Whether the ranking produced by a model trained *elsewhere* agrees with what a local model would say has not been measured.

**Gap.** No public multi-institution, multi-platform benchmark of early-warning transfer exists; no label-free representation fix has been tested; explanation portability after transfer has not been quantified. This paper supplies all three.

---

## III. Data and Canonical Schema

### A. Five institutions, five platforms

| Institution (dataset) | Platform | Country | Cohorts | Students | Outcome |
|---|---|---|---|---|---|
| Open University — OULAD [1] | OU VLE | UK | 19 module-presentations | 30,059 | Pass/Distinction = 1; Fail/Withdrawn = 0 |
| Universidad de Oviedo [13] | Moodle 2.x | Spain | 20 courses, AY 2014/15 | 3,789 | Gradebook course total ≥ 50 % |
| Univ. of KwaZulu-Natal [3] | Moodle | South Africa | 16 course-years, 2018–21 | 7,254 | Final result code P* = 1 |
| KU Leuven [2] | Toledo | Belgium | 6 course-years, 2018–21 | 3,951 | PASSED |
| Univ. of Zambia [14] | Moodle | Zambia | 3 years of one course | 183 | Final exam mark ≥ 50 |
| **Total** | | | **64** | **45,236** | |

All five datasets are public; four are CC-BY 4.0 and the Oviedo release accompanies an Apache-2.0 repository. A cohort is admitted if it has ≥ 50 students with ≥ 15 in the rarer outcome class, below which an AUC estimate is too unstable to enter a mean. Oviedo contributes 94 eligible courses; the 20 with the largest minority class are kept so that the mean over pairs does not become an Oviedo statistic.

Pass rates span 0.21 to 0.95 across cohorts, and Zambia's single course moves from 0.64 to 0.21 to 0.39 across three consecutive years. This spread is the point: it is what a fixed alerting threshold has to survive.

### B. Enrolment, calendars and privacy

For the three Moodle institutions, enrolment is the intersection of the outcome table and the activity log, which avoids labelling students whose site is absent from an export. None of the three publishes a course calendar, so the active span is inferred from the log as the first to the last calendar week in which at least 10 % of enrolled students were active; OULAD and KU Leuven ship calendars. The Zambia release includes a column of real personal names beside its hashed identifier; the adapter never reads it, and all joins use the hash.

### C. Canonical engagement schema

Each adapter emits, per student and course week, four counters: clicks, active days, content clicks, and social (forum) clicks. Seven leakage-safe features are then derived identically everywhere: cumulative clicks, cumulative active days, cumulative content clicks, cumulative social activity, current-week clicks, number of active weeks so far, and weeks since the last active week. No assessment, demographic or course-structure features are used — KU Leuven publishes no intermediate marks, UKZN and Zambia export none, and the point of the schema is that any LMS can supply it. Section V-E shows the restriction does not drive the results.

### D. Early-warning cutoff

Course lengths range from 14 to 46 weeks, so the prediction point is relative: one row per student at week ⌈⅓ × course length⌉, with sensitivity analyses at ¼ and ½. Everything the model sees exists at that week; the label is the final course outcome.

---

## IV. Method

### A. Transfer-distance ladder

For an ordered pair of cohorts (S, T): **D0** if S = T, scored by 5-fold stratified cross-validation within the cohort; **D1** if they are the same course in different years; **D2** if they are different courses at the same institution; **D3** if they belong to different institutions. All 4,096 ordered pairs are evaluated, so each aggregate is a mean over pairs with a 1,000-resample bootstrap confidence interval. Because the four classes are means over different sets of target cohorts, the headline table additionally restricts to targets present at all four distances, making the columns describe the same cohorts. Two pooled sources complete the design: all other cohorts of the target's own institution (leave-one-cohort-out), and all cohorts of the other four institutions.

### B. Representations

Three representations of the same seven features, each computed *within the cohort being scored*, at the cutoff week, without using labels: **raw** counts; **z-score** (within-cohort standardisation); **percentile** (within-cohort rank scaled to [0, 1]). For a tree model the percentile transform is monotone, so within a cohort it cannot change predictions; any gain at D1–D3 is therefore attributable to cross-cohort alignment alone, which is the property under test.

### C. Models and metrics

The object of study is a fixed gradient-boosting classifier [16] (200 trees, depth 3, learning rate 0.05). Logistic regression and random forest are run alongside as robustness checks, the former because linear models have been reported to transfer better [10]. Each model is fitted once per source cohort and applied to every target. ROC-AUC is primary because it is threshold-free and therefore isolates discrimination from the base-rate shift; F1 at a fixed 0.5 threshold is reported precisely to expose what that shift does to a deployed alerting rule.

### D. Explanation portability

Permutation importance [17] over the seven features (AUC scoring) is computed on the target cohort twice: once for the transferred model and once for a model trained on that target. Agreement is Kendall τ and the Jaccard overlap of the top three.

### E. Few-shot calibration

For each target, the other-institution pooled model is refitted with k ∈ {0, 25, 50, 100} randomly chosen labelled target students added, and evaluated on the remaining target students over five seeds.

### F. Disclosed compute settings

Permutation importance is the only O(cohorts²) term, so three settings bound it, all affecting explanation rankings only and never a reported AUC or F1: rankings are computed for the primary model alone; `n_repeats` is 3; and targets larger than 1,500 students are label-stratified subsampled for the ranking. A ranking over seven features is a rank statistic and is stable well below that size.

---

## V. Results

Unless stated otherwise, ladder figures are means over ordered pairs, aggregated per target cohort and then restricted to the 40 target cohorts present at all four distances, so every column describes the same cohorts. Intervals are 1,000-resample bootstraps over pairs.

### A. Within-cohort baseline

Trained and tested inside its own cohort, the seven-feature model reaches ROC-AUC 0.746 on average, but the mean hides the point of the benchmark: the signal is institution-specific, not a property of student engagement in general.

| Institution | Cohorts | D0 AUC | Range |
|---|---|---|---|
| OULAD | 19 | 0.845 | 0.709-0.897 |
| UKZN | 16 | 0.667 | 0.536-0.814 |
| KU Leuven | 6 | 0.611 | 0.586-0.653 |
| Oviedo | 20 | 0.606 | 0.384-0.953 |
| Zambia | 3 | 0.521 | 0.455-0.556 |

Clickstream engagement predicts course outcome well at the Open University and barely at all at KU Leuven or Zambia. Any single-dataset study of this task measures one point of that range and reports it as the state of the art. This is the first quantity a five-institution benchmark can supply and a one-institution study cannot.

### B. Discrimination degrades with transfer distance

All three model families lose discrimination monotonically as the source moves away from the target (Table II). With raw counts the loss from D0 to D3 is 0.131 for gradient boosting, 0.173 for logistic regression and 0.092 for random forest, exceeding the pre-registered 0.05 criterion for a real degradation in every case. Random forest is the most robust of the three under raw features and gradient boosting the least, which qualifies the finding of Schwerter et al. [10] that linear models transfer best: that ordering appears here only after the representation is fixed.

### C. The decision threshold fails before discrimination does

Discrimination is threshold-free, so it understates what breaks in deployment. At a fixed 0.5 threshold, F1 falls from 0.809 within cohort to 0.507 across institutions for gradient boosting, and from 0.828 to 0.489 and from 0.819 to 0.532 for logistic regression and random forest (Table III). The cause is visible in Table I: cohort pass rates span 0.21 to 0.95, and a score calibrated to one prevalence is meaningless at another. The threshold therefore loses about 37 % of its F1 where discrimination loses 17 % of its AUC.

This is the failure a deployed early-warning system actually experiences, and it is the one the cohort-relative representation repairs most decisively. Under the percentile representation, cross-institution F1 recovers to 0.639, 0.629 and 0.642 for the three families, between 44 % and 47 % of the loss. Unlike the AUC gain, this repair is uniform across model families.

### D. The representation fix on discrimination, and its mechanism

On AUC the fix is real but uneven. Logistic regression gains 0.089 at D3 under z-scoring (0.602 to 0.691), meeting the pre-registered success criterion; gradient boosting gains 0.021 under percentiles and random forest 0.005, both in the partial band. The asymmetry is expected rather than anomalous: a tree ensemble is already invariant to monotone rescaling *within* a cohort, so it can only benefit from what the transform does *between* cohorts, whereas a linear model is sensitive to feature scale directly.

A regression of per-pair AUC loss on four measured shift quantities supports that reading. Averaged over the ladder, every shift measure grows with distance in step with the loss:

| Distance | Prevalence shift | Click-scale shift | Distribution-shape shift | AUC loss |
|---|---|---|---|---|
| D1 same course, other year | 0.053 | 0.192 | 0.210 | 0.013 |
| D2 other course, same institution | 0.116 | 0.323 | 0.298 | 0.032 |
| D3 other institution | 0.274 | 0.539 | 0.515 | 0.101 |

For gradient boosting the four measures explain 11.6 % of the pair-level variance in loss under raw features and 6.2 % under percentiles, and the correlation between loss and distribution-shape distance falls from 0.283 to 0.189. The representation removes part of the model's sensitivity to shift, which is what it was introduced to do. It removes only part: the residual variance is large, and prevalence shift in particular survives it.

Restating the claim in terms of measured shift rather than institution identity also frees it from the number of institutions: loss tracks how far apart two cohorts are, and "another institution" is simply the largest gap this benchmark contains.

### E. Explanations do not transfer, and the fix does not repair them

For each pair we compare the permutation-importance ranking of the transferred model, computed on the target, against the ranking a model trained on that target would produce (Table IV).

| Distance | Kendall tau | Top-3 Jaccard |
|---|---|---|
| D1 same course, other year | 0.20 | 0.42 |
| D2 other course, same institution | 0.10 | 0.37 |
| D3 other institution | 0.03 | 0.33 |

Across 3,034 cross-institution pairs the two rankings are effectively uncorrelated, and a top-three overlap of 0.33 out of seven features is close to what random rankings would give. The representation that repairs predictions leaves this untouched: tau is 0.026 under percentiles against 0.038 under raw counts.

The practical reading is direct. A teacher-facing panel that displays the risk factors of a model trained elsewhere is showing factors a locally trained model would not have selected, even where that model's ranking of students is still usable. Prediction portability and explanation portability are separate properties, and only the first has been studied.

### F. Two controls

**Feature richness does not govern transferability.** Within OULAD, where richer data exists, we repeat the ladder on three nested feature sets (Table VII). Adding click categories, ratios and course progress, then intermediate assessment scores, which are the strongest known predictors and are unavailable at the other four institutions, raises within-cohort AUC from 0.858 to 0.902. The D0-to-D2 gap does not shrink with it: 0.022 for the shared seven features against 0.021 for the seventeen-feature set. Richness buys accuracy, not portability, so the shared schema is not what limits transfer.

**The result is not an artefact of counting withdrawal as failure.** OULAD labels withdrawn students as failures, and withdrawal is close to tautological given a clickstream. Excluding them and predicting pass against fail among students who completed lowers within-cohort AUC from 0.858 to 0.793 across the twelve original cohorts: the tautology accounts for part of the within-cohort signal, and the signal survives its removal. Oviedo carries the analogous risk, with 9.9 % of students scoring exactly zero, and its adapter exposes the same control.

### G. Pooled sources and few-shot calibration

Two pooled settings (Table V) show that the best source depends on how much local history an institution has. For OULAD, pooling its own other cohorts gives 0.858 against 0.784 from the other four institutions. The ordering reverses at Zambia, whose three cohorts yield 0.536 from its own institution but 0.630 from the others: an institution with little history is better served by borrowing than by learning from itself.

Adding labelled target students helps far less than expected (Table VI). At OULAD, AUC rises from 0.778 at k = 0 to 0.828 at k = 100; at UKZN and KU Leuven the curve is flat, and at Oviedo 100 labelled students make it worse. The remaining gap is therefore not a shortage of target labels, and few-shot calibration is not a substitute for the representation fix.

### H. Sensitivity to the cutoff

The whole ladder was rerun with the cutoff at one quarter and one half of each course. All 64 cohorts survive both, and every conclusion replicates (gradient boosting, paired targets):

| Cutoff | AUC D0 | AUC D3 raw | AUC D3 pct | F1 D0 | F1 D3 raw | F1 D3 pct | tau at D3 |
|---|---|---|---|---|---|---|---|
| 1/4 | 0.726 | 0.602 | 0.638 | 0.801 | 0.486 | 0.636 | 0.039 |
| 1/3 | 0.746 | 0.616 | 0.637 | 0.809 | 0.507 | 0.639 | 0.033 |
| 1/2 | 0.777 | 0.644 | 0.677 | 0.836 | 0.536 | 0.655 | 0.032 |

A later cutoff sees more of each student's activity and predicts better everywhere, as expected. What does not move is the structure: the cross-institution AUC loss stays between 0.124 and 0.133, the threshold collapse stays between 0.300 and 0.315 of F1, the percentile representation recovers between 0.119 and 0.150 of that F1 at every cutoff, and explanation agreement across institutions stays at tau 0.032 to 0.039. The three findings are properties of the transfer, not of where the alarm is raised.

---

## VI. Discussion and Limitations

Three properties of an early-warning model degrade at different rates when it is moved, and the literature has measured only the slowest. Discrimination loses about 0.13 AUC across institutions and is partly recoverable. A fixed decision threshold loses a third of its F1 and is largely recoverable, for free, with an unsupervised within-cohort transform. Explanations lose everything and are not recoverable by that transform. A system reporting only AUC would call the third case a success.

The mechanism analysis suggests why the cheap fix works and where it stops. Re-expressing features as within-cohort percentiles removes differences in platform click scale and part of the difference in distribution shape, but nothing about it addresses prevalence shift, which is the largest single component at D3 and the one that breaks thresholds. That is consistent with the fix repairing F1 more than AUC, and it points at per-cohort threshold calibration as the natural next step.

**Limitations.** Outcome semantics differ across the five institutions: OULAD counts withdrawal as failure, Oviedo's label is a gradebook course total rather than a registrar decision, and the other three are examination or registrar outcomes. Section V-F bounds the first and Oviedo's zero-grade control the second, but the benchmark is not label-homogeneous and its cross-institution numbers absorb some of that heterogeneity. Course calendars are not published for the three Moodle institutions and are inferred from activity. Zambia contributes only three small cohorts. Oviedo is capped at 20 of its 94 eligible courses to keep the ladder balanced. The design is correlational throughout: nothing here identifies a causal driver of failure, and the feature rankings must not be read as such. Finally, although five institutions is the largest public benchmark of this kind we are aware of, the 2026 census of the field [11] found only four public datasets carrying timestamped activity, a course outcome and a join key. The population this benchmark draws from is small, which bounds how far any result of this shape can generalise.

## VII. Conclusion

Early-warning models are reported as if accuracy were the whole of their quality, and as if a number measured on one cohort described the model rather than the cohort. On a public benchmark of 64 cohorts from five institutions and five platforms, neither holds. Within-cohort discrimination ranges from 0.85 at the Open University to 0.52 at the University of Zambia, so a single-dataset result describes a context, not a method. Moving a model across institutions costs about 0.13 AUC, costs a third of the F1 of any fixed alerting threshold, and costs essentially all of the agreement between its explanation and the one a local model would give.

The three failures need three different responses. Threshold failure is the largest and the cheapest to repair: expressing each feature as a percentile within the cohort being scored uses no target labels, costs one line of preprocessing, and recovers about two thirds of the lost F1 for every model family we tested. Discrimination loss is partly repaired by the same transform, more for linear models than for tree ensembles, and the residual is dominated by prevalence shift that the transform does not touch. Explanation failure is not repaired at all, and we know of nothing in the current literature that would repair it.

The practical consequence is that a transferred model may be safe to rank students with and unsafe to explain them with, and that these must be validated separately. We release the benchmark, the adapters for all five institutions, and the frozen results so that a proposed fix for either property can be measured against the same ladder.

---

## References

[1] J. Kuzilek, M. Hlosta, and Z. Zdrahal, "Open University Learning Analytics dataset," *Scientific Data*, vol. 4, art. 170171, 2017, doi: 10.1038/sdata.2017.171.
[2] E. Tiukhova, D. Van Landuyt, B. Baesens, and M. Snoeck, "Open data, private learners: a de-identified student activity and performance dataset for learning analytics," *Scientific Data*, vol. 13, art. 548, 2026, doi: 10.1038/s41597-026-06821-3.
[3] R. Raghavjee, P. R. Subramaniam, and I. Govender, "Anonymized dataset of Information Systems and Technology students at a South African university for learning analytics," *Data*, vol. 11, no. 1, art. 1, 2026, doi: 10.3390/data11010001.
[4] J. López de la Rosa et al., "A modular and explainable machine learning pipeline for student dropout prediction in higher education," *Algorithms*, vol. 18, no. 10, art. 662, 2025, doi: 10.3390/a18100662.
[5] S. Boujmiraz, H. Darhmaoui, and A. Drissi el Maliani, "Predicting student performance: a comprehensive review of machine learning, deep learning, and explainable AI approaches," *Computers and Education: Artificial Intelligence*, vol. 10, art. 100548, 2026, doi: 10.1016/j.caeai.2026.100548.
[6] W. Villegas-Ch et al., "Machine learning models for academic performance prediction: interpretability and application in educational decision-making," *Frontiers in Education*, vol. 10, art. 1632315, 2025, doi: 10.3389/feduc.2025.1632315.
[7] J. López-Zambrano, J. A. Lara, and C. Romero, "Towards portability of models for predicting students' final performance in university courses starting from Moodle logs," *Applied Sciences*, vol. 10, no. 1, art. 354, 2020, doi: 10.3390/app10010354.
[8] J. López-Zambrano, J. A. Lara, and C. Romero, "Improving the portability of predicting students' performance models by using ontologies," *Journal of Computing in Higher Education*, vol. 34, pp. 1–19, 2022, doi: 10.1007/s12528-021-09273-3.
[9] J. Gardner, R. Yu, Q. Nguyen, C. Brooks, and R. Kizilcec, "Cross-institutional transfer learning for educational models: implications for model performance, fairness, and equity," in *Proc. ACM Conf. Fairness, Accountability, and Transparency (FAccT)*, 2023.
[10] J. Schwerter et al., "Cross-course generalizability of SRL-aligned predictive models using digital learning traces," arXiv:2604.22812, 2026.
[11] V. Švábenský, B. Flanagan, C. López Zapata, and A. Shimada, "Open datasets in learning analytics: trends, challenges, and best practice," *ACM Trans. Knowledge Discovery from Data*, 2026, doi: 10.1145/3798096.
[12] V. Swamy, M. Marras, and T. Käser, "Meta transfer learning for early success prediction in MOOCs," in *Proc. 9th ACM Conf. Learning @ Scale (L@S)*, 2022.
[13] M. Riestra-González, M. del P. Paule-Ruíz, and F. Ortin, "Massive LMS log data analysis for the early prediction of course-agnostic student performance," *Computers & Education*, vol. 163, art. 104108, 2021, doi: 10.1016/j.compedu.2020.104108.
[14] L. Phiri et al., "A multi-source dataset for CS1 failure prediction in a sub-Saharan African context," Zenodo, 2026, doi: 10.5281/zenodo.21292883.
[15] E. Tiukhova et al., "Explainable learning analytics: assessing the stability of student success prediction models by means of explainable AI," *Decision Support Systems*, vol. 182, art. 114229, 2024, doi: 10.1016/j.dss.2024.114229.
[16] J. H. Friedman, "Greedy function approximation: a gradient boosting machine," *Annals of Statistics*, vol. 29, no. 5, pp. 1189–1232, 2001.
[17] L. Breiman, "Random forests," *Machine Learning*, vol. 45, no. 1, pp. 5–32, 2001.
[18] S. Kapoor and A. Narayanan, "Leakage and the reproducibility crisis in machine-learning-based science," *Patterns*, vol. 4, no. 9, art. 100804, 2023.

---

*ARCHIVED 2026-09-05: full-length version (4697 words), kept before compression to the SIDe 2026 six-page limit. This is the source for the extended journal version (Intelligent Automation & Soft Computing special issue, deadline 2027-05-31). Do not edit; edit `side2026_paper.md`.*
