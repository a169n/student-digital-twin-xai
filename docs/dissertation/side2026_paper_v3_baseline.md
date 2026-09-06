# Cross-Institution Transfer of Early-Warning Models: Discrimination, Calibration and Explanation Stability Across Five Universities

*Anonymous submission — SIDe 2026, Track 1 (Computational Intelligence).*

---

## Abstract

Early-warning models that flag students at risk of failing a course are almost always trained and evaluated inside one course, so what survives when such a model is moved is unknown. We release a public transfer benchmark of 63 cohorts from five universities on five learning-management platforms in four countries, covering 35,529 distinct students under one seven-feature engagement schema and a cutoff at one third of each course, and evaluate every ordered pair of cohorts. Four results follow. First, the signal itself is institution-specific: within-cohort ROC-AUC ranges from 0.845 at the Open University to 0.527 at the University of Zambia, so a single-dataset study reports a property of its dataset. Second, transfer separates cleanly along the lines the clinical prediction-model literature would predict: discrimination degrades gradually, from 0.691 within cohort to 0.597 across institutions, while calibration collapses, with calibration-in-the-large moving from -0.008 to +0.119 and the Brier score from 0.197 to 0.361. A within-cohort percentile representation, computed without target labels, restores calibration-in-the-large almost exactly (-0.009) and improves the Brier score, so it is a recalibration device rather than a performance fix. Third, and negatively, it does not improve the decision: at a realistic 20 % flag budget, recall of failing students is 0.272 raw and 0.274 under the transform, and every rule we tested — including a source-rate threshold — loses on F1 to simply alerting everyone. Fourth, the explanation finding that motivated this work does not survive a baseline: two models trained on disjoint halves of the same cohort agree at Kendall tau 0.338, against 0.026 across institutions and 0.303 expected from random rankings, so permutation-importance rankings over these features are weakly identified before transfer is considered. We also report two methodological hazards found while auditing our own pipeline: F1 computed on the passing class flatters every model, and 72 of 78 same-course transfer pairs share students between training and evaluation, up to 94 % of the target cohort. Disaggregating by published attributes, transfer harms the worst-served group most: at UKZN, recall for the lowest school-quintile group falls from 0.65 locally to 0.18 after transfer.

**Keywords** — learning analytics; early warning; model portability; external validation; calibration; explainable AI; trustworthy AI; fairness.

---

## I. Introduction

Predicting course failure from learning-management-system activity is one of the most replicated tasks in learning analytics, and the standard experiment trains and tests on a held-out split of a single course presentation. That is not how such a model is used. An institution applies it to the cohort it is teaching now, to courses that did not exist when it was built, and, if the system is a product, at other institutions whose platform records activity on a different scale.

Three distinct things can break in that move: the model's ability to rank students, the calibration that turns a score into a decision, and the explanation a teacher is shown. The learning-analytics literature reports the first and rarely separates the second, which is unfortunate, because the clinical prediction-model literature has known for two decades that a transported model routinely keeps its discrimination while its calibration fails, and has a settled vocabulary and a repair procedure for exactly that [11], [12], [13].

This paper contributes:

1. **A public five-institution benchmark**, 63 cohorts and 35,529 distinct students across five platforms and four countries, with adapters and frozen results released (Section III).
2. **A separation of three failure modes** along a transfer-distance ladder, in the external-validation vocabulary: discrimination, calibration, and explanation agreement degrade at very different rates (Section V-B, V-C).
3. **The limits of the repair.** A label-free cohort-relative representation restores calibration but does not improve the decision at a fixed flag budget; and the explanation instability we set out to attribute to transfer is largely present within a single cohort (Section V-D, V-E).
4. **Two methodological hazards** that we found by auditing our own pipeline and that are easy to reproduce accidentally: a majority-class F1 that flatters every model, and shared students that contaminate within-institution transfer evaluation (Section V-G).
5. **A fairness disaggregation** showing that transfer costs the worst-served group more than the average (Section V-F).

We do not propose a new algorithm. We report what a competent, ordinary early-warning model does when it leaves home, using metrics that cannot hide the answer.

---

## II. Related Work

