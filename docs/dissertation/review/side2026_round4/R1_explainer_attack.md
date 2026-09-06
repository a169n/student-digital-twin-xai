# R1 — Round-4 hostile review: the explainer-disagreement claim

**Manuscript:** `docs/dissertation/side2026_paper.md` (§V-C, §V-D, Abstract, Conclusion)
**Target:** the NEW central claim only. Findings of rounds 1–3 (eleven reviewers) are not repeated except where a prior finding has become load-bearing for the new claim, in which case it is credited.
**Claim under attack:**

> Applied to the same fitted model on the same students, three standard feature-importance estimators disagree: permutation vs SHAP tau 0.408, permutation vs drop-column 0.258, SHAP vs drop-column 0.123. Since 0.123 is below the 0.210 achieved by a model retrained on a different year's students, the choice of explainer destabilises the feature ranking more than the training sample does.

**Provenance of every number below.** All computations are mine, run against this repository at `f98af10`. Two independent re-implementations were built in a scratch directory, using only the project's own loaders and model factory, and they reproduce the published artifacts exactly:

- an instrumented clone of `run_explainer_agreement.py` that records the raw importance **scores** instead of only the derived ranks (63 cohorts × 3 seeds × 5 score vectors = 6,615 rows). Its between-estimator taus come back at **0.408 / 0.258 / 0.123**, matching `exp_022/f33/summary.csv` to three decimals;
- a replication of the ladder's D1 ranking comparison, which reproduces `exp_014/f33` D1-clean permutation tau at **0.210**, pair for pair, value for value.

The measurement is therefore not in doubt. What it means is.

---

## Verdict

# SURVIVES NARROWED

The three taus are real, reproducible, and correctly computed. The **ordering** built on them — the sentence the abstract, §V-D and the Conclusion all rest on — **does not survive**. It fails in four independent ways, each with a number:

1. The two figures are measured on different evaluation protocols, and the paper's own `exp_018` supplies the conversion factor. Normalised to their **matched** ceilings, explainer choice costs 0.619 of attainable agreement and next-year retraining costs 0.621. The difference is 0.002.
2. The comparison does not hold the estimator fixed. I ran the cell the paper never ran — next-year retraining measured under each estimator in turn — and got permutation 0.210, **SHAP 0.505, drop-column 0.067**. Pick drop-column for the comparator arm and retraining costs *more* than switching explainers. The ordering is a free parameter.
3. On top-3 Jaccard, the statistic that matches the paper's own "top three risk factors" framing, the ordering reverses: 0.389 (explainer) against 0.380 (next year).
4. The 0.123 and the 0.210 have overlapping, nested cluster-bootstrap intervals: [0.073, 0.171] and [0.048, 0.394]. No test is reported anywhere in the manuscript.

What survives, and is stronger than what the paper claims, is stated in **§Honest note, item 5**.

---

## Challenge-by-challenge

### C1 — The degeneracy objection [MAJOR — sustained in a sharper form, defeated in its strong form]

**The strong form fails, and I record that first.** If all seven importances were near-equal, any ranking would be arbitrary and low tau would be guaranteed. They are not near-equal. Median sorted importance profile, normalised to the top feature (63 cohorts × 3 seeds):

| rank | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| SHAP | 1.000 | 0.695 | 0.507 | 0.394 | 0.234 | 0.157 | 0.075 |
| permutation | 1.000 | 0.505 | 0.250 | 0.126 | 0.046 | −0.011 | −0.112 |
| drop-column | 1.000 | 0.553 | 0.275 | 0.100 | **−0.057** | **−0.311** | **−0.639** |

Dispersion statistics (mean over the 189 cells; Gini is 0 for a flat vector and 0.857 for a one-hot vector over 7 features; entropy is normalised so 1.0 is flat):

| estimator | Gini | entropy | top-1 share of mass | top1 − median | top-1 / median |
|---|---|---|---|---|---|
| SHAP | 0.372 | 0.859 | 0.336 | 0.766 | 2.89× |
| permutation | 0.584 | 0.616 | 0.518 | 0.104 | 6.5× |
| drop-column | 0.616 | 0.536 | 0.555 | 0.041 | 25× |

