# Methodological Justification of Model and Experiment Design

## Executive summary

The current experimental design is methodologically appropriate for a dissertation-stage study of structured educational prediction, provided it is presented explicitly as a **baseline-first, leakage-aware evaluation of a Digital Twin representation under synthetic but schema-controlled conditions**. Recent reviews show that student-performance prediction in higher education is commonly framed as prediction of assessment/course outcomes or identification of at-risk/failing students using academic, behavioral, and LMS-derived variables; these problems are typically **tabular supervised-learning tasks**, not image- or language-like tasks, so conventional linear models and tree ensembles are the correct starting point rather than deep architectures. citeturn17search12turn18search1turn24search3turn6search2

Within that setting, the implemented model stack is conservative in the right way. Logistic regression provides a low-capacity, interpretable classification reference; the current regression baseline is more accurately characterized as **Ridge** rather than unpenalized OLS, which is methodologically preferable when engineered features are correlated, because scikit-learn explicitly notes that ordinary least squares becomes unstable under multicollinearity whereas Ridge improves conditioning through L2 shrinkage. Random forests and gradient boosting then supply stronger nonlinear baselines for tabular data, with the original formulations and current scikit-learn guidance both supporting their use as general-purpose regression/classification methods and, in the case of gradient-boosted trees, as especially strong methods for tabular data. citeturn8view1turn8view3turn8view4turn9view0turn7view1turn10view0turn7view8turn21view0

The remainder of the design is also well-justified. `final_grade` is the correct primary target because it preserves more information than a thresholded pass/fail label, while `risk_level` should remain excluded because a heuristic label derived from the same snapshot features would create a tautological supervision problem closely related to data leakage. Grouped-by-student and temporal-forward evaluation are likewise necessary because repeated weekly records from the same student violate the assumptions behind row-wise random splitting; both scikit-learn and the broader methodological literature warn that random CV is inappropriate when grouped or temporal dependence structures exist. Finally, experiment IDs, metadata files, result artifacts, and per-experiment Markdown summaries are not merely engineering conveniences: they align with current reproducibility norms in machine learning, which emphasize exact split descriptions, preprocessing disclosure, code/data traceability, and structured reporting of assumptions and limitations. citeturn16search3turn16search6turn7view2turn7view3turn7view4turn22view0turn22view1turn23view0turn23view1turn22view2

## Project scope and binding assumptions

All project-specific statements below should be treated as **repository-bound assumptions** when inserted into the dissertation. In the final draft, each item should be linked to an exact repository path or experiment artifact rather than left implicit. These assumptions are based on the current internal audit, baseline summary, ablation summary, EDA report, and ML service documentation supplied with the project. fileciteturn0file0 fileciteturn0file1 fileciteturn0file2 fileciteturn0file3 fileciteturn0file4

| Project element | Current assumed state | Binding note for final dissertation text |
| --- | --- | --- |
| Schema version | `v1.2` | Insert exact schema path, e.g. the active contract file under `packages/contracts/schema_versions/` |
| Snapshot grain | `1 student × 1 week` | Insert exact data-model document path describing snapshot construction |
| Dataset baseline | Current refined synthetic benchmark | Insert exact generator config and artifact root |
| Regression stack | `Ridge`, `RandomForestRegressor`, `GradientBoostingRegressor` | Clarify that the config label `linear_regression` currently resolves to **Ridge** |
| Classification stack | `LogisticRegression`, `RandomForestClassifier`, `GradientBoostingClassifier` | Insert exact model-factory path |
| Feature hierarchy | `A_simple`, `B_lms`, `C_twin`, plus targeted ablation sets | Insert exact feature-set registry path |
| Experiment inventory | `exp_001_baseline`, `exp_002_twin_ablation` | Insert exact docs/registry paths |
| Artifact policy | CSV/JSON/Markdown outputs plus experiment metadata | Insert exact artifact root and registry path |

