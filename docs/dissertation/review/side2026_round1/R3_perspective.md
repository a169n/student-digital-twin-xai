# Reviewer 3 — Perspective (cross-disciplinary, practical and ethical impact)

**Manuscript:** *What Transfers and What Does Not: Predictions, Thresholds and Explanations of Early-Warning Models Across Five Institutions*
**Venue:** SIDe 2026, Track 1 (Computational Intelligence — Explainable AI, fairness, bias mitigation; Trustworthy & Responsible AI)
**Seat:** R3 — the outside-the-subfield reading. I did not see the other reviewers' reports.
**Recommendation:** **Major revision.** Reasoning at the end.

---

## Summary

The paper does something the learning-analytics literature genuinely has not done: it assembles 64 public cohorts across five institutions, five LMS platforms and four countries, and asks what survives when an early-warning model is moved. Three properties are separated — ranking, threshold, explanation — and shown to degrade at three different rates. That separation is the paper's real contribution and it is a good one. The engineering is honest: the controls in Section V-F pre-empt the two objections I would otherwise have raised, the cutoff sensitivity analysis in V-H is more than most papers do, and the limitations section names the label-heterogeneity problem instead of hiding it.

My concerns are not that the experiments were done wrong. They are about what the paper thinks it has found, who it thinks the finding is for, and what vocabulary it is using to describe it.

Three things stand out from outside the subfield.

**First, the central finding already has a name in another field, with a mature methodology attached.** "Discrimination degrades moderately, calibration collapses, the model needs updating in the new setting" is the standard result of clinical prediction-model external validation. The paper rediscovers it with weaker instruments and cites none of that literature. This is not a nitpick about missing references — the clinical work would change what the paper *measures*, not just what it cites.

**Second, the deployment metric is computed on the wrong class.** I checked the code (`services/ml/src/experiments/transfer_benchmark.py:162`): `f1_score(y, (p >= 0.5).astype(int))` with scikit-learn's default `pos_label=1`, and label 1 is *pass* in every adapter ("Pass/Distinction = 1", "PASSED", "≥ 50"). Every F1 in the abstract, Table III, Section V-C, V-H and the Conclusion is the F1 of the students the early-warning system does **not** alert on. The paper's loudest practical claim — a fixed alerting threshold collapses — is supported by a metric that says nothing about alerts.

**Third, the fairness omission is not defensible on the grounds the paper implies.** The manuscript never disaggregates by any student attribute and never says who bears the cost of a bad transfer. The natural defence — engagement-only schema, these datasets have no demographics — is factually wrong for most of this benchmark. I checked the raw releases in the repository. OULAD ships `gender`, `region`, `highest_education`, `imd_band` (deprivation), `age_band`, `disability`. UKZN ships `GENDER`, `RACE`, `HOMELANGDESC`, `QUINTILE` (South African school quintile), `NSFASBURSARYYN` / `NSFASLOANYN` (means-tested state aid), residence and area. Zambia ships `Gender`, `Nationality`, `Sponsor`, `CampusAccommodation` and a prior-computer-access survey block. That is 37,496 of 45,236 students — **82.9 % of the benchmark** — with usable equity strata sitting in the source files. Only KU Leuven and Oviedo are genuinely bare.

The "so what" test, applied honestly: *an early-warning model moved to a new university still ranks students roughly right, but its alarm setting and its stated reasons both stop meaning anything.* That sentence survives, and a provost would care about it. This is a good paper with a mis-aimed evaluation and a missing ethics paragraph, not a paper with a wrong result.

---

## Cross-Disciplinary Connections Missed

### 1. Clinical prediction models: discrimination vs calibration (the most damaging omission)

The paper's headline structure — AUC falls a little, threshold performance falls a lot — is, in the clinical prediction literature, the textbook signature of **preserved discrimination with lost calibration**, specifically a shift in **calibration-in-the-large** (the model's average predicted risk no longer matches the event rate in the new population). This is not an analogy; it is the same quantity, and clinical methodology has a hierarchy for it, a diagnostic plot for it, and a decision procedure for what to do about it.

