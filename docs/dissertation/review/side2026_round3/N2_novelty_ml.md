# N2 — Novelty Verdict: the ML / statistics literature

**Stage:** bibliography and source verification, adversarial (goal = falsify novelty).
**Hypothesis under attack:** *"Given a new tabular dataset, one can predict from its UNLABELLED properties alone (sample size, feature distributions, dispersion, share of degenerate rows) both how well a supervised model will perform on it, and whether that model will beat a trivial single-feature baseline."*
**Concrete instance:** 63 student cohorts, 5 universities, within-cohort AUC 0.44–0.94, corr(AUC, n) = +0.60.
**Date:** 2026-09-06. Every reference below was verified against Crossref (`api.crossref.org/works/<DOI>`) or a page actually fetched. Unverifiable candidates were dropped.

---

## 1. Search strategy — exact queries run

Web search (Google-backed), then DOI verification through the Crossref REST API for every retained item.

1. `meta-learning meta-features predicting classifier performance new dataset algorithm selection survey Brazdil Vanschoren`
2. `"predicting model accuracy on unlabeled data" unsupervised accuracy estimation without labels distribution shift`
3. `meta-learning predict whether machine learning model outperforms baseline dataset meta-features "worth" applying`
4. `Lorena "how complex is your classification problem" survey data complexity measures review`
5. `learning curve extrapolation predict final model performance sample size "learning curve" database Mohr van Rijn LCDB`
6. `Riley minimum sample size required developing clinical prediction model logistic regression`
7. `Bayes error rate estimation before modelling irreducible error estimating achievable accuracy dataset`
8. `individual participant data meta-analysis external validation heterogeneity AUC across cohorts meta-regression study-level characteristics Debray Riley`
9. `Ferrari Dacrema "Are we really making much progress" recommender baselines RecSys 2019 reproducibility`
10. `"value of information" decision whether to build predictive model expected benefit before development machine learning`
11. `McElfresh "When Do Neural Nets Outperform Boosted Trees on Tabular Data" meta-features predict which model wins NeurIPS 2023`
12. `Dataset2Vec meta-feature learning dataset representation performance prediction Jomaa Schmidt-Thieme`
13. `meta-learning educational data mining predict dropout model performance across courses dataset characteristics sample size AUC variation`
14. `label-free "unsupervised" meta-features algorithm selection without target labels predict task difficulty before labelling`
15. `Muñoz Villanova Baatar Smith-Miles "Instance spaces for machine learning classification" Machine Learning 2018 footprints meta-features`
16. `Musgrave "A Metric Learning Reality Check" AND Lin "neural hype" weak baselines ad hoc retrieval`
17. `Christodoulou systematic review machine learning versus logistic regression no performance benefit clinical prediction; sample size determines whether ML outperforms logistic regression`
18. `Deng Zheng "Are Labels Always Necessary for Classifier Accuracy Evaluation" dataset-level regression predict accuracy Frechet distance`
19. `meta-learning predict performance gap between AutoML and default baseline "is it worth" running expensive search dataset meta-features`
20. `Ethayarajh "Understanding Dataset Difficulty with V-Usable Information" ICML 2022 predictability of dataset`
21. `"meta-learning" predict "improvement over" simple baseline dataset characteristics "when is machine learning useful" tabular datasets regression on meta-features`
22. `"comprehensive benchmark" machine deep learning tabular datasets meta-learning predict whether deep learning outperforms 92% accuracy statistical properties`
23. `predicting external validation AUC at new hospital site from site characteristics case-mix heterogeneity transportability prediction model before validation`
24. `van Klaveren Steyerberg "model-based concordance" new concordance measure risk prediction external validation case-mix 2016`
25. `van Leeuwen "Instability of the AUROC" clinical prediction models Statistics in Medicine 2025 sample size stable`
26. `meta-features weak predictive power meta-learning performance prediction unreliable landmarkers dominate critique evaluation of meta-learning algorithm selection`
27. `Bilalli Abello Aluja-Banet "On the predictive power of meta-features in OpenML" International Journal of Applied Mathematics and Computer Science 2017 DOI`
28. `data quality metrics predict machine learning model performance "data readiness" missingness constant rows dataset quality score predicts accuracy`
29. `Sadatsafavi "Uncertainty and the value of information in risk prediction modeling" EVPI development whether model should be abandoned Medical Decision Making`
30. `learning analytics generalizability predictive models across institutions courses "sample size" predicts AUC variation early warning cross-institutional`