A short repository note should also be added to the final thesis version at the first mention of the model stack, stating that the **implemented regression baseline is Ridge**, even if the legacy config name still says `linear_regression`. This matters because the methodological argument is stronger when the estimator description matches the actual code path.

## Justification of the model families

Student-performance prediction in LMS-like environments is a canonical **tabular prediction** problem: the inputs are scalar summaries of assessment, attendance, engagement, submission behavior, and course-time context, while the targets are academic outcomes such as grades, pass/fail status, or risk of failure. Educational reviews consistently describe this area in exactly those terms, and broader benchmark work on tabular learning continues to show that strong tree ensembles are difficult to beat on medium-sized structured datasets. That makes a baseline family consisting of linear/logistic models plus tree ensembles both conventional and defensible. citeturn17search12turn18search1turn17search7turn6search2

The role of the **linear/logistic family** is not to maximize accuracy at all costs; it is to establish an interpretable reference. Scikit-learn’s linear-model documentation formalizes linear regression as a model in which the target is expressed as a linear combination of the predictors, while logistic regression is the corresponding regularized logit classifier for classification. Because these models expose learned coefficients directly, they enable inspection of sign, relative magnitude, and stability of effects, even though such interpretation must be handled carefully when features are correlated or when the linear form is misspecified. In dissertation terms, they answer the essential question: *how much predictive signal is available before nonlinear interactions or ensemble effects are introduced?* citeturn7view0turn9view0turn26search0

For the current project, **Ridge** is methodologically preferable to unpenalized OLS as the realized regression baseline. Scikit-learn explicitly notes that ordinary least squares becomes highly sensitive when features are correlated and the design matrix is close to singular, whereas Ridge addresses this by penalizing coefficient magnitude and thereby improving robustness to collinearity. This is especially relevant in a Digital Twin feature space, where cumulative averages, mastery proxies, trends, and composite indices are structurally likely to correlate. Thus, even if “linear regression” remains useful as a conceptual family label in the dissertation narrative, the code-level choice of Ridge is the more statistically defensible implementation for the current feature space. citeturn8view1turn8view3turn8view4

The **tree-ensemble family** provides the necessary nonlinear counterpoint. Random forests average many randomized trees and are designed to improve predictive accuracy while controlling overfitting through aggregation and decorrelation across trees. Gradient boosting builds an additive model stage by stage, fitting weak learners to the negative gradient of a chosen loss function; both the original Friedman paper and current scikit-learn documentation describe it as a strong general-purpose method for both regression and classification, with particular strength on tabular data. Moreover, scikit-learn notes that the classic `GradientBoosting*` estimators can remain preferable at small sample sizes, whereas histogram-based variants mainly offer advantages once the sample size becomes much larger. That detail is important here because the current experiment setting is medium-sized rather than large-scale. citeturn0search9turn7view1turn7view8turn10view0turn10view3turn21view0

This four-part family therefore creates a deliberate **interpretability–prediction spectrum**:

| Model family | Main methodological function | Why it belongs in this study |
| --- | --- | --- |
| Linear regression / Ridge | Transparent regression baseline; coefficient-level diagnosis | Tests whether Twin features add value beyond a simple additive signal; Ridge stabilizes inference under collinearity |
| Logistic regression | Transparent binary-classification baseline | Establishes whether the classification task is intrinsically easy before nonlinear models are invoked |
| Random forest | Nonlinear, interaction-capable, bagged tree ensemble | Strong tabular baseline with limited preprocessing burden |
| Gradient boosting | High-performing stage-wise tree ensemble | Often the strongest classical baseline for medium-sized tabular prediction |

Taken together, this is exactly the kind of baseline selection that should precede any XAI layer: simple models first, stronger tabular baselines second, and only then explanation of the best-performing lean representation. citeturn6search2turn10view0turn22view2

## Justification of targets and feature sets

