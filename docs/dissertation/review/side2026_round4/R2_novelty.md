# R2 — Novelty Verdict: explainer disagreement vs data-induced disagreement

**Stage:** adversarial novelty check (goal = falsify).
**Claim under attack:** *"On a benchmark of 63 student cohorts from five universities, the agreement between two standard feature-importance estimators applied to the SAME fitted model on the SAME data (Kendall tau 0.123 for SHAP vs drop-column) is LOWER than the agreement between two models retrained on different years' students with a fixed estimator (0.210). Therefore the choice of explanation method destabilises a teacher-facing feature ranking more than the training data does."*
**Load-bearing element:** the ORDERING — explainer-induced disagreement placed on the same scale as data-induced disagreement, with a direction.
**Date:** 2026-09-06. Every reference below verified via Crossref (`api.crossref.org/works/<DOI>`) or a page/PDF actually fetched and read. Unverifiable candidates dropped.

---

## 1. Search strategy — exact queries run

Web search (Google-backed), then DOI verification through the Crossref REST API or direct fetch of the paper.

1. `explanation method disagreement versus data variability feature importance rank correlation which is larger`
2. `variance decomposition feature importance instability sources estimator seed sample model class`
3. `Swamy Käser "Evaluating the Explainers" black-box explainable machine learning student success prediction MOOCs EDM 2022`
4. `Verdinelli Wasserman "Feature Importance: A Closer Look at Shapley Values and LOCO" Statistical Science`
5. `Kalousis Prados Hilario "Stability of feature selection algorithms" high-dimensional spaces similarity between different algorithms outputs versus data perturbation`
6. `"choice of explanation method" versus "random seed" versus "data split" variance feature attribution ANOVA sources of variation`
7. `"explanation" stability "across retraining" versus "across explanation methods" same metric comparison Kendall tau feature ranking benchmark`
8. `SHAP versus permutation importance versus drop-column importance disagreement ranking same model empirical comparison`
9. `"more variation" OR "larger effect" "explanation method" than "the data" feature importance ranking teachers education explainable AI cohorts`
10. `Dong Rudin "variable importance clouds" Rashomon set Nature Machine Intelligence 2020 range of variable importance across good models`
11. `"matters more than" explainer choice model choice feature importance "explanation" empirical study which source dominates`
12. `learning analytics compare SHAP permutation importance LIME same student dropout model rank agreement multiple institutions`
13. `"disagreement problem" explanations compared with "model multiplicity" OR "predictive multiplicity" same benchmark relative magnitude which larger`
14. `benchmark quantifying explanation instability "method-induced" and "data-induced" variability feature ranking clinical risk model`
15. `Nogueira Sechidis Brown "On the Stability of Feature Selection Algorithms" JMLR 2018 similarity measure data perturbation`
16. `Haury Gestraud Vert "influence of feature selection methods on accuracy, stability and interpretability of molecular signatures" PLoS ONE 2011 overlap between methods versus between bootstrap samples`
17. `"explanation" disagreement "larger than" OR "exceeds" the variation from "different training sets" feature importance ranking study`
18. `"which source of variability" feature importance "explanation method" "data sample" "model" ranked comparison study interpretable machine learning 2024 2025`
19. `"explainer" OR "attribution method" disagreement benchmark "compared to" retraining across years cohorts temporal drift feature ranking same metric education`
20. `"the choice of explanation method" contributes more variance than "the training data" feature importance ranking study benchmark`
21. `Krishna Han Gu Pombra Jabbari Wu Lakkaraju "disagreement problem" published journal version 2024 Transactions Machine Learning Research`

**Read in full, not just snippets:** the Swamy et al. EDM 2022 PDF (text extracted locally with PyMuPDF and grepped); the Krishna et al. arXiv HTML v4 (downloaded, stripped, grepped for `retrain|random seed|different training set|resampl|bootstrap|data sampling`); arXiv abstract pages for 2603.15821, 2306.15786, 2607.16652, 2412.12115, 2602.11760, 2505.15728, 2507.22877, 2505.22541; the EDM 2022 proceedings landing page; the Haury et al. PMC full text; Crossref records for every DOI cited.

---

## 2. What Krishna et al. actually own

