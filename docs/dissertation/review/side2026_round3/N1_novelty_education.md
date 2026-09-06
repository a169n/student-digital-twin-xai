# N1 — Novelty verdict, education literature (learning analytics / EDM / AIED / MOOC)

Stage: bibliography and source verification. Goal: falsify the claim of novelty.
Date of search: 2026-09-06. Every source listed below was resolved to a DOI or a URL that was
actually fetched in this session. Anything that could not be resolved was dropped.

**Hypothesis under attack.**
From cohort properties observable *without outcome labels* — number of students, volume and
dispersion of LMS activity, share of zero-activity students, course length, platform — one can
predict in advance (a) how well an at-risk model will perform on that cohort, and (b) whether it
will beat a trivial no-model rule such as ranking students by number of distinct login days.

---

## 1. Search strategy — exact queries run

Engine: web search (broad, US index) plus direct API verification against `api.crossref.org`,
`api.semanticscholar.org`, `arxiv.org`.

1. `predicting predictive model performance across courses learning analytics course characteristics moderators AUC`
2. `Gasevic "Learning analytics should not promote one size fits all" course-specific models`
3. `Conijn "Predicting student performance from LMS data" comparison of 17 blended courses Moodle IEEE Transactions Learning Technologies`
4. `meta-analysis moderators of predictive accuracy student dropout prediction course characteristics sample size effect`
5. `meta-learning dataset meta-features predict classifier performance educational data mining algorithm selection`
6. `simple baseline outperforms machine learning at-risk student prediction "number of logins" trivial baseline comparison`
7. `Ocumpaugh population validity detectors urban suburban rural affect detectors generalize`
8. `"predicting the predictability" OR "how predictable is a course" learning analytics cohort characteristics prediction difficulty`
9. `Gardner Brooks "Student success prediction in MOOCs" review User Modeling User-Adapted Interaction generalizability`
10. `MOOC dropout prediction across many courses "course-level" variance in AUC course features enrollment size predictive accuracy`
11. `Jayaprakash "Early alert of academically at-risk students" Open Academic Analytics Initiative cross-institution portability Journal of Learning Analytics`
12. `sample size requirements predictive learning analytics "how much data" training set size effect on AUC student prediction course`
13. `"course characteristics" explain variation in "prediction accuracy" early warning system multiple courses LAK conference paper`
14. `learning analytics weak baselines reproducibility "simple baseline" deep learning knowledge tracing outperformed by simple heuristic critique`
15. `Andres Baker "MOOC Replication Framework" studying MOOC completion at scale moderators course features replication LAK 2018`
16. `"cross-institutional" transfer early warning model generalizability multiple universities AUC varies institution characteristics learning analytics`
17. `systematic review meta-analysis machine learning student performance prediction moderator analysis "sample size" "dataset size" effect on reported accuracy education`
18. `"early warning system" feasibility readiness assessment before deployment "is it worth" institution decide whether predictive analytics will work`
19. `"meta-learning" educational datasets predict which course will have accurate student model "meta-features" cohort level learning analytics`
20. `Saqr "why do predictive models fail" OR "generalizability crisis" learning analytics course context transferability across courses 2023 2024`
21. `"data complexity measures" OR "class separability" educational data mining dataset difficulty student dropout predict classifier performance`
22. `Finnegan Morris Lee "course-level differences" online course student success predictors disciplines LMS variables`
23. `"course size" OR "class size" associated with higher prediction accuracy student model "predictive performance" varied across courses correlation learning analytics study`
24. `"Reliable or Just Accurate" "Cross-Dataset Audit of Early-Warning Models Under Course-Level Distribution Shift" abstract authors`
25. `"Elastic Net" most stable across courses and institutions early warning base rate threshold adjustment dropout prediction 2026 study institutions A B C D retention`
26. `"one feature" OR "single predictor" baseline audit published at-risk prediction models education "do we need machine learning" replication study simple rule`
27. `OULAD module-level differences prediction performance varies across modules AAA BBB CCC AUC comparison presentation`
28. `"predict the performance" of student prediction models before training unlabeled data education "without labels" estimate accuracy new course`
29. `"active days" OR "number of logins" alone as good as machine learning model predicting dropout at-risk students simple count baseline learning analytics evaluation`
30. `"which courses" suitable for predictive modelling screening decide where early warning will fail learning analytics "not all courses" prediction viable`
31. `EDM LAK paper "simple baseline" beats published models student prediction audit "we show that" ranking students by total clicks matches complex models`
32. `"majority class" OR "trivial classifier" baseline comparison neglected educational prediction studies critique reporting AUC above chance meaningless`
33. `"Modelability" Xu Zhang Blake Stigler Journal of Learning Analytics predictive models generalizability scalability`