- **Van Calster B, McLernon DJ, van Smeden M, Wynants L, Steyerberg EW, et al. "Calibration: the Achilles heel of predictive analytics." *BMC Medicine* 17:230, 2019.** https://link.springer.com/article/10.1186/s12916-019-1466-7
  *What it would change:* supplies the four-level calibration hierarchy (mean / weak / moderate / strong) and the calibration curve. The paper should supplement Table III with **calibration-in-the-large and calibration slope at D0–D3** — two numbers per pair, computable from predictions the authors already have, measuring exactly what F1-at-0.5 is gesturing at without the class-choice confound. My prediction: calibration-in-the-large will track the prevalence-shift column of the Section V-D table almost exactly, turning a descriptive finding into a mechanism.

- **Collins GS, Reitsma JB, Altman DG, Moons KGM. "Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD): the TRIPOD Statement." *BMC Medicine* 13:1, 2015.** https://link.springer.com/article/10.1186/s12916-014-0241-z — and the ML-aware update, **Collins GS, Moons KGM, Dhiman P, Riley RD, et al. "TRIPOD+AI statement." *BMJ* 385:e078378, 2024.** https://pmc.ncbi.nlm.nih.gov/articles/PMC11019967/
  *What it would change:* TRIPOD gives the settled vocabulary for exactly this study design — *external validation* as a test of **transportability**, with temporal, geographical and domain validation as named sub-types. The D1/D2/D3 ladder is a reinvention of that taxonomy under new labels. Mapping onto the existing names costs one sentence and buys an audience outside learning analytics. TRIPOD+AI additionally mandates reporting of subgroup/fairness analyses — the external norm the paper is currently outside of.

- **Vergouwe Y, Nieboer D, Oostenbrink R, Debray TPA, et al. "A closed testing procedure to select an appropriate method for updating prediction models." *Statistics in Medicine* 36(28):4529–4539, 2017.** https://onlinelibrary.wiley.com/doi/abs/10.1002/sim.7179
  *What it would change:* this is the missing section. The clinical answer to "your model transferred badly" is a *ladder of updating methods* — recalibration-in-the-large (re-estimate the intercept only), recalibration (intercept + slope), full revision — ordered by how many target labels each costs. The paper's few-shot experiment (Table VI: k ∈ {0,25,50,100}, full refit) jumps straight to the most expensive rung and concludes few-shot calibration does not help. It does not help *because refitting on 25 students is the wrong intervention*. Re-estimating a single intercept on 25 target students is a far better use of them and is very likely to recover most of the threshold loss. A few lines of code on results the authors already hold.

- **Vickers AJ, Elkin EB. "Decision curve analysis: a novel method for evaluating prediction models." *Medical Decision Making* 26(6):565–574, 2006.** https://journals.sagepub.com/doi/10.1177/0272989X06295361
  *What it would change:* answers "which threshold, and is the model worth using at all?" — the question the institution in Section VI actually has. Net benefit across a range of thresholds is what replaces the arbitrary 0.5. An institution with capacity to contact 15 % of a cohort has an implied threshold; decision curve analysis tells it whether a transferred model beats "alert everyone" and "alert no-one" at that operating point. This is the most deployment-relevant single addition available to the paper.

### 2. Dataset-shift ML: the prevalence problem has a label-free solution the paper says does not exist

Sections V-D and VI state that prevalence shift survives the percentile transform and is the largest component at D3, then name per-cohort threshold calibration as future work. Two standard methods already do this **without target labels**:

- **Saerens M, Latinne P, Decaestecker C. "Adjusting the outputs of a classifier to new a priori probabilities: a simple procedure." *Neural Computation* 14(1):21–41, 2002.** https://direct.mit.edu/neco/article/14/1/21/6577/
- **Lipton ZC, Wang Y-X, Smola A. "Detecting and correcting for label shift with black box predictors." *ICML* 2018 (BBSE).** https://proceedings.mlr.press/v80/lipton18a.html

*What they would change:* the SLD/EM procedure estimates target prevalence from unlabelled target scores and rescales the posteriors — no target labels, exactly like the percentile transform. BBSE does the same through the source confusion matrix. Either turns the paper's open problem into a second measured result, and "feature-side fix (percentile) vs score-side fix (prior correction) vs both" is the natural table. As written the paper claims a gap that has been closed since 2002; a reviewer from the shift community will say so less gently than I am.

### 3. Explanation disagreement already has a metric suite