The choice of `final_grade` as the **primary target** is methodologically stronger than using `passed` as the central objective. Reviews of student-success prediction repeatedly show that the field commonly predicts course outcomes, assessment performance, or at-risk status; in such settings, a continuous grade target preserves more information than a binary threshold because it retains both rank order and distance between students. Put differently, `final_grade` allows the model to learn *how far* a learner is from excellence, adequacy, or failure, whereas `passed` collapses those distinctions into a single boundary decision. The binary label remains useful for operational reporting and early-warning framing, but it is a coarser endpoint. citeturn17search12turn18search1turn17search1

The secondary role of `passed` is even easier to defend under the current internal results, because the project’s current experiment reports indicate that pass/fail prediction is essentially saturated. Once a binary target approaches ceiling performance across multiple feature sets and models, it ceases to be the right benchmark for testing whether a richer representation is justified. In that situation, the more discriminating regression target is the correct place for the Twin representation to prove its value. *Repository note: insert the exact relative path to the baseline and ablation reports here.* fileciteturn0file1 fileciteturn0file3

The exclusion of `risk_level` as a supervised target is not merely a preference; it is a methodological necessity. If `risk_level` is a teacher-facing heuristic derived from the same weekly snapshot features that serve as model inputs, then training against it would amount to teaching the model to reconstruct a hand-designed rule system rather than predict an independent empirical outcome. That is closely aligned with what the leakage literature defines as the introduction of information about the target that would not legitimately be available as new information at prediction time. In dissertation terms, `risk_level` belongs in the **monitoring and intervention interface**, not in the ground-truth layer. citeturn16search3turn16search6turn7view2

The feature hierarchy is also well designed because it is **nested and hypothesis-driven** rather than ad hoc. Educational reviews consistently describe the predictive feature space in terms of academic performance variables, prior/current assessment results, and behavior or activity measures derived from online systems. The progression from `A_simple` to `B_lms` to `C_twin` mirrors that literature: first a minimal academic baseline, then a stronger LMS behavior baseline, and finally a Digital Twin state representation that introduces trends, mastery, composite indices, and temporal context. That structure makes the central research question precise: *does the Twin representation add value beyond what a competent LMS analytics baseline already captures?* citeturn24search3turn24search10turn17search12

| Feature set | Methodological role | Rationale |
| --- | --- | --- |
| `A_simple` | Minimal academic baseline | Tests how much can be predicted from the most basic teacher-visible signals alone |
| `B_lms` | Stronger non-Twin baseline | Approximates a realistic LMS analytics layer with activity, timing, and submission behavior |
| `C_twin` | Full Twin hypothesis | Tests whether engineered state variables add value beyond LMS-visible behavior |
| Targeted ablation | Component-level follow-up | Tests which Twin subgroups add marginal value and which simply restate baseline information |

The **targeted ablation** stage is especially important. Once the full Twin block underperforms or appears redundant, the scientifically correct next step is not to discard the representation wholesale, but to test semantically coherent subgroups—such as trends, mastery, composite indices, and temporal context—against the same strong baseline. Ablation is a standard way to estimate the contribution of individual components inside a larger system, and in this project it is additionally justified by the internal redundancy diagnostics already observed in the evolving Twin space. citeturn20search1turn16search6

For the final dissertation text, this point should be stated explicitly: the ablation phase is not exploratory “feature tinkering,” but a **structured decomposition of a failed or over-redundant representation hypothesis**. *Repository note: bind this paragraph to the current EDA report, `exp_001_baseline`, and `exp_002_twin_ablation` documentation.*

## Justification of splitting and preprocessing

The case against a row-wise random split is straightforward. The project’s unit of analysis is a repeated weekly snapshot per learner; therefore, multiple rows belong to the same student, and later rows are temporally downstream of earlier ones. Under such dependence, random splitting can leak subject-specific and temporal structure across train and test, producing over-optimistic performance estimates. The methodological literature on structured data is unequivocal on this point: when observations are grouped, temporally ordered, spatially structured, or otherwise dependent, random cross-validation underestimates error and blocked/grouped approaches are more appropriate. Scikit-learn’s own splitters make the same distinction by providing group-based and time-ordered strategies specifically for settings where independence assumptions do not hold. citeturn22view0turn7view3turn7view4