**Krishna, S., Han, T., Gu, A., Pombra, J., Jabbari, S., Wu, S., & Lakkaraju, H. (2022/2024). The Disagreement Problem in Explainable Machine Learning: A Practitioner's Perspective.** arXiv:2202.01602 (v4); published in *Transactions on Machine Learning Research*, 2024 (OpenReview forum `jESY2WTZCe`). HTML v4 fetched and read.

**What they measure.** Verbatim from the paper: *"a rigorous empirical analysis with four real-world datasets, six state-of-the-art post hoc explanation methods, and six different predictive models, to measure the extent of disagreement between the explanations generated by various popular explanation methods."*

- Explanation methods: LIME, KernelSHAP, Vanilla Gradient, Gradient×Input, Integrated Gradients, SmoothGrad.
- Datasets: COMPAS, German Credit, AG_News, ImageNet-1k — three modalities.
- Models: logistic regression, dense feed-forward NN, random forest, gradient-boosted tree, LSTM text classifier, ResNet-18.
- Metrics: feature agreement, rank agreement, sign agreement, signed rank agreement, **rank correlation**, pairwise rank agreement — the first four for top-*k*, the last two over a selected feature set.
- Plus a practitioner interview study and an online user study.

**Representative numbers.** Verbatim: *"for the neural network model trained on the COMPAS dataset, rank correlation displays a wide range of values across explanation method pairs, with 14 out of 15 explanation method pairs even exhibiting negative rank correlation when explaining multiple data points."* And: *"the average rank correlation between LIME and all other explanation methods is 0.273, as opposed to 0.113 in case of KernelSHAP."*

**What they do NOT own — the critical negative.** I grepped the full v4 HTML for `retrain`, `random seed`, `different training set`, `resampl`, `bootstrap`, `data sampling`. The **only** hit is a citation of ROAR ("Remove and Retrain") as a *faithfulness* evaluation technique in related work. There is **no baseline** in Krishna et al. against which the reported disagreement magnitudes can be judged. Their disagreement numbers float free: 0.113 is "low" only rhetorically. **They never place explainer disagreement on the same scale as data-, seed-, or model-induced disagreement.** This is exactly the gap the claim wants to occupy — and it is real *with respect to Krishna et al.*

That gap is real. It is just not unoccupied. See §5, Tier 1.

---

## 3. The variance-decomposition line — who has decomposed importance instability into sources

Nobody has published the specific two-way decomposition {estimator × data} on one scale in a general-ML venue. Several papers have published adjacent one-way or complementary decompositions.

**Closest: Thackshanaramana, B. (2026). Hypothesis Class Determines Explanation: Why Accurate Models Disagree on Feature Attribution.** arXiv:2603.15821v1, 16 Mar 2026. Abstract page and HTML fetched. This is the **exact mirror image** of the claim: it fixes the explainer and varies the model. From the paper: *"They fix the model and vary the explanation method. We fix the explanation method (SHAP) and vary the model."* Design: 24 datasets, prediction-equivalent models, Spearman rank correlation on SHAP rankings, seeds {42, 123, 456}, 80/20 splits. Reported means: tree–tree ρ = 0.676, linear–linear ρ = 0.827, tree–linear ρ = 0.415; a same-split control gives ρ = 1.000 within class versus 0.369 across classes; Cohen's *d* = 2.78 for the cross-class gap; training variance is reported as effectively zero within class. **It performs a same-scale ranking of sources (hypothesis class ≫ seed) — but the explainer is held fixed.** Caveat: single-author preprint, no venue, no peer review; low citation weight but it exists and it is on the record.

**Müller, S., Toborek, V., Beckh, K., Jakobs, M., Bauckhage, C., & Welke, P. (2023). An Empirical Evaluation of the Rashomon Effect in Explainable Machine Learning.** *ECML PKDD 2023*, LNCS, 462–478. DOI 10.1007/978-3-031-43418-1_28 — verified via Crossref; ar5iv HTML fetched. This paper formally defines **both** disagreement operators: `D(f_a, f_a, X, φ1, φ2, d)` — two attribution methods on the same model (the Disagreement Problem) — and `D(f_a, f_b, X, φ1, φ1, d)` — two models with the same attribution method (the Rashomon Effect). It computes both across model classes, hyperparameters, attribution methods, datasets and agreement metrics. **It stops short of the ordering claim**: its headline finding is about metric choice (*"In nearly all cases the human-oriented agreement metrics provide a very different picture than the Euclidean distances"*), not about which source dominates. This is the single most dangerous general-ML paper for the *framework*: the notation for both halves of the comparison is already published, and computing the ratio is a one-line extension a reviewer can point at.