- **Krishna S, Han T, Gu A, Pombra J, Jabbari S, Wu S, Lakkaraju H. "The disagreement problem in explainable machine learning: a practitioner's perspective." *TMLR* 2022 / arXiv:2202.01602.** https://arxiv.org/abs/2202.01602
  *What it would change:* Krishna et al. define six agreement metrics (feature, rank, sign, signed-rank agreement, rank correlation, pairwise rank agreement) and — more usefully for this paper — interview 25 practitioners about what they actually do when explanations disagree. The paper's Kendall τ plus top-3 Jaccard is a two-element subset of that suite under private names. Adopting the standard names makes the result comparable to a body of work, and the practitioner interviews supply the empirical warrant for the "a teacher would be misled" claim that the paper currently asserts unsupported.

- **Hooker G, Mentch L, Zhou S. "Unrestricted permutation forces extrapolation: variable importance requires at least one more model, or there is no free variable importance." *Statistics and Computing* 31:82, 2021.** https://link.springer.com/article/10.1007/s11222-021-10057-z
  *What it would change:* an unacknowledged threat to validity. The seven features are heavily correlated by construction — cumulative clicks, cumulative content clicks, cumulative social clicks and active weeks are near-collinear. Permutation importance under strong feature dependence forces the model to extrapolate off-manifold and produces rankings known to be unstable *even between two models fit to the same data*. Some unknown fraction of τ = 0.03 is estimator noise, not transfer failure. The fix is cheap and mandatory: **report τ between two locally trained models on the same cohort under different seeds/folds** — the noise floor. If local-vs-local τ is 0.5 the finding stands and is stronger for having a floor; if it is 0.1 the headline claim is much weaker than stated.

### 4. Psychometrics: measurement invariance is the same question, asked properly

- **Putnick DL, Bornstein MH. "Measurement invariance conventions and reporting: the state of the art and future directions for psychological research." *Developmental Review* 41:71–90, 2016.** https://www.sciencedirect.com/science/article/abs/pii/S0273229716300351
  *What it would change:* psychometrics has spent decades on "does this instrument mean the same thing in group A and group B," with a *graded* answer — configural (same structure), metric (same loadings), scalar (same intercepts) — rather than a binary one. The percentile transform is, in that language, an attempt to buy metric invariance by rescaling. Framing it so explains *why* it repairs thresholds more than rankings (it addresses scale, not intercept) and predicts that the residual is an intercept problem — which is exactly what the prevalence-shift result shows. One paragraph would sharpen Section V-D's mechanism argument and connect the paper to an education-adjacent audience that already thinks this way.

### 5. Educational fairness literature the paper cannot skip at this venue

- **Baker RS, Hawn A. "Algorithmic bias in education." *International Journal of Artificial Intelligence in Education* 32:1052–1092, 2022.** https://link.springer.com/article/10.1007/s40593-021-00285-9
- **Gardner J, Brooks C, Baker R. "Evaluating the fairness of predictive student models through slicing analysis." *LAK* 2019 (ABROCA).** https://dl.acm.org/doi/10.1145/3303772.3303791
- **Yu R, Lee H, Kizilcec RF. "Should college dropout prediction models include protected attributes?" *L@S* 2021 / arXiv:2103.15237.** https://arxiv.org/abs/2103.15237

  *What they would change:* Baker & Hawn is the field's map of known harms and of the "unknown unknowns" problem — bias against groups whose data is never recorded — which is directly relevant to a benchmark whose smallest and worst-served institution is also its poorest. ABROCA is the field-standard disaggregated metric and is built on exactly the AUC analysis the paper already runs; adding it wherever demographics exist is close to free. Yu et al. is the paper the authors should cite when defending the demographics-free schema — it finds protected attributes add little predictive value while raising equity risk — but note carefully that it defends *excluding attributes from the features*, not *refusing to measure performance by them*. Those are different decisions, and the manuscript conflates them.

- **Chen J, Kallus N, Mao X, Svacha G, Udell M. "Fairness under unawareness: assessing disparity when protected class is unobserved." *FAT\** 2019, pp. 339–348 / arXiv:1811.11154.** https://arxiv.org/abs/1811.11154
  *What it would change:* the answer for KU Leuven and Oviedo, the two cohorts that genuinely lack attributes. It shows how to bound disparity using proxies and soft imputation, and quantifies the bias of doing so naively. With it, "we could not audit two of five institutions" becomes a stated method rather than a shrug.

### 6. Decolonial and Global-South technology critique