Pages fetched in full (not just snippets): arXiv abstract pages for 2405.07662, 2409.01635, 2408.14817, 2201.04234; the NeurIPS 2023 D&B abstract page for McElfresh et al.; the PLOS ONE article page for Nieboer et al.; the PMC article page for Uddin & Lu.

---

## 2. The meta-learning verdict — blunt

**Meta-learning owns the hypothesis as stated. Not most of it: essentially all of it.**

The hypothesis is Rice's algorithm selection problem with the performance-prediction head attached. Rice defined the problem in 1976 as a mapping from *problem features* to *algorithm performance*, which is literally the claim (Rice, J. R. (1976). The Algorithm Selection Problem. *Advances in Computers*, 65–118. DOI 10.1016/S0065-2458(08)60520-3 — verified). Smith-Miles' survey established the meta-learning formulation across disciplines fifteen years before this project (Smith-Miles, K. A. (2009). Cross-disciplinary perspectives on meta-learning for algorithm selection. *ACM Computing Surveys*, 41, 1–25. DOI 10.1145/1456650.1456656 — verified).

Three specific dismantlings:

**(a) "Predict how well a supervised model will perform on a new dataset" is the textbook definition of a meta-model.** Vanschoren's AutoML-book chapter states the task directly — build a meta-model over meta-features that predicts the performance of a configuration on a previously unseen task (Vanschoren, J. (2019). Meta-Learning. In *Automated Machine Learning*, Springer Series on Challenges in Machine Learning, 35–61. DOI 10.1007/978-3-030-05318-5_2 — verified). The book-length treatment is Brazdil, P., van Rijn, J. N., Soares, C., & Vanschoren, J. (2022). *Metalearning: Applications to Automated Machine Learning and Data Mining* (2nd ed.), Cognitive Technologies, Springer. DOI 10.1007/978-3-030-67024-5 — verified. The infrastructure that made it routine is OpenML (Vanschoren, J., van Rijn, J. N., Bischl, B., & Torgo, L. (2014). OpenML: networked science in machine learning. *ACM SIGKDD Explorations Newsletter*, 15, 49–60. DOI 10.1145/2641190.2641198 — verified).

**(b) The "UNLABELLED properties alone" restriction buys nothing.** The named properties — sample size, feature distributions, dispersion — are the *simple* and *statistical* meta-feature families, catalogued and standardised long ago. Rivolli et al. give the canonical taxonomy and explicitly separate simple/statistical meta-features (number of instances, number of attributes, mean, standard deviation, skewness, kurtosis, correlation) from the label-dependent families (information-theoretic, model-based, landmarking) (Rivolli, A., Garcia, L. P. F., Soares, C., Vanschoren, J., & de Carvalho, A. C. P. L. F. (2022). Meta-features for meta-learning. *Knowledge-Based Systems*, 240, 108101. DOI 10.1016/j.knosys.2021.108101 — verified). Computing them without labels is not an innovation; it is the default for that half of the standard feature set. Learned label-free dataset embeddings also already exist (Jomaa, H. S., Schmidt-Thieme, L., & Grabocka, J. (2021). Dataset2Vec: learning dataset meta-features. *Data Mining and Knowledge Discovery*, 35, 964–985. DOI 10.1007/s10618-021-00737-9 — verified).