**Gan, L., Zikry, T. M., & Allen, G. I. (2025). Are machine learning interpretations reliable? A stability study on global interpretations.** arXiv:2505.15728 — abstract page fetched. Studies stability of global interpretations under *"small random perturbations to the data or algorithms"*, and reports that interpretations are *"notably less stable than the predictions themselves"*. It does not separate estimator-choice from data-perturbation into a ranked comparison.

**Paillard, J., Reyero Lobo, A., Engemann, D. A., & Thirion, B. (2026). Aggregate Models, Not Explanations: Improving Feature Importance Estimation.** arXiv:2602.11760 — abstract fetched. Names *"data sampling and algorithmic stochasticity"* as the instability sources and proposes model-level ensembling as the fix. No estimator-vs-data ranking.

**The Rashomon / variable-importance-cloud line owns the model-multiplicity half only:**
- Fisher, A., Rudin, C., & Dominici, F. (2019). All Models are Wrong, but Many are Useful: Learning a Variable's Importance by Studying an Entire Class of Prediction Models Simultaneously. *JMLR* 20(177). https://jmlr.org/papers/v20/18-760.html — page fetched. Model class reliance = the *range* of importance across near-optimal models. A range, not a comparison against explainer choice.
- Dong, J., & Rudin, C. (2020). Exploring the cloud of variable importance for the set of all good models. *Nature Machine Intelligence* 2, 810–824. DOI 10.1038/s42256-020-00264-0 — Crossref verified.
- Education instance: Kuzilek, J., & Çavuş, M. (2024). Rashomon effect in Educational Research: Why More is Better Than One for Measuring the Importance of the Variables? arXiv:2412.12115, 2 Dec 2024 — abstract fetched. OULAD; demonstrates that a Rashomon set of accurate models yields inconsistent variable-importance rankings, varying across courses. **Model-selection effects only; does not vary the importance estimator.**

**Estimator-theory comparisons of exactly the pair in the claim:**
- Verdinelli, I., & Wasserman, L. (2024). Feature Importance: A Closer Look at Shapley Values and LOCO. *Statistical Science* 39(4), 623–636. DOI 10.1214/24-STS937 — Crossref verified. LOCO (leave-out-covariates) *is* drop-column. This paper establishes analytically that SHAP and LOCO are different estimands, not two noisy estimates of one thing, and that correlation between features drives them apart. **This is the theory that predicts the claim's headline number — and it means low SHAP↔drop-column agreement is an expected consequence of a known result, not a discovery.**
- Hooker, G., Mentch, L., & Zhou, S. (2021). Unrestricted permutation forces extrapolation: variable importance requires at least one more model, or there is no free variable importance. *Statistics and Computing* 31, 82. DOI 10.1007/s11222-021-10057-z — Crossref verified. Same point from the extrapolation side.

---

## 4. Feature-selection stability — does it own the framing under another name?

**Partly, and it is the strongest "you reinvented a 20-year-old subfield" attack available to a reviewer — but it does not own the ordering.**

