# Reviewer 2 — Domain (learning analytics / educational data mining)

**Manuscript:** *What Transfers and What Does Not: Predictions, Thresholds and Explanations of Early-Warning Models Across Five Institutions* (`docs/dissertation/side2026_paper.md`, draft v1.0, 2026-09-05)
**Round:** 1
**Scope of this seat:** literature coverage, theoretical framing, correctness of domain claims, size of the incremental contribution.
**Recommendation:** **Major revision.**

---

## Summary

The paper assembles 64 cohorts from five public datasets (OULAD, Oviedo/Riestra, UKZN, KU Leuven, Zambia) on five LMS platforms into one seven-feature engagement schema with a relative early-warning cutoff, then evaluates all 4,096 ordered source→target pairs along a four-rung transfer-distance ladder. It reports three separable degradations — discrimination (ROC-AUC 0.746 → 0.616), a fixed 0.5 decision threshold (F1 0.809 → 0.507), and permutation-importance agreement with a locally trained model (Kendall τ 0.03) — and offers a label-free within-cohort percentile representation that repairs the second substantially and the first partly, and the third not at all.

The assembly work is real and the ladder is a sensible experimental object. Two things stand between this draft and acceptance at a learning-analytics venue.

First, the **operational metric is measured on the wrong class.** F1 is computed with scikit-learn's default `pos_label=1` against `y = passed` (`services/ml/src/experiments/transfer_benchmark.py:162`), i.e. on the *pass* class — the class an early-warning system does not alert on. The paper's second headline finding ("the threshold fails first", "this is the failure a deployed early-warning system actually experiences") is therefore a statement about the majority-class F1 of a fixed cutoff under a prevalence that ranges 0.21–0.95. That number is *guaranteed* to move with prevalence almost independently of anything the model learned. This is a domain-correctness error, not a presentation choice, and it is the finding the fix is credited with repairing.

Second, the **gap statement is over-claimed on two of its three legs.** One near-identical design (Angeioplastis et al., *Computers* 2026) and one label-free relative-representation fix (Yoneda, Švábenský et al., EDM 2025) are both uncited and both directly reachable by a referee's first search. The third leg — explanation portability after transfer — survives falsification and is the paper's genuinely novel measurement; it is currently the least emphasised of the three.

The label harmonisation is defensible in outline but has two construct defects that a learning-analytics referee will find in the code (repeat-registration `max()` collapse; conceded/supplementary passes counted as passes), plus a modality confound at D3 that the paper never names.

---

## Gap-Claim Verification

The manuscript's Section II closes with three claims (line 45): (a) no public multi-institution, multi-platform benchmark of early-warning transfer exists; (b) no label-free representation fix has been tested; (c) explanation portability after transfer has not been quantified.

### Claim (a): "No public multi-institution, multi-platform benchmark of early-warning transfer exists"

**Verdict: survives only in a narrowed form. As written, a referee can name a 2026 paper that comes very close, plus two older lines of work that make the framing look uninformed.**

Searches run: `cross-institutional transfer learning educational models fairness Gardner Kizilcec FAccT 2023`; `"transfer" OR "portability" early warning student model across institutions benchmark public datasets multi-platform 2025 2026`; `"train on OULAD" ... cross-dataset generalization`; `multi-institution public benchmark learning analytics early warning generalization 2026 harmonized schema at-risk`; `MORF "MOOC Replication Framework" ... benchmark`; `Riestra-Gonzalez Ortin Moodle log dataset public repository ... 532 courses`.

**The dangerous one.** Angeioplastis, Konstantakis & Tsimpiris, "Reliable or Just Accurate? A Cross-Dataset Audit of Early-Warning Models Under Course-Level Distribution Shift", *Computers* 2026, 15(9), 572 — <https://www.mdpi.com/2073-431X/15/9/572>, abstract verified via <https://api.semanticscholar.org/graph/v1/paper/DOI:10.3390/computers15090572>. It evaluates **three datasets** (International Hellenic University Moodle, plus the two public benchmarks OULAD *N*=22,437 and Riestra *N*=25,260 — i.e. two institutions, two platforms, public), with **six semantically harmonised behavioural features**, at **10%, 25%, 33% and 50% observation cutoffs**, under random-row / unseen-student / **unseen-course** validation, with a **label-definition audit** ("grade-scale audit identified substantial inconsistencies between configured and observed course maxima") and explicit attention to **prevalence-sensitive metrics**. Its stated recommendation — "unseen-course evaluation, label-definition audits, course-aware uncertainty estimates ... as standard reporting practices" — is the practical conclusion this manuscript also reaches.

What it does *not* do: source→target ordered-pair transfer (it uses grouped held-out validation, not train-here-apply-there), no distance ladder, no representation fix, no explanation portability, three datasets rather than five. So claim (a) is not falsified — but the sentence "no public multi-institution, multi-platform benchmark of early-warning transfer exists" is false on a plain reading, and the relative-cutoff grid (10/25/33/50%) plus the harmonised-behavioural-schema idea are both prior art. **This paper must be cited and distinguished, in Related Work and in the gap sentence.**