The primary split, **grouped-by-student**, is therefore the right default. `GroupShuffleSplit` is designed to split according to unique groups rather than individual samples; this directly maps to students as the grouping variable and prevents the same learner from appearing in both train and test partitions. That is the minimum requirement for any fair estimate of generalization to new students when repeated weekly rows exist. citeturn7view3

The secondary split, **temporal-forward with held-out students**, is even stronger. Scikit-learn’s `TimeSeriesSplit` documents the core principle that time-ordered data must not be evaluated by training on future observations and testing on past ones. The current project appropriately strengthens that logic by also holding out students, which avoids both **future leakage** and **identity leakage**. This split addresses a distinct question from the grouped split: not merely “can the model generalize to unseen students?” but “can it generalize from earlier-course evidence to later-course outcomes for unseen students?” For an early-warning or intervention-oriented dissertation, that is a highly defensible secondary evaluation regime. citeturn7view4turn22view0

The preprocessing choices are likewise sound because they follow scikit-learn’s explicit leakage-avoidance guidance. The library states that data must be split into train and test **before preprocessing**, that `fit`/`fit_transform` must be performed on training data only, and that `transform` should then be applied consistently to held-out data. It also explicitly identifies `StandardScaler` and `SimpleImputer` as transformations that can cause leakage if fit on all data. Train-only imputation is therefore not optional; it is required. citeturn7view2turn7view5turn11view1turn11view2

Median imputation is reasonable here because the feature space is dominated by bounded educational aggregates and counts rather than uninterrupted Gaussian measurements, while missingness indicators are justified because missingness itself may carry signal in educational records. Scikit-learn’s imputation tools explicitly support both simple univariate imputation strategies and binary missingness indicators, and the current design—explicit indicator columns where the schema already models missingness, plus train-derived median fills for the remaining numeric gaps—is a defensible compromise between simplicity and information retention. citeturn1search1turn1search5turn7view5

Feature scaling for the **linear models only** is also appropriate. Scikit-learn documents that standardization is a common requirement for many estimators because regularization terms and optimization routines can behave poorly when features are on very different scales; the scaler stores means and variances computed on the training set and reapplies them to later data. This is particularly important for regularized linear models and for any coefficient interpretation after fitting. By contrast, the project imposes no equivalent scaling requirement on the tree ensembles, which is consistent with using scaling only where it directly serves optimization and coefficient comparability. citeturn11view1turn11view2turn26search0

Finally, the use of **forbidden columns** is methodologically exactly right. Excluding identifiers, end-of-course outcomes, heuristic risk fields, snapshot-level predicted outcomes, and generation-only latent variables operationalizes the learn–predict separation emphasized in the leakage literature. Put simply, if a field would not be legitimately available at the intended prediction time—or if it encodes a hidden synthetic cause rather than an observable educational signal—it should not enter the model matrix. citeturn16search3turn16search6turn7view2

## Evaluation, reproducibility, and experiment governance

The evaluation protocol should be framed as **task-aligned and multi-metric** rather than single-score optimization. Scikit-learn’s model-evaluation guidance explicitly recommends choosing metrics in light of the ultimate prediction goal. For regression, the combination of **MAE**, **RMSE**, and **R²** is methodologically strong because each answers a different question: MAE summarizes average absolute deviation, RMSE penalizes larger misses more heavily while keeping the error in the same units as the target, and R² reports the proportion of variance explained by the model. In a course-grade setting, that trio balances interpretability and sensitivity to large errors. citeturn7view6turn12view0turn13view2turn14view2

For classification, **precision**, **recall**, and **F1** should be treated as the core threshold-dependent metrics, while **ROC-AUC** should be retained as a threshold-independent ranking measure whenever probability or score outputs are available. This is standard scikit-learn practice, and the broader evaluation literature also supports emphasizing precision–recall-aware reporting when class imbalance or asymmetric costs matter, because ROC views alone can be overly forgiving in imbalanced settings. Accuracy can still be reported descriptively, but it should not be the sole decision metric. citeturn12view3turn12view4turn12view5turn15view0turn15view2turn25search0turn25search3