**Prediction on public LMS data.** Gradient boosting or random forests over weekly features, with post-hoc explanations attached, is the standard configuration, and reviews catalogue hundreds of such models [4]–[6]. The reporting unit is one configuration on one cohort.

**Portability within learning analytics.** López-Zambrano, Lara and Romero found that decision-tree models port between Moodle courses only when the courses are structurally similar [7], and later improved portability with an ontology of actions [8]. Gardner et al. transferred across four US universities and reported that zero-shot transfer can approach local performance, on harmonised institutional data that is not public [9]. Schwerter et al. found degradation across institutions with different base rates [10]. Riestra-González et al. predicted course-agnostic performance across 532 Moodle courses at one university [14]. Swamy, Marras and Käser used meta-transfer over 26 MOOCs [15]. Two things are absent from this line: public data spanning more than a handful of institutions, and any separation of calibration from discrimination.

**External validation, borrowed.** In clinical prediction modelling, transporting a model to a new hospital is a named experimental design with a standard reporting checklist [11], a calibration hierarchy that distinguishes calibration-in-the-large from weaker and stronger forms [12], and a closed-testing ladder that tries intercept-only recalibration before refitting anything [13]. Label-free prior correction has existed since Saerens, Latinne and Decaestecker [16]. We adopt this vocabulary rather than reinventing it, and Section V-D reports what happens when the ladder's cheapest rung is skipped.

**Explanation stability.** Tiukhova et al. showed with SHAP that feature importances of student-success models shift across cohorts of one programme [17]. Independently, Hooker, Mentch and Zhou showed that permutation importance evaluated outside the data manifold is unreliable and that a defensible variable-importance estimate needs refitting [18]. Section V-E measures both the noise floor and the attainable ceiling before making any claim about transfer, which is what those two results together demand.

**Data scarcity.** A 2026 census hand-coded 1,125 LAK, EDM and AIED papers and published its annotated inventory of 172 datasets [19]. Our own filtering of that public inventory finds very few datasets carrying timestamped per-student activity, a course outcome, and a key joining them; the figure is ours, not the census authors'. Meanwhile the largest cross-course study in the field publishes code and withholds data [15].

---

## III. Data and Canonical Schema

### A. Five institutions, five platforms

| Institution | Platform | Country | Cohorts | Students | Outcome |
|---|---|---|---|---|---|
| Open University — OULAD [1] | OU VLE | UK | 19 | 30,059 | Pass/Distinction = 1; Fail/Withdrawn = 0 |
| Universidad de Oviedo [14] | Moodle 2.x | Spain | 20 | 3,789 | Gradebook course total ≥ 50 % |
| Univ. of KwaZulu-Natal [3] | Moodle | South Africa | 16 | 7,254 | Result code beginning P |
| KU Leuven [2] | Toledo | Belgium | 6 | 3,951 | PASSED |
| Univ. of Zambia [20] | Moodle | Zambia | 2 | 117 | Final exam mark ≥ 50 |
| **Total** | | | **63** | **35,529 distinct** | |

Cohort rows sum to 45,158, but only 35,529 students are distinct: 21 % appear in more than one cohort. Section V-G shows why that matters. A cohort is admitted with at least 50 students and 15 in the rarer class. Oviedo contributes 20 of its 94 eligible courses, the largest by minority class, so that the mean over pairs is not an Oviedo statistic.

Outcome semantics differ by institution, and we do not claim otherwise: OULAD counts withdrawal as failure, Oviedo's label is a gradebook total rather than a registrar decision, and the other three are examination or registrar outcomes. Label definition and institution are perfectly collinear here, so no analysis in this paper can separate a label effect from an institution effect. This is a property of the available public data, and it bounds every cross-institution number we report.

### B. Enrolment, calendars, and one correction

For the three Moodle institutions, enrolment is the intersection of the outcome table and the activity log. None publishes a course calendar, so the active span is inferred as the first to the last week in which at least 10 % of enrolled students were active. The Zambia release records one final examination mark per student with no sitting year; assigning that mark to every year in which the student appears would leak a later outcome backwards, so each student is assigned to their last active year. This removed one Zambia cohort from the benchmark, and we report the smaller benchmark rather than the leaked one.

### C. Canonical schema and cutoff