Verification fetches (all returned metadata; results folded into the source list below):
Crossref DOI lookups for 10.1016/j.iheduc.2015.10.002, 10.1109/TLT.2016.2616312, 10.1111/bjet.12156,
10.18608/jla.2014.11.3, 10.1007/s11257-018-9203-z, 10.1145/3170358.3170369, 10.1145/3593013.3594107,
10.1080/03075079.2022.2061450, 10.3390/computers15090572, 10.1145/3051457.3053974, 10.2196/60231;
Crossref bibliographic queries for the Mathrani, Gardner–Brooks-JLA, Finnegan and "AUC is not the
problem" titles; Semantic Scholar DOI lookups for 10.3390/computers15090572, 10.3390/educsci16071110,
10.18608/jla.2026.9099; arXiv abstract fetches for 2604.22812, 2604.19279, 2305.00927, 1702.06404,
1801.08494; full-text PDF fetch of the JLA "Modelability" article.

**Dropped for failed verification (per the rules, "hard to verify" = FAIL):**

- "On Fixing the Right Problems in Predictive Analytics: AUC Is Not the Problem" — a PDF exists at
  `learninganalytics.upenn.edu/ryanbaker/AUC-is-not-the-problem.pdf` but the fetch returned
  unparseable binary and Crossref returned no matching record. Not used as evidence.
- MDPI HTML pages return 403 to the fetcher; MDPI items below were verified through Crossref and
  Semantic Scholar metadata instead, which returned title, authors, venue and full abstract.

---

## 2. Closest prior work, ranked by threat level

### T1 — HIGH. Angeioplastis, Konstantakis & Tsimpiris (2026)

*Reliable or Just Accurate? A Cross-Dataset Audit of Early-Warning Models Under Course-Level
Distribution Shift.* **Computers** 15(9):572. DOI **10.3390/computers15090572**
(verified: Crossref record; abstract retrieved verbatim via Semantic Scholar).

What it did: audited LMS early-warning models under *unseen-course* validation across one
institutional Moodle deployment (International Hellenic University: 1,284 student-course
observations, 924 students, 35 courses) plus OULAD (N = 22,437) and Riestra (N = 25,260). Six
harmonized behavioural features at 10/25/33/50% observation cutoffs, four model families.
Unseen-course balanced accuracy: OULAD 0.619–0.686, Riestra 0.584–0.639, IHU 0.470–0.582 and
*statistically indistinguishable from chance at the earliest cutoff*. They ran **repeated
size-matched controls**, which attenuated the Riestra–IHU gap but left the OULAD advantage largely
unchanged. Conclusion sentence: "Reported performance is associated with validation design, label
definition, course composition, and dataset scale."

Closeness: this is the nearest published work to part (a). It (i) establishes that within-cohort
performance varies enormously across courses and datasets, (ii) explicitly names *dataset scale* and
*course composition* as associated with performance, and (iii) actually manipulates size through
size-matched resampling to test the size explanation. Its chance-level comparison is a weak cousin
of part (b).
Where it stops short: three datasets, not 63 cohorts; no cohort-level meta-model; no *prospective*
prediction for a new unlabelled cohort; no scalar cohort covariate such as activity dispersion or
zero-activity share; and the reference point is chance (0.5 balanced accuracy), not a trivial
single-feature ranking rule. Nothing in it lets a practitioner forecast an AUC for a cohort they
have not yet labelled.