| Task | Metrics to report | Why the combination is justified |
| --- | --- | --- |
| Regression | MAE, RMSE, R² | MAE gives absolute average error; RMSE emphasizes large misses and stays in target units; R² quantifies explained variance |
| Classification | Precision, Recall, F1, ROC-AUC | Precision/recall/F1 capture thresholded operational behavior; ROC-AUC adds threshold-independent ranking quality |

Cross-split comparison is essential because the two main splits answer different generalization questions. A model that performs well under grouped-by-student splitting but deteriorates under temporal-forward evaluation is not necessarily “bad”; rather, it may be exploiting information that is stable across a student’s snapshots but less transferable to a forward-looking early-warning scenario. The dissertation should therefore report results **per feature set, per model, per split**, not just global winners. This is also aligned with reproducibility guidance that asks authors to disclose exact split definitions, preprocessing steps, dataset statistics, and the code/instructions needed to reproduce the reported tables. citeturn22view0turn23view0turn23view1

This is where **experiment versioning and artifact logging** become methodologically important rather than purely operational. Pineau et al. emphasize that reproducibility in machine learning depends on better practices for conducting, communicating, and evaluating experiments; the NeurIPS checklist requires precise information about datasets, splits, preprocessing, code, commands, and the exact conditions under which results were generated. Model-card style reporting further reinforces the broader principle that machine-learning artifacts should be accompanied by concise but structured documentation of intended use, evaluation setup, and observed behavior. Repository-level experiment IDs, metadata JSON files, CSV/JSON result dumps, per-experiment Markdown summaries, and a registry page are all lightweight, defensible ways to embody those norms in a dissertation codebase. citeturn22view1turn23view0turn23view1turn22view2

| Governance artifact | Methodological function |
| --- | --- |
| Versioned experiment ID | Prevents silent overwriting and makes claims citable |
| Frozen YAML config | Records model families, feature sets, split settings, and output locations |
| Metadata file | Captures dataset version, seed, schema assumptions, and runtime context |
| CSV/JSON result artifacts | Preserve machine-readable evidence for later re-analysis |
| Markdown summary | Produces human-readable, dissertation-friendly narrative output |
| Experiment registry | Creates a cumulative, auditable research logbook |

A concise sentence should be added in the final dissertation methods chapter stating that **every experiment claim is bound to an experiment ID, exact config, split definition, artifact folder, and narrative summary**. *Repository note: insert the exact relative path to the experiment registry and artifact root here.*

## Limitations and next steps

The main limitations are not failures of the methodology, but boundaries of the current research setting. The dataset is synthetic; therefore, the conclusions are about the **internal validity of the Twin representation under a controlled prototype environment**, not yet about external validity in an institutional deployment. In addition, the current internal reports indicate two specific constraints: first, `passed` is too easy to serve as the main comparative benchmark; second, the full Twin block is not yet consistently justified relative to the stronger LMS baseline, which raises a serious but scientifically useful question about redundancy and construct validity inside the Twin layer. fileciteturn0file1 fileciteturn0file2 fileciteturn0file3

That leads naturally to the next methodological phase. Before any schema redesign, the correct move is to preserve the existing experiments as immutable references and continue with **representation-level refinement**. In practical terms, that means: preserving `exp_001_baseline` and `exp_002_twin_ablation` unchanged; auditing whether mastery and composite indices are too directly aligned with `final_grade`; recalibrating the generator only through a new versioned dataset/config if necessary; and moving to SHAP/XAI first on the **lean Twin candidate** rather than on the full Twin block. This progression keeps the scientific story clean: baseline comparison, targeted ablation, generator review if warranted, and only then explanation of the selected lean representation. That ordering is also the one most compatible with reproducibility and transparent reporting norms. citeturn22view1turn23view0turn22view2