Each adapter emits four weekly counters — clicks, active days, content clicks, social clicks — from which seven leakage-safe features are derived identically: four cumulative counters, current-week clicks, active weeks so far, and weeks since last activity. No demographic or assessment features enter the model. Course lengths range from 14 to 46 weeks, so the prediction point is relative: one row per student at week ⌈⅓ × length⌉, with the ladder rerun at ¼ and ½.

---

## IV. Method

### A. Transfer-distance ladder

For an ordered pair (S, T): **D0** if S = T, scored by 5-fold stratified cross-validation; **D1** the same course in another year; **D2** another course at the same institution; **D3** another institution. All 3,969 ordered pairs are evaluated for three representations and three model families. Because the four classes average over different sets of target cohorts, headline tables restrict to the 40 targets present at all four distances and we state plainly that this restriction excludes Oviedo, which has one academic year, and Zambia, which has one course; all-target figures are reported alongside.

### B. Representations

**raw** counts; **z-score** and **percentile**, both computed within the cohort being scored, at the cutoff week, using no labels.

### C. Models

The object of study is a fixed gradient-boosting classifier [21] (200 trees, depth 3, learning rate 0.05), the configuration the literature reaches for by default. Logistic regression with standardised inputs and a 300-tree random forest are run alongside as robustness checks, the first because linear models have been reported to transfer better [10]. No hyperparameter is tuned per cohort: the question is what an ordinary model does when moved, not how well a tuned one can be made to score. Each model is fitted once per source cohort and applied to every target.

### D. Metrics

Discrimination is ROC-AUC. Calibration is the Brier score and calibration-in-the-large, the mean predicted failure probability minus the observed failure rate. Decision quality is recall and precision of failing students inside a fixed 20 % flag budget, which is what an institution with finite advising capacity actually sets. F1 is reported on the **failing** class, always beside the F1 of alerting everyone. Explanation agreement is Kendall tau and top-3 Jaccard between the transferred model's permutation-importance ranking on the target and a locally trained model's, with the floor, ceiling and random baseline of Section V-E.

### E. Disclosed compute settings

Permutation-importance rankings are computed for the primary model only, with three repeats and targets subsampled to 1,500 rows. None affects a reported AUC, calibration or decision metric.

---

## V. Results

### A. The signal is a property of the institution

| Institution | Cohorts | D0 AUC | Range |
|---|---|---|---|
| OULAD | 19 | 0.845 | 0.709–0.897 |
| UKZN | 16 | 0.667 | 0.536–0.814 |
| KU Leuven | 6 | 0.611 | 0.586–0.653 |
| Oviedo | 20 | 0.606 | 0.384–0.953 |
| Zambia | 2 | 0.527 | 0.455–0.598 |

Clickstream engagement predicts course outcome well at the Open University and near chance at Zambia. A single-dataset study measures one point of this range and reports it as the state of the art.

### B. Discrimination degrades gradually

Across all 63 targets, gradient boosting falls from 0.691 within cohort to 0.597 across institutions; on the paired 40 the figures are 0.746 and 0.614 (Table II, Fig. 2a). The gap is 0.09 to 0.13 depending on the estimator, and we report both rather than the flattering one. Random forest is the most robust family under raw features and gradient boosting the least, which qualifies the report that linear models transfer best [10]: that ordering appears only after the representation is fixed.

### C. Calibration collapses, and a label-free transform restores it

| Gradient boosting, all 63 targets | D0 | D3 raw | D3 percentile |
|---|---|---|---|
| ROC-AUC | 0.691 | 0.597 | 0.617 |
| Brier score | 0.197 | 0.361 | 0.322 |
| Calibration-in-the-large | −0.008 | **+0.119** | **−0.009** |

A transferred model over-predicts failure risk by 12 percentage points, and the within-cohort percentile representation removes that bias almost exactly, at every rung, without a single target label. In the vocabulary of [12] this is calibration-in-the-large restored while weaker calibration remains imperfect, and it is what the clinical updating ladder [13] would attempt first.

The mechanism is not the one we initially assumed. A regression of per-pair AUC loss on measured shift shows the correlation with click-scale shift essentially unchanged under the transform (0.067 to 0.077); what falls is the correlation with distribution-shape shift, from 0.283 to 0.189, and the explained variance from 0.116 to 0.062. Prevalence shift, the largest component at D3, survives the transform untouched — which is precisely why it repairs calibration-in-the-large and nothing else.