- Kalousis, A., Prados, J., & Hilario, M. (2007). Stability of feature selection algorithms: a study on high-dimensional spaces. *Knowledge and Information Systems* 12(1), 95–116. DOI 10.1007/s10115-006-0040-8 — Crossref verified. Defines stability as *sensitivity of feature preferences (weights, ranks, or subsets) to variation in the training set*, and measures rank stability with **Spearman/Kendall-family rank correlation on importance rankings**. The claim's *right-hand quantity* (0.210) is a stability coefficient in exactly this sense.
- Nogueira, S., Sechidis, K., & Brown, G. (2018). On the Stability of Feature Selection Algorithms. *JMLR* 18(174), 1–54. https://jmlr.org/papers/v18/17-514.html — page verified. The definitive statistical treatment: stability estimator, its variance, confidence intervals, and **hypothesis tests for comparing feature-selection procedures**. If the paper wants to claim 0.123 < 0.210 is significant, this is the machinery a reviewer will demand it use.
- Haury, A.-C., Gestraud, P., & Vert, J.-P. (2011). The Influence of Feature Selection Methods on Accuracy, Stability and Interpretability of Molecular Signatures. *PLoS ONE* 6(12), e28210. DOI 10.1371/journal.pone.0028210 — Crossref verified; PMC full text fetched. 32 feature-selection methods, 4 breast-cancer expression datasets. They measure per-method stability under soft-perturbation (80% overlap), hard-perturbation (0% overlap) and between-dataset resampling. **They do not measure the overlap between signatures from different methods on the same data, and therefore do not place the two on one scale.** Verified by reading the full text. This is a useful *negative* for the claim's defence.

**Net:** the stability field owns the data-perturbation half and the measurement machinery. It compares *algorithms by their stability*, not *between-algorithm disagreement against within-algorithm data-induced disagreement*. The ordering framing survives contact with this literature.

---

## 5. Closest prior work, ranked by threat level

### Tier 1 — states the claim's conclusion, in the same application domain, four years earlier

**Swamy, V., Radmehr, B., Krco, N., Marras, M., & Käser, T. (2022). Evaluating the Explainers: Black-Box Explainable Machine Learning for Student Success Prediction in MOOCs.** *Proceedings of the 15th International Conference on Educational Data Mining (EDM 2022)*. DOI 10.5281/zenodo.6852964 (proceedings page fetched); arXiv:2207.00551. **PDF downloaded and text extracted locally.**

Design: five explainers (LIME, PermutationSHAP, KernelSHAP, DiCE, CEM) on BiLSTM student-success models across five MOOCs; comparison via PCA, Jensen–Shannon distance and **Spearman's rank-order correlation** on feature-importance vectors.

Verbatim from the abstract:

> "Our results come to the concerning conclusion that the choice of explainer is an important decision and is in fact paramount to the interpretation of the predictive results, **even more so than the course the model is trained on**."

Verbatim from §3.4 (RQ2), closing paragraph:

> "all our analyses (PCA, Spearman's Rank-Order Correlation, Jensen Shannon Distance) demonstrate that **the choice of explainability method has a much larger influence on the obtained feature importance score than the underlying model and data**."

Verbatim from the PCA paragraph:

> "The most notable takeaway from Figure 3 is that there are clearly identifiable clusters based on explainability method and not on course. It therefore seems that the resulting feature importance scores are mainly influenced by the explainability rather than by the model or data (i.e. the characteristics of the course and students' data)."

And from §4:

> "Using PCA, we identified clear clusters of explanations by explainability method and not by the course the model was trained upon, suggesting that an explainability method might be prone to mark specific features as important regardless of the model (and the course)."

**Assessment.** This is the claim's sentence, published at EDM 2022, in learning analytics, on student-success models, with teacher-facing framing (the discussion even reasons about *"the mean feature importance vector over all students"* for global interventions and about *"teachers' and students' misplaced confidence"*). Any SIDe reviewer with an EDM background will surface it in one search.

**The one crack, and it is narrow.** Swamy et al. establish the ordering **structurally, not on a common scalar scale**. Their evidence is (i) a PCA scatter in which markers cluster by explainer colour rather than by course marker, and (ii) per-course heatmaps of *pairwise-between-explainer* Spearman ρ. They never compute a between-course agreement number for a fixed explainer. They cannot: their importance vectors have length `w_c × h` with course-specific `w_c` (different numbers of weeks), so a cross-course rank correlation is not even defined in their setup — which is presumably why they reached for PCA. So the *comparison of two commensurable scalars* is not in Swamy et al.; only the qualitative ordering is.

Second crack: their five explainers are all local, perturbation- or counterfactual-based attributions on one BiLSTM. Neither SHAP-vs-drop-column nor any refit-based estimator appears. And "course" confounds data, feature space, and model, whereas the claim's data axis is *same institution, same feature space, different cohort year* — a cleaner and strictly harder-to-beat contrast.