In final thesis form, the limitations section should explicitly name the following project-bound assumptions: synthetic-data setting, schema `v1.2`, snapshot grain `1 student × 1 week`, current refined dataset baseline, current grouped and temporal-forward split logic, and the still-pending XAI stage. *Repository note: insert exact config names and artifact paths for the EDA report, baseline report, ablation report, and future explainability module here.*

## References

Alyahyan, E., & Düştegör, D. (2020). *Predicting academic success in higher education: Literature review and best practices*. International Journal of Educational Technology in Higher Education. citeturn18search1

Alalawi, K., Athauda, R., & Chiong, R. (2023). *Contextualizing the current state of research on the use of machine learning for student performance prediction: A systematic literature review*. Engineering Reports. citeturn17search0turn17search6

Breiman, L. (2001). *Random forests*. Machine Learning, 45(1), 5–32. citeturn7view8turn2search3

Friedman, J. H. (2001). *Greedy function approximation: A gradient boosting machine*. The Annals of Statistics, 29(5), 1189–1232. citeturn21view0

Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022). *Why do tree-based models still outperform deep learning on tabular data?* NeurIPS Datasets and Benchmarks. citeturn7view7

Kaufman, S., Rosset, S., Perlich, C., & Stitelman, O. (2012). *Leakage in data mining: Formulation, detection, and avoidance*. ACM Transactions on Knowledge Discovery from Data. citeturn16search3turn16search6

Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., & Gebru, T. (2019). *Model cards for model reporting*. FAT* 2019. citeturn22view2

NeurIPS. (2026). *Paper checklist guidelines*. Proceedings of the Neural Information Processing Systems Conference guidance pages. citeturn23view0

Pineau, J., Vincent-Lamarre, P., Sinha, K., Larivière, V., Beygelzimer, A., d’Alché-Buc, F., Fox, E., & Larochelle, H. (2021). *Improving reproducibility in machine learning research*. Journal of Machine Learning Research, 22, 1–20. citeturn22view1turn19search17

Roberts, D. R., Bahn, V., Ciuti, S., Boyce, M. S., Elith, J., Guillera-Arroita, G., Hauenstein, S., Lahoz-Monfort, J. J., Schröder, B., Thuiller, W., Warton, D. I., Wintle, B. A., Hartig, F., & Dormann, C. F. (2017). *Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure*. Ecography, 40(8), 913–929. citeturn22view0turn3search3

Saito, T., & Rehmsmeier, M. (2015). *The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets*. PLOS ONE, 10(3), e0118432. citeturn25search0turn25search3

scikit-learn developers. (2026). *Common pitfalls and recommended practices*. In *scikit-learn User Guide*. citeturn7view2

scikit-learn developers. (2026). *Cross-validation: evaluating estimator performance*; *GroupShuffleSplit*; *TimeSeriesSplit*. In *scikit-learn User Guide* and API reference. citeturn7view3turn7view4turn1search15

scikit-learn developers. (2026). *Ensemble methods: Gradient boosting, random forests, bagging, voting, stacking*. In *scikit-learn User Guide*. citeturn7view1turn10view0

scikit-learn developers. (2026). *Imputation of missing values*; *SimpleImputer*; *MissingIndicator*. In *scikit-learn User Guide* and API reference. citeturn7view5turn1search1turn1search5

scikit-learn developers. (2026). *Linear models*; *LogisticRegression*; *Ridge*; *StandardScaler*; *Metrics and scoring*. In *scikit-learn User Guide* and API reference. citeturn7view0turn9view0turn8view4turn11view1turn7view6

Project documentation. (n.d.). *Internal repository documentation for schema v1.2, feature-set registry, current ML/experiment audit, baseline summary, ablation summary, EDA report, and ML service README*. [Insert exact relative paths when integrating into the dissertation.] fileciteturn0file0 fileciteturn0file1 fileciteturn0file2 fileciteturn0file3 fileciteturn0file4