### D. Recalibration is necessary but not sufficient

At a 20 % flag budget the transform is worth nothing: recall of failing students is 0.272 raw and 0.274 percentile at D3, against 0.326 within cohort. Lift over random flagging falls from 1.63 to 1.36. On F1 over the failing class the transform is actively worse (0.421 raw, 0.348 percentile), and a source-rate threshold — flagging the share of the target that the source cohort had failing — recovers percentile to 0.415 while leaving raw at 0.406.

All four rules lose to alerting everyone, which scores 0.546, and none beats it in more than 27 % of pairs. F1 on a class with prevalence near 0.4 is dominated by the trivial rule, so it should not be reported in this setting without that baseline beside it. What survives is the flag-budget result: a transferred model still finds 36 % more failing students than random selection, and that, not F1, is the honest deployment number.

### E. Explanation agreement has a low ceiling before transfer is considered

| Reference point (gradient boosting) | Kendall tau | top-3 Jaccard |
|---|---|---|
| Same model, reseeded (noise floor) | 0.707 | 0.744 |
| Two models, disjoint halves of the same cohort (ceiling) | 0.338 | 0.487 |
| Transferred model vs local, other institution | 0.026 | 0.323 |
| Independent random rankings | 0.000 | 0.303 |

We set out to show that transfer destroys explanations. It does not, because there was little to destroy: two models trained on disjoint halves of the *same* cohort, ranked on the same data, agree at 0.338. Cross-institution agreement of 0.026 sits barely above the random baseline, and the percentile transform does not help (0.018). Agreement declines monotonically with distance — 0.207 at D1, 0.102 at D2, 0.026 at D3 — but the correct statement is that permutation-importance rankings over these seven correlated features are weakly identified in the first place, consistent with [18], and transfer moves them from weakly identified to indistinguishable from chance. A teacher-facing panel showing such a ranking is not made trustworthy by keeping the model local.

### F. Transfer costs the worst-served group most

Sensitive attributes are used only to evaluate, never as features. At a 20 % flag budget:

| Attribute | Gap, local | Gap, transferred | Worst group recall, local → transferred |
|---|---|---|---|
| Deprivation index (OULAD) | 0.182 | 0.164 | 0.285 → 0.209 |
| School quintile (UKZN) | 0.125 | 0.160 | 0.654 → 0.182 |
| Race (UKZN) | 0.102 | 0.154 | 0.526 → 0.205 |
| Gender (OULAD) | 0.035 | 0.038 | 0.392 → 0.275 |

Deprivation produces the widest disparity even locally. Transfer widens the gap on the two South African attributes and lowers the worst-served group's recall in every case. The UKZN local figures rest on few cohorts and should be read as indicative; the transferred figures do not. A click-volume risk score is partly a device-and-connectivity score, and this is what that looks like at the point of decision.

### G. Two hazards we created and then found

**A majority-class F1 flatters every model.** Our first implementation scored F1 with the default positive label, which is *passing*. Every configuration then looked healthy while losing to a trivial rule on the class that matters. The check that catches this costs one line: print the trivial baseline beside every F1.

**Within-institution transfer is contaminated by shared students.** 72 of 78 same-course pairs and 324 of 916 other-course pairs share students between training and evaluation, up to 94 % of the target cohort. Cross-institution pairs are effectively clean: 78 of 2,912 show any overlap at all, and never more than 1.5 %. Removing contaminated pairs lowers D1 from 0.715 to 0.656 and, with it, removes the artefact by which same-course transfer appeared to *beat* within-cohort performance. Any ladder of this shape must report per-pair overlap.

### H. Sensitivity

Rerunning the ladder at one quarter and one half of course length moves every level and no conclusion (gradient boosting, all 63 cohorts):