- **Mohamed S, Png M-T, Isaac W. "Decolonial AI: decolonial theory as sociotechnical foresight in artificial intelligence." *Philosophy & Technology* 33:659–684, 2020.** https://link.springer.com/article/10.1007/s13347-020-00405-8
- **Prinsloo P, Slade S. "An elephant in the learning analytics room: the obligation to act." *LAK* 2017.** https://dl.acm.org/doi/10.1145/3027385.3027406

  *What they would change:* Mohamed et al. name the specific pattern this benchmark instantiates — systems developed on data from wealthy contexts and exported to poorer ones, with beta-testing and extraction as recognised failure modes — and give the authors a principled way to state the Zambia result without either apologising for it or overselling it. Prinsloo & Slade supply the other half: once a model tells you a student is at risk you have incurred an obligation to act, and an institution with no advising capacity is harmed rather than helped by a better-ranked list. Both are one-sentence citations that would let Section VI say something true instead of nothing.

---

## Fairness and Ethics Assessment

**Verdict: the omission is not acceptable at this venue, and the usual excuse does not apply here.**

Track 1 explicitly lists "Explainable AI, fairness, bias mitigation" and "Trustworthy & Responsible AI." A paper submitted to that track, about deploying risk models on students across four countries, containing zero disaggregated results and zero discussion of who is harmed, is outside its own venue's stated scope. A fairness-minded reviewer will not accept it, and should not.

The practical constraint the authors would invoke is real for KU Leuven and Oviedo and **false for the rest**. Verified against the raw releases in this repository:

| Institution | Students | Equity strata in the published raw release |
|---|---|---|
| OULAD | 30,059 | gender, region, highest_education, **imd_band** (deprivation decile), age_band, **disability** |
| UKZN | 7,254 | GENDER, **RACE**, HOMELANGDESC, **QUINTILE** (school quintile), **NSFAS bursary/loan** flags, residence, area, matric points |
| Zambia | 183 | Gender, Nationality, Sponsor, CampusAccommodation, prior computer ownership/access survey |
| KU Leuven | 3,951 | none (de-identified by design) |
| Oviedo | 3,789 | none |

82.9 % of the benchmark's students carry usable attributes — including the two most consequential for a *clickstream-only* model: UKZN's school quintile and NSFAS means-tested-aid flags, and Zambia's computer-ownership items. A model that infers risk from LMS click volume is, mechanically, partly a model of **device and connectivity access**. Predicting failure from clicks where clicks depend on whether a student owns a laptop is close to a textbook proxy-discrimination case, and the data to check it is in the download.

**The minimum the authors must say and do.** In a 4–6 page paper I would accept:

1. **One disaggregated result.** ABROCA (Gardner et al. 2019) or per-subgroup AUC at D0 and D3, on OULAD by `imd_band` and `disability`, and on UKZN by `QUINTILE` or NSFAS status. Two rows, four numbers each. The question it must answer: *does transfer degrade uniformly, or does it degrade more for students who were already worse served?* That is a genuinely novel question — Gardner et al. [9] asked it across four harmonised US institutions and found transfer did not harm fairness; testing whether that survives a five-platform, four-country move is a real contribution, not a compliance exercise.
2. **One paragraph naming the harm asymmetry.** The two error types are not symmetric and the paper never says so. A false negative is a student who fails without ever being contacted. A false positive is a student who gets an unneeded email or — in a system that surfaces "risk factors" — is labelled to a teacher on the basis of reasons a local model would not have chosen. At Zambia's D3 AUC of 0.63 in a 21 %-pass year, an alerting rule's precision is near chance, and the paper should say what that means for a student.
3. **One scope sentence for the two bare cohorts**, citing Chen et al. (2019), rather than silence.
4. **An explicit "do not deploy" boundary.** The paper releases a benchmark and a fix; someone will read it as a licence to ship a transferred model with percentile preprocessing bolted on. State the conditions under which a transferred model is *not* fit for use. The paper's own numbers (D3 AUC 0.616, τ = 0.03) support drawing that line firmly.

None of this requires new experiments beyond scoring existing predictions by an attribute column.

### The North–South dimension: both comfortable and troubling, and only the comfortable half is reported

The finding is stated as: an institution with little history is better served by borrowing (0.630) than by learning from itself (0.536). Read literally that is useful and even generous — pooled public data can help an under-resourced institution that cannot build its own model. That reading deserves to stay. But three things are missing, and their absence makes the sentence read as advocacy rather than as a finding.

