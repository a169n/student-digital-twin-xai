# T2 — Contribution and Genre Audit (Round 3)

**Manuscript:** `docs/dissertation/side2026_paper.md`
**Read against:** `review/side2026_round1/` (5 seats + editorial decision), `review/side2026_round2/` (S1 statistics, S2 adversarial, S3 senior PC), and the released artifacts under `data/artifacts/experiments/`.
**Numbers below marked *(verified)* were recomputed in this audit from the released CSVs.**
**Date:** 2026-09-06. Nothing outside this file was modified.

---

## 0. Reading note before anything else

The brief I was given describes a paper in better shape than the one that exists. Three items in that brief are, on the released artifacts and on S1/S2's recomputations, not what the authors think they are:

- **"Moving a model across institutions costs ~0.09 AUC and breaks calibration."** The 0.09 discrimination cost survives institution-clustered inference (GB/raw D0−D3 = 0.0931, clustered 95 % CI [0.035, 0.155]). The calibration half does not: clustered on institution, the +0.122 calibration-in-the-large has a 95 % CI of [−0.053, +0.325], and 93 % of the effect is UKZN's base rate. "Calibration breaks" is, on this benchmark, "UKZN passes 73–95 % of its students and nobody else does."
- **"Their proposed fix loses to a one-line intercept recalibration."** True, and worse than stated: S2 ran rung 1 and got Brier 0.223 against the transform's 0.322, per-pair |CIL| exactly 0.000 against 0.249, failing-class F1 0.432 against 0.348. The transform is not a weaker version of the same thing; it is a different thing that the paper describes incorrectly.
- **"Permutation-importance rankings are unstable even within one cohort (ceiling 0.338, random 0.303)."** 0.303 is the random **top-3 Jaccard**; the random Kendall tau is 0.000. The correct comparison is ceiling 0.338 vs random 0.000, which is a much weaker version of the claim the authors want. And the 0.338 is trained on one third of each cohort while the ladder trains on whole cohorts, and it pools institutions whose ceilings run from +0.670 (KU Leuven) to **−0.095** (Zambia).

I flag this here because sections 1–6 below are calibrated against the artifacts, not against the brief, and the two disagree.

---

## 1. The contribution, in one sentence, as a hostile but fair senior researcher would concede it

> **They paid the assembly cost nobody else in learning analytics has paid — five public LMS datasets from four countries harmonised into one leakage-audited transfer benchmark of 63 cohorts and 35,529 students, with adapters released — and that benchmark yields exactly one genuinely new empirical fact (within-cohort predictability of clickstream engagement ranges from ROC-AUC 0.845 at the Open University to ~0.53–0.61 at four other institutions, so a single-dataset early-warning result is a measurement of its dataset) and one genuinely new comparison (a transferred model's permutation-importance ranking against a locally trained model's, scored against a measured within-cohort ceiling rather than against 1.0).**