**The one a senior LA referee will name from memory.** Jayaprakash, Moody, Lauría, Regan & Baron, "Early Alert of Academically At-Risk Students: An Open Source Analytics Initiative", *Journal of Learning Analytics* 1(1), 6–47, 2014 — <https://files.eric.ed.gov/fulltext/EJ1127037.pdf>. The Open Academic Analytics Initiative built an early-alert model at Marist and **ported it to partner institutions**, reporting exactly the transfer degradation this paper re-discovers, twelve years earlier. Not public data, not a benchmark, single platform — but a manuscript whose Introduction says the deployment question is "left open" without mentioning OAAI reads as unaware of its own field's history.

**Also relevant to the framing:** Gardner, Brooks, Andres & Baker, "MORF: A Framework for Predictive Modeling and Replication At Scale With Privacy-Restricted MOOC Data" — <https://arxiv.org/abs/1801.05236> — is an institutional multi-source replication benchmark of exactly the kind whose absence the paper asserts, resolved by federated execution rather than open data. The paper's own point (line 23) that such benchmarks "are not reproducible" is the right response, but it should be made against MORF explicitly, since MORF is the field's standard answer to the data-sharing problem.

**Safe re-wording:** the novel claim is *scale and design*, not existence — "the largest public cross-institution transfer evaluation we are aware of, and the first to evaluate ordered source→target pairs along a distance ladder rather than grouped held-out validation".

### Claim (b): "No label-free representation fix has been tested"

**Verdict: falsified as written.**

Searches run: `percentile rank normalization within course features cross-course transfer student dropout prediction unsupervised feature alignment EDM`; `domain adaptation cross-course student performance prediction unsupervised feature normalization learning analytics`; `"quantile" OR "percentile" OR "rank-based" feature transformation transfer across courses at-risk student prediction "generalizability"`.

**Direct hit.** Yoneda, Švábenský, Li, Deguchi & Shimada, "Ranking-Based At-Risk Student Prediction Using Federated Learning and Differential Features", EDM 2025 — <https://arxiv.org/html/2505.09287>, proceedings entry <https://educationaldatamining.org/EDM2025/proceedings/2025.EDM.long-papers.51/index.html>. Their "differential features" are within-course pairwise differences of student activity vectors, introduced for precisely this manuscript's stated reason, in their words: *"differential features use relative values, reducing the impact of such discrepancies and enabling the construction of a more generalized model"*, with gains attributed to "(2) relative value utilization mitigating feature distribution disparities". The feature transform uses no target labels. Their scope is narrower than this manuscript's (Kyushu University only, BookRoll e-textbook only, 7 training + 5 hold-out courses, 1,136 students, and they explicitly concede "since all data in this study originates from a single institution and platform, the generalizability of the proposed method to different institutional contexts remains an open question") — which is a gift to the present paper, but only if it is cited and positioned as the thing being extended.

**Second, weaker but awkward hit.** The Riestra public release itself already encodes behavioural variables as *"normalized event-percentage proxies rather than raw log counts"* (per the Angeioplastis description above). One of this paper's five sources therefore ships a percentage-normalised representation, which makes "raw counts" a partly artificial baseline for that institution and should be stated in Section III.

**Third.** López-Zambrano et al. 2022 [8] is itself a label-free representation fix for portability (an ontology of actions replacing low-level log attributes). The manuscript cites it and then writes the blanket sentence anyway.

**Safe re-wording:** the defensible claim is the narrow one already in Section II line 41 — "a within-cohort *rank/percentile rescaling of the shared features themselves* has not been tested *across institutions*" — plus the first evidence that such a transform is uniform across model families and repairs thresholds more than discrimination. Delete the blanket clause from the abstract and from line 45.

### Claim (c): "Explanation portability after transfer has not been quantified"

**Verdict: survives. This is the paper's real contribution. Drop the absolute phrasing and position it against three adjacent lines.**

Searches run: `SHAP feature importance agreement across institutions student success prediction stability explainable learning analytics`; `feature importance ranking agreement transferred model versus locally trained model Kendall tau Jaccard cross-domain explanation transferability`; `Swamy Käser "Trusting the explainers" ... Kendall`; `"Federated and explainable learning analytics" ...`.

I could not find any work that computes agreement between the importance ranking of a *transferred* model and the ranking a *locally trained* model would produce, in education or (for that matter) in a comparable tabular-transfer setting. The nearest work:

- **Tiukhova et al., DSS 2024 [15]** — measures SHAP rank stability *across cohorts/academic years for locally retrained models* using feature agreement, rank agreement and rank correlation. Different quantity (temporal stability of local explanations, not portability of a transferred one), but methodologically the closest, and the manuscript is right that the distinction is real. See "Citation Accuracy" below for a characterisation problem with this reference.
- **A 2026 federated-XAI paper**, "Federated and explainable learning analytics for privacy-preserving academic risk modeling across heterogeneous educational institutions", *Computers and Education: Artificial Intelligence* — <https://www.sciencedirect.com/science/article/pii/S2666920X26000913> (ScienceDirect blocked my fetch; details from the indexed abstract only, so treat as **unverified in detail**). It reports **"highly stable feature importance rankings (RankStab = 0.99–1.00)"** on OULAD under simulated institutional heterogeneity, and argues that "even when the global model converges predictively, local explanatory patterns may diverge due to differences in data distributions". A referee holding this paper will ask why a federated study reports RankStab ≈ 1.0 while this paper reports τ = 0.03 — the answer (theirs is one dataset partitioned into clients with a shared global model; τ here is across genuinely different institutions and *different* models) is a strong paragraph the manuscript is currently missing.
- **Explainer-vs-explainer disagreement**: Swamy, Du, Marras & Käser, "Trusting the Explainers", LAK 2023 — <https://dl.acm.org/doi/10.1145/3576050.3576147>; and the general formulation, Krishna et al., "The Disagreement Problem in Explainable Machine Learning: A Practitioner's Perspective" — <https://arxiv.org/abs/2202.01602>. These establish that importance rankings are unstable *within* a fixed setting across explanation methods. Without them, a referee can argue that τ = 0.03 is the disagreement problem re-labelled as a transfer result. The paper needs a same-model, same-cohort, different-seed/different-explainer floor to rule that out (see Domain Concerns).

