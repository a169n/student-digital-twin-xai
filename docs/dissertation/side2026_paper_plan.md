# SIDe 2026 paper — research plan v2 (transfer ladder)

**Date:** 2026-09-03 (v2, supersedes the v1 "explanation stability + bagging" plan of the same day)
**Deadline:** 2026-09-10  **Venue:** SIDe 2026, Astana, Track 1 *Computational Intelligence* (AI/ML, Explainable & Trustworthy AI), IEEE route, 4–6 pages, double-blind.
**Status:** experiment code written (`services/ml/src/experiments/transfer_benchmark.py`, `run_transfer_ladder.py`, `services/ml/src/benchmarks/ukzn_adapter.py`); first full run in progress. Numbers marked *[to measure]* are unknown until `exp_014` finishes.

---

## 0. Why v1 was replaced

The user's objection to v1 ("it feels like we did nothing and got a mediocre result") is correct: measuring explanation instability and fixing it with bagging is a methods note, and bagging feature importance is well known. v2 keeps the build → break → fix arc but makes every step substantive:

- **build** a portable early-warning model from engagement signals every LMS records;
- **break** it by moving it across cohorts, courses and institutions (a real deployment question);
- **fix** it with a cohort-relative feature representation that needs no target labels, then quantify how many labelled target students close the remaining gap.

The dataset scope is what makes the paper feel like work was done: **three institutions, three LMS platforms, ~45 real cohorts, all public** — versus one or two cohorts in the earlier paper.

---

## 1. Venue constraints (verified on side.nu.edu.kz, 2026-09-03)

4–6 pages including references, IEEE two-column template, English, **double-blind** (no names, ORCID, affiliations, or GitHub handle; repo via anonymous.4open.science), submission on CMT `SIDE2026`, ≤ 6 authors. Track 1 lists "Explainable AI, fairness, bias mitigation" and "Trustworthy & Responsible AI". Notification 09-20, camera-ready 10-05. Route: IEEE.

---

## 2. The paper in one sentence

> Early-warning student-risk models trained on one course rarely survive transfer to another course or institution; on 45 cohorts from three universities and three LMS platforms we show that a label-free, cohort-relative representation of engagement makes the same model portable, and that the surviving gap closes with a few dozen labelled students.

**Working title:** *Portable Early-Warning Models Across Institutions: A Cohort-Relative Representation for Explainable Student-Risk Prediction*

### Contributions (each maps to one table/figure)

| # | Contribution | Evidence |
|---|---|---|
| C1 | A public, three-institution transfer benchmark for early-warning models: OULAD (12 module-presentations, OU VLE), KU Leuven (2 courses, 2026 dataset), UKZN (Moodle logs, ~30 course-years 2018–2021). One canonical engagement schema (7 features) and a relative-time cutoff (⅓ of each course) | Table I, Fig. 1 |
| C2 | A **transfer-distance ladder** D0 within cohort → D1 same course other year → D2 other course same institution → D3 other institution, plus two pooled sources (leave-one-cohort-out within institution; all other institutions) | Table II, Fig. 2 |
| C3 | Finding: raw-feature transfer degrades monotonically with distance *[to measure]*; the most portable signals are recency and regularity, not volume *[to measure]* | Table II, Table IV |
| C4 | Fix: **cohort-relative representation** (within-cohort percentile or z-score at the cutoff week, no labels) recovers most cross-institution AUC *[to measure]*; **few-shot** addition of k ∈ {25, 50, 100} labelled target students closes the rest *[to measure]* | Table III, Fig. 3 |
| C5 | Explanation portability: permutation-importance rankings of the transferred model vs the locally trained model (Kendall τ, top-3 Jaccard) by distance and representation; the caveat text the teacher panel shows is derived from these numbers | Table IV |

---

## 3. Research questions and pre-registered decision rules