| Cutoff | D0 AUC | D3 AUC raw | D3 AUC pct | D3 calibration raw | D3 calibration pct | D3 recall@20 raw | D3 recall@20 pct | D3 tau |
|---|---|---|---|---|---|---|---|---|
| 1/4 | 0.669 | 0.587 | 0.616 | +0.120 | −0.001 | 0.265 | 0.271 | 0.038 |
| 1/3 | 0.691 | 0.597 | 0.617 | +0.119 | −0.009 | 0.272 | 0.274 | 0.026 |
| 1/2 | 0.723 | 0.624 | 0.654 | +0.125 | −0.000 | 0.293 | 0.301 | 0.029 |

A later cutoff sees more activity and predicts better everywhere. What does not move is the structure: the cross-institution discrimination gap stays between 0.082 and 0.099, the calibration bias stays near +0.12 and is removed to within 0.01 at every cutoff, the flag-budget gain from the transform stays under 0.01, and explanation agreement stays between 0.026 and 0.038. All four results are properties of the transfer, not of where the alarm is raised.

---

## VI. Discussion and Limitations

The useful way to read these results is that early-warning models fail in the way transported clinical risk models fail, and should be reported the same way. Discrimination is the property that travels; calibration is the property that breaks; and the cheapest repair in the clinical updating ladder — adjust the intercept, change nothing else — is what our percentile transform turns out to be, arrived at by a different route. An institution deploying a borrowed model should recalibrate before it does anything else, and should not expect recalibration to make the model better at finding students.

Two of our own hypotheses did not survive contact with the right baselines, and we report them as results rather than removing them. That is the point of releasing the benchmark: the same ladder can now be used against a proposed fix by someone else.

**Limitations.** Label semantics differ across institutions and are perfectly collinear with institution, so no analysis here separates the two. Course calendars for the three Moodle institutions are inferred from activity, not published. Zambia contributes two small cohorts and its numbers should be read as indicative. Oviedo is capped at 20 of 94 eligible courses. The headline paired estimator excludes Oviedo and Zambia structurally, which is why all-target figures are given beside it. Bootstrap intervals resample pairs, which share target cohorts, so they are narrower than a fully clustered interval would be. Everything here is correlational: the feature rankings are not causal accounts of failure, and Section V-E is an argument against reading them that way at all.

---

## VII. Conclusion

On a public benchmark of 63 cohorts from five institutions, an ordinary early-warning model loses about 0.1 ROC-AUC when it crosses an institutional boundary, over-predicts risk by 12 percentage points, and produces a feature ranking indistinguishable from random. A within-cohort percentile representation, requiring no target labels, removes the calibration bias entirely and improves nothing else. At a fixed flag budget the transferred model still finds a third more failing students than random selection, and that modest number is the honest case for deploying one.

Two of our three original claims did not survive their own baselines, and the reasons generalise. F1 on the majority class makes any model look adequate. Permutation-importance rankings over correlated engagement features are unstable before any transfer occurs. And a cross-course evaluation inside one institution can share almost all of its students between training and test. We release the benchmark, five institution adapters, and the frozen results so that the next proposed fix can be measured against the same ladder, including the parts of it that defeated ours.

---

## References