- **The comparison is between two failures.** 0.630 AUC is not a working model, it is a less-broken one. Section V-A already reports Zambia's within-cohort ceiling at 0.521 — clickstream engagement barely predicts outcome there at all. The honest headline is not "borrowing works for Zambia" but "**nothing in this benchmark works for Zambia, and the imported model is the least useless of the failures.**" The current phrasing is quotable by a vendor, and will be.
- **The evidence is three cohorts and 183 students**, with a pass rate swinging 0.64 → 0.21 → 0.39 across consecutive years, and Table VI shows Zambia's few-shot curve going *down* at k = 25 (0.604 → 0.543) with k = 50 and k = 100 blank for lack of students. Print the bootstrap CI on 0.630 vs 0.536 in the text. If, as I expect, the intervals overlap substantially, the claim in V-G and the Conclusion must be softened.
- **The direction is never reversed.** All 4,096 ordered pairs were computed, so Zambia→OULAD and UKZN→OULAD already exist. The paper reports the Global South only as a *target*. Does the southern data contribute anything to the pool that serves the north? Is the pooled source better or worse with the African cohorts in it? One extra row turns a one-way export story into a reciprocity result, and it is the difference between a benchmark that studies these institutions and one that uses them.

The uncomfortable framing to state plainly, once, in Section VI: this benchmark's structure — abundant northern data, a 183-student southern cohort admitted at the margin of the eligibility rule, and a recommendation that the southern institution import the northern model — reproduces a pattern Mohamed et al. (2020) describe as algorithmic coloniality. Saying so does not weaken the paper. Declining to say so, in a paper whose stated topic is trustworthy AI, is what will look bad in five years.

---

## Practical Impact Assessment

### The deployment story stops one step short, and the missing step is the cheap one

If a registrar read this paper, here is Monday's takeaway: *don't trust a vendor's AUC; don't trust its default threshold; don't show your teachers its reason panel.* That is real and worth publishing. But three negatives and one preprocessing trick is less than the data supports.

1. **The threshold fix itself is missing.** The paper diagnoses threshold collapse, attributes it to prevalence shift, shows the percentile transform does not repair prevalence shift, and names per-cohort threshold calibration as future work. The fix is label-free and one line: **alert the bottom p % of the target cohort by score**, where p is the institution's historical failure rate or its advising capacity. That is what deployed systems do, it needs no target labels, and it is computable from stored predictions in an afternoon. As it stands the practical advice is "percentile-scale your features" while the paper's own analysis says the dominant failure is on the score side.
2. **No capacity-aware metric.** No institution alerts at p = 0.5; it alerts as many students as it has advisors for. Precision@top-k% or Vickers–Elkin net benefit over a plausible threshold range is the number a dean needs. F1 at 0.5 is the number that fits in a table.
3. **No validation recipe.** The most useful artefact for a real institution is not the benchmark, it is a checklist: *before deploying a model you did not train* — (a) check calibration-in-the-large on one unlabelled cohort by comparing mean predicted risk to your known base rate; (b) set the threshold by capacity, not by 0.5; (c) recalibrate the intercept on your first ~50 labelled outcomes; (d) do not surface feature-importance panels from a foreign model. All four follow from results the paper already has. Fifteen lines, and it would be the most-read part of the paper.

### The F1 problem, in deployment terms

`transfer_benchmark.py:162` computes `f1_score(y, (p >= 0.5).astype(int))` with `pos_label` defaulting to 1, and 1 = **pass** across all five adapters. So every reported F1 measures how well the model identifies students who will pass — the class the system does not alert on.

It shows in the numbers: D0 F1 of 0.809 alongside D0 AUC of 0.746 is only reachable on the majority class in cohorts with pass rates up to 0.95. Part of the claimed 0.809 → 0.507 "collapse" is therefore not threshold failure but the pass-class F1 mechanically tracking the target's pass rate, since F1 on a class is bounded by that class's prevalence. The paper says "cohort pass rates span 0.21 to 0.95" without noticing that this makes the metric partly an arithmetic restatement of the prevalence spread rather than an independent measurement of its consequences.

The finding may well survive — I expect a real threshold problem is there — but it cannot be claimed on this evidence. **Recompute with the at-risk class as positive**, report precision and recall separately since institutions weigh them very differently, and add calibration-in-the-large, which isolates the intended construct.