**(c) "Whether the model beats a baseline" is also already a meta-learning target, twice over, and once with the exact meta-features named in the hypothesis.** McElfresh et al. analyse "dozens of metafeatures to determine what properties of a dataset make NNs or GBDTs better-suited to perform well" over "19 algorithms across 176 datasets", and the winning meta-features are precisely feature-distribution shape — irregular, skewed, heavy-tailed features favour GBDTs (McElfresh, D., Khandagale, S., Valverde, J., Prasad C, V., Ramakrishnan, G., Goldblum, M., & White, C. (2023). When Do Neural Nets Outperform Boosted Trees on Tabular Data? *Advances in Neural Information Processing Systems 36*, Datasets and Benchmarks Track. https://proceedings.neurips.cc/paper_files/paper/2023/hash/f06d5ebd4ff40b40dd97e30cee632123-Abstract-Datasets_and_Benchmarks.html — page fetched; preprint arXiv:2305.02997). More damaging still, one paper trains an explicit binary meta-classifier for "does the more complex family win": Shmuel, A., Glickman, O., & Lazebnik, T. (2024). A Comprehensive Benchmark of Machine and Deep Learning Across Diverse Tabular Datasets. arXiv:2408.14817 — abstract page fetched; the abstract states they "train a model that predicts scenarios where DL models outperform alternative methods with 86.1% accuracy (AUC 0.78)" over 111 datasets and 20 models. That is the second half of the hypothesis, executed, with a reported skill figure.

**Consequence.** Any reviewer who knows this literature will read the hypothesis as "we did meta-learning on 63 tasks". The only things they will look for are (i) whether the meta-target is new, (ii) whether the meta-dataset design is new, and (iii) whether n = 63 with 5 institution clusters can support a meta-regression at all. On (iii) the honest answer is no: the comparison corpora are 111, 176, 200, 216 and 246 datasets, and 63 cohorts nested in 5 institutions gives roughly 5 independent points for any institution-level meta-feature.

A closely related instance-space line makes the "where do simple things suffice" question explicit through algorithm *footprints* in meta-feature space: Muñoz, M. A., Villanova, L., Baatar, D., & Smith-Miles, K. (2018). Instance spaces for machine learning classification. *Machine Learning*, 107, 109–147. DOI 10.1007/s10994-017-5629-5 — verified.

---

## 3. Label-free performance prediction — what exists, and how close it gets

This is an active subfield. It is closer than the meta-learning line in *method*, further in *setting*.

- **AutoEval, the direct methodological analogue.** Deng & Zheng formulate accuracy estimation on an unlabelled test set as a *dataset-level regression* — regress classifier accuracy on overall feature statistics of the test set, trained over a meta-dataset of synthesised datasets. Deng, W., & Zheng, L. (2021). Are Labels Always Necessary for Classifier Accuracy Evaluation? *Proceedings of the IEEE/CVF CVPR 2021*, 15069–15078. https://openaccess.thecvf.com/content/CVPR2021/html/Deng_Are_Labels_Always_Necessary_for_Classifier_Accuracy_Evaluation_CVPR_2021_paper.html (page fetched; preprint arXiv:2007.02915). "Dataset-level regression of performance on unlabelled distributional statistics" is the hypothesis's own sentence, published in 2021.
- **Average Thresholded Confidence (ATC).** Garg, S., Balakrishnan, S., Lipton, Z. C., Neyshabur, B., & Sedghi, H. (2022). Leveraging Unlabeled Data to Predict Out-of-Distribution Performance. *ICLR 2022*. arXiv:2201.04234 — abstract page fetched. Inputs: labelled source data plus **unlabelled target data**; output: predicted target accuracy.
- **Distinction that partially saves the hypothesis.** ATC, agreement- and confidence-based estimators, and AutoEval all require *a trained model scored on the new data*. They predict how an existing model will do on a new sample; they do not predict how well a model *trained on that sample* will do. The hypothesis is about the latter — achievable within-cohort performance, model not yet trained. That is a real gap between the two problems, and it is the strongest technical point available here.
- **But the clinical literature closes exactly that gap for the cross-cohort case.** Model-based concordance computes the *expected* c-statistic in a new cohort using only the development model's coefficients and the new cohort's predictor values, with outcomes simulated rather than observed — i.e. an expected AUC from unlabelled case-mix. van Klaveren, D., Gönen, M., Steyerberg, E. W., & Vergouwe, Y. (2016). A new concordance measure for risk prediction models in external validation settings. *Statistics in Medicine*, 35, 4136–4152. DOI 10.1002/sim.6997 — verified. Its applied companion: Nieboer, D., van der Ploeg, T., & Steyerberg, E. W. (2016). Assessing Discriminative Performance at External Validation of Clinical Prediction Models. *PLOS ONE*, 11(2), e0148820. DOI 10.1371/journal.pone.0148820 — verified and fetched; the article states "the mbc is the expected c-statistic in a population given that the prediction model is correct." The framework that motivates it: Debray, T. P. A., Vergouwe, Y., Koffijberg, H., Nieboer, D., Steyerberg, E. W., & Moons, K. G. M. (2015). A new framework to enhance the interpretation of external validation studies of clinical prediction models. *Journal of Clinical Epidemiology*, 68, 279–289. DOI 10.1016/j.jclinepi.2014.06.018 — verified. Heterogeneity of AUC across cohorts and its attribution to cohort characteristics is standard IPD-MA practice: Steyerberg, E. W., Nieboer, D., Debray, T. P. A., & van Houwelingen, H. C. (2019). Assessment of heterogeneity in an individual participant data meta-analysis of prediction models: An overview and illustration. *Statistics in Medicine*, 38, 4290–4309. DOI 10.1002/sim.8296 — verified; and Snell, K. I. E., Hua, H., Debray, T. P. A., Ensor, J., Look, M. P., Moons, K. G. M., & Riley, R. D. (2016). Multivariate meta-analysis of individual participant data helped externally validate the performance and implementation of a prediction model. *Journal of Clinical Epidemiology*, 69, 40–50. DOI 10.1016/j.jclinepi.2015.05.009 — verified.

**Net:** label-free prediction of *deployed* accuracy is largely solved in ML; label-free prediction of *expected discrimination in a new cohort* is largely solved in clinical statistics. Between them the hypothesis has almost no uncontested ground.

---

## 4. Closest prior work, ranked by threat level

Every entry verified. Threat = how directly it pre-empts the hypothesis.

### Tier 1 — kills the hypothesis as stated

| # | Work | Why fatal |
|---|---|---|
| 1 | Rice, J. R. (1976). The Algorithm Selection Problem. *Advances in Computers*, 65–118. DOI 10.1016/S0065-2458(08)60520-3 | Defines "map problem features → algorithm performance". Fifty years old. |
| 2 | Vanschoren, J. (2019). Meta-Learning. In *Automated Machine Learning*, 35–61. DOI 10.1007/978-3-030-05318-5_2 | Canonical statement of performance prediction from meta-features on a new task. |
| 3 | Rivolli, A., Garcia, L. P. F., Soares, C., Vanschoren, J., & de Carvalho, A. C. P. L. F. (2022). Meta-features for meta-learning. *Knowledge-Based Systems*, 240, 108101. DOI 10.1016/j.knosys.2021.108101 | The exact meta-features named in the hypothesis, standardised and taxonomised, with the label-free subset explicitly delineated. |
| 4 | Shmuel, A., Glickman, O., & Lazebnik, T. (2024). A Comprehensive Benchmark of Machine and Deep Learning Across Diverse Tabular Datasets. arXiv:2408.14817 | Trains a meta-model that predicts *whether the more complex approach wins*: 86.1% accuracy, AUC 0.78, 111 datasets. This is the "beats a baseline" head, published with a skill number. |
| 5 | McElfresh, D., Khandagale, S., Valverde, J., Prasad C, V., Ramakrishnan, G., Goldblum, M., & White, C. (2023). When Do Neural Nets Outperform Boosted Trees on Tabular Data? *NeurIPS 36*, Datasets and Benchmarks Track. | Predicts which family wins from *feature-distribution shape* (skew, heavy tails) — the hypothesis's own predictor set, on 176 datasets. |

### Tier 2 — kills the cross-cohort instance specifically

| # | Work | Why |
|---|---|---|
| 6 | van Klaveren, D., Gönen, M., Steyerberg, E. W., & Vergouwe, Y. (2016). A new concordance measure for risk prediction models in external validation settings. *Statistics in Medicine*, 35, 4136–4152. DOI 10.1002/sim.6997 | Model-based concordance: expected AUC in a new cohort from unlabelled covariates alone. |
| 7 | Nieboer, D., van der Ploeg, T., & Steyerberg, E. W. (2016). *PLOS ONE*, 11(2), e0148820. DOI 10.1371/journal.pone.0148820 | Applies it; separates the case-mix effect from model invalidity as the explanation of AUC differences across validation cohorts. |
| 8 | Debray, T. P. A., Vergouwe, Y., Koffijberg, H., Nieboer, D., Steyerberg, E. W., & Moons, K. G. M. (2015). *Journal of Clinical Epidemiology*, 68, 279–289. DOI 10.1016/j.jclinepi.2014.06.018 | Membership model over covariates quantifies the relatedness of a new cohort and anticipates performance there. |
| 9 | Steyerberg, E. W., Nieboer, D., Debray, T. P. A., & van Houwelingen, H. C. (2019). *Statistics in Medicine*, 38, 4290–4309. DOI 10.1002/sim.8296 | Cross-cohort AUC heterogeneity and its attribution is routine IPD-MA methodology. |

### Tier 3 — label-free performance prediction (methodologically adjacent, different setting)

| # | Work |
|---|---|
| 10 | Deng, W., & Zheng, L. (2021). Are Labels Always Necessary for Classifier Accuracy Evaluation? *CVPR 2021*, 15069–15078. (openaccess.thecvf.com page fetched; preprint arXiv:2007.02915) — "dataset-level regression" from unlabelled feature statistics. |
| 11 | Garg, S., Balakrishnan, S., Lipton, Z. C., Neyshabur, B., & Sedghi, H. (2022). Leveraging Unlabeled Data to Predict Out-of-Distribution Performance. *ICLR 2022*. arXiv:2201.04234. |

### Tier 4 — difficulty / complexity, and the sample-size axis

| # | Work | Escape hatch |
|---|---|---|
| 12 | Ho, T. K., & Basu, M. (2002). Complexity measures of supervised classification problems. *IEEE TPAMI*, 24, 289–300. DOI 10.1109/34.990132 | **Label-dependent.** Cannot be computed on unlabelled data. |
| 13 | Lorena, A. C., Garcia, L. P. F., Lehmann, J., Souto, M. C. P., & Ho, T. K. (2019). How Complex Is Your Classification Problem? A Survey on Measuring Classification Complexity. *ACM Computing Surveys*, 52, 1–34. DOI 10.1145/3347711 | Same: the measures are "extracted from the training datasets", i.e. with labels. |
| 14 | Ethayarajh, K., Choi, Y., & Swayamdipta, S. (2022). Understanding Dataset Difficulty with V-Usable Information. *PMLR* 162, 5988–6008. https://proceedings.mlr.press/v162/ethayarajh22a.html | Label-dependent; measures usable information in (X, Y). |
| 15 | Mohr, F., Viering, T. J., Loog, M., & van Rijn, J. N. (2023). LCDB 1.0: An Extensive Learning Curves Database for Classification Tasks. *LNCS*, 3–19. DOI 10.1007/978-3-031-26419-1_1 | Owns the *sample-size → performance* axis empirically: 20 learners × 246 datasets. |
| 16 | Kielhöfer, L., Mohr, F., & van Rijn, J. N. (2024). Learning Curve Extrapolation Methods Across Extrapolation Settings. *LNCS*, 145–157. DOI 10.1007/978-3-031-58553-1_12 | Extrapolates performance from partial data — but requires labels for the observed portion. |

### Tier 5 — the baseline-audit literature (documents the phenomenon; does *not* predict it)

| # | Work |
|---|---|
| 17 | Ferrari Dacrema, M., Cremonesi, P., & Jannach, D. (2019). Are we really making much progress? A worrying analysis of recent neural recommendation approaches. *RecSys '19*, 101–109. DOI 10.1145/3298689.3347058 |
| 18 | Yang, W., Lu, K., Yang, P., & Lin, J. (2019). Critically Examining the "Neural Hype": Weak Baselines and the Additivity of Effectiveness Gains from Neural Ranking Models. *SIGIR '19*, 1129–1132. DOI 10.1145/3331184.3331340 |
| 19 | Musgrave, K., Belongie, S., & Lim, S.-N. (2020). A Metric Learning Reality Check. *ECCV 2020*, LNCS, 681–699. DOI 10.1007/978-3-030-58595-2_41 |
| 20 | Christodoulou, E., Ma, J., Collins, G. S., Steyerberg, E. W., Verbakel, J. Y., & Van Calster, B. (2019). A systematic review shows no performance benefit of machine learning over logistic regression for clinical prediction models. *Journal of Clinical Epidemiology*, 110, 12–22. DOI 10.1016/j.jclinepi.2019.02.004 |
| 21 | Knauer, R., & Rodner, E. (2024). Squeezing Lemons with Hammers: An Evaluation of AutoML and Tabular Deep Learning for Data-Scarce Classification Applications. ICLR 2024 Workshop on Practical ML for Low Resource Settings. arXiv:2405.07662 — abstract page fetched; L2-regularised logistic regression matches AutoML on the majority of 44 datasets with n ≤ 500. |
| 22 | Knauer, R., Grimm, M., & Rodner, E. (2024). PMLBmini: A Tabular Classification Benchmark Suite for Data-Scarce Applications. AutoML 2024 Workshop Track. arXiv:2409.01635 — abstract page fetched; "state-of-the-art AutoML and deep learning approaches often fail to appreciably outperform even a simple logistic regression baseline." (A separate paper from #21 — do not merge the two.) |

**Note on Tier 5:** none of these *predicts in advance where* the simple baseline will not be beaten. They audit retrospectively. #21 and #22 come closest because they isolate the data-scarce regime (n ≤ 500) as the condition — which is sample size, the hypothesis's leading predictor — but they report it as a benchmark finding, not as a fitted predictive rule.

### Tier 6 — the go/no-go decision, and the inverse (sample size from performance)

| # | Work | Relation |
|---|---|---|
| 23 | Sadatsafavi, M., Lee, T. Y., & Gustafson, P. (2022). Uncertainty and the Value of Information in Risk Prediction Modeling. *Medical Decision Making*, 42, 661–671. DOI 10.1177/0272989X221078789 | Development EVPI decides whether a model advances to validation, is abandoned, or needs a larger sample — but computed **after fitting, using outcomes**. |
| 24 | Sadatsafavi, M., Lee, T. Y., Wynants, L., Vickers, A. J., & Gustafson, P. (2023). Value-of-Information Analysis for External Validation of Risk Prediction Models. *Medical Decision Making*, 43, 564–575. DOI 10.1177/0272989X231178317 | Whether external validation is worth doing. Same limitation. |
| 25 | Riley, R. D., Snell, K. I. E., Ensor, J., Burke, D. L., Harrell, F. E. Jr., Moons, K. G. M., & Collins, G. S. (2019). Minimum sample size for developing a multivariable prediction model: PART II — binary and time-to-event outcomes. *Statistics in Medicine*, 38, 1276–1296. DOI 10.1002/sim.7992 | **Inverse direction, and an opening.** The formula requires an *anticipated* Cox-Snell R² as an input, currently guessed from a similar published study. |
| 26 | Hiniduma, K., Byna, S., & Bez, J. L. (2025). Data Readiness for AI: A 360-Degree Survey. *ACM Computing Surveys*, 57, 1–39. DOI 10.1145/3722214 | Covers the "share of degenerate rows" style of predictor as a data-quality construct; readiness scoring, not performance regression. |

---

## 5. Contradicting evidence (reported as required)

Three findings cut *against* the hypothesis being achievable at all, which is separate from it being novel. They must appear in any honest write-up.

1. **Meta-features are weak predictors for classification specifically.** Bilalli, B., Abelló, A., & Aluja-Banet, T. (2017). On the predictive power of meta-features in OpenML. *International Journal of Applied Mathematics and Computer Science*, 27, 697–712. DOI 10.1515/amcs-2017-0048 — verified. A 2026 study over 216 tabular datasets reports that regression performance is inferable from dataset characteristics while classification is not, with standard complexity measures failing to give actionable guidance: Billa, M., Orlandi, G., Guidetti, V., & Mandreoli, F. (2026). Interpretable ML Under the Microscope: Performance, Meta-Features, and the Regression-Classification Predictability Gap. arXiv:2601.00428 — abstract page fetched. If the hypothesis succeeds on 63 cohorts where these fail on 216 datasets, the reviewer's first assumption will be overfitting, not discovery.
2. **The +0.60 corr(AUC, n) is probably contaminated by estimator instability, not only by true difficulty.** van Leeuwen, F. D., Steyerberg, E. W., van Klaveren, D., Wessler, B., Kent, D. M., & van Zwet, E. W. (2025). Instability of the AUROC of Clinical Prediction Models. *Statistics in Medicine*, 44. DOI 10.1002/sim.70011 — verified. Small cohorts give noisy AUROC estimates *and* overfit more (Riley et al. 2019, above); both push measured within-cohort AUC around as a function of n. The correlation is at minimum confounded, and possibly an artifact. This is a bigger threat to the paper than novelty is.
3. **Sample size is not monotonically helpful in the existing meta-feature-to-performance literature.** Uddin, S., & Lu, H. (2024). Dataset meta-level and statistical features affect machine learning performance. *Scientific Reports*, 14, 1670. DOI 10.1038/s41598-024-51825-x — verified and fetched. 200 tabular datasets; meta-features = number of attributes, dataset size, positive-to-negative class ratio, plus mean / SD / skewness / kurtosis; multiple linear regression on accuracy. Dataset size was *negative* for SVM and logistic regression in imbalance-filtered analyses and insignificant elsewhere; the authors conclude "the relationship between dataset size and ML performance is not always direct." A cross-dataset study with 200 datasets and effectively the same predictor set found the opposite sign to the one being claimed here.

---

## 6. Verdict

### **ALREADY PUBLISHED** as stated. **PARTIALLY ANTICIPATED** at best after narrowing.

The hypothesis in its general form is a restatement of meta-learning for performance prediction (Rice 1976; Smith-Miles 2009; Vanschoren 2019; Brazdil et al. 2022), using the standard simple/statistical meta-feature families (Rivolli et al. 2022), with a "does the complex model win" head that has itself been published with a skill figure (Shmuel et al. 2024; McElfresh et al. 2023). The label-free framing, which looks like the distinguishing move, is the standard label-free half of the meta-feature catalogue, and separately it is the whole premise of a well-populated ML subfield (Deng & Zheng 2021; Garg et al. 2022). The cross-cohort instance is owned by clinical prediction methodology, where expected AUC in a new cohort is computed from unlabelled case-mix as a matter of routine (van Klaveren et al. 2016; Nieboer et al. 2016).

**Do not present this as a new question. It will be desk-rejected by anyone with an AutoML background.**

---

## 7. What survives, exactly

One cell of the design space is genuinely unclaimed, and it is small:

> **A prospective, label-free go/no-go test — "will *any* model beat the single best raw feature on this cohort?" — as the meta-target, in a meta-dataset where the task, the feature schema and the pipeline are held fixed and only the cohort varies.**

Three components; the novelty lives only in their conjunction.

1. **The reference arm is a trivial single-feature baseline, not a rival learner.** In every meta-learning study located, the comparator is another non-trivial algorithm in a portfolio (NN vs GBDT; AutoML vs the portfolio's best; DL vs classical). The "is modelling worth doing at all" arm is absent from meta-learning. It exists in the value-of-information literature (Sadatsafavi et al. 2022, 2023), but there it is computed *after fitting, with outcomes*. **Prospective + label-free + trivial-baseline reference is the one unclaimed combination.** It is a real distinction and it is thin — a reviewer can reasonably call the trivial baseline "just another portfolio arm".
2. **The task is held fixed across the meta-instances.** Every meta-learning corpus (OpenML, UCI, PMLB, the 176 / 200 / 216 / 246-dataset benchmarks) confounds meta-feature variation with task identity: a small dataset is also a *different problem*. 63 cohorts of one task, one schema, one pipeline decouple those. This is a design control, not a new question — but it is a control the meta-learning literature does not have, and it is the most defensible thing in the whole hypothesis.
3. **The unclaimed downstream use is achievable discrimination as an input to sample-size planning.** Riley et al.'s formula (DOI 10.1002/sim.7992) needs an anticipated Cox-Snell R² that practitioners currently borrow from a published analogue. Estimating it from unlabelled cohort properties addresses a named open input in a widely used method.

**What does not survive, stated plainly so it is not claimed by accident:** predicting accuracy or AUC from meta-features; using unlabelled meta-features; predicting which model family wins; sample size as the leading meta-feature; label-free accuracy estimation; expected AUC in a new cohort from case-mix; and the observation that simple baselines often are not beaten.

---

## 8. The strongest framing that survives an ML reviewer who knows this literature

Concede everything in §2 in the first paragraph, then claim only the control and the target. Something with this shape:

> Meta-learning has predicted algorithm performance from dataset meta-features since Rice (1976), and recent tabular benchmarks predict which model family wins from feature-distribution meta-features over 111–176 datasets (McElfresh et al. 2023; Shmuel et al. 2024). Every such corpus, however, confounds meta-feature variation with task identity: the small dataset is also a different problem, with a different schema, a different label definition and a different irreducible error. We contribute a **controlled meta-learning testbed** in which task, feature schema, label definition and pipeline are held fixed and only the cohort varies — 63 cohorts across 5 institutions — and we change the meta-target from *which algorithm* to *whether to model at all*: does any learner beat the single best raw feature? Under this control the dominant meta-feature is sample size (r = +0.60 with within-cohort AUC), and we quantify how much of that association is attributable to AUROC estimator instability at small n (van Leeuwen et al. 2025) rather than to intrinsic difficulty. We report the go/no-go meta-model's skill honestly, including where it fails, and note that with 63 cohorts nested in 5 institutions the effective sample for institution-level meta-features is 5.

Why this framing holds up:

- It cites the threats first, so the reviewer cannot spring them.
- Its contribution is a **control** plus a **negative-result decomposition**, both defensible at n = 63; a positive predictive claim is not.
- It pre-empts the strongest objection (§5.2) by making the confound part of the contribution rather than something caught in review.
- It does not claim to predict accuracy, which is settled, and does not claim label-free estimation as new, which it is not.

Framings that will not hold up and should be dropped: "we predict model performance from unlabelled dataset properties" (Vanschoren 2019); "we show unlabelled meta-features suffice" (Rivolli et al. 2022); "we predict whether ML beats a baseline" without the word *trivial* and without the fixed-task control (Shmuel et al. 2024); "we show sample size drives predictability" (LCDB, Mohr et al. 2023, plus §5.3's opposite-sign finding).