### T2 — HIGH (method, wrong field). Silvey & Liu (2024)

*Sample Size Requirements for Popular Classification Algorithms in Tabular Clinical Data: Empirical
Study.* **Journal of Medical Internet Research** 26:e60231. DOI **10.2196/60231**
(verified: Crossref record with abstract).

What it did: across 16 large clinical datasets and 4 algorithms, empirically located the sample size
at which performance plateaus, then fitted **multivariable models predicting that requirement from
dataset-level characteristics**, explaining 66.5%–84.5% of the variation, and argued those
characteristics "can be influenced or estimated before the start of a research study."

Closeness: the strongest evidence that the *general move* — regress achievable model performance on
dataset-level meta-features known in advance — is not new. It is the clinical-tabular analogue of
part (a), and a reviewer who knows it will call the education version an application rather than an
invention.
Where it stops short: not education, not cohorts, and critically its predictors include class
balance and label-dependent complexity, i.e. **it is not label-free**. The label-free constraint,
which is the operational point of the hypothesis (screen a cohort before any outcomes exist), is not
satisfied. The same holds for the broader meta-learning / data-complexity tradition it belongs to
(dataset meta-features to expected classifier accuracy), which is likewise label-dependent.

### T3 — MEDIUM-HIGH. Conijn, Snijders, Kleingeld & Matzat (2017)

*Predicting Student Performance from LMS Data: A Comparison of 17 Blended Courses Using Moodle LMS.*
**IEEE Transactions on Learning Technologies** 10(1):17–29. DOI **10.1109/TLT.2016.2616312**
(verified: Crossref record; open copy at `pure.uvt.nl/ws/portalfiles/portal/17062754/`).

17 blended courses, 4,989 students, one institution; explained variance in final exam grade from LMS
predictors ranged 8%–37% across courses; portability across courses judged low.

Closeness: the canonical demonstration that within-cohort predictive performance is strongly
course-dependent — it establishes the *phenomenon* the hypothesis proposes to forecast. Reviewers
will cite it as "we already knew performance varies by course."
Where it stops short: course-to-course differences are discussed qualitatively (course type,
learning design, which Moodle modules were used). No model of performance as a function of measured
course properties, no cross-institution or cross-platform spread, no baseline rule.

### T4 — MEDIUM-HIGH. Gašević, Dawson, Rogers & Gašević (2016)

*Learning analytics should not promote one size fits all: The effects of instructional conditions in
predicting academic success.* **The Internet and Higher Education** 28:68–84.
DOI **10.1016/j.iheduc.2015.10.002** (verified: Crossref record).

Nine blended undergraduate courses, n = 4,134; compared generalized against course-specific models
and showed instructional conditions change both predictive power and which predictors matter.

Closeness: the field's standard citation for "context moderates predictive performance", and the
conceptual parent of the hypothesis.
Where it stops short: the moderators are *instructional design* variables coded by researchers, not
label-free quantitative cohort statistics; the analysis is explanatory (does the course-specific
model fit better?) rather than predictive (what AUC will this new cohort yield?); nine courses, one
institution, one platform; no trivial-rule comparison.

### T5 — MEDIUM (terminology collision). Xu, Zhang, Blake & Stigler (2026)

*Modelability as a Strategy for Improving the Generalizability and Scalability of Predictive
Models.* **Journal of Learning Analytics** 13:89–109. DOI **10.18608/jla.2026.9099**
(verified: Crossref record; full PDF fetched from
`learning-analytics.info/index.php/JLA/article/download/9099/7955`).

Introduces "modelability" — a *purposefully designed* learning ecosystem (CourseKata instrumented
textbook) whose measurement, implementation and ecosystem properties make predictive models
generalize across institutions and disciplines.