---

## Citation Accuracy Audit

| # | Reference | Exists? | Characterised correctly? | Note |
|---|---|---|---|---|
| [1] | Kuzilek et al., OULAD, *Sci Data* 4:170171, 2017 | **Yes** — <https://www.nature.com/articles/sdata2017171> | Yes | Standard. Not independently re-checked beyond venue/DOI. |
| [2] | Tiukhova et al., "Open data, private learners", *Sci Data* 2026, doi 10.1038/s41597-026-06821-3 | **Yes** — <https://www.nature.com/articles/s41597-026-06821-3>; Zenodo mirror CC-BY 4.0 <https://zenodo.org/records/17087849> | Cannot fully verify | Nature redirected to an auth wall; **volume 13 / article 548, the Toledo platform, 6 course-years 2018–21, 3,951 students, the binary `PASSED` field, and "publishes no intermediate marks" are unverified against the source.** Verify before submission. |
| [3] | Raghavjee, Subramaniam & Govender, *Data* 11(1):1, 2026 | **Yes** — <https://www.mdpi.com/2306-5729/11/1/1>, doi 10.3390/data11010001 | Mostly | Search-indexed description says ~14,000 registered student records over **10** IS&T courses; the manuscript uses 16 course-years over 8 courses / 7,254 students after admission filtering, which is consistent with filtering but should be stated as such. MDPI blocked direct fetch, so the result-code vocabulary is **unverified** (see [MAJOR] D-3). |
| [4] | López de la Rosa et al., *Algorithms* 18(10):662, 2025 | Not verified | n/a | Not checked; used only as an example of the standard configuration. |
| [5] | Boujmiraz et al., *CAEAI* 10:100548, 2026 | **Probably** — a 2026 CAEAI review with this title exists at <https://www.sciencedirect.com/science/article/pii/S2666920X26000093> | Not verified | ScienceDirect 403'd. **The volume/article number/DOI could not be confirmed and the PII does not obviously correspond to article 100548.** Check. |
| [6] | Villegas-Ch et al., *Frontiers in Education* 10:1632315, 2025 | Not verified | n/a | Not checked. |
| [7] | López-Zambrano, Lara & Romero, *Appl. Sci.* 10(1):354, 2020 | **Yes** — abstract retrieved via S2 (doi 10.3390/app10010354) | **Yes** | Abstract confirms 24 university courses, decision trees, grouping by degree or similar activity-usage level. Accurate. |
| [8] | López-Zambrano, Lara & Romero, *JCHE* 34, 2022 | **Yes** — doi 10.1007/s12528-021-09273-3 | Yes in substance | Abstract confirms the ontology/taxonomy-of-actions portability improvement. **Bibliographic detail wrong or unverified: S2 records the year as 2021 (online first) and the manuscript's "pp. 1–19" looks like an online-first placeholder rather than the final *JCHE* 34 pagination.** Fix. |
| [9] | Gardner, Yu, Nguyen, Brooks & Kizilcec, FAccT 2023 | **Yes** — <https://arxiv.org/abs/2305.00927>, doi 10.1145/3593013.3594107 | **Yes, and unusually well** | Abstract verified verbatim: "a simple zero-shot cross-institutional transfer procedure can achieve similar performance to locally-trained models for all institutions in our study, without sacrificing model fairness", four universities, >200,000 students annually, no training-data sharing. The manuscript's summary at line 41 is exact. **Add the ACM DOI to the reference.** |
| [10] | Schwerter et al., arXiv:2604.22812, 2026 | **Yes** — <https://arxiv.org/abs/2604.22812> | **Yes** | Verified: three theoretical-CS courses at two universities; "performance and calibration declined between institutions with different base rates"; "Random Forest achieved the highest in-sample accuracy" while "Elastic Net generalized more robustly across contexts". The manuscript's characterisation at lines 21, 41 and 128 is accurate, including the careful qualification in §V-B. |
| [11] | Švábenský, Flanagan, López Zapata & Shimada, *ACM TKDD* 2026, doi 10.1145/3798096 | **Yes** — <https://dl.acm.org/doi/10.1145/3798096>, preprint <https://arxiv.org/abs/2602.17314> | **PARTLY — see [MAJOR] L-1** | Verified from the preprint: 1,125 LAK/EDM/AIED papers, **2020–2024 inclusive** (correct in the manuscript), 172 datasets in 204 publications, and the availability split **130 (75.6%) by direct download**, 24 after login, 18 on request — so "130 publicly available" is a fair reading. **But the census does not report the count of datasets carrying timestamped per-student activity + a course outcome + a join key.** The paper attributes "only four" to [11] twice (lines 23 and 198). Either it is the authors' own derivation from the supplementary material (<https://zenodo.org/records/18667402>), in which case say so and show the filter, or it is wrong. |
| [12] | Swamy, Marras & Käser, L@S 2022 | **Yes** — <https://arxiv.org/abs/2205.01064>, doi 10.1145/3491140.3528273 | Substantively yes; **number to check** | 26 courses and withheld data are correct (code at <https://github.com/epfl-ml4ed/meta-transfer-learning>). That repository describes "26 courses, **100k** students"; the manuscript says **145,714**. Reconcile. |
| [13] | Riestra-González, Paule-Ruíz & Ortin, *Computers & Education* 163:104108, 2021 | **Yes** — abstract verified via S2 (doi 10.1016/j.compedu.2020.104108) | Yes, but **incomplete** | Confirmed: one university, prediction at 10/25/33/50% of course delivery; the 532-course / 25,260-observation figure and the public GitHub release (<https://github.com/moisesriestra/moodle-early-performance-prediction>) are corroborated. **The manuscript never credits it for the relative-cutoff design it reuses** (see [MINOR] D-8), and the Apache-2.0 licence claim is unverified — check the repo LICENSE. |
| [14] | Phiri, Zenodo, doi 10.5281/zenodo.21292883, 2026 | **Yes** — <https://zenodo.org/doi/10.5281/zenodo.21292883> | Mostly | Verified: "A Multi-Source Dataset for CS1 Failure Prediction in a Sub-Saharan African Context", Lighton Phiri, University of Zambia, CC-BY 4.0, **284 students across four cohorts 2017/18–2020/21**, 17,870 LMS events, "20 weekly quizzes, four semester tests, and a final examination". The manuscript uses 3 cohorts / 183 students — consistent with the ≥50-student admission rule, but say so. **"Univ. of Zambia … export none [no intermediate marks]" (line 72) is contradicted by the record's own description of 20 weekly quizzes and four semester tests.** Fix that sentence. Author list "L. Phiri et al." — the record shows a single author. |
| [15] | Tiukhova et al., *DSS* 182:114229, 2024 | **Yes** — doi 10.1016/j.dss.2024.114229, <https://www.sciencedirect.com/science/article/abs/pii/S0167923624000629> | **Questionable** | Authors verified via S2: Tiukhova, Vemuri, **López Flores, Islind, Óskarsdóttir**, Poelmans, Baesens, Snoeck. Three of those are at Reykjavík University, which makes the manuscript's "cohorts of one KU Leuven programme" (line 43) likely wrong or at least unverified — the study appears to span more than one institution. I could not retrieve the abstract (S2 returned no abstract; ScienceDirect 403). **Verify the study's institutional scope before making a gap claim that depends on it being single-institution.** The substantive characterisation (SHAP importances shift across cohorts; stable factors are the actionable ones) matches the indexed description. |
| [16] | Friedman 2001 | Yes | Yes | — |
| [17] | Breiman 2001, "Random forests" | Yes | **Mis-attributed use** | Cited at line 96 for *permutation importance*. Breiman 2001 does introduce permutation importance for random forests, but the paper computes **model-agnostic permutation importance on held-out data**, whose standard citation is Fisher, Rudin & Dominici, "All Models are Wrong…" (JMLR 2019, <https://arxiv.org/abs/1801.01489>) — and, if the sklearn implementation is meant, that is what sklearn's docs point to. Add it. |
| [18] | Kapoor & Narayanan, *Patterns* 2023 | Yes | **Never cited in the body** | Reference [18] appears in the list but nowhere in the text. Either cite it (it belongs in §III/§IV where leakage-safety is asserted) or drop it. |

---

## Missing References

Ordered by how much damage their absence does.

1. **Angeioplastis, Konstantakis & Tsimpiris (2026), "Reliable or Just Accurate? A Cross-Dataset Audit of Early-Warning Models Under Course-Level Distribution Shift", *Computers* 15(9):572** — <https://www.mdpi.com/2073-431X/15/9/572>. *Why:* nearest prior work by a wide margin; three datasets including two of this paper's five, harmonised behavioural features, the same relative-cutoff grid, unseen-course validation, label-definition auditing, prevalence-sensitive metrics. Its absence makes the gap claim untenable and the design look less novel than it is. Cite, and state precisely what the ordered-pair ladder adds over grouped held-out validation.
2. **Yoneda, Švábenský, Li, Deguchi & Shimada (2025), "Ranking-Based At-Risk Student Prediction Using Federated Learning and Differential Features", EDM 2025** — <https://arxiv.org/html/2505.09287>. *Why:* falsifies the label-free-fix claim as written; also the natural comparator for the percentile transform (relative-value features vs rank features) and a ready-made "extends to five institutions" story.
3. **Jayaprakash, Moody, Lauría, Regan & Baron (2014), *JLA* 1(1):6–47** — <https://files.eric.ed.gov/fulltext/EJ1127037.pdf>. *Why:* the field's canonical cross-institutional early-alert portability study, at deployment scale. Its omission is the kind of thing a senior LA referee treats as disqualifying for a paper claiming the deployment question is open.
4. **Ocumpaugh, Baker, Gowda, Heffernan & Heffernan (2014), "Population validity for educational data mining models: A case study in affect detection", *BJET* 45(3):487–501** — <https://bera-journals.onlinelibrary.wiley.com/doi/10.1111/bjet.12156>. *Why:* the theoretical frame the paper is missing. "Population validity" is the established EDM term for exactly what the ladder measures; framing the contribution as population validity for early-warning models (rather than as generic ML "transfer") would make it legible to the LAK/EDM audience and would give the Introduction a construct-validity spine.
5. **Herodotou et al. (2019), "Empowering online teachers through predictive learning analytics", *BJET*** — <https://bera-journals.onlinelibrary.wiley.com/doi/abs/10.1111/bjet.12853>, plus the OU Analyse system page <https://research.stem.open.ac.uk/ouanalyse/>. *Why:* the paper asserts what "an institution that adopts an early-warning system" does (line 19) without a single citation to a system actually deployed at scale. OU Analyse is the obvious one — and it runs on the same institution as the paper's strongest dataset, which is a rhetorical asset.
6. **Arnold & Pistilli (2012), "Course Signals at Purdue", LAK '12** — <https://dl.acm.org/doi/10.1145/2330601.2330666>. *Why:* the other deployed-at-scale reference; also the standard cautionary tale about how deployment claims get evaluated. Together with (5) it converts "as if the system is a product" into a grounded premise.
7. **Baker & Hawn (2022), "Algorithmic Bias in Education", *IJAIED* 32:1052–1092** — <https://link.springer.com/article/10.1007/s40593-021-00285-9>. *Why:* the paper claims the keyword "trustworthy AI", cites Gardner et al. for a fairness result, and then reports no subgroup analysis at all. At minimum it must acknowledge that a representation change and a threshold change both have distributional consequences across student subgroups, and cite the review that says so.
8. **Krishna et al. (2022), "The Disagreement Problem in Explainable Machine Learning"** — <https://arxiv.org/abs/2202.01602>; and **Swamy, Du, Marras & Käser (2023), "Trusting the Explainers", LAK '23** — <https://dl.acm.org/doi/10.1145/3576050.3576147>. *Why:* explanation-ranking instability is a documented baseline phenomenon. Without these, the τ = 0.03 result has no floor and can be dismissed as re-measuring known explainer instability.
9. **Fisher, Rudin & Dominici (2019), "All Models are Wrong, but Many are Useful"** — <https://arxiv.org/abs/1801.01489>. *Why:* correct citation for model-agnostic permutation importance (currently attributed to Breiman 2001).
10. **Gardner, Brooks, Andres & Baker (2018/2019), MORF** — <https://arxiv.org/abs/1801.05236>. *Why:* the field's existing answer to "benchmarks of this kind are not reproducible" (line 23); the paper's open-data alternative should be argued against it, not around it.
11. **The 2026 CAEAI federated-XAI paper** — <https://www.sciencedirect.com/science/article/pii/S2666920X26000913> (verify details; I could not fetch it). *Why:* it reports near-perfect cross-client importance stability on OULAD, which superficially contradicts this paper's headline. Better to pre-empt it.
12. **Boyer & Veeramachaneni (2015), "Transfer Learning for Predictive Models in MOOCs", AIED** — <https://link.springer.com/chapter/10.1007/978-3-319-19773-9_6>. *Why:* the earliest systematic treatment of transfer across course offerings; makes the D1 rung look like a deliberate contact with prior work rather than an omission.

Optional but strengthening: work on prevalence/label shift and threshold selection under changing base rates. The general-ML anchor is Lipton, Wang & Smola's label-shift correction and its successors (e.g. <https://arxiv.org/pdf/1901.06852>); in education the concrete practice question is where a district or institution sets the flag cutoff given outcome prevalence and intervention capacity (see the IES REL descriptive study, <https://ies.ed.gov/rel-mid-atlantic/2025/01/descriptive-study-24>). If §VI is going to name per-cohort threshold calibration as "the natural next step", it should name the estimator family that does it.

---

## Domain Concerns

### [CRITICAL] D-1. F1 is measured on the pass class, but the paper reads it as an alerting rule

`f1_score(y, (p >= 0.5).astype(int))` at `services/ml/src/experiments/transfer_benchmark.py:162` uses scikit-learn's default `pos_label=1`, and `y` is `passed` in every adapter (`oulad_adapter.py:1321`, `ukzn_adapter.py:89`, `zambia_adapter.py`, `oviedo_adapter.py` `PASS_FRACTION`). So the reported F1 is the F1 of predicting **pass** — the class no early-warning system alerts on.

Consequences:

- Line 19 ("the threshold that turns a score into an alert"), line 92 ("what that shift does to a deployed alerting rule"), line 132 ("This is the failure a deployed early-warning system actually experiences") and the abstract are all describing a majority-class F1 as if it were an alerting metric. It is not.
- The F1 collapse 0.809 → 0.507 is substantially mechanical. Positive-class F1 is a monotone-ish function of positive prevalence at a fixed operating point; with cohort pass rates spanning 0.21–0.95, a large drop is expected even from a model with unchanged ranking behaviour. The paper says as much ("a score calibrated to one prevalence is meaningless at another") without noticing that this makes its headline metric partly a restatement of the prevalence spread rather than a measurement of model failure.
- Symmetrically, "the percentile representation recovers 44–47% of the lost F1, uniformly across model families" is at risk of being a statement about how the transform shifts the *score distribution* relative to 0.5, not about at-risk identification.

**Required fix.** Report the operational metrics an early-warning deployment actually uses, at minimum: precision/recall/F1 **on the at-risk (fail) class**, and a **fixed flag-rate** metric (precision and recall in the top-*k*% of risk scores, *k* set by intervention capacity — 10% and 20% are the usual choices), which is base-rate-robust and is what OU Analyse, Course Signals and OAAI-style systems are evaluated on. Add a prevalence-matched null (what does a random or prior-only scorer achieve at each rung?) so the reader can see how much of the collapse is model failure and how much is arithmetic. If the fail-class numbers tell the same story, the paper is stronger; if they do not, finding #3 in the contribution list has to be rewritten.

### [CRITICAL] D-2. Repeat registrations are collapsed with `max()`, which changes the construct

`ukzn_adapter.py:97` — `groupby(["student_id","subj","year"]).max()` — and `zambia_adapter.py` — `groupby("student_id").max()`, comment "Repeat sitters appear more than once; keep the best outcome, as for UKZN".

For UKZN the grouping includes `year`, so the collapse is within a cohort (multiple result rows for one registration); acceptable, but it should be documented and the multiplicity reported. **For Zambia the grouping is by `student_id` alone**, with no course-year key — if the exam file spans the four cohorts, a student who failed in 2018/19 and passed on re-registration in 2019/20 is labelled `passed = 1` in *both* cohorts. That silently converts the outcome from "fails this course this year" to "ever passes this course", which is a different educational construct, weakens the link to the current cohort's clickstream, and would inflate the pass rate. Zambia's D0 AUC of 0.521 — chance — is exactly what this defect would produce. Please verify the cohort keying of the Zambia label join and report it.

More generally: whether a supplementary/re-sit outcome counts as pass is a substantive pedagogical decision, not a data-cleaning detail, and it differs by institution. State the rule per institution in §III-A.

### [MAJOR] D-3. UKZN `startswith("P")` almost certainly folds conceded and supplementary passes into "pass"

`ukzn_adapter.py:89` maps any final result code beginning with "P" to 1. South African result vocabularies routinely include **PC / PCON (pass conceded)**, **PS (pass supplementary)** and similar codes alongside plain **P**. A conceded pass is a student who did not meet the pass standard and was passed by rule; a supplementary pass is a student who failed the main assessment. Both are students an early-warning system exists to flag. The docstring asserts "Fail / supplementary-fail / deregistered → 0" but the code does not enumerate anything — it pattern-matches a single letter, so any future or unlisted P-prefixed code is a pass by default. UKZN's pass rates (0.60–0.95, the highest in the benchmark) and its middling D0 AUC (0.667) are both consistent with a label that has absorbed marginal students into the pass class.

**Fix:** enumerate the observed result-code vocabulary in the paper (a small table), state the mapping code by code, and run the ladder once with conceded/supplementary passes recoded to 0 as a sensitivity check — the same treatment the paper gives to OULAD withdrawal.

### [MAJOR] D-4. Oviedo's label is partly produced by the same interactions the features count

`oviedo_adapter.py` takes the Moodle gradebook **course-total** item and thresholds it at 50% of `grademax`. In a Moodle installation the course total is an aggregate of the gradebook's constituent items, many of which are graded **online activities** — quizzes, assignments submitted through Moodle, workshop items. The seven features count clicks on those same components. This is criterion contamination: part of the label is mechanically generated by the behaviour being used to predict it, and the strength of the relationship varies by how much of a course's assessment is Moodle-hosted. Oviedo's D0 range (0.384–0.953) is the widest in the benchmark and is consistent with a per-course mix of contaminated and uncontaminated labels.

A learning-analytics referee will also make the more basic objection: an **unconfigured or partially configured** gradebook total is not a course outcome. Many instructors never curate the course total; it then reflects whatever items happen to exist. Angeioplastis et al. found precisely this ("substantial inconsistencies between configured and observed course maxima") on their institutional Moodle and audited it explicitly. This paper's only mitigation is the zero-grade control (9.9% at exactly zero).

**Fix:** report, per retained Oviedo course, the number and type of graded items composing the course total and the share that are Moodle-hosted activities; exclude courses whose total is dominated by online-graded items, or at minimum show the ladder with and without them. Say explicitly that Oviedo's label is an LMS-derived proxy for a registrar outcome, in §III-A and not only in the Limitations.

### [MAJOR] D-5. D3 confounds "another institution" with "another teaching modality"

The Open University is a fully **distance** institution: essentially all study activity passes through the VLE, and withdrawal is visible in the clickstream. Oviedo, UKZN and Zambia are **contact** institutions where Moodle is a supplementary resource repository, so clicks measure file-downloading behaviour and capture a small, course-dependent share of study effort. KU Leuven's Toledo is blended. The manuscript's most interesting descriptive result — D0 AUC 0.845 at OULAD vs 0.606 / 0.521 at Oviedo / Zambia — is at least as plausibly a *modality* effect as an *institution* effect, and the D3 rung mixes the two irreversibly (most cross-institution pairs involve OULAD on one side).

This matters for the paper's own thesis. Section V-D argues that "loss tracks how far apart two cohorts are, and 'another institution' is simply the largest gap this benchmark contains" — good instinct, but the shift measures used (prevalence, click scale, distribution shape) do not capture *LMS centrality*, which is the construct actually varying. A referee will say the benchmark measures transfer across **modes of instruction**, and that five institutions is really "one distance provider plus four contact providers".

**Fix:** name the confound in §III-A, tabulate modality per institution, and either (a) add a distance/contact indicator to the shift regression, or (b) report the D3 ladder with OULAD held out as a source, so the reader can see cross-institution loss among the contact institutions alone. Option (b) is one line of aggregation over results you already have.

### [MAJOR] D-6. Pooling five outcome constructs into one "course outcome" is under-defended

Beyond the individual issues above, the five labels are five different constructs measured on five different scales:

| Institution | Construct | Standard-setting authority |
|---|---|---|
| OULAD | Module-presentation final result, withdrawal folded into fail | Registrar |
| Oviedo | Moodle gradebook course total ≥ 50% | The instructor's gradebook configuration |
| UKZN | Subject result code beginning "P" | Registrar, including conceded/supplementary rules |
| KU Leuven | Binary `PASSED` (Belgian 20-point scale, pass at 10) | Examination board, with deliberation |
| Zambia | **Final examination mark ≥ 50** | A single terminal assessment, ignoring coursework |

Zambia's is the outlier: it is not a course outcome at all but a single-exam outcome, and the dataset itself carries 20 weekly quizzes and four semester tests that a course grade would incorporate. Belgian deliberation practice (an examination board can pass a student below threshold on the balance of a year) makes KU Leuven's `PASSED` a partly *social* decision rather than a score threshold, which is a known reason for weak clickstream signal — and KU Leuven's D0 AUC is 0.611. The manuscript's Limitations paragraph names the heterogeneity but treats it as noise absorbed into the cross-institution numbers. It is not noise: it is systematically correlated with which institution is the target, and therefore with the D3 estimates.

**How a learning-analytics referee will attack it:** "You have not shown that your outcome variable measures the same thing in five places, so your cross-institution degradation is at least partly a measurement-invariance failure in the *label*, not a portability failure in the *model*." That is a serious charge because it has a cheap partial answer the paper has not run: **a same-institution label-variant control**. On OULAD you can construct several label variants (registrar result; result excluding withdrawals — already done; a continuous-assessment threshold analogous to Oviedo's) and show how much D0/D2 moves under label re-definition alone. If label re-definition moves AUC by an amount comparable to the D3 gap, the paper must say so; if it does not, the pooling defence is largely made.

### [MINOR] D-7. No floor for the explanation-agreement result

τ = 0.03 over seven features is reported against an implicit "random rankings" baseline mentioned only for J@3. Two floors are needed and both are cheap: (i) **same cohort, same model family, different seed / different data subsample** — how much do two locally trained models agree with each other? (ii) **same model, different explanation method** (permutation vs a gain-based or SHAP ranking) on the same cohort. `n_repeats = 3` with subsampling to 1,500 students is a thin estimate; the paper asserts stability ("a ranking over seven features is a rank statistic and is stable well below that size") without showing it. One bootstrap over repeats would settle it. Without floors, the strongest result in the paper is the one most exposed.

### [MINOR] D-8. Prior art on the relative cutoff is uncredited

Section III-D presents the relative cutoff (⌈⅓ × course length⌉, with ¼ and ½ sensitivity) as a design decision of this paper. Riestra-González et al. [13] — one of the five source datasets — predicts at 10%, 25%, 33% and 50% of course delivery, and Angeioplastis et al. (2026) reuse exactly that grid. Credit it; it costs nothing and removes an easy criticism.

### [MINOR] D-9. Feature-availability claim contradicts a source dataset

Line 72: "UKZN and Zambia export none [no intermediate marks]". The Zambia Zenodo record explicitly lists "20 weekly quizzes, four semester tests, and a final examination". Even if those marks are not usable at the cutoff week, the sentence as written is false and undermines the "any LMS can supply it" argument. Restate as "not used", with the reason.

### [MINOR] D-10. Naming a privacy defect in someone else's published dataset

Line 68 states that the Zambia release ships a column of real personal names beside its hashed identifier. If true, that is a live re-identification risk in a CC-BY dataset, and publishing the observation in a paper is a disclosure decision, not a methods note. The correct sequence is: notify the depositor and Zenodo first, then describe it in the paper (ideally as "the release contained a directly identifying column at the time of access; this was reported to the depositor"). Ethically the paper's own handling (never reading the column) is right; the reporting is not. A reviewer with an ethics remit will raise this, and some venues will require an ethics statement. Relatedly, the paper has **no data-ethics / IRB / licence-compliance statement at all**, which for a five-dataset assembly at a track that cares about trustworthy AI is a gap.

### [MINOR] D-11. No fairness or subgroup analysis, while claiming trustworthy AI

Gardner et al. [9] is cited for the finding that transfer does not harm fairness. This paper changes the representation *and* implicitly the operating point, and reports nothing about subgroup effects. OULAD carries the usual demographics (IMD band, disability, age band, prior education); UKZN's dataset carries demographics too. One subgroup table on OULAD — does the percentile transform preserve, improve or degrade the gap in at-risk recall across IMD bands? — would let the paper keep "trustworthy AI" as a keyword honestly. Without it, delete the keyword.

### [MINOR] D-12. Explanation results exist for one model family only

Table IV has empty rows for logistic regression and random forest. §IV-F discloses this as a compute setting, which is honest, but the Conclusion generalises ("costs essentially all of the agreement between its explanation and the one a local model would give") to models the paper did not measure. Either narrow the wording or fill the rows for at least one representation — logistic-regression coefficients are free to rank.

---

## Contribution Assessment

Blunt reading: **a useful benchmark paper with one genuinely new measurement, currently packaged around a headline that the code does not support.**

What is solidly new:

1. **Explanation portability after transfer.** Nobody has measured agreement between a transferred model's importance ranking and a local model's ranking, in education or nearby. It is the right question, it has a clean practical consequence ("safe to rank with, unsafe to explain with"), and it is the only one of the three headline findings that survived my falsification attempts intact. It is also, at present, the *third* thing the paper talks about.
2. **The five-institution assembly itself.** Five adapters over five platforms in four countries, with an admission rule and frozen results, is real infrastructure and is worth releasing regardless of the analysis. It is larger than Angeioplastis et al.'s three and does something they do not (ordered source→target pairs).
3. **The D0 spread across institutions** (0.845 → 0.521) is a quietly powerful result — it says a single-dataset AUC describes a context, not a method — and it is the one finding no single-dataset study can produce. The paper states it and moves on.

What is not new, or not yet established:

- **The transfer-degrades finding** replicates López-Zambrano 2020/2022, Gardner et al. 2023, Schwerter et al. 2026 and Angeioplastis et al. 2026. Scale and public data are the increments, not the direction.
- **The label-free representation fix** exists in the literature in adjacent form (differential features, EDM 2025; normalised event-percentage variables in the Riestra release; the ontology fix in [8]). Percentile-within-cohort is a clean, simple instance and the mechanism regression is a nice touch, but "one line of preprocessing" is being sold harder than a 0.021 AUC gain for the primary model supports.
- **The threshold-failure finding** is, as measured, partly an artefact (D-1). Until fail-class and fixed-flag-rate numbers appear, this cannot be counted as a contribution at all.

So: not a repackaging — there is new measurement and new infrastructure here — but not yet the three-findings paper the abstract claims. It is one strong finding (explanations), one solid descriptive finding (cross-institution D0 spread), one replication at larger scale (discrimination), and one finding that needs re-measuring (thresholds). For a 4–6 page double-blind track that is still a respectable submission, **if** it is honest about which is which.

The strategic advice, offered as a referee who would like to see this in the programme: lead with explanations. "Predictions transfer, explanations do not" is a sharper and more defensible claim than "three properties degrade at three rates", it is the part no one has done, and it does not depend on the metric that is currently broken.

---

## Recommendation

**Major revision.**

Not reject: the data assembly is genuine, the explanation-portability measurement is novel after a serious attempt to falsify it, and the two most damaging problems (the F1 class, the gap over-claim) are both fixable without new experiments — the fail-class and top-*k* metrics come from predictions already computed, and the literature repair is writing.

Not minor revision: the paper's second headline finding is currently measured on the wrong class and framed as a deployment result; two of the three gap claims are refutable from a first-page search; and three label constructions (Zambia cohort keying, UKZN P-prefix, Oviedo gradebook composition) need documented sensitivity checks before an education audience will accept the pooled outcome variable.

Conditions I would set for acceptance:

1. Re-report all threshold results on the at-risk class **and** at a fixed flag rate, with a prevalence-only null. Rewrite §V-C, the abstract and contribution #3 around whatever those show. **(D-1, blocking)**
2. Cite and distinguish Angeioplastis et al. (2026) and Yoneda/Švábenský et al. (2025); rewrite the Section II gap sentence and the abstract so no claim is broader than what those two allow. Add OAAI and Ocumpaugh et al. for framing. **(Gap claims a and b, blocking)**
3. Verify the Zambia label's cohort keying; enumerate the UKZN result-code vocabulary and run a conceded/supplementary sensitivity check; characterise the composition of Oviedo course totals. Move the label constructions out of Limitations and into §III with a per-institution table. **(D-2, D-3, D-4, blocking)**
4. Name the distance-vs-contact confound and report D3 with OULAD excluded as a source. **(D-5)**
5. Fix the [11] attribution ("only four datasets"), the [15] institutional scope, the [17] permutation-importance citation, the [14] intermediate-marks contradiction, and the orphan [18]; check the [12] student count and the [8] pagination. **(Citation audit)**
6. Add an ethics/data-licence statement, and either add a subgroup analysis or drop "trustworthy AI" from the keywords. **(D-10, D-11)**

If (1)–(3) come back and the fail-class picture holds up, this is a paper I would argue to accept.

---

### Verification notes and limits

- Full text was retrieved for: arXiv 2305.00927 (Gardner), arXiv 2604.22812 (Schwerter), arXiv 2602.17314v1 (Švábenský census), arXiv 2505.09287 (Yoneda), Zenodo 21292883 (Phiri). Abstracts via the Semantic Scholar API for: 10.3390/computers15090572, 10.1016/j.compedu.2020.104108, 10.3390/app10010354, 10.1007/s12528-021-09273-3, 10.1016/j.dss.2024.114229 (metadata only — S2 returned no abstract).
- **Blocked and therefore unverified beyond indexed metadata:** ScienceDirect (DSS 2024 [15], CAEAI [5], the CAEAI federated-XAI paper), MDPI article pages (UKZN [3], Angeioplastis 2026 — abstract obtained via S2 instead), Nature (KU Leuven [2] — auth wall), the ACM full-text of Gardner et al. and of Swamy et al. I have flagged every claim resting only on a search-engine snippet as unverified rather than treating it as confirmed.
- References [4] and [6] were not checked at all; they are used only as examples of a genre and I did not consider them load-bearing.
- Label-construction claims were checked against the repository code, not against the raw datasets: `services/ml/src/benchmarks/{oulad,ukzn,oviedo,zambia}_adapter.py` and `services/ml/src/experiments/transfer_benchmark.py`. I did not run anything.