[1] J. Kuzilek, M. Hlosta, and Z. Zdrahal, "Open University Learning Analytics dataset," *Scientific Data*, vol. 4, art. 170171, 2017, doi: 10.1038/sdata.2017.171.
[2] E. Tiukhova, D. Van Landuyt, B. Baesens, and M. Snoeck, "Open data, private learners: a de-identified student activity and performance dataset for learning analytics," *Scientific Data*, vol. 13, art. 548, 2026, doi: 10.1038/s41597-026-06821-3.
[3] R. Raghavjee, P. R. Subramaniam, and I. Govender, "Anonymized dataset of Information Systems and Technology students at a South African university for learning analytics," *Data*, vol. 11, no. 1, art. 1, 2026, doi: 10.3390/data11010001.
[4] A. Bettahi, F.-Z. Belouadha, and H. Harroud, "A modular and explainable machine learning pipeline for student dropout prediction in higher education," *Algorithms*, vol. 18, no. 10, art. 662, 2025, doi: 10.3390/a18100662.
[5] S. Boujmiraz, H. Darhmaoui, and A. Drissi el Maliani, "Predicting student performance: a comprehensive review of machine learning, deep learning, and explainable AI approaches," *Computers and Education: Artificial Intelligence*, vol. 10, art. 100548, 2026, doi: 10.1016/j.caeai.2026.100548.
[6] R. Guevara-Reyes, I. Ortiz-Garcés, R. Andrade, F. Cox-Riquetti, and W. Villegas-Ch, "Machine learning models for academic performance prediction: interpretability and application in educational decision-making," *Frontiers in Education*, vol. 10, art. 1632315, 2025, doi: 10.3389/feduc.2025.1632315.
[7] J. López-Zambrano, J. A. Lara, and C. Romero, "Towards portability of models for predicting students' final performance in university courses starting from Moodle logs," *Applied Sciences*, vol. 10, no. 1, art. 354, 2020, doi: 10.3390/app10010354.
[8] J. López-Zambrano, J. A. Lara, and C. Romero, "Improving the portability of predicting students' performance models by using ontologies," *Journal of Computing in Higher Education*, vol. 34, pp. 1–19, 2022, doi: 10.1007/s12528-021-09273-3.
[9] J. Gardner, R. Yu, Q. Nguyen, C. Brooks, and R. Kizilcec, "Cross-institutional transfer learning for educational models: implications for model performance, fairness, and equity," in *Proc. ACM Conf. Fairness, Accountability, and Transparency (FAccT)*, 2023.
[10] J. Schwerter et al., "Cross-course generalizability of SRL-aligned predictive models using digital learning traces," arXiv:2604.22812, 2026.
[11] G. S. Collins, K. G. M. Moons, P. Dhiman, and R. D. Riley, "TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods," *BMJ*, vol. 385, art. e078378, 2024, doi: 10.1136/bmj-2023-078378.
[12] B. Van Calster, D. J. McLernon, M. van Smeden, et al., "Calibration: the Achilles heel of predictive analytics," *BMC Medicine*, vol. 17, art. 230, 2019, doi: 10.1186/s12916-019-1466-7.
[13] Y. Vergouwe, D. Nieboer, R. Oostenbrink, and T. P. A. Debray, "A closed testing procedure to select an appropriate method for updating prediction models," *Statistics in Medicine*, vol. 36, pp. 4529–4539, 2016, doi: 10.1002/sim.7179.
[14] M. Riestra-González, M. del P. Paule-Ruíz, and F. Ortin, "Massive LMS log data analysis for the early prediction of course-agnostic student performance," *Computers & Education*, vol. 163, art. 104108, 2021, doi: 10.1016/j.compedu.2020.104108.
[15] V. Swamy, M. Marras, and T. Käser, "Meta transfer learning for early success prediction in MOOCs," in *Proc. 9th ACM Conf. Learning @ Scale (L@S)*, 2022.
[16] M. Saerens, P. Latinne, and C. Decaestecker, "Adjusting the outputs of a classifier to new a priori probabilities: a simple procedure," *Neural Computation*, vol. 14, no. 1, pp. 21–41, 2002, doi: 10.1162/089976602753284446.
[17] E. Tiukhova et al., "Explainable learning analytics: assessing the stability of student success prediction models by means of explainable AI," *Decision Support Systems*, vol. 182, art. 114229, 2024, doi: 10.1016/j.dss.2024.114229.
[18] G. Hooker, L. Mentch, and S. Zhou, "Unrestricted permutation forces extrapolation: variable importance requires at least one more model, or there is no free variable importance," *Statistics and Computing*, vol. 31, art. 82, 2021, doi: 10.1007/s11222-021-10057-z.
[19] V. Švábenský, B. Flanagan, C. López Zapata, and A. Shimada, "Open datasets in learning analytics: trends, challenges, and best practice," *ACM Trans. Knowledge Discovery from Data*, 2026, doi: 10.1145/3798096.
[20] L. Phiri, "A multi-source dataset for CS1 failure prediction in a sub-Saharan African context," Zenodo, 2026, doi: 10.5281/zenodo.21292883.
[21] J. H. Friedman, "Greedy function approximation: a gradient boosting machine," *Annals of Statistics*, vol. 29, no. 5, pp. 1189–1232, 2001.

---

*ARCHIVED 2026-09-06. Version 3, built around the zero-training baseline. Superseded when exp_022 showed that explainer choice destabilises feature rankings more than the training sample does. The baseline audit survives as a control in the current draft. Current: side2026_paper.md.*