**RQ1.** How well does a fixed Gradient Boosting model on seven engagement features predict `passed` at ⅓ of the course within each cohort (D0)? Expected AUC OULAD 0.85–0.92, KU Leuven 0.65–0.73 (exp_011/012), UKZN unknown.

**RQ2.** How much AUC is lost at each ladder step with raw features? Success criterion for the *break* step: mean D3 AUC at least 0.05 below D0 with raw features.

**RQ3.** Does the cohort-relative representation recover it? Pre-registered rule: **success** if percentile or z-score raises mean D3 AUC by ≥ 0.05 over raw (bootstrap-over-pairs CI excluding zero) with no D0 loss; **partial** if the gain is 0.02–0.05; **null** otherwise — then the paper's headline becomes the benchmark + the few-shot curve.

**RQ4.** How many labelled target students close the remaining gap? Report AUC vs k with 5 seeds.

**RQ5.** Do explanations transfer? τ between transferred and local rankings by distance/representation.

Every branch is publishable because C1–C2 (the benchmark) stand alone.

---

## 4. Method

### 4.1 Data (all public, CC-BY 4.0)
| Institution | LMS | Cohorts | Students / cohort | Label | Calendar |
|---|---|---|---|---|---|
| Open University (OULAD, Kuzilek 2017) | OU VLE | BBB, DDD, FFF × 2013B/2013J/2014B/2014J = 12 | 1,228–2,365 | Pass/Distinction = 1; Fail/Withdrawn = 0 | presentation length in `courses.csv` |
| KU Leuven (Tiukhova et al. 2026) | Toledo | 2 courses, 2018–19 | ≈ 750 each | PASSED | `course_info.json` semester weeks |
| UKZN (Raghavjee et al. 2026, Zenodo 14810607) | Moodle | 8–9 IS&T modules × 2018–2021 ≈ 30 with n ≥ 50 | 50–1,100 | final result code starts with P = 1; F*/DE = 0 | inferred: first–last calendar week with ≥ 10 % of enrolled students active |

UKZN enrollment = students in the marks file **and** in the Moodle log (avoids labelling students from a campus whose site is not exported). Stated as a design decision.

### 4.2 Canonical engagement schema (derived identically for all three)
Per week: clicks, active days, content clicks, social clicks (forum). Derived, leakage-safe: `cum_clicks`, `cum_active_days`, `cum_content_clicks`, `cum_social`, `cur_clicks`, `active_weeks`, `weeks_since_active`. No assessment or demographic features (not available at KU Leuven; keeps the schema portable).

### 4.3 Task
Binary `passed`, one row per student at week = round(⅓ × course length). Sensitivity at ¼ and ½.

### 4.4 Representations (all unsupervised, computed within the *target* cohort)
`raw`; `zscore` (within-cohort standardisation); `percentile` (within-cohort rank). For a tree model, `percentile` equals `raw` within a cohort (monotone), so any D0 difference is a sanity check, and any cross-cohort gain is attributable to the representation alone.

### 4.5 Models
Fixed Gradient Boosting (200 trees, depth 3, lr 0.05) as the object of study; Logistic Regression as the linear reference (Schwerter et al. 2026 report linear models transfer better). Models are fitted once per source cohort and applied to every target.

### 4.6 Evaluation
ROC-AUC (threshold-free, primary), F1 at 0.5 (to show the calibration/prevalence problem). D0 = 5-fold stratified CV within cohort. Aggregates per (distance, representation, model) with a 1,000-resample bootstrap over pairs. Few-shot: other-institution pooled source + k labelled target students, evaluated on the remaining target students, 5 seeds.

### 4.7 Explanation portability
Permutation importance (5 repeats, AUC scoring) of the transferred model on the target vs the target's own model; Kendall τ and top-3 Jaccard per pair.

---

## 5. Experiment inventory