Everything else the paper currently advertises is one of: a textbook clinical-prediction result confirmed in a new domain (discrimination travels, calibration does not); an arithmetic identity of the ordered-pair design masquerading as a repair (the percentile transform's calibration "restoration"); a hazard published eight years ago in the target subfield's own flagship journal (majority-class F1 — Bosch & Paquette 2018, *JLA*); a leakage principle that has been canon since Kaufman et al. 2012; or an extreme-value artifact (the fairness "worst-served group" claim).

That is a real contribution. It is a **one-and-a-half-finding resource paper**, not a four-contribution research paper, and the manuscript does not say so.

---

## 2. Who benefits, and the specific decision each audience changes

### 2.1 A university about to buy or borrow an early-warning system — **benefits most, and the paper does not currently tell them**

Three decisions change, and two of the three rest on numbers the paper deleted.

**(a) Do not wait a year to collect labels for the course you want to protect.** *(verified from `exp_014_transfer_ladder/f33/pooled.csv`)* A gradient-boosting model trained on the institution's **other** cohorts, never on the target cohort, reaches AUC 0.686 (raw) / 0.699 (percentile) / 0.701 (z-score) against 0.691 for a model cross-validated on the target cohort itself. The cost of never having seen this course is **0.005 AUC**. The standard practice of running a course for a year to build a local model buys essentially nothing. This is the single most actionable result in the whole artifact set and it appears nowhere in the manuscript.

**(b) If you must borrow from outside, pool sources and standardise within cohort — do not borrow one foreign model.** *(verified)* Single-source cross-institution transfer: 0.594 (raw). Pooled over the four other institutions: **0.602 raw, but 0.683 under the percentile representation** — a gap to local of 0.009 instead of 0.097. The paper's headline ("an ordinary model loses about 0.1 ROC-AUC when it crosses an institutional boundary") is true only of the worst available deployment architecture. The percentile transform, which the paper apologises for, is worth **+0.081 AUC** in exactly the configuration a real deployment would use — and the paper never reports it there.

**(c) When you borrow, recalibrate the intercept on the first ~100 labelled target students; expect it to fix your thresholds and nothing else.** *(from S2's rerun of Vergouwe rung 1 on the same 2,912 pairs)* Brier 0.361 → 0.223, per-pair |CIL| 0.301 → 0.000, failing-class F1 0.420 → 0.432, and AUC and recall@20 % **byte-identical** at 0.5972 and 0.2729. Separately *(verified from `fewshot.csv`)*, adding 100 labelled target students to the pooled foreign model moves AUC 0.682 → 0.712 and Brier 0.269 → 0.196. So: the advising list barely changes, the risk numbers you show a human become honest. Budget for 100 labels, not for a year of data collection.

**(d) Ignore any vendor AUC quoted from one institution.** 0.845 at the OU, 0.527–0.667 elsewhere, on identical features and identical code. Insist on a pilot scored on your own cohorts before contract. This one the paper *does* say, and it is the paper's best public-interest sentence.

**(e) Calibrate expectations on the advising budget itself.** At a 20 % flag budget the transferred model recovers 27 % of failing students — 1.36× random, and (S1's framing, which is better) **47 % of the recall an oracle ranker could achieve at that budget**, against 56 % for a locally trained model. If your intervention needs 60 % coverage, no model in this benchmark gets you there at 20 % capacity.

### 2.2 Builders of teacher-facing explanation dashboards — **benefits, and this is the dissertation-relevant audience**

Decision changed: **do not ship a per-student "why this student is at risk" panel driven by permutation importance over correlated engagement counters, and do not assume that keeping the model local makes it safe.** Two models trained on disjoint halves of the *same* cohort agree at τ = 0.338 (ladder-matched) / 0.198 (strict), against a same-model noise floor of 0.707 and a random-ranking expectation of **0.000**; the per-institution ceiling ranges +0.670 (KU Leuven) to −0.095 (Zambia), i.e. at one institution the ranking carries no information at all. Cross-institution agreement is 0.026–0.034, statistically at the edge of the random null. If the dashboard's purpose is "which behaviour should this student change", these features cannot support it at any transfer distance including zero.

Caveat this audience must be told: the ceiling is currently confounded with training-set size (corr(log n, ceiling τ) = +0.423; quartile ceilings 0.214 → 0.396), so the *magnitude* is not yet defensible. The *direction* is.

### 2.3 Learning-analytics reviewers and methodologists — **benefits modestly**

Decision changed: when refereeing a cross-course or cross-cohort transfer study, demand per-pair student-overlap figures. *(verified)* 72 of 78 same-course pairs and 324 of 916 other-course pairs share students between train and eval, up to 83 % (D1) / 94 % (D2) of the target cohort, while cross-institution pairs are genuinely clean (78 of 2,912, max 1.5 %). The *principle* is canon (Kaufman 2012; Saeb 2017; Kapoor & Narayanan 2023) and the *quantity* is new: nobody has published the overlap gradient along a transfer ladder. That is a one-paragraph methods note, not a contribution bullet.

The majority-class F1 hazard gives this audience nothing. It is Bosch & Paquette (2018) in the *Journal of Learning Analytics*, almost verbatim, plus Flach & Kull (2015) for the always-positive baseline. Presenting it as a discovery invites a one-line desk rejection.

### 2.4 The ML transfer / distribution-shift community — **gains nothing**

Everything methodological here is downstream of results they already own: prevalence shift and label-free prior correction (Saerens 2002), unrestricted-permutation importance being unidentified (Hooker, Mentch & Zhou 2021 — cited by the authors for exactly this), discrimination-vs-calibration under transport (Steyerberg 2009; Van Calster 2016/2019). The benchmark itself may interest them as a dataset; the findings will not.

### 2.5 Fairness and equity researchers — **gains nothing from this paper as written; say so and drop the section**

S1 item 10 is decisive and the authors should stop defending Section V-F. The best-served group's recall falls by essentially the same amount as the worst-served group's (OULAD gender −0.114 vs −0.117; UKZN GENDER −0.485 vs −0.488), and for `imd_band` and `disability` the worst group loses **less** than the best. Gap direction is 5 of 8 attributes, sign test p = 0.36. The `RACE` row is one cohort and one in-sample model. The "local" arm is a resubstitution fit (0.654 in-sample vs 0.330 cross-validated at UKZN), so most of the dramatic 0.65 → 0.18 fall in the abstract is the train-on-test gap, not transfer. And by the authors' own stated bound (label semantics perfectly collinear with institution) this section cannot separate "transfer harms the lowest quintile" from "a withdrawal-trained model applied under a registrar-pass rule harms the lowest quintile." There is no fairness finding here. There is a uniform collapse plus an order statistic.

### 2.6 Students and advisors — **gains nothing directly**

No result here changes what a student or an advisor does. The nearest thing is 2.1(e), and it is an argument for lower expectations, not for a different action.

---

## 3. Genre

### It is a **resource / benchmark paper**. Argued.

Rule out the alternatives first, because two of them are tempting and both are traps.

- **Negative-results paper — no.** A negative-results paper needs negatives that are (i) surprising, (ii) about someone else's claim, and (iii) robust. These are none of the three. "Our transform doesn't improve the decision" is a negative about the authors' own method, which is a correction, not a finding. "Explanations are unstable" is Hooker et al. 2021 restated. And S2's C3 is the killer: the authors *deleted two positive results* (pooled 0.683 vs local 0.692; few-shot k=100 at 0.712) that are sitting in their own released artifacts, then led with two negatives. A referee who opens `pooled.csv` — and one did — concludes the negativity is a posture. Do not submit a negative-results paper whose positive results are in the supplementary data.
- **Replication / reality-check paper — no, but it could become one.** The genre requires re-running *named published claims* and showing they don't hold (Ferrari Dacrema et al., below). This paper never reproduces a single prior result. S2's alternative — audit N recent LA transfer papers for majority-class F1 and unreported cohort overlap — *would* be a reality-check paper and would be a genuine contribution. It is a weekend of work and it is not in this manuscript.
- **Measurement paper — half true, and it is the right *sub*-framing.** The V-A range and the explanation floor/ceiling/transfer triple are measurements of quantities the field had not measured. But a measurement paper needs its measurements to be robust, and two of the three currently are not (the calibration measurement is a design identity; the ceiling is size-confounded). Measurement is the *spine inside* the resource paper, not the paper's genre.
- **Nothing publishable — no.** That verdict would be wrong. The assembly cost is real, the artifact is real, and 2.1(a)/(b) are decision-changing facts nobody has published.

**Resource/benchmark is right** because it is the only genre where the paper's largest true asset — five adapters over five platforms in four countries, with a leakage audit and a released frozen ladder — is the *contribution* rather than the *setup*, and where empirical results are allowed to be "here is how hard this benchmark is" rather than "here is our method winning."

### Exemplars, verified, and how each framed work of this shape so it landed

**1. Koh et al., *WILDS: A Benchmark of in-the-Wild Distribution Shifts*, ICML 2021.**
https://proceedings.mlr.press/v139/koh21a.html · https://arxiv.org/abs/2012.07421
The template. Ten curated datasets of *naturally occurring* shifts (across hospitals, camera traps, time and geography), one harmonised API, default models, a leaderboard. Their headline empirical result is purely negative — "standard training yields substantially lower out-of-distribution than in-distribution performance, and this gap remains even with models trained by existing methods for tackling distribution shifts" — and it lands as *evidence the benchmark is worth having*, not as a failure. Note what they did **not** do: they did not propose a fix and then report that it lost. The framing move to copy: the negative result is the benchmark's justification, stated in the abstract as difficulty, never as disappointment.

**2. Kuzilek, Hlosta & Zdrahal, *Open University Learning Analytics dataset*, Scientific Data 2017.**
https://doi.org/10.1038/sdata.2017.171
The authors' own reference [1], and the field's proof that in learning analytics a well-documented dataset with a schema *is* a publication, with no model and no finding attached. It is also the most-cited object in this literature. Framing move: describe the data, the provenance, the caveats, and the intended reuse; claim nothing else. If the benchmark is the contribution, this is the honesty standard it must meet — which means shipping the eligible-94 Oviedo table, the per-pair overlap file, and the schema non-commensurability disclosure (S2 §2.1: `social` is forum *posts* at KU Leuven, forum *click volume* at the OU, and Forum/Chat *log rows* under Moodle — the current III-C sentence "derived identically" is false as written and a dataset paper cannot survive that).

**3. Ocumpaugh, Baker, Gowda, Heffernan & Heffernan, *Population validity for educational data mining models: a case study in affect detection*, BJET 45(3):487–501, 2014.**
https://doi.org/10.1111/bjet.12156
The LA-native precedent for the paper's one new empirical fact. Their result — detectors built on urban students degrade on rural students and vice versa — is structurally identical to V-A, and it landed because they gave the phenomenon a **name borrowed from measurement theory** ("population validity") and presented it as a threat to the validity of the field's existing corpus rather than as a performance table. The authors should do the same with V-A: the finding is not "AUC varies", it is "single-cohort AUC has no external referent", and it retrospectively reinterprets hundreds of published numbers.

**4. Gardner, Yu, Nguyen, Brooks & Kizilcec, *Cross-Institutional Transfer Learning for Educational Models*, FAccT 2023.**
https://doi.org/10.1145/3593013.3594107 · https://arxiv.org/abs/2305.00927
The nearest prior work and therefore the paper's real competitor. Four US universities, harmonised, **not public**. They framed it as "a framework and metrics for assessing the utility and fairness of transferred dropout models" — i.e. they sold the *protocol*, and the data limitation became a footnote. This paper's one structural advantage over Gardner is that everything is public and reproducible, which is exactly why every reproducibility defect S1 found (headline numbers not matching `aggregate.csv`; Oviedo selection not auditable from the release) is disqualifying rather than cosmetic. Against Gardner, "public" is the whole pitch; if the release does not reproduce, there is no pitch.

**5. D'Amour et al., *Underspecification Presents Challenges for Credibility in Modern Machine Learning*, JMLR 23(226):1–61, 2022.**
https://www.jmlr.org/papers/v23/20-1335.html · https://arxiv.org/abs/2011.03395
The model for how to write the explanation result. Their finding — pipelines return many predictors with equivalently strong held-out performance that then disagree out of distribution — is the same phenomenon as "two models on disjoint halves of one cohort rank features at τ = 0.338". They made it a contribution by (i) naming it, (ii) measuring it as a *stress test protocol* across several domains, and (iii) framing the instability as a property of the pipeline rather than a failure of any model. The authors' V-E is one instance of this in one domain; framed as D'Amour framed it — "here is the identifiability floor of importance-based explanations on LMS engagement features, and it is below what any dashboard requires" — it is publishable. Framed as "transfer destroys explanations" it is falsified by their own ceiling.

**6. Ferrari Dacrema, Cremonesi & Jannach, *Are We Really Making Much Progress? A Worrying Analysis of Recent Neural Recommendation Approaches*, RecSys 2019 (Best Long Paper).**
https://arxiv.org/abs/1907.06902 · https://doi.org/10.1145/3298689.3347058
Included as the genre the authors are **not** in but could enter. Dacrema et al. took 18 named published methods, could reproduce 7, and beat 6 of those with properly tuned classical baselines. That is a reality-check paper: it puts a number on other people's claims. The equivalent here is S2's proposal (ii) — audit recent LA transfer papers for majority-class F1 without a chance baseline and for unreported cohort overlap. Note that the standard they would be auditing against is already published in the subfield: Bosch & Paquette, *Metrics for Discrete Student Models: Chance Levels, Comparisons, and Use Cases*, JLA 5(2):86–104, 2018, https://learning-analytics.info/index.php/JLA/article/view/5798 · https://doi.org/10.18608/jla.2018.52.6.

**7. Gardner, Brooks, Andres & Baker, *MORF: A Framework for Predictive Modeling and Replication at Scale with Privacy-Restricted MOOC Data*, IEEE Big Data 2018.**
https://arxiv.org/abs/1801.05236 — with Andres et al., *Studying MOOC completion at scale using the MOOC replication framework*, LAK 2018, https://doi.org/10.1145/3170358.3170369
The LA field's existing answer to "make transfer results checkable". Useful as related work and as a warning: infrastructure papers in this field get cited for the infrastructure and forgotten for the findings, which is an argument for making the release excellent rather than for making the findings dramatic.

---

## 4. The honest novelty statement — defensible at a viva

> We built the first public cross-institution transfer benchmark for LMS-based early warning — 63 cohorts, five universities, five platforms, four countries, 35,529 distinct students, one leakage-audited schema, adapters released — and used it to measure two quantities that the field had assumed rather than measured. First, the predictability of course failure from engagement clickstreams is a property of the institution, not of the method: identical features and identical code yield within-cohort ROC-AUC of 0.845 at the Open University and 0.53–0.67 at four others, which means a single-dataset early-warning result carries no information about any other institution, and the field's published performance range is largely a sampling of institutions rather than of methods. Second, permutation-importance explanations over engagement features are weakly identified *before* any transfer occurs: against a same-model noise floor of τ = 0.707 and a random-ranking expectation of 0.000, two models trained on disjoint halves of the same cohort agree at only τ ≈ 0.34, and the agreement between a transferred model and a locally trained one is 0.03 — so the instability that teacher-facing explanation dashboards would inherit is not caused by transfer, and cannot be avoided by keeping the model local.

**What to concede in the same breath, before the examiner does it for you:** the discrimination/calibration dissociation is a textbook clinical-prediction result confirmed in a new domain; the two evaluation hazards are known in ML broadly and one is published in *JLA* — what is new is the measurement, not the hazard; and the percentile transform's apparent calibration repair is an averaging artifact of the ordered-pair design that a supervised intercept update dominates.

---

## 5. Is this enough for a Master's, or for a PhD chapter?

### Master's: yes, comfortably — with one condition.

By volume and by rigour this exceeds a typical MSc empirical core: five dataset adapters, 3,969 evaluated ordered pairs, three cutoffs, three model families, three representations, a contamination audit, and a sensitivity grid, all released. The condition is that the thesis must claim what survived rather than what was hoped for. An MSc examiner will not punish "our proposed representation lost to a 2002 baseline"; they will punish a thesis that claims a calibration repair the candidate's own CSVs show to be `mean(source_rate − target_rate)` over a swap-symmetric pair set. Write the failure in, cite the reviewers, and this passes well.

### PhD chapter: yes as **one** chapter. No, as the whole empirical core.

Blunt version. The dissertation is on intelligent educational platforms with digital twins and explainable AI. The earlier synthetic study collapsed because the target was a deterministic function of the model's own features. This work replaced it, and it is far better science — but note the pattern an examiner will see: **study one measured a quantity that was true by construction; study two's headline positive result is also true by construction** (S1's finding 1: post-transform calibration-in-the-large ≡ source rate − target rate, R² = 0.961, and the pair set is exactly closed under source/target swap so its mean is 0.000000 at every rung, on any labels, including random ones). Twice in a row the candidate has reported a design identity as an empirical finding. That is the question a hostile examiner will actually ask, and it is a question about method, not about this dataset. The defence has to be that the candidate *found* the second one — but they did not; their reviewer did. The only durable answer is to lead with the identity, derive it, and present the design-artifact detection as part of the methodology.

What the chapter has that is PhD-grade: an artifact of real scholarly value, one new empirical fact with retrospective consequences for a literature, and one new comparison (transferred-vs-local explanation against a measured ceiling) that two review panels independently failed to find prior art for. What it lacks: a mechanism, a method that survives its own baselines, and a claim that is both new and robust. One chapter, not three.

For a PhD you need **two more chapters** beyond this one. The obvious candidates, in order of cost: (i) the compliance audit of the published LA transfer literature against the two hazards — cheap, self-contained, genuinely novel; (ii) an explanation-identifiability chapter that goes beyond permutation importance to a refit-based variable-importance estimator, which is what Hooker, Mentch & Zhou actually prescribe and which the current work only cites.

### The single additional experiment that would most raise it

**Re-run the explanation-identifiability experiment correctly, per institution, with training-set size matched to the ladder, and with a second importance estimator.** Specifically: train the two disjoint-half models on true 50 % splits (not the current sixths — `run_explanation_ceiling.cohort_reference_points` trains each ceiling model on ~1/3 of the cohort while the ladder trains on 100 %), rank on the full cohort, report the floor / ceiling / D3 triple **separately for each institution**, and add either SHAP or a refit-based model-reliance estimator (Fisher, Rudin & Dominici) alongside permutation importance to establish whether the instability is a property of the explanation method or of the features.

Why this one and not the others:

- It is the only experiment that repairs the dissertation's *thematic* core. The thesis is about explainable AI in educational platforms. Its single uncontested-novel claim is currently computed on a statistic that is confounded with sample size (corr(log n, ceiling τ) = +0.423; quartile ceilings 0.214 → 0.396) and pooled across institutions whose ceilings run +0.670 to −0.095, compared against a D3 average over a differently weighted population. In its present form the claim is not defensible at a viva. Fixed, it becomes a clean identifiability result that stands independently of every calibration and transfer dispute in the paper.
- It costs two lines of code and one cheap re-run (S1's own estimate), plus one added estimator.
- Adding a second importance method converts "permutation importance is unstable here" — which is Hooker et al. — into "importance-based explanation of LMS engagement models is unstable under *two* estimators, so the problem is the feature space, not the estimator", which is new and which is a claim about educational data specifically.

**Not chosen, and why:** the pooled / few-shot deployment analysis (§2.1) is more useful to practitioners and must be restored, but it is **re-analysis of data that already exists**, not an additional experiment — it costs an afternoon and there is no excuse for its absence. Treat it as a prerequisite, not an option. The literature compliance audit is the best *second* addition but belongs to a different chapter.

---

## 6. The strongest honest paper that can be written from what already exists

Everything below is computable from the released artifacts with no new data collection. It requires the pooled/few-shot restoration, the intercept-recalibration reference arm (S2 already ran it), institution-clustered intervals, per-institution disaggregation of the calibration and explanation results, and the deletion of Section V-F.

### Title

> **How Much of an Early-Warning Model Is the Institution? A Five-University Public Benchmark for Transferring Engagement-Based Risk Prediction**

### One-sentence thesis

> On 63 public cohorts from five universities, the accuracy, the calibration and the feature explanation of an ordinary LMS-based early-warning model are all properties of the institution it was measured at rather than of the model — with the practical consequence that an institution's own other cohorts are worth as much as the target cohort itself (AUC 0.686 vs 0.691), a single borrowed foreign model is worth 0.09 AUC less while pooled foreign sources are worth only 0.01 less (0.683 vs 0.692), and the per-feature explanation is not identified at any transfer distance including zero.

### Four section headings

1. **A five-institution public transfer benchmark, and what it cost to build**
   Schema, adapters, the four counters and seven features — including the honest statement that the counters are the nearest platform equivalents and differ by orders of magnitude, not the same measurement. The Zambia backward-label correction. The Oviedo selection rule, its bias (selected 20 courses: median n 137, |rate−0.5| 0.114; excluded 74: median n 76, |rate−0.5| 0.202), and the eligible-94 table shipped. The per-pair contamination audit as a released artifact: 72/78 at D1, 324/916 at D2, 78/2,912 at D3.

2. **Within-cohort predictability is an institutional property, not a model property**
   ROC-AUC 0.845 (OULAD, 19 cohorts, median n 1,614) against 0.53–0.67 elsewhere, with the small-institution endpoints reported as noisy rather than as a range endpoint. The retrospective consequence for the single-dataset literature, framed as population validity after Ocumpaugh et al. This is the paper's headline and it should be Section II, not Section V-A.

3. **What survives a move: discrimination, prevalence, and the architecture that actually matters**
   The distance ladder with institution-clustered intervals (D0−D3 = 0.093, [0.035, 0.155]). Calibration failure stated as what it is — prevalence shift, 93 % of it UKZN, per-pair |CIL| 0.301 → 0.249 under the transform, not "restored to −0.009" — with the swap-symmetry identity derived explicitly so the reader sees why the pooled mean is zero by construction. Then the deployment comparison the paper currently omits: **own-institution pooled 0.686 ≈ local 0.691 > pooled-foreign-percentile 0.683 ≫ single-foreign 0.594**, with intercept-only recalibration as the reference repair (Brier 0.361 → 0.223, |CIL| → 0.000, ranking unchanged) and the percentile transform positioned honestly as a label-free surrogate that recovers about a quarter of it. Recall at a 20 % flag budget throughout, reported against the oracle ceiling (47 % of attainable, transferred; 56 %, local).

4. **Explanations are weakly identified before they are transferred**
   Floor 0.707, ceiling ~0.34 (size-matched, per institution: +0.670 KU Leuven to −0.095 Zambia), transferred 0.026–0.034, random 0.000 for τ and 0.303 for J@3 — with the tau and Jaccard columns reconciled rather than one quietly dropped, and with the contamination filter applied here as well as to AUC (on clean pairs the D1/D2 gradient disappears: 0.086 vs 0.089). Conclusion for practice: no importance-ranked explanation panel over these features is trustworthy at any transfer distance, and locality does not rescue it.

**Deleted from the strongest version:** the fairness section (§2.5 above), the click-scale mechanism claim, the "monotonically" gradient, and every sentence claiming the percentile transform *is* the clinical updating ladder's first rung.

**What this buys:** a paper with one prescriptive deployment finding, one retrospective methodological finding, one clean identifiability result, and a released artifact — four things, all true, none of them the four things the manuscript currently claims.