**Related follow-up, verified:** Swamy, V., Du, S., Marras, M., & Käser, T. (2023). Trusting the Explainers: Teacher Validation of Explainable Artificial Intelligence for Course Design. *LAK23*, 345–356. DOI 10.1145/3576050.3576147 — Crossref verified. Extends to teacher validation, not to a scalar ordering. Swamy, V. (2025). *A Human-Centric Approach to Explainable AI for Personalized Education* (PhD thesis, EPFL), arXiv:2505.22541 — abstract fetched; reports *"systematic disagreements between post-hoc explainers"*; no scalar ordering in the abstract.

### Tier 2 — owns the framework or one arm of the comparison

| # | Work | Threat |
|---|---|---|
| 2 | Müller et al. (2023), ECML PKDD, DOI 10.1007/978-3-031-43418-1_28 | Defines both disagreement operators (method-pair and model-pair) in one formal framework and computes both. Does not rank them. A reviewer can say the ratio is a corollary. |
| 3 | Thackshanaramana (2026), arXiv:2603.15821 | Same-scale ranking of sources with a fixed explainer (model class ≫ seed); explicitly frames itself as the complement of "fix the model, vary the explainer". Unrefereed preprint. |
| 4 | Verdinelli & Wasserman (2024), *Statistical Science* 39(4), 623–636, DOI 10.1214/24-STS937 | Establishes SHAP and LOCO/drop-column as **different estimands**. Makes τ = 0.123 theoretically unsurprising and reframes it as measurement of a known non-identity. |
| 5 | Krishna et al. (2022/2024), arXiv:2202.01602 / TMLR | Owns explainer disagreement measurement, including rank correlation, with numbers of the same magnitude (0.113, 0.273, negative correlations). No baseline — this is the gap, but §5 Tier 1 fills it. |
| 6 | Nogueira, Sechidis & Brown (2018), *JMLR* 18(174) | Owns the statistical machinery for stability comparison; will be demanded for the significance of 0.123 vs 0.210. |
| 7 | Kalousis, Prados & Hilario (2007), *KAIS* 12(1), 95–116, DOI 10.1007/s10115-006-0040-8 | Owns "data-induced rank instability of importance rankings" as a named research object, since 2007. |

### Tier 3 — domain-adjacent, non-fatal

| # | Work | Note |
|---|---|---|
| 8 | Tiukhova, E., Vemuri, P., López Flores, N., Islind, A. S., Óskarsdóttir, M., Poelmans, S., Baesens, B., & Snoeck, M. (2024). Explainable Learning Analytics: Assessing the stability of student success prediction models by means of explainable AI. *Decision Support Systems* 182, 114229. DOI 10.1016/j.dss.2024.114229 — Crossref verified | Owns the cohort-stability arm in education with SHAP fixed. Second estimator absent. |
| 9 | Kuzilek & Çavuş (2024), arXiv:2412.12115 | Rashomon variable importance on OULAD; model multiplicity, not estimator choice. |
| 10 | Hooker, Mentch & Zhou (2021), *Stat. Comput.* 31, 82, DOI 10.1007/s11222-021-10057-z | Permutation importance off-manifold; explains *why* the estimators diverge. |
| 11 | Saarela, M., & Jauhiainen, S. (2021). Comparison of feature importance measures as explanations for classification models. *SN Applied Sciences* 3, DOI 10.1007/s42452-021-04148-9 — Crossref verified, abstract read | *"the most important features differ depending on the technique."* Medical data (UCI breast cancer, running-injury). Estimator comparison only, no data axis. |
| 12 | Zhao, Z., Chrysostomou, G., Bontcheva, K., & Aletras, N. (2022). On the Impact of Temporal Concept Drift on Model Explanations. *Findings of EMNLP 2022*, 4039–4054. DOI 10.18653/v1/2022.findings-emnlp.298 — Crossref verified | Temporal drift × eight attribution methods; measures explanation *faithfulness* under drift, not rank agreement between arms. Closest thing to "temporal axis meets explainer axis". |
| 13 | Haury, Gestraud & Vert (2011), *PLoS ONE* 6(12), e28210, DOI 10.1371/journal.pone.0028210 | Full text read: per-method stability under resampling, **no** between-method overlap. A clean negative. |
| 14 | Fisher, Rudin & Dominici (2019), *JMLR* 20(177) | Model class reliance; the range-over-models framing. |
| 15 | Dong & Rudin (2020), *Nature Mach. Intell.* 2, 810–824, DOI 10.1038/s42256-020-00264-0 | Variable importance clouds. |