| ID | What | Code | Outputs |
|---|---|---|---|
| exp_014_transfer_ladder | 45 cohorts, all ordered pairs × 3 representations × 2 models; pooled sources; few-shot; explanation τ | `run_transfer_ladder.py` → `transfer_benchmark.py`; adapters `oulad_adapter`, `ku_leuven_adapter`, **`ukzn_adapter` (new)** | `data/artifacts/experiments/exp_014_transfer_ladder/f33/{cohorts,pairs,aggregate,pooled,fewshot}.csv`, `run_metadata.json` |
| exp_014 sensitivity | same at fractions 0.25 and 0.50 | `--fraction` | `f25/`, `f50/` |

Caches (not in git): `datasets/cache/*.parquet` (OULAD, KU), `datasets/ukzn/cache/*.parquet`.

---

## 6. Paper skeleton (IEEE, 6 pages, ~3,300 words)

| § | Section | Content |
|---|---|---|
| — | Abstract | 45 cohorts, 3 institutions, 3 LMS; ladder; raw drop; relative fix; few-shot; τ |
| I | Introduction | early-warning models are built per course and never leave it; portability is the deployment question; C1–C5 |
| II | Related work | (a) OULAD prediction + SHAP is standard [López de la Rosa 2025; Boujmiraz 2026]; (b) **portability**: López-Zambrano, Lara & Romero 2020 (24 Moodle courses, one university, decision trees, portability only between similar courses) and 2021 (ontology of actions improves it); Gardner et al. FAccT 2023 (4 US universities, private data, zero-shot ≈ local); Schwerter et al. 2026 (3 courses, 2 universities, degradation, linear models transfer better); Swamy, Marras & Käser L@S 2022 (meta-transfer across 26 MOOCs); (c) explanation stability: Tiukhova et al. DSS 2024. Gap: no public multi-institution, multi-LMS benchmark; no label-free representation fix tested; explanations never checked after transfer |
| III | Data and canonical schema | Table I cohorts; schema; cutoff; UKZN calendar rule; leakage control |
| IV | Method | ladder definition, representations, models, few-shot, metrics |
| V | Results | A. within-cohort baseline; B. ladder raw vs relative (Table II, Fig. 2 heat/strip plot); C. pooled sources + few-shot curve (Table III, Fig. 3); D. explanation portability (Table IV); E. what transfers: feature ranking across institutions |
| VI | Discussion & limitations | why relative works (platform-specific click scales, prevalence shift); linear vs GBM; UKZN inferred calendar; label semantics differ (Withdrawn); no demographics; correlational |
| VII | Conclusion | |

Figures: Fig. 1 three-institution schema + ladder; Fig. 2 AUC by distance × representation; Fig. 3 few-shot curves per target institution. Tables I–IV.

---

## 7. Schedule

| Day | Deliverable |
|---|---|
| Sep 3 (done) | UKZN adapter, canonical schema, ladder code, unit test, caches, first run started |
| Sep 4 | Full run f=0.33; inspect; fix pathologies (tiny cohorts, degenerate labels); sensitivity f=0.25/0.50; exp_014 doc + registry row |
| Sep 5 | Figures 1–3, Tables I–IV; paper draft §I–IV |
| Sep 6 | §V–VII; references DOI-verified; anonymised repo snapshot |
| Sep 7 | Simulated review (ARS reviewer); revise |
| Sep 8 | Supervisor read; IEEE .docx; page fit |
| Sep 9 | Buffer / polish |
| Sep 10 | Submit on CMT |

---

## 8. Novelty statement (honest)

First public benchmark of early-warning model transfer across **three institutions and three LMS platforms** (~45 cohorts) with a shared, label-free engagement schema and relative-time cutoff; first test of a within-cohort relative representation as a portability fix in learning analytics; first measurement of explanation portability after transfer. Not claimed: new algorithm, accuracy record, causal factors.

## 9. Risks