SHAP's top feature carries 33.6 % of the attributed mass against 14.3 % under flatness, and the decay from rank 1 to rank 7 is smooth and monotone with no plateau. SHAP's ranking is also reproducible: its self-agreement across three independent two-thirds resamples of the same cohort is tau **0.594**, and its top-1 feature is identical across estimators-and-splits far above chance. **The paper is not measuring noise around ties at the top of the list.** The degeneracy objection, as usually posed, is refuted.

**The sharper form is sustained, and it is where the headline lives.** Degeneracy is not in the top of the list; it is in the *tail*, and it is estimator-specific:

| estimator | mean features with importance ≤ 0 | cells with ≥ 3 such features |
|---|---|---|
| SHAP | 0.08 / 7 | 0 % |
| permutation | 2.06 / 7 | 37 % |
| drop-column | **3.23 / 7** | **63 %** |

A feature the estimator scores at or below zero has no defined position; its rank is decided by the sign of sampling noise. Kendall tau weights those positions exactly as it weights the top of the list. I simulated the ceiling this imposes on its own: hold the two rankings in *perfect* agreement on every informative feature and shuffle only the dead tails, per cell, at the observed dead-feature counts:

| pair | max attainable tau under perfect agreement on informative features |
|---|---|
| permutation vs SHAP | 0.887 |
| permutation vs drop-column | 0.725 |
| SHAP vs drop-column | 0.759 |

So dead tails alone cannot explain a 0.123. But recomputing tau over only the features that are strictly positive under **both** estimators does most of the rest of the work:

| pair | tau over all 7 | tau over informative features only | mean informative k | Spearman on the raw scores |
|---|---|---|---|---|
| permutation vs SHAP | 0.408 | **0.537** | 4.9 | +0.506 |
| permutation vs drop-column | 0.258 | **0.303** | 3.1 | +0.316 |
| SHAP vs drop-column | 0.123 | **0.324** | 3.7 | +0.157 |

The headline pair nearly **triples**, from 0.123 to 0.324, once the positions neither estimator claims are informative are dropped. And the ordering the paper's §V-C table asserts — that SHAP-vs-drop-column is the worst pair — **reverses**: on informative features SHAP-vs-drop (0.324) beats permutation-vs-drop (0.303).

*Settling statement:* importances are well separated at the top and the estimators still disagree there, which strengthens the qualitative finding. But **0.123 is not the number that describes that disagreement.** It is a number about the ordering of features the model does not use, and the pair the paper singles out as worst is the pair with the most such features. The paper must report the informative-subset figure alongside the all-features figure and must state the dead-feature counts.

### C2 — Are the three estimators even comparable? [MAJOR]

**The case that this is a category error.** Permutation importance answers "how much predictive performance does this fitted model lose when this column is made uninformative, evaluated off the data manifold". SHAP answers "how large is this feature's average marginal contribution to individual predictions, under a specific coalitional value function". Drop-column answers "how much performance does the *model class* lose when this feature is unavailable at fit time". These are three different estimands with three different populations of counterfactual. They *should* disagree, and their disagreement carries no information about explanation reliability — only about the fact that three different questions have three different answers. The evidence for this reading is in my data. The estimators do not disagree randomly; they disagree **systematically and interpretably**. Top-1 feature frequency over the 189 cells:

| estimator | weeks_since_active | cum_clicks | cum_active_days | cum_social |
|---|---|---|---|---|
| SHAP | **46** | 47 | 31 | 4 |
| permutation | **45** | 37 | 29 | 10 |
| drop-column | **18** | 38 | 28 | 22 |

Drop-column demotes `weeks_since_active` (46 → 18) and promotes `cum_social` (4 → 22). That is exactly the redundancy signature C3 predicts, not noise: a recency feature that a refit model can reconstruct from the cumulative counters loses its drop-column worth, and the one weakly-correlated feature gains. A category error that produces a legible, mechanistic pattern is a real finding about the estimands, not a measurement of instability.

**The case that they are comparable.** A practitioner building the teacher-facing panel does not choose an estimand; they choose an import statement. `shap.TreeExplainer`, `sklearn.inspection.permutation_importance` and a hand-rolled refit loop are all presented in tooling, tutorials and the learning-analytics literature as answers to "which features drove this". None of the three ships a warning that it answers a different question from the other two, and no deployed dashboard I am aware of states which one produced its list. In the only sense the paper cares about — what appears on the screen in front of a teacher — they are substitutes, and the variance across substitutes is a real property of the deployed artifact.