### The explanation claim: the proxy is weaker than the claim it carries

The argument is: a transferred model's permutation-importance ranking disagrees with a local model's (τ = 0.03), therefore a teacher-facing panel of risk factors from a foreign model is misleading. Three problems, in increasing severity.

- **No noise floor.** Two locally trained models on the same cohort with different folds would also disagree, possibly a lot, with seven correlated features and `n_repeats = 3`. Hooker et al. (2021) show permutation importance under feature dependence is unstable in principle. Without local-vs-local τ the reader cannot separate transfer failure from estimator noise. **This control is mandatory** and is a few lines of code.
- **A global ranking is not what a teacher sees.** Teacher-facing panels in real systems (Course Signals and its descendants) show a *local, per-student* reason — "this student's activity dropped in weeks 4–6" — not a cohort-level ordering of seven features. The right operationalisation is per-student local attribution: SHAP values per student, compared between transferred and local models by per-student rank correlation, or simply by whether the top reason shown for a given student is the same one. That is a strictly stronger and more relevant test, and the authors already compute per-student predictions.
- **A teacher would not act on a ranking at all.** Teachers act on a name and a suggested contact. Whether the panel says "low forum activity" or "few active weeks" changes the intervention only marginally; what changes it is whether the *student* is the right student. This is the uncomfortable question the paper should confront: if the ranking of students is still usable at D3 and only the reasons are wrong, how much practical harm is that? The honest answer — a wrong reason misdirects the *content* of an intervention and, more importantly, invites teachers to trust a causal story the paper itself disclaims in Section VI — is defensible, and should be argued rather than assumed.

The weaker proxy does not kill the claim. It does mean the claim must be stated as "the *global feature-importance ranking* of a transferred model does not agree with a local one," with the noise floor reported, and the teacher-facing interpretation offered as a motivated hypothesis rather than a demonstrated harm. As written, V-E and the Conclusion ("costs essentially all of the agreement") overreach what a τ with no floor can support.

### The "so what" test

**Passes.** One sentence for a non-specialist: *"A dropout-warning model bought from another university will still put roughly the right students near the top of the list, but its alarm setting and its stated reasons will both be wrong, and nobody currently checks either."* A vice-chancellor, a procurement officer or a journalist would all care. That is more than most papers in this area can claim.

It passes *because of* the multi-institution benchmark, and the Section V-A table (0.845 at the OU down to 0.521 at Zambia) may be the most quotable single result in the paper — a decade of single-dataset AUC numbers have been describing contexts rather than methods. I would consider promoting it in the framing.

---

## Concerns

### [CRITICAL]

- **C1 — F1 is computed on the pass class, not the at-risk class.** `services/ml/src/experiments/transfer_benchmark.py:162`; `pos_label` defaults to 1 = pass. The paper's central deployment claim (abstract, V-C, V-H, VII) rests on a metric for the class the system does not alert on, and one whose ceiling is mechanically tied to the very prevalence spread the paper offers as its explanation. Recompute with at-risk positive, report precision and recall separately, and add calibration-in-the-large and calibration slope.
- **C2 — No fairness disaggregation, at a track that names fairness in its call.** Not defensible on data-availability grounds: OULAD, UKZN and Zambia (82.9 % of students) publish equity strata, including UKZN's school quintile and NSFAS flags and Zambia's computer-access items — the variables most likely to confound a click-volume model. Minimum: one disaggregated transfer result (ABROCA or per-subgroup AUC at D0 vs D3), one paragraph on harm asymmetry, one scope note citing Chen et al. (2019) for the two bare cohorts.
- **C3 — The explanation finding has no noise floor.** τ between two locally trained models on the same cohort is not reported, and permutation importance over seven correlated features with `n_repeats = 3` is a known-unstable estimator (Hooker et al. 2021). Without this control, "explanations do not transfer at all" is not established.

### [MAJOR]