| Risk | Fallback |
|---|---|
| Relative representation does not help at D3 | Headline = benchmark + few-shot curve; the null is itself informative against Gardner 2023 |
| UKZN inferred calendar is noisy | Report sensitivity to the 10 % threshold; drop cohorts whose span < 8 weeks |
| Over 6 pages | Drop LR columns, then sensitivity fractions |
| Reviewer: labels differ across institutions | Say so; AUC is rank-based; prevalence shift is exactly why raw thresholds fail |

## 10. Out of the paper (dissertation only)
Architecture, Digital-Twin ablation, synthetic circularity, regression target, what-if panel.


---

## 11. Dataset expansion and two adapter bugs (2026-09-05)

### 11.1 Why the scope grew
Reviewer-facing weakness of the v2 design: the D3 claim rests on ordered
*institution* pairs, and three institutions give only six. Two cheap expansions
and a search for a fourth institution were carried out.

### 11.2 KU Leuven: 2 cohorts -> 6 (two bugs found and fixed)
The Zenodo record 17087849 ships **three** academic years (1819, 1920, 2021);
only 1819 had been downloaded and used.

**Bug 1 — hardcoded year.** `ku_leuven_adapter` had module constants
`LOG_FILE = "1819_log_activity.csv"` etc.; the `year` argument only selected the
calendar. Building "1920" or "2021" silently re-processed 1819 data. Caught
because all three years returned byte-identical counts (20,973 rows / 1,495
students / pass rate 0.633). Fixed with `_year_files(year)`; `year="1819"`
reproduces the original filenames, so exp_011 output is unchanged.

**Bug 2 — parallel sections dropped.** In 2020-21 the dataset splits
"Global economics" into "Global economics 1" (341 students) and
"Global economics 2" (335, zero student overlap, i.e. parallel sections), while
`course_info.json` still carries one calendar under the base name. Both sections
were silently dropped. Fixed with `_expand_calendar_aliases`, which attaches a
course name to the longest calendar key that is a prefix of it. Covered by
`test_expand_calendar_aliases_maps_parallel_sections_to_base_course`.

Result: KU Leuven now contributes 6 cohorts / 3,951 students, gains its own D1
(same course, other year) pairs, and spans the shift to online teaching. Its
base rate moves substantially across years (Global economics: 0.563 -> 0.755 ->
0.616 / 0.513), which is a within-institution prevalence shift worth reporting.

### 11.3 OULAD: 12 cohorts -> 19
All 22 module-presentations are now cached (modules AAA, BBB, CCC, DDD, EEE,
FFF, GGG); 19 pass the >= 50 students / >= 15 minority-class filter. This mainly
strengthens D2 (other course, same institution).

### 11.4 Search for a fourth institution: rejected, with reasons
| Candidate | Why rejected |
|---|---|
| Middle East College, Oman (Zenodo 5591907) | Moodle logs have `User full name` blanked to "-"; outcomes are keyed by "Student N" roll numbers. No key links activity rows to outcomes. Also ~33 students per module-term. |
| Univ. of Genoa, EPM (UCI 346) | Logs are joinable by numeric student id, but `final_grades.xlsx` covers only **52** students, i.e. one cohort far too small for a stable AUC. |
| Zenodo 14003233 "Streaming Learning Analytics" | Derivative of OULAD, not an independent institution. |

This scarcity is itself reportable: public datasets that link per-student
timestamped LMS activity to a course outcome are rare, which is precisely why a
three-institution benchmark is a contribution. State it in Limitations rather
than hiding the institution count.

### 11.5 Current benchmark size
| Institution | Cohorts | Modules | Students | Mean pass rate |
|---|---|---|---|---|
| OULAD | 19 | 6 | 30,059 | 0.487 |
| UKZN | 16 | 8 | 7,254 | 0.822 |
| KU Leuven | 6 | 2 | 3,951 | 0.652 |
| **Total** | **41** | **16** | **41,264** | |

Ordered pairs: D0 41, D1 76, D2 536, D3 1,028 (was 496).