**Which wins.** The second, but only for a claim the paper does not currently make. The comparison is legitimate as a statement about *deployment practice*: "three tools a developer would treat as interchangeable produce different lists". It is illegitimate as a statement about *epistemics*: "the ranking is unstable", because the estimators are not three noisy measurements of one latent ranking, and the paper's framing ("the ranking is not a property of the model that transfer degrades. It is an artifact of the estimator" — `run_explainer_agreement.py` docstring) presupposes that they are. §V-C reads as the latter and the docstring says the latter outright.

*What the paper must state to survive this:* that the three estimators target different estimands, that their disagreement is therefore expected on statistical grounds and is not evidence of unreliability, and that the claim is about interchangeability in practice. §VI already contains one sentence in this direction ("Nor do we claim SHAP is wrong and drop-column right"); it is not enough, because §V-C's framing and the abstract both trade on the epistemic reading. The systematic `weeks_since_active` / `cum_social` swap above should be reported — it converts a bare disagreement number into a mechanism, and it is the strongest thing in the experiment.

### C3 — Drop-column with correlated features [CRITICAL — sustained]

The premise checks out. Mean within-cohort Spearman correlation across the 63 cohorts:

```
cum_clicks  ~ cum_content_clicks   0.912
cum_clicks  ~ cum_active_days      0.874
cum_active_days ~ active_weeks     0.865
cum_active_days ~ cum_content_clicks 0.802
cum_clicks  ~ active_weeks         0.758
cum_social  ~ everything           0.33-0.54   (the one non-redundant feature)
```

10.3 % of within-cohort feature pairs reach |rho| ≥ 0.90. And drop-column behaves exactly as predicted for that setting. Median scores: top feature **0.0276 AUC**, second 0.0101, fourth 0.0011, and ranks 5-7 are **negative** — removing the feature *improves* held-out AUC. The median gap between the top-1 and top-2 drop-column scores is **0.0117 AUC**, i.e. the entire ranking below rank 1 is decided by AUC differences in the third decimal place, measured on a held-out third that has a median of 111 students.

The decisive number is not a magnitude argument, which is contestable because paired AUC differences on a common evaluation set are correlated and their standard error is smaller than a naive 1/√n. It is drop-column's agreement **with itself**. Same estimator, same cohort, a different stratified two-thirds:

| estimator | self-agreement across the 3 resamples | agreement with the other estimators |
|---|---|---|
| SHAP | **0.594** | 0.408 (perm), 0.123 (drop) |
| permutation | **0.345** | 0.408 (SHAP), 0.258 (drop) |
| drop-column | **0.181** | 0.258 (perm), 0.123 (SHAP) |

**Drop-column agrees with permutation on identical data (0.258) better than it agrees with itself on a resample of the same cohort (0.181).** It carries almost no reproducible ranking signal at these sample sizes. Correcting each observed between-estimator tau by the geometric mean of the two estimators' self-reliabilities (Spearman disattenuation, using the across-resample reliabilities, which are the right ones for "would another sample of these students give this answer"):

| pair | observed | disattenuated |
|---|---|---|
| permutation vs SHAP | 0.408 | 0.901 |
| permutation vs drop-column | 0.258 | **1.03** |
| SHAP vs drop-column | 0.123 | 0.375 |

Permutation and drop-column agree with each other as well as either agrees with itself. There is no evidence of a systematic estimand difference between them at all; their observed 0.258 is entirely each one's own resampling noise.

*Settling statement:* the headline 0.123 is substantially an artifact of one broken arm. The honest, defensible headline is **permutation vs SHAP, 0.408** — the only pair in which both arms have non-trivial reliability (0.345 and 0.594) and the only pair for which the disagreement exceeds what either arm's own instability explains. Note this does **not** rescue the ordering, because 0.408 sits above the 0.210 comparator, not below it.

### C4 — Sample size and stability [CRITICAL — sustained]

Three seeds, a held-out third capped at 1,500 rows. The stability accounting:

| source of variation | tau |
|---|---|
| permutation, same split, only the permutation seed changed | 0.703 |
| drop-column, same split, only the model seed changed | 0.906 |
| SHAP, same split, re-run | 1.000 (deterministic given the model) |
| **permutation, across the 3 splits** | **0.345** |
| **SHAP, across the 3 splits** | **0.594** |
| **drop-column, across the 3 splits** | **0.181** |
| between: permutation vs SHAP | 0.408 |
| between: permutation vs drop-column | 0.258 |
| between: SHAP vs drop-column | 0.123 |

Two of the three headline "explainer disagreement" figures (0.258 and 0.123) are **at or below** the within-estimator variability of at least one of their own arms. Only permutation-vs-SHAP (0.408) sits clearly above both of its arms' self-agreement — and it is above them, i.e. the two estimators agree with each other better than either agrees with itself across resamples, which is again the signature of a shared systematic component rather than instability.

Variance decomposition of the per-cell taus in the released `pairs.csv`:

| pair | mean within-cohort SD across the 3 seeds | SD of the cohort means | share of variance that is seed-to-seed |
|---|---|---|---|
| drop-column vs permutation | 0.293 | 0.177 | 76.6 % |
| drop-column vs SHAP | 0.286 | 0.199 | 71.9 % |
| permutation vs SHAP | 0.204 | 0.223 | 54.9 % |

**72 % of the variance in the headline quantity is which two-thirds of the cohort was drawn, not which cohort.** In **41 of 63 cohorts the three seeds do not agree on the sign** of the SHAP-vs-drop-column tau. No per-cohort statement is supportable and the paper's "the disagreement is not one institution's quirk: the SHAP-versus-drop-column pair ranges only from 0.090 to 0.185 across the five institutions" is a statement about five means with 6 to 60 observations each, of which the Zambia entry is 6 observations from 2 cohorts.

Only the grand mean is estimable. Cluster bootstrap by cohort (63 clusters, 20,000 resamples) — the paper reports no interval at all:

```
permutation vs SHAP         0.408  95% CI [0.353, 0.462]
drop-column vs permutation  0.258  95% CI [0.213, 0.301]
drop-column vs SHAP         0.123  95% CI [0.073, 0.171]
```

Three seeds is also simply too few to estimate the seed component that dominates. With a within-cohort SD near 0.29 and n = 3, the per-cohort standard error is ≈ 0.17. Twenty seeds is not expensive here — my full instrumented replication of all 63 cohorts × 3 seeds, including a doubled drop-column arm, ran in under thirty minutes on one laptop core.

### C5 — The ordering claim [CRITICAL — fails, four independent ways]

**(a) The protocols differ, and the authors' own artifact converts between them.**

- `exp_022` (0.123): model fitted on two thirds of a cohort, both rankings computed on the **held-out third**, capped at 1,500 rows. Median evaluation set: 111 students.
- `exp_014` D1 (0.210): source model fitted on the **whole** source cohort, target model fitted on the **whole** target cohort, both ranked on the **whole target cohort** — which for the local arm is the data it was fitted on. Median evaluation set: 508 students.

`exp_018` measures *the same comparison* under both evaluation protocols and reports both:

```
ceiling, ranked on the full cohort   (ladder-matched)   0.3376
ceiling, ranked on a held-out third  (exp_022-matched)  0.1982
ratio                                                   0.5871
```

Normalise each headline figure to its **own protocol's** ceiling:

```
SHAP vs drop-column  0.1227 / 0.1982 = 0.6191
same course, next yr 0.2095 / 0.3376 = 0.6207
```

**0.6191 against 0.6207.** Equivalently, rescale the next-year figure into `exp_022`'s protocol: 0.2095 × 0.5871 = **0.1230**, against the paper's headline of 0.1227. The entire claimed difference between "switching the explainer" and "retraining on next year's students" is, to three decimal places, the difference between ranking on a third of a cohort and ranking on all of it.

§V-B says "Every ratio in this paper is computed against 0.338, which understates the instability rather than overstating it." For the explainer arm that is the wrong direction and the wrong ceiling: 0.338 is the ceiling for the ladder's protocol, and using it for a figure measured under `exp_022`'s protocol **overstates** the instability by a factor of 1/0.587 = 1.70. The generous-ceiling choice, defensible for the ladder, manufactures the ordering when applied across two protocols.

**(b) The estimator is not held fixed across the comparison the ordering is about.** The paper compares (one estimator, two training samples) against (two estimators, one training sample) and reads the difference as "explainer versus data". Estimator identity is confounded with the axis under study. I ran the missing cell — the same-course-next-year comparison under the ladder's exact protocol, changing only the estimator:

| estimator used for the next-year comparison | tau | cluster 95 % CI (6 course-pairs) | top-3 Jaccard |
|---|---|---|---|
| SHAP | **0.505** | [0.333, 0.671] | 0.47 |
| permutation (the paper's 0.210) | 0.210 | [0.040, 0.394] | 0.38 |
| drop-column | **0.067** | [−0.057, 0.171] | 0.32 |

The comparator ranges over **0.438 of tau** depending on an estimator choice the paper does not disclose it is making. Choose SHAP and next-year retraining costs almost nothing and the paper's ordering holds comfortably. Choose drop-column and **0.067 < 0.123**: retraining on another year's students destabilises the ranking *more* than switching explainers, and §V-D inverts. The paper picked the middle value, and it picked it because the ladder happened to be built on permutation for unrelated runtime reasons (`transfer_benchmark.py`, `EXPLAIN_MODEL` / `IMPORTANCE_REPEATS` comments).

**(c) The ordering reverses on the paper's own other metric.** §VI's practical claim is about "the top three risk factors for this student". On top-3 Jaccard:

| comparison | J@3 | above random (0.303), normalised | J@3 / matched ceiling |
|---|---|---|---|
| SHAP vs drop-column | 0.389 | 0.124 | 0.939 |
| same course, next year | 0.380 | 0.111 | 0.780 |

Switching explainers preserves *more* of the top-three list than a year of new students does. Both `exp_022/summary.csv` and `exp_014` report J@3; §V-C prints the column and §V-D draws its conclusion from tau only.

**(d) The comparator is 10 pairs from 6 course-pairs and its interval swallows the headline.** Round 2 (`S1_statistics.md` §9) established that the clean D1 rung is 10 directed pairs from 6 undirected course-pairs; that finding was about AUC, and it is now load-bearing for the tau. Cluster bootstrap over the 6 undirected course-pairs:

```
same course, next year   0.2095  95% CI [0.048, 0.394]   (k = 6)
SHAP vs drop-column      0.1227  95% CI [0.073, 0.171]   (k = 63)
```

The headline interval is entirely nested inside the comparator's. Per course family the comparator is: KU Globaleconom 0.405 (4 pairs), OULAD BBB 0.238 (2), Zambia 0.000 (2), UKZN 0.048 (1), OULAD FFF −0.048 (1). Remove KU Leuven and the comparator is 0.088, below the headline. The manuscript reports no interval and performs no test for the strict inequality on which §V-D, the abstract and the Conclusion all depend.

**(e) The two figures are computed on different cohort populations.** 0.123 pools all 63 cohorts; 0.210 involves 9 target cohorts. On `exp_022`'s own protocol, 20 of the 63 cohorts have an attainable ceiling of 0.052 (Oviedo, median 130 students → a 43-student evaluation set) and 2 have −0.000 (Zambia). Restricting to the 36 cohorts whose matched ceiling exceeds 0.15:

```
permutation vs SHAP         0.493  (vs 0.408 pooled)
drop-column vs permutation  0.277  (vs 0.258)
drop-column vs SHAP         0.154  (vs 0.123)
```

*The fairest matched comparison I can construct.* Restrict to the 9 cohorts that appear as D1-clean targets, and normalise each arm to its own protocol's ceiling computed on those same 9 cohorts:

```
SHAP vs drop-column   0.0829 / 0.1958 = 0.423
same course, next yr  0.2095 / 0.3545 = 0.591
```

On this matching the ordering **holds** — the explainer arm retains less. I report it because it is the one construction that favours the authors, and because it is honest to say that the direction of the effect is never actually reversed by the protocol correction; it is the *magnitude* and the *statistical distinguishability* that evaporate. But it rests on 9 cohorts and 6 course-pairs and it disagrees with the pooled matched comparison in (a), which puts the two at 0.619 and 0.621. Two defensible matchings give "equal" and "explainer worse"; a third, (b), gives "explainer better". **The ordering is not identified by this design.**

### C6 — Other things that would not survive a competent methodologist

**[CRITICAL] A measurement exceeds its own ceiling, and the paper's central framing depends on it not doing so.** §IV-B: "Agreement is Kendall tau over the seven features and the Jaccard overlap of the top three, so every comparison sits on one scale." Normalised to the ceiling that matches its protocol, permutation-vs-SHAP is **0.408 / 0.198 = 2.06**. Two different explanation methods applied to one model agree twice as well as two models fitted to disjoint halves of one cohort do. A quantity that lands at 206 % of its ceiling is not on the same scale as the quantity that defines the ceiling. Either the "one scale" sentence goes, or a separate, protocol-matched ceiling is reported for each arm.

**[MAJOR] A third of the explained models have nothing to explain.** Median held-out AUC of the models `exp_022` explains is 0.696, but **30.7 % of cells are below 0.60 and 14.8 % below 0.55**. Splitting the cells at the median AUC:

| pair | weak-model half | strong-model half |
|---|---|---|
| permutation vs SHAP | 0.267 | **0.551** |
| drop-column vs SHAP | 0.081 | 0.165 |
| drop-column vs permutation | 0.256 | 0.259 |

The permutation-vs-SHAP figure doubles on models that actually discriminate. Pooling explanations of near-chance models into a headline about explanation reliability inflates the disagreement. This compounds round 3's H-1 and H-4 (the trivial baseline, and cohorts with no local signal) but is a distinct point: those were about the *accuracy* claims; this is about which cells belong in the *explanation* average.

**[MAJOR] Undisclosed protocol details in §IV-A.** "One model, fitted once per cohort on two thirds of its students; three importance rankings computed on the held-out third" omits: the 1,500-row evaluation cap (`EVAL_CAP`), that only 3 seeds are used, that permutation uses only 3 repeats, and — critically — that this evaluation protocol differs from the one used for every figure it is compared against. §IV-A describes the training-sample arm as "Two models fitted to disjoint halves of one cohort and ranked on common data" without saying that "common data" means the full cohort in the reported 0.338 and a held-out third in the unreported 0.198, and that the choice between them moves the number by 41 %.

**[MINOR] The ladder's D1 local arm is ranked in-sample.** In `run_ladder`, `target_rankings` is built by ranking the target-local model on `t.X(rep), t.y` — the data it was just fitted on — while the source model is ranked out of sample on the same rows. `exp_018`'s own docstring identifies this asymmetry and fixes it for the ceiling; the D1 tau of 0.210 still carries it. Direction unknown, magnitude unmeasured, not disclosed in §IV.

**[MINOR] `is_clean` is `contamination < 1 %`, not zero.** Three of the ten D1-clean pairs have 0.65-0.92 % overlap. Round 2 noted the definition is unstated; it remains unstated and now qualifies the comparator in the paper's headline ordering.

---

## What the authors must change

**Mandatory before this claim can be published in its current position.**

1. **Withdraw the ordering as stated.** Delete "Since 0.123 is below the 0.210…" from the abstract, §V-C, §V-D and the Conclusion. Four independent constructions from the released artifacts put the two quantities at equal, explainer-better, and explainer-worse respectively; none of them is decisive and the paper reports the one that is not protocol-matched.
2. **Report a protocol-matched ceiling per arm.** `exp_018` already computes both (0.198 held-out-third, 0.338 full-cohort). Use 0.198 for every `exp_022` figure and 0.338 for every `exp_014` figure, and say so. Then the honest §V-D reads: *both* explainer choice and a year of retraining cost about 38 % of attainable agreement.
3. **Publish the estimator × source factorial.** The next-year comparison under all three estimators (0.505 / 0.210 / 0.067) is a two-hour run and it is a better result than the one currently in the paper. As it stands the design confounds the axis under study with the instrument measuring it.
4. **Report intervals.** Cluster-bootstrap CIs by cohort for `exp_022` and by undirected course-pair for the D1 rung. The comparator's is [0.048, 0.394] on 6 clusters; that number cannot carry a strict inequality.
5. **Report the informative-subset tau and the dead-feature counts** (drop-column 3.23/7 features at ≤ 0 importance, 63 % of cells with ≥ 3). 0.123 rises to 0.324 when the uninformative positions are dropped, and the "worst pair" designation flips.
6. **Report each estimator's self-agreement across resamples** (SHAP 0.594, permutation 0.345, drop-column 0.181) next to the between-estimator table. Without it a reader cannot tell that two of the three headline numbers are smaller than one of their own arms' noise.
7. **Demote or drop the drop-column arm as a headline.** Keep it as a documented negative result — "a refit-based estimator is not estimable on seven collinear behavioural features at these cohort sizes" is itself worth a paragraph and directly qualifies reference [8]'s recommendation in this setting. Move the headline to permutation-vs-SHAP, 0.408, and state its matched-ceiling ratio honestly (which is above 1, and therefore is *not* evidence of instability relative to the training sample).
8. **State the estimand distinction explicitly in §V-C**, not only in §VI, and report the systematic `weeks_since_active` (46 → 18) / `cum_social` (4 → 22) top-1 swap that shows the disagreement is mechanistic rather than random.

**Recommended.** Raise the seed count from 3 to ≥ 20 (72 % of the variance is seed-to-seed). Exclude, or report separately, cells whose model is below AUC 0.60. Disclose `EVAL_CAP`, the repeat count and the seed count in §IV-A.

---

## Honest note: what I tried to break and could not

1. **The degeneracy objection, in its strong form, fails.** I expected flat importances and did not find them. SHAP's profile decays smoothly from 1.000 to 0.075 with the top feature at 2.9× the median and 33.6 % of the mass; zero dead features in zero cells. The estimators disagree in a region where the scores are genuinely separated, and SHAP's own ranking is reproducible across resamples at 0.594. This is a real disagreement between well-defined rankings, not noise around ties.
2. **The measurement reproduces exactly.** Two independent re-implementations, written from the loaders up, returned 0.408 / 0.258 / 0.123 and 0.210 to three decimals, the latter pair-for-pair identical. Whatever is wrong with this claim, it is not the arithmetic or the code. This is more than most of the artifacts examined in rounds 1-3 could say.
3. **Attenuation runs against the authors' convenience, not for it.** I expected to find that the low 0.123 was permutation noise. The opposite holds: SHAP and drop-column are both deterministic given the split, so their 0.123 carries *no* estimator noise, while the two permutation-based pairs are attenuated (reliability 0.703 same-split). Disattenuating raises 0.408 → 0.487 and 0.258 → 0.323 while leaving 0.123 → 0.129. The reported spread among the three explainer pairs is, if anything, understated.
4. **The explainer effect is not zero and does not vanish under any correction I applied.** After restricting to informative features (0.324), after disattenuating by across-resample reliability (0.375), and on the 36 cohorts with a usable ceiling (0.154), SHAP and drop-column still disagree substantially. Something real is being measured.
5. **The paper's thesis is true in a stronger form than the paper states, and my own attack is what establishes it.** The estimator choice moves the *measured cost of a year of retraining* from 0.067 to 0.505 — a range of **0.438**, five times the 0.087 gap the paper claims between explainer choice and retraining. The right claim is not "explainer choice costs more than the training sample". It is: **the estimator choice determines what you will conclude about every other source of variation, including how much the training sample matters.** That is a sharper result, it is supported by a factorial the authors can run in an afternoon, it survives every correction in this review, and it makes the governance recommendation in §V-D follow much more directly than the ordering does.

---

### Reproduction notes

Scratch scripts (not committed; regenerate as needed):

- `dump_scores.py` — instrumented clone of `run_explainer_agreement.py`; identical split, cap, seeds and estimators, plus a second permutation draw at `seed+1000` and a second drop-column refit at model seed `seed+1000`. Writes 6,615 score rows. Run from `services/ml` with `PYTHONPATH=.` under `.venv`.
- `analyse.py` — dispersion (Gini, normalised entropy, top-1 mass share, gaps), dead-feature counts, top-1 agreement, within- vs between-estimator tau, disattenuation, dead-tail simulation.
- `d1_by_estimator.py` — the missing cell: the ladder's D1-clean comparison (seed 42, 1,500-row stratified ranking subsample, full-cohort fits) recomputed under permutation, SHAP and drop-column.
- `corr.py` — within-cohort Spearman correlations of the seven canonical features.

Artifacts read: `exp_022_explainer_agreement/f33/{pairs,summary,by_institution}.csv`, `exp_018_explanation_ceiling/f33/{per_cohort,summary}.csv`, `exp_014_transfer_ladder/f33/{pairs,cohorts,run_metadata}`, `exp_017_contamination/f33/pair_overlap.csv`. No project file was modified.