- **M4 — The clinical prediction-model literature is absent, and its absence costs both vocabulary and instruments.** Discrimination vs calibration, calibration-in-the-large, transportability, model updating: TRIPOD / TRIPOD+AI, Van Calster et al. (2019), Vergouwe et al. (2017). The paper's finding may already have a standard name. Cite it, adopt the metrics, reposition the ladder as a transportability study.
- **M5 — Prevalence shift is presented as an open problem when label-free solutions have existed since 2002.** Saerens et al. (2002) EM prior adjustment; Lipton et al. (2018) BBSE. Either tests whether the residual is repairable, and the feature-side vs score-side comparison is a strong extra result.
- **M6 — The few-shot result is a negative finding about the wrong intervention.** Table VI refits the full model on k target students. The clinical updating ladder (intercept only → intercept + slope → full revision) uses the same k far more efficiently. "Few-shot calibration does not help" should not be claimed until intercept-only recalibration has been tried.
- **M7 — The Zambia result is over-stated relative to its evidence and under-stated relative to its ethics.** Three cohorts, 183 students, pass rate 0.64/0.21/0.39, a few-shot curve that *drops* at k = 25 and cannot reach k = 50. Print the CI on 0.630 vs 0.536; state that both sides are below usable performance; add one sentence on what it means that this benchmark is northern-data-in, southern-deployment-out (Mohamed et al. 2020; Prinsloo & Slade 2017).
- **M8 — The deployment advice stops before the fix its own analysis points at.** Prevalence-matched or capacity-based thresholding is label-free, one line, and addresses the failure mode the paper calls dominant. Add it, or at minimum state it as the concrete recommendation with the percentile transform as a complement.
- **M9 — Transfer direction is only ever reported target-side.** All 4,096 ordered pairs exist. Report whether the small and southern cohorts contribute to or degrade the pooled source, so the benchmark reads as reciprocal rather than extractive.
- **M10 — Table IV ships twelve blank cells.** Section IV-F discloses that rankings were computed for the primary model only, which is a legitimate compute decision, but an empty table invites the reader to suspect suppression. Delete the empty rows and state the restriction in the caption.

### [MINOR]

- **m11 — No "do not deploy" boundary.** The paper releases a benchmark and a fix; state where a transferred model should not be used at all. Its own numbers support the line.
- **m12 — D1/D2/D3 reinvents established validation nomenclature** (temporal / geographical / domain external validation). Keep the ladder, map it to the existing names in one sentence.
- **m13 — The percentile transform's mechanism is a measurement-invariance argument** and would be sharper stated as one (metric invariance achieved, scalar invariance not) — Putnick & Bornstein (2016). One sentence, and it *predicts* the prevalence residual rather than merely observing it.
- **m14 — Zambia's real-names column deserves more than half a sentence** (III-B). A public release carrying student names beside a hashed ID is a live privacy problem for the students in it, not just a handling note for this paper. Two sentences: what the authors did, and that redistributing the benchmark must not propagate it.
- **m15 — "the tautology accounts for part of the within-cohort signal" (V-F)** carries a lot of weight for one clause. This is the natural place to invoke the leakage framing.
- **m16 — Reference [18] (Kapoor & Narayanan) is never cited in the body.** Use it at m15 or drop it.

---

## Recommendation

**Major revision.**

Reasoning. The benchmark is a real contribution and the three-way separation of ranking, threshold and explanation is a framing the field needs. I want this paper to exist. But as submitted, two of its three headline findings rest on evidence that does not support them: the threshold claim is measured on the class the system does not alert on (C1), and the explanation claim has no noise floor for an estimator known to be noisy in exactly this regime (C3). Both are fixable from data the authors already hold, using code they have already written. Neither requires a new experiment.

The fairness gap (C2) is not a matter of taste at a track that lists fairness and bias mitigation in its call. It would be a defensible limitation if the datasets were bare; they are not — 82.9 % of these students come with equity strata in the published files, including the two variables most likely to confound a click-volume model. One disaggregated table and one honest paragraph is a small price for closing an objection that will otherwise sink the paper at this venue or the next.

The cross-disciplinary point I would press hardest: the clinical prediction-model community has been running this exact study, under the name *external validation of transportability*, for thirty years, and has settled instruments for it — the calibration hierarchy, calibration-in-the-large, the closed-testing model-updating ladder, decision curve analysis. The paper's central result may already have a standard name there. Adopting that vocabulary costs four citations and roughly a paragraph, and in exchange it replaces the paper's weakest measurement (F1 at 0.5) with the field-standard one, converts its negative few-shot result into a positive one, and gives the work an audience far beyond learning analytics. That is an unusually good trade, and it is the single change I would most like to see.

With C1, C2 and C3 addressed and M4–M8 taken seriously, this becomes a paper I would argue to accept.