### 11.6 Runtime note
Permutation importance runs once per ordered pair, so it dominates an
O(cohorts^2) ladder. For the ranking only, `n_repeats` is 3 and targets are
label-stratified subsampled to 1,500 rows (`IMPORTANCE_REPEATS`,
`IMPORTANCE_MAX_ROWS`). All reported AUC / F1 still use the full target cohort.
Disclose this in the Method section.

### 11.7 Results already in hand (30-cohort run, to be refreshed at 41)
- Ladder degrades: paired per-target, GBM raw 0.756 (D0) -> 0.648 (D3); LR raw 0.785 -> 0.641.
- Fixed threshold breaks: F1 at 0.5 falls from ~0.82 (D0) to 0.52 (D3 raw), recovering to 0.65 under the percentile representation.
- Relative representation: LR z-score +0.098 AUC at D3 (pre-registered success); GBM percentile +0.024 (partial). Gains are heterogeneous by target institution.
- Few-shot k <= 100 does not close the gap for KU Leuven or UKZN targets.
- **Explanations do not transfer**: Kendall tau ~ 0 at D3, top-3 Jaccard ~0.28, and the representation fix does not repair it. This is the strongest and most novel claim; promote it to the headline.
- **exp_015 feature-richness control (OULAD, GBM)** refutes "your features are too crude":

| Feature set | n | D0 | D2 | drop |
|---|---|---|---|---|
| Shared 7 | 7 | 0.858 | 0.836 | 0.022 |
| Rich engagement | 11 | 0.861 | 0.821 | 0.040 |
| + assessment scores | 17 | 0.902 | 0.881 | 0.021 |

Richness raises accuracy but not transferability.
- **Withdrawal-tautology control**: excluding OULAD "Withdrawn" students (32% of the sample) lowers within-cohort AUC from 0.858 to 0.793. The signal survives; report as a robustness section.

### 11.8 Revised headline
Not "a relative representation fixes transfer". Rather: *predictions transfer
partially and can be partly repaired for free; explanations do not transfer at
all and are not repaired by the same fix.* This is a trust/deployment claim, it
needs multiple institutions to make, and it fits Track 1 directly.


---

## 12. Systematic dataset search, round 2 (2026-09-05)

Round 1 was a shallow search; on request it was redone with three parallel
agents (~250 verified checks, every verdict confirmed by downloading files or
fetching a repository listing, never from an abstract).

### 12.1 The scarcity is now a citable fact, not an apology
Svabensky, Flanagan, Lopez Zapata & Shimada (2026), "Open Datasets in Learning
Analytics: Trends, Challenges, and Best Practice", *ACM TKDD*,
doi 10.1145/3798096 (arXiv 2602.17314), hand-coded **1,125 LAK + EDM + AIED
papers (2020-2024)** and extracted **172 datasets**, 143 of them absent from
every prior survey; the annotated inventory is public (Zenodo 18667402, CC-BY).
**Of its 130 publicly available datasets, exactly four satisfy timestamped
activity + course outcome + a join key** — OULAD, HarvardX/MITx, Canvas Network
and XuetangX. Cite this in Limitations: the benchmark spans nearly the whole
population of suitable public data, rather than a convenience sample of three.

A second citable point from the same sweep: the largest cross-course pass/fail
studies publish **code but not data** (EPFL, 26 MOOCs / 145,714 students, L@S
2022; the EDM 2021 flipped-classroom set). The benchmarks exist and are not
reproducible, which is exactly the gap a public transfer ladder fills.

### 12.2 Added: institution 4 — University of Zambia
Phiri, L. et al. (2026), Zenodo 10.5281/zenodo.21292883, CC-BY 4.0. Moodle
standard log (87,429 events) + `FinalExamination` marks; label = mark >= 50.
Course ICT 1110 across three calendar years, all three clearing the filter:

| Cohort | Students | Weeks | Pass rate | Minority |
|---|---|---|---|---|
| 2019 | 55 | 34 | 0.636 | 20 |
| 2020 | 76 | 43 | 0.211 | 16 |
| 2021 | 52 | 36 | 0.385 | 20 |

The same course swings from 0.64 to 0.21 to 0.39 — the sharpest prevalence
shift in the benchmark, and it supplies D1 pairs for a fourth institution.
PRIVACY: the release ships a `StudentName` column of real personal names beside
the hash; the adapter never reads it.

### 12.3 Added: institution 5 — Universidad de Oviedo
Riestra-Gonzalez, Paule-Ruiz & Ortin (2021), *Computers & Education* 163:104108;
full anonymised Moodle 2.x dump for AY 2014/15 (781 MB zipped / 4.83 GB SQL).
`oviedo_extract` streams the dump once and writes only the needed columns; the
activity log is partitioned into twelve Spanish month tables sharing the
`mdl_log` schema, **46.6 M events total**. 858 courses carry a course-total
gradebook item; **94 clear >= 50 students and >= 15 minority**, capped at
**20 cohorts** so the ladder stays balanced (uncapped, the mean over pairs would
be an Oviedo statistic).

Two caveats to state in the paper. (a) The label is the Moodle gradebook course
total, not a registrar outcome, unlike the other four institutions. (b) 9.9% of
students score exactly zero, so absence of activity partly entails the label —
the same tautology as OULAD's "Withdrawn", and the adapter exposes
`drop_zero_grades` to run the identical control.

The repository's own feature CSVs are deliberately NOT used: they carry
grade-derived predictors for a grade-derived label, the circularity failure this
project already documented. Features are rebuilt from raw click logs.

### 12.4 Rejected, with the specific failing criterion
| Candidate | Fails on |
|---|---|
| XuetangX AAAI'19 (247 courses, 42 M events) and KDD Cup 2015 (39 courses) | Label is "no activity in the next 10 days", not a course outcome. Mixing it in would confound a label-definition change with an institution change. Both are freely downloadable if a dropout-window arm is ever wanted. |
| HarvardX / MITx Person-Course | Aggregate lifetime totals only (`nevents`, `ndays_act`); no per-week breakdown. Guestbook-walled. |
| Canvas Network Person-Course | Aggregate totals, and dates coarsened to calendar quarters. |
| MOOCCubeX / MOOC-Radar | No course-level outcome anywhere in the schema. |
| UEF Finland (lamethods) | Chapter states the release is synthetic, generated from a real course — the circularity risk this project already documented. |
| GdP MOOC (edX, Sorbonne; 1,007 students, 383/624) | Genuinely usable and verified, but activity is bundled into four coarse phases with no daily granularity, so `cum_active_days` cannot be built and at the 1/3 cutoff the cumulative and current features coincide. Adapter written (`gdp_mooc_adapter`); hold for a 6-feature robustness arm at the 1/2 cutoff. |
| Middle East College Oman | Confirmed unrecoverable: log usernames blanked to "-", outcomes keyed by roll number, no published mapping between the two id spaces. |
| EPM Genoa | Final grades exist for only 52 students. |
| Perugia, ILEDA, Cadiz, Brazilian HEI | Excellent timestamped logs, no outcome data at all. |
| Patras augMENTOR | Log and grade files pseudonymised independently: only 47 of ~230 users join. |

### 12.5 Benchmark after round 2
Five institutions, five platforms: OULAD 19 cohorts, UKZN 16, Oviedo 20,
KU Leuven 6, Zambia 3 — **64 cohorts**. Ordered institution pairs rise from 6 to
**20**, which was the actual weak point.

### 12.6 Runtime change forced by the larger ladder
64 cohorts give 4,096 ordered pairs x 3 representations x 3 models. Permutation
importance dominates, so rankings are now computed for the primary model only
(`EXPLAIN_MODEL = "gradient_boosting"`); the other two families are AUC
robustness checks and their explanation columns are NaN. Combined with
`IMPORTANCE_REPEATS = 3` and the 1,500-row stratified subsample, this keeps the
run tractable. Disclose all three settings in the Method section.