---

## 6. VERDICT

### **PARTIALLY ANTICIPATED — and the headline sentence, as written, is ALREADY PUBLISHED.**

Split the claim in two.

**(a) The conclusion sentence — "the choice of explanation method destabilises a teacher-facing feature ranking more than the training data does" — is already published.** Swamy et al. (EDM 2022) state it twice, in the abstract and in the results, in the same application domain (student success prediction), from a study designed to answer that exact question (their RQ2). The wording is nearly interchangeable: *"the choice of explainability method has a much larger influence on the obtained feature importance score than the underlying model and data."* Presenting this as the paper's headline finding will be caught, and the paper will read as an uncited replication. **This is the single most important finding in this review: the paper MUST cite Swamy et al. 2022 and must not claim the ordering as novel.**

**(b) The measurement — two commensurable scalars, τ_explainer = 0.123 vs τ_data = 0.210, on a common Kendall-tau scale, over 63 cohorts and 5 institutions — is not published.** Verified negatives:
- Krishna et al. report explainer disagreement with **no** data/seed/retraining baseline (grep-verified over the full v4 text).
- Swamy et al. establish the ordering by PCA cluster structure and per-course between-explainer heatmaps; they never compute a between-course, fixed-explainer agreement number, and their variable-length feature vectors make one undefined.
- Müller et al. define both operators but rank neither.
- Thackshanaramana ranks sources with the explainer fixed and says so explicitly.
- Haury et al. measure per-method stability only.
- No work found, in any domain, that reports *estimator-induced* and *data-induced* rank agreement as two numbers on one scale for the same models with an ordering statement.