Closeness: it owns the word. Any paper claiming to measure "how modellable is this cohort" collides
with a 2026 JLA construct of the same name.
Where it stops short: on the full-text check the paper gives no operational definition of modelability
as a *measurable pre-hoc property*, performs no analysis predicting model performance from context
characteristics, and uses no trivial baseline. It prescribes designing environments to be modellable;
it does not diagnose whether a given cohort is.

### T6 — MEDIUM (contradicting evidence). Whitehill, Mohan, Seaton, Rosen & Tingley (2017)

*MOOC Dropout Prediction: How to Measure Accuracy?* Proceedings of the 4th ACM Conference on
Learning @ Scale (L@S '17), 161–164. DOI **10.1145/3051457.3053974** (verified: Crossref record).
Extended version: arXiv:1702.06404, *Delving Deeper into MOOC Student Dropout Prediction*
(verified: arXiv abstract page fetched at `arxiv.org/abs/1702.06404`).

Dropout classifiers over 40 HarvardX MOOCs; proxy-label classifiers reached 87.33% against 90.20%
AUC (averaged over 8 weeks) for post-hoc training; and **classifier performance does not vary
significantly with the academic discipline**.

Why it matters: this is the one explicit published test of "does a course-level attribute predict
model performance?" in a large multi-course setting, and for discipline the answer was *no*. It cuts
both ways — prior art for asking the question, and a negative result a reviewer can use against
cohort-level predictors generally. The tested attribute was categorical and semantic; size, activity
volume and zero-activity share were not tested.

### T7 — MEDIUM. Saqr, Jovanovic, Viberg & Gašević (2022)

*Is there order in the mess? A single paper meta-analysis approach to identification of predictors of
success in learning analytics.* **Studies in Higher Education** 47(12):2370–2391.
DOI **10.1080/03075079.2022.2061450** (verified: Crossref record. The publisher HTML returned 403 to
the fetcher, so the description below stays inside what metadata supports).

Meta-analyses predictor–outcome effect sizes across many offerings of courses from one programme with
homogeneous design; the same predictor can be significant in one offering and null in the next.

Closeness: applies meta-analytic machinery at the course level in learning analytics — the
methodological neighbour of "meta-regress AUC on cohort features".
Where it stops short: the dependent variable is the *effect size of individual predictors*, not the
*performance of a model*, and the work documents heterogeneity rather than predicting it from
label-free cohort attributes. Because the full text could not be fetched, no strong claim leans on
this entry.

### T8 — MEDIUM-LOW. Ocumpaugh, Baker, Gowda, Heffernan & Heffernan (2014)

*Population validity for educational data mining models: A case study in affect detection.*
**British Journal of Educational Technology** 45(3):487–501. DOI **10.1111/bjet.12156**
(verified: Crossref record; open PDF at `learninganalytics.upenn.edu/ryanbaker/BJET%20revised2%202013%20v30jlo%20(1).pdf`).

Detectors trained on urban, suburban or rural sub-populations fail to generalize across them.
Establishes that *who is in the cohort* governs model validity — the demographic analogue of the
hypothesis. Population membership is a categorical label, no performance forecast is produced, and
there is no baseline-rule comparison.

### T9 — MEDIUM-LOW. Jayaprakash, Moody, Lauría, Regan & Baron (2014)

*Early Alert of Academically At-Risk Students: An Open Source Analytics Initiative.*
**Journal of Learning Analytics** 1(1):6–47. DOI **10.18608/jla.2014.11.3**
(verified: Crossref record; open PDF at `files.eric.ed.gov/fulltext/EJ1127037.pdf`).

The OAAI transported a Marist-trained model to partner institutions and reported portability loss.
Cross-institution deployment evidence; no meta-model of where portability will hold.

### T10 — MEDIUM-LOW. Gardner, Yu, Nguyen, Brooks & Kizilcec (2023)

*Cross-Institutional Transfer Learning for Educational Models: Implications for Model Performance,
Fairness, and Equity.* FAccT '23, 1664–1684. DOI **10.1145/3593013.3594107**
(verified: Crossref record; preprint arXiv:2305.00927 fetched).

Four universities, more than 200,000 enrolled students annually; a simple zero-shot cross-institutional
transfer procedure matched locally trained models without sacrificing fairness. On direct check the
paper analyses what happens *after* transfer and does **not** model institution-level properties that
would forecast transfer success. Its result is also mild counter-evidence to a strong
"context decides everything" framing.

### T11 — LOW-MEDIUM. Andres, Baker, Gašević, Siemens, Crossley & Joksimović (2018)

*Studying MOOC completion at scale using the MOOC replication framework.* LAK '18, 71–78.
DOI **10.1145/3170358.3170369** (verified: Crossref record; open PDF at
`learninganalytics.upenn.edu/ryanbaker/LAK_Paper49.pdf`).

Replicated 15 published findings across 29 iterations of 17 MOOCs; 12 of 15 replicated significantly.
The closest thing in education to a systematic multi-cohort audit — but of *claims*, not of model
performance, and its conclusion (behaviours associated with completion are largely common across
MOOCs) again pushes against strong context-dependence.

### T12 — LOW-MEDIUM (relevant to section 5). Gardner & Brooks (2018)

*Evaluating Predictive Models of Student Success: Closing the Methodological Gap.*
**Journal of Learning Analytics** 5(2):105–125. DOI **10.18608/jla.2018.52.7**
(verified: Crossref record; preprint arXiv:1801.08494 fetched).

Argues learning analytics "overwhelmingly uses only naive methods for model evaluation or statistical
tests which are not appropriate for predictive model evaluation", demonstrated over 96 predictive
models on MOOC data. The field's standing critique of evaluation practice — about *statistical
comparison procedure between models*, not about benchmarking published models against a no-model rule.

### T13 — LOW-MEDIUM (relevant to sections 4 and 5). Pérez, Nikulin & Madariaga (2026)

*Low-Overhead Learning Analytics: A Parsimonious Early Warning System for At-Risk Students in Chilean
STEM Courses.* **Education Sciences** 16(7):1110. DOI **10.3390/educsci16071110**
(verified: Semantic Scholar record with full abstract).

Deliberately uses **one predictor** (the first partial grade) in univariate logistic regression across
two introductory mathematics courses at two Chilean universities, externally validated on the next
year's cohort without retraining, AUC 0.85–0.93. Framed as "a replicable, low-overhead floor for
early warning practice in comparable courses."

Closeness to part (b): the closest published expression of the *spirit* of a no-model floor.
Where it stops short: the predictor is a graded assessment, not label-free behaviour; no ML
alternative is compared; no audit of other published models is performed. It supports the framing
rather than pre-empting it.

### T14 — LOW. Finnegan, Morris & Lee (2008)

*Differences by Course Discipline on Student Behavior, Persistence, and Achievement in Online Courses
of Undergraduate General Education.* **Journal of College Student Retention: Research, Theory &
Practice** 10(1):39–54. DOI **10.2190/cs.10.1.d** (verified: Crossref record).
22 courses in three disciplinary groups; explained variance in final grades 26%–36%, with no single
predictor shared across disciplines. Historical anchor for course-level heterogeneity.

### T15 — LOW. Mathrani, Susnjak, Ramaswami & Barczak (2021)

*Perspectives on the challenges of generalizability, transparency and ethics in predictive learning
analytics.* **Computers and Education Open** 2:100060. DOI **10.1016/j.caeo.2021.100060**
(verified: Crossref record). Perspective piece naming generalizability as the open problem; offers no
measurement of it.

### T16 — LOW (checked and cleared). Two 2026 preprints that surfaced repeatedly

- Schwerter, Sabel, Bose, Bernacki, Xu, Schmellenkamp, Zeume & Doebler (2026), *Cross-Course
  Generalizability of SRL-Aligned Predictive Models Using Digital Learning Traces*, arXiv:2604.22812
  (abstract fetched, submitted 14 April 2026). Three theoretical computer science courses
  (N = 137 / 104 / 148) at two universities. On direct check it **does not** predict AUC from course
  characteristics and uses no trivial baseline. It is the source of the "Elastic Net was most stable
  across courses and institutions" and threshold-recalibration findings that appear in search snippets.
- Schwerter, Krivosija, Novak, Ickstadt & Munteanu (2026), *Early Prediction of Student Performance
  Using Bayesian Updating with Informative Priors Across Cohorts*, arXiv:2604.19279 (abstract fetched,
  submitted 21 April 2026). Two consecutive cohorts (N1 = 307, N2 = 323) of one blended mathematics
  course; cohorts are treated as temporal units, with no cohort-property model.

---

## 3. Verdict on part (a) — predicting model performance from unlabelled cohort properties

**PARTIALLY ANTICIPATED — the specific claim survives, the broad phrasing does not.**

Already published, and to be conceded up front:

- Within-cohort predictive performance varies wildly across courses, institutions and platforms —
  Conijn et al. 2017 (8%–37% explained variance over 17 courses), Gašević et al. 2016, Finnegan et al.
  2008, Angeioplastis et al. 2026 (balanced accuracy 0.47–0.69 across three datasets).
- The variation is *associated with* course composition and dataset scale — stated in those words in
  Angeioplastis et al. 2026, who additionally ran size-matched resampling, a direct partial test of
  the cohort-size explanation.
- Regressing achievable model performance on dataset-level meta-features estimable in advance is an
  established methodology in adjacent fields — Silvey & Liu 2024 in clinical tabular data, plus the
  wider meta-learning and data-complexity literature.

Not done by any located source:

- No education paper builds a **cohort-level meta-model** whose unit of analysis is the cohort and
  whose dependent variable is that cohort's predictive performance.
- No education paper restricts the covariates to **label-free** cohort statistics. Every
  performance-versus-properties analysis found uses either categorical context descriptors
  (discipline, institution, demographic group, instructional design) or label-dependent quantities
  (class balance, prevalence, complexity measures). Silvey & Liu, the strongest methodological
  precedent, is explicitly label-dependent.
- No education paper reports a quantitative association between cohort size or activity volume and
  attained AUC at anything like this breadth (63 cohorts, 5 institutions, 5 platforms, 4 countries).
  The only attribute-versus-performance test at comparable scale is Whitehill et al. 2017's discipline
  test over 40 HarvardX MOOCs, and it was a **null** result.

Contradicting evidence to disclose rather than bury: Whitehill et al. 2017 (course attribute did not
move performance), Andres et al. 2018 (findings largely replicate across MOOCs) and Gardner et al.
2023 (zero-shot cross-institutional transfer works better than feared) all push against a strong
"cohort context determines model quality" story. The defence is that these tested semantic or
categorical attributes and transfer rather than scalar size and activity covariates on in-cohort
performance. But the +0.60 / +0.61 correlations must be reported alongside those nulls, and with the
obvious confound named: AUC estimated on a small cohort is noisier and differently distributed than
AUC estimated on a large one, so part of any size–AUC correlation is an estimation artefact rather
than a property of the cohort. Angeioplastis et al.'s size-matched control is the existing precedent
for handling exactly this; omitting an equivalent control is the single most likely reason a reviewer
kills part (a).

## 4. Verdict on part (b) — predicting whether the model beats a trivial rule

**NOVEL.** No source located, in education or adjacent, predicts *in advance* whether a trained
at-risk model will outperform a no-model rule on a given cohort. The nearest approaches:

- Angeioplastis et al. 2026 determine post hoc, per dataset, that IHU unseen-course performance was
  statistically indistinguishable from **chance** at the earliest cutoff. Chance is a weaker reference
  than a single-feature ranking rule, and the determination is retrospective.
- Pérez et al. 2026 advocate a minimal single-predictor system as a practical floor, without
  forecasting when that floor suffices.

Part (b) is the strongest and cleanest novelty claim in the hypothesis and should carry the paper.

## 5. Verdict on the no-model baseline audit — has anyone done it in this field?

**NOT DONE, as far as this search can establish.** Queries 6, 14, 26, 29, 31 and 32 targeted this
specifically and returned nothing that systematically re-evaluates published at-risk models against a
trivial single-feature ranking rule. What exists is adjacent and weaker:

- Gardner & Brooks 2018 (DOI 10.18608/jla.2018.52.7) criticises naive *evaluation methodology* and the
  absence of appropriate model comparison — the closest standing critique, but about statistical
  procedure between models, not a no-model floor.
- Andres et al. 2018 (LAK '18) is the field's large-scale replication audit, of *findings* rather than
  of model utility against a baseline.
- Gardner & Brooks 2018 UMUAI review (*Student success prediction in MOOCs*, User Modeling and
  User-Adapted Interaction 28(2):127–203, DOI **10.1007/s11257-018-9203-z**, verified via Crossref)
  catalogues methodological gaps in MOOC success prediction — extensive subpopulation filtering,
  ineffective evaluation, use of data unavailable in real deployment — but runs no baseline audit.

Caveat on the strength of this negative: absence in a web-index search is weaker evidence than
presence. Before submission, re-check directly against the full LAK and EDM proceedings indexes; a
short EDM paper doing exactly this would not necessarily surface in a general web search.

## 6. Narrowed wording that is defensible

The hypothesis survives if stated as prediction from label-free scalar cohort statistics, against a
named no-model rule, at multi-institution scale, with the estimation-noise confound controlled:

> Across 63 course cohorts drawn from 5 institutions, 5 LMS platforms and 4 countries, cohort-level
> statistics computable **before any outcome labels exist** — enrolment count, mean and dispersion of
> LMS activity volume, share of students with zero recorded activity, course length in weeks, and
> platform — predict (i) the discrimination a standard at-risk model attains on that cohort and
> (ii) whether that model outranks a no-model rule that ranks students by number of distinct active
> days. We report cohort-level meta-regression with size-matched controls separating genuine cohort
> effects from the sampling variability of AUC estimated on small cohorts, and we evaluate the
> meta-model by leave-one-institution-out prediction rather than in-sample fit.

Three load-bearing wording constraints:

1. Say **label-free** everywhere. It is the only property separating the claim from Silvey & Liu 2024
   and from the meta-learning literature.
2. Say **beats a named trivial rule**, not "beats chance". Angeioplastis et al. 2026 already own
   "indistinguishable from chance".
3. Do not use **modelability** as a technical term. Xu et al. 2026 (JLA 13:89–109) defined it as an
   ecosystem *design* strategy; reusing it for a measurable cohort property collides head-on with a
   2026 paper in the target field's flagship journal.

## 7. Does it survive?

**Yes, narrowly, and not in its current broad phrasing.** No single paper kills it.

The paper that comes closest to killing part (a) is **Angeioplastis, Konstantakis & Tsimpiris (2026),
*Reliable or Just Accurate? A Cross-Dataset Audit of Early-Warning Models Under Course-Level
Distribution Shift*, Computers 15(9):572, DOI 10.3390/computers15090572** — recent, an audit, it names
dataset scale and course composition as drivers of reported performance, and it already ran the
size-matched control. It must be cited, contrasted explicitly, and the contribution positioned as
*prospective cohort-level prediction* against its *retrospective three-dataset diagnosis*. If a
reviewer knows this paper and the manuscript does not cite it, part (a) is dead on arrival.

The paper that most threatens the framing is **Xu, Zhang, Blake & Stigler (2026), JLA 13:89–109,
DOI 10.18608/jla.2026.9099** — terminology only, no substantive overlap.

The paper that most threatens the method's originality is **Silvey & Liu (2024), JMIR 26:e60231,
DOI 10.2196/60231** — same idea, different field, label-dependent, which is the escape hatch.