---

## 13. Round-1 simulated review and the resulting rewrite (2026-09-05)

A five-seat panel (journal fit, methodology, domain, perspective, devil's
advocate) reviewed the draft; each seat committed without sight of the others.
All five returned Major Revision or worse. The full reports and the editorial
decision are in `docs/dissertation/review/side2026_round1/`. The full-length
pre-review draft is preserved at `side2026_paper_v1_full.md`.

### 13.1 What the review broke, and what was verified before acting
Every finding below was reproduced by us before it changed the paper.

| Finding | Seats | Status |
|---|---|---|
| F1 computed with `pos_label=1`, i.e. on the PASSING class | 4 of 5 | Confirmed. A constant "everyone passes" rule scored 0.765 and beat every configuration. On the failing class the claimed repair reverses. **Second headline claim withdrawn.** |
| Headline paired estimator excludes Oviedo and Zambia structurally | 2 | Confirmed: Oviedo has one year (no D1), Zambia one course (no D2). Paired-40 = OULAD 19 + UKZN 15 + KU 6. |
| Mechanism claim contradicted by our own regression | 2 | Confirmed: `corr_d_scale` rises 0.067→0.077 under percentiles; `d_shape` is what falls. **Claim retracted.** |
| Shared students contaminate D1/D2 | DA | Confirmed: 72/78 D1 and 324/916 D2 pairs, up to 94 % of the target. |
| Student count double-counted | DA | Confirmed: 35,529 distinct, not 45,158 summed. |
| Zambia label leaked backwards | 2 | Confirmed and fixed; cost one cohort. |
| Demographics claimed unavailable | perspective | **False**: OULAD ships `imd_band`/`disability`/`gender`/`age_band`; UKZN ships `RACE`/`QUINTILE`/NSFAS flags. |
| Explanation claim is estimator noise | DA | **Rejected by the challenger's own measurement**: self-agreement tau = 0.921, stable across `n_repeats`. |
| ...but the ceiling is not 1.0 | DA | Upheld. Disjoint halves of the same cohort agree at 0.338. **Third claim narrowed.** |
| Two wrong author attributions, one wrong "et al." | domain | Confirmed against Crossref/DataCite; all corrected. |

### 13.2 New experiments the review forced
- `exp_017_contamination` — per-pair student overlap, clean-pair recomputation, distinct-student count.
- `exp_018_explanation_ceiling` — noise floor (0.707), attainable ceiling (0.338 ladder-matched), analytic random baseline (top-3 Jaccard 0.303).
- `exp_019_threshold_transfer` — four label-free decision rules; all four lose to "alert everyone" at 0.546.
- `exp_020_fairness` — per-group recall at a 20 % flag budget; transfer costs the worst-served group most (UKZN school quintile 0.65 → 0.18).
- Metric suite rebuilt: F1 on the failing class beside its trivial baseline, recall/precision/lift at a 20 % flag budget, Brier, calibration-in-the-large.

### 13.3 The rewritten claim set
Discrimination degrades gradually (0.691 → 0.597); **calibration collapses** (calibration-in-the-large −0.008 → +0.119) and the label-free percentile transform restores it almost exactly (−0.009) while improving nothing else; the transform does **not** help the decision at a flag budget; and explanation rankings were weakly identified before transfer. Framed in the external-validation vocabulary of clinical prediction modelling (TRIPOD+AI, the calibration hierarchy, the model-updating ladder), which the review correctly identified as the missing literature.

### 13.4 Standing rule adopted
`services/ml/scripts/verify_paper_claims.py` recomputes every number in the
manuscript from a released artifact. 57 claims currently pass. A number that
cannot be recomputed from an artifact does not go in the paper.