**(c) Two components make the measurement stronger than Swamy's, and are worth defending:**
1. **The estimator pair.** SHAP vs drop-column (= LOCO) crosses the additive-attribution / refit-removal boundary. Swamy's five explainers are all local perturbation or counterfactual attributions on one BiLSTM. Verdinelli & Wasserman make this crossing theoretically meaningful — and simultaneously make the low number *predictable*, which cuts both ways.
2. **The data axis.** Same institution, same feature space, different cohort year is a strictly cleaner and more adversarial data-perturbation arm than "different MOOC", which confounds data, features, model and domain. It also happens to be the arm learning analytics actually cares about (will last year's advice hold this year?).

**Residual risk that is not addressable by rewriting.** Two reviewers can kill this independently:
- An EDM/LAK reviewer citing Swamy et al. 2022 as prior art for the conclusion.
- A statistics reviewer citing Verdinelli & Wasserman 2024 to say τ = 0.123 between two *different estimands* is not a stability failure at all, and that the comparison is category-confused: SHAP and drop-column answer different questions, so their disagreement is not on the same footing as two estimates of the same quantity diverging under resampling. **The paper needs an answer to this before submission.** The honest answer is the practitioner one — a teacher receiving one ranking cannot tell which estimand produced it — and it must be stated as a *deployment* argument, not a statistical one.

---

## 7. If it survives: defensible wording and mandatory citations

### Wording that is defensible

> "That post-hoc explanation methods disagree is established in general ML (Krishna et al., 2022) and has been shown for student success prediction, where the choice of explainer was found to influence feature importance more than the course the model was trained on (Swamy et al., 2022). That finding, however, rests on cluster structure in a shared embedding rather than on a common agreement scale, and the data axis it contrasts against ('different course') confounds cohort, feature space and model. **Our contribution is to make the two sources commensurable**: across 63 cohorts at 5 institutions, we measure agreement in Kendall's τ for (i) two estimators — SHAP and drop-column — on the *same* fitted model and *same* data, and (ii) one fixed estimator across models retrained on *different cohort years* within the same institution and feature space. Estimator choice yields τ = 0.123; a full year of different students yields τ = 0.210. **The ordering reported by Swamy et al. holds on a common scale, against a stricter data-perturbation baseline, and with an estimator pair that crosses the attribution/refit boundary** (Verdinelli & Wasserman, 2024)."

Rules for this paragraph:
- Never write "we show for the first time that the explanation method matters more than the data."
- Never write "explainers disagree" as a finding.
- Do write "commensurable", "on a common scale", "against a within-institution temporal baseline".
- Frame the number as a *calibration* of a known qualitative claim, not as the claim.

### Citations that MUST appear

Mandatory — omission is a rejection risk:
1. Swamy, V., Radmehr, B., Krco, N., Marras, M., & Käser, T. (2022). Evaluating the Explainers: Black-Box Explainable Machine Learning for Student Success Prediction in MOOCs. *EDM 2022*. DOI 10.5281/zenodo.6852964.
2. Krishna, S., Han, T., Gu, A., Pombra, J., Jabbari, S., Wu, S., & Lakkaraju, H. (2024). The Disagreement Problem in Explainable Machine Learning: A Practitioner's Perspective. *TMLR*. arXiv:2202.01602.
3. Verdinelli, I., & Wasserman, L. (2024). Feature Importance: A Closer Look at Shapley Values and LOCO. *Statistical Science*, 39(4), 623–636. DOI 10.1214/24-STS937.
4. Tiukhova, E., Vemuri, P., López Flores, N., Islind, A. S., Óskarsdóttir, M., Poelmans, S., Baesens, B., & Snoeck, M. (2024). Explainable Learning Analytics: Assessing the stability of student success prediction models by means of explainable AI. *Decision Support Systems*, 182, 114229. DOI 10.1016/j.dss.2024.114229.
5. Hooker, G., Mentch, L., & Zhou, S. (2021). Unrestricted permutation forces extrapolation. *Statistics and Computing*, 31, 82. DOI 10.1007/s11222-021-10057-z.

Strongly recommended — a reviewer who knows the area will expect them:
6. Müller, S., Toborek, V., Beckh, K., Jakobs, M., Bauckhage, C., & Welke, P. (2023). An Empirical Evaluation of the Rashomon Effect in Explainable Machine Learning. *ECML PKDD 2023*, LNCS, 462–478. DOI 10.1007/978-3-031-43418-1_28. — *cite as the source of the two-operator framework the paper instantiates.*
7. Nogueira, S., Sechidis, K., & Brown, G. (2018). On the Stability of Feature Selection Algorithms. *JMLR*, 18(174), 1–54. — *use its estimator and hypothesis tests to show 0.123 < 0.210 is significant, not eyeballed.*
8. Kalousis, A., Prados, J., & Hilario, M. (2007). Stability of feature selection algorithms: a study on high-dimensional spaces. *KAIS*, 12(1), 95–116. DOI 10.1007/s10115-006-0040-8.
9. Fisher, A., Rudin, C., & Dominici, F. (2019). All Models are Wrong, but Many are Useful. *JMLR*, 20(177). — *to pre-empt "this is just the Rashomon effect".*
10. Swamy, V., Du, S., Marras, M., & Käser, T. (2023). Trusting the Explainers. *LAK23*, 345–356. DOI 10.1145/3576050.3576147. — *for the teacher-facing framing.*

Optional, for the temporal axis:
11. Zhao, Z., Chrysostomou, G., Bontcheva, K., & Aletras, N. (2022). On the Impact of Temporal Concept Drift on Model Explanations. *Findings of EMNLP 2022*, 4039–4054. DOI 10.18653/v1/2022.findings-emnlp.298.

### Contradicting evidence recorded

- Verdinelli & Wasserman (2024) argue SHAP and LOCO are different estimands. Under that reading τ = 0.123 is the expected consequence of a theorem, not an empirical instability finding. **This directly weakens the framing of the left-hand number.**
- Thackshanaramana (2026) reports the opposite emphasis for a fixed explainer: model class dominates, training variance is ~0. If both results hold, the honest ordering is `model class ≳ estimator > data year > seed`, and a paper that reports only two of the four arms is telling a partial story. A reviewer may ask for the model-class arm.
- Müller et al. (2023) show the ordering can flip with the choice of agreement metric (rank-based vs Euclidean). **A single Kendall τ comparison is fragile; the paper should report at least one second agreement metric (e.g. top-*k* feature agreement, or Nogueira stability) and confirm the ordering survives.**
