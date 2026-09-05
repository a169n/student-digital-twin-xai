# R4 — Devil's Advocate Report

**Paper:** *What Transfers and What Does Not: Predictions, Thresholds and Explanations of Early-Warning Models Across Five Institutions* (SIDe 2026, Track 1, draft v1.0)
**Role:** Adversarial seat. This report does not score and is not balanced. It argues one side.
**Basis:** every number below was recomputed by me from `data/artifacts/experiments/exp_014_transfer_ladder/{f25,f33,f50}/`, `exp_016_shift_analysis/f33/`, and by re-running `services/ml/src/experiments/transfer_benchmark.py` against the repository's own parquet caches. Nothing here is taken on the manuscript's word.

---

## 1. The Strongest Case Against This Paper

The paper reports three failure modes. I will argue that the second one is an artefact of a metric bug, the third is not a transfer finding, the ladder that separates them is contaminated, and the benchmark that underwrites all of it does not reproduce.

**Start with the metric.** The paper's most quotable result — "the threshold fails first", F1 collapsing 0.809 → 0.507 and being "repaired" to 0.639 — is computed with `pos_label=1`, and in this codebase `y = passed`. Every F1 in Table III, in the abstract, and in the conclusion is the F1 of *identifying students who pass*. An early-warning system alerts on failure. The paper measures the deployment quality of an alarm using the class the alarm is not raised for. Once that is noticed, two things follow immediately, and I computed both. First, the constant classifier "predict everyone passes" scores F1 = 0.734 averaged over the 64 targets, beating the percentile-repaired transferred model in **63 of 64 target cohorts** and beating the *within-cohort* model in 21 of 40. The paper's headline repair does not reach a classifier that ignores the data. Second, recomputing the same pairs with `pos_label=0` — the class that would actually trigger an intervention — the percentile transform makes things **worse**: 0.421 raw → 0.350 percentile, against 0.546 for "alert everyone". The single contribution the paper calls "the largest and the cheapest to repair" is, on the alerting-relevant class, a regression below a trivial baseline. There is no baseline anywhere in the paper against which this could have been caught.

**Then the mechanism.** Section V-D attributes the fix to removing sensitivity to platform click scale. The real mechanism is simpler and less interesting. Rank-transforming every cohort makes every cohort's marginal feature distribution identical, so a transferred model emits on any target the score distribution it emitted on its own source. I measured it: the correlation between the transferred model's predicted-positive rate on the target and the *source's own* positive rate is **r = 0.914** under percentiles against 0.424 under raw counts, and the mean absolute gap between the two falls from 0.267 to 0.074. The percentile representation does not align the model to the target; it pins the alert rate to the source. That is prior matching, and prior matching is a thresholding operation. To prove it, I applied a one-line, label-free per-cohort threshold to the **raw** model — take the top `source_positive_rate` fraction of target scores — and got F1 **0.633 against percentile's 0.622, beating the representation fix in 42 of 64 targets** with the features untouched. The paper's own Discussion nominates per-cohort threshold calibration as "the natural next step". It is not the next step; it is the baseline that already wins, and the paper's contribution 4 does not survive it.

**Then the ladder.** D0→D1→D2→D3 is presented as a distance axis. It is also, undisclosed, a contamination axis. Restricted to the 64 admitted cohorts, the *same students* appear in source and target for 72 of 78 D1 pairs (mean 12.3% of the target, max 83%) and 324 of 916 D2 pairs (max **93.8%** of the target already in the source's training set, with labels), while D3 is essentially clean at 0.01%. `ukzn_ISTN103_2020 → ukzn_ISTN101_2020` trains on 857 of the target's students, in the same semester, where one person's two outcomes are strongly coupled. Contaminated pairs score higher than clean ones at both rungs (D1 0.761 vs 0.731; D2 0.667 vs 0.648). The reported D2→D3 cliff is therefore part distance and part the point at which individual-level memorisation stops being available. Kapoor & Narayanan sits in this paper's reference list at [18] and is cited nowhere in the text.

**Then the population.** The headline ladder is "restricted to the 40 target cohorts present at all four distances". I enumerated them: OULAD 19, UKZN 15, KU Leuven 6. **All 20 Oviedo cohorts and all 3 Zambia cohorts are excluded** — Oviedo because it is a single academic year and so has no D1 rung, Zambia because it is a single course and so has no D2 rung. Tables II and III, the abstract's 0.746 / 0.616 / 0.809 / 0.507, and the conclusion's "five institutions and five platforms" describe a **three-institution** ladder that drops precisely the two institutions carrying the paper's most distinctive claims. Meanwhile Table IV's explanation numbers *are* computed over all 64 cohorts by pair, so the three headline findings are not measured on the same population, and this is not stated. Section V-A then prints "the seven-feature model reaches ROC-AUC 0.746 on average" directly above a per-institution table whose own 64-cohort average is 0.689.

**Finally, the benchmark.** The paper's first contribution is reproducibility. `run_f33.log` — the log of the primary configuration that line 3 of the manuscript points at — reads `cohorts at fraction 0.33: 63` and lists **two** Zambia cohorts (2020: n=65, pass 0.246). The frozen `f33/cohorts.csv` the paper is built from lists **three** (2019: n=55, pass 0.636; 2020: n=76, pass 0.211). Re-running the released pipeline against the released caches today gives 63 cohorts, matching the log and not the artifacts. Table I's "3 cohorts / 183 students / 0.21–0.64" and Section III-A's motivating sentence "Zambia's single course moves from 0.64 to 0.21 to 0.39 across three consecutive years" both depend on a cohort the current code does not produce and a pass rate the log contradicts. A benchmark paper whose selling point is that the field's benchmarks are not reproducible cannot ship frozen results that its own run log disagrees with.

**What I am not claiming.** I tried hard to kill the explanation result as estimator noise and failed: the permutation-importance ranking is a stable statistic here (self-agreement τ = 0.921). The dissociation between prediction and explanation is real. But it is not a *transfer* finding, and Challenge 1 shows why.

**Recommendation at the PC:** reject in current form. Two of the three headline findings do not survive contact with a baseline, and the benchmark does not reproduce.

---

## 2. Challenge-by-Challenge

### Challenge 1 — The central dissociation is real, but it is not a transfer result [CRITICAL]

**The attack I was asked to run, and its outcome: not sustained.** I computed the noise floor directly on the real cohorts, using the paper's own `_ranking` function, `n_repeats=3` and the 1,500-row stratified subsample.

| Control | What varies | Mean τ | Mean J@3 | n |
|---|---|---|---|---|
| A — same fitted model, same data, different importance seed | estimator noise only | **0.921** (sd 0.105) | 0.923 | 960 (64 cohorts × 15 seed pairs) |
| B — same transferred model, same target, seed 42 vs 1 | estimator noise, D3 conditions | **0.764** (sd 0.263) | 0.787 | 400 D3 pairs |
| Random null | — | 0.000 | 0.303 | analytic |

`P(τ < 0.2)` under control A is 0.004 and `P(τ ≤ 0.038)` is 0.000. Subsampled targets (n > 1500) show the same floor as unsubsampled ones (0.923 vs 0.921), and raising `n_repeats` from 3 to 10 to 30 moves the floor only 0.924 → 0.952 → 0.957. **The τ ≈ 0.03 at D3 is not the estimator's variance**, and neither disclosed compute setting produces it. I withdraw that objection; the authors should keep this table as a defence.

**The attack that does land.** The paper's comparator is wrong in two ways, and the correct comparator removes most of the effect.

*(a) The local baseline is scored in-sample.* In `run_ladder`, `target_rankings[...] = _ranking(m, c.X(rep), c.y, seed)` where `m` was fit on **all of** `c`. The "what a locally trained model would say" ranking is a permutation importance measured on the model's own training rows; the transferred model's ranking is measured out-of-sample. Part of the reported disagreement is that regime difference, baked into the estimator.

*(b) The ceiling is not 1.0, it is 0.395.* I ran the control the paper does not: train two gradient-boosting models on **disjoint stratified halves of the same cohort**, rank both on that cohort, compare. This holds course, institution, platform, label definition, calendar and prevalence exactly constant — transfer distance is zero, only the training sample changes.

| Setting | τ | J@3 |
|---|---|---|
| **Within-cohort resampling control (mine, n=192)** | **0.395** (sd 0.320) | **0.530** |
| D1 same course, other year (paper) | 0.217 | 0.418 |
| D2 other course, same institution | 0.089 | 0.372 |
| D3 other institution | 0.038 | 0.336 |
| Random null | 0.000 | 0.303 |

Per institution the control is τ = 0.322 (OULAD), 0.378 (Oviedo), 0.431 (UKZN), 0.709 (KU Leuven), 0.164 (Zambia). Two models trained on two halves of *the same OULAD cohort* agree at τ = 0.32. Changing only the model's `random_state`, with data fixed, gives τ = 0.969 — so this is sampling variability in what the model learns, not implementation noise.

Re-expressed against the achievable ceiling rather than against 1.0: D1 recovers 55% of attainable agreement, D2 23%, D3 10%. The honest claim is *"explanations are unstable to resampling within a single cohort, and transfer distance makes an already-unstable quantity worse."* That is materially weaker, and its first half is Tiukhova et al. [15], which this paper cites. The manuscript's "Explanations lose everything" and "explanation portability after transfer has not been quantified" both rest on an implicit ceiling of 1.0 that the data does not support.

**Data-integrity note [MINOR]:** at D0 the code does not measure agreement, it assigns it — `tau = 1.0 if explain else nan`. `aggregate.csv` therefore ships `tau_mean = 1.0` at D0 as a computed result. The measured value is 0.921.

### Challenge 2 — Random baselines: the paper is right and never computed it [MAJOR]

Over 7 features, top-3 set overlap follows a hypergeometric; the exact expectation is

`E[J@3] = Σ_i P(i)·i/(6−i) = (18/35)(0.2) + (12/35)(0.5) + (1/35)(1) = 10.6/35 = 0.3029`

confirmed by Monte Carlo at 0.304 (sd 0.206, 20,000 draws). `E[τ] = 0` with **sd 0.317 per pair**.

| Quantity | Reported | Random | Above chance |
|---|---|---|---|
| D3 J@3, raw | 0.336 | 0.3029 | +0.033 |
| D3 J@3, percentile | 0.320 | 0.3029 | +0.017 |
| D2 J@3, raw | 0.372 | 0.3029 | +0.069 |
| D1 J@3, raw | 0.418 | 0.3029 | +0.115 |
| D3 τ, raw | 0.038 | 0.000 | +0.038 |

The claim "a top-three overlap of 0.33 out of seven features is close to what random rankings would give" is **correct** — indeed the reported figure is 0.033 above chance, not merely "close". Two consequences the paper misses. (i) Under the null, `P(single-pair τ ≥ 0.038) = 0.496` — the reported D3 value sits at the *median* of the random distribution, a stronger statement than the paper makes and one it should make. (ii) The same baseline deflates D1: 0.418 against a floor of 0.303 and an empirical ceiling of 0.530 (Challenge 1). The entire Table IV Jaccard column lives in a 0.23-wide band and is presented as though it ran from 0 to 1.

### Challenge 3 — The fix is accidental recalibration, and a proper threshold beats it [CRITICAL]

Confirmed, with the numbers requested.

**Mechanism.** `represent(..., "percentile")` is `x.rank(pct=True)`, which forces every cohort's marginal feature distribution to Uniform[0,1]. A source model therefore sees, on any target, the same input distribution it saw on its own source, and emits the same score distribution. Measured over all 3,034 D3 pairs (gradient boosting):

| | raw | percentile |
|---|---|---|
| corr(predicted-positive rate on target, source's own positive rate) | 0.424 | **0.914** |
| mean \|target positive rate − source positive rate\| | 0.267 | **0.074** |
| mean predicted-positive rate | 0.479 | 0.656 (source mean: 0.643) |

The transform does not adapt to the target; it reproduces the source's alert rate. Consistent with this, the F1 gain from percentiles correlates with the *target's* pass rate (r = 0.190; mean gain 0.208 where target pass rate > 0.7 against 0.073 where < 0.5) — the fix helps most exactly where forcing more positives is what the majority class wanted anyway.

**The competing baseline, which the paper never runs.** I applied a label-free per-cohort rank threshold to the raw model: predict positive for the top `r_source` fraction of the target's scores, where `r_source` is the source model's positive rate on its own training set. No target labels, no feature transform, one line.

| Rule (per-target means, 64 targets, 3,034 D3 pairs) | F1 (pass class) |
|---|---|
| raw, fixed 0.5 (paper's "failure") | 0.480 |
| percentile, fixed 0.5 (paper's "fix") | 0.622 |
| **raw + source-rate threshold (mine)** | **0.633** |
| **constant "predict everyone passes"** | **0.734** |

The threshold rule beats the representation fix in **42/64** targets. The constant classifier beats it in **63/64**. Section VI says per-cohort threshold calibration "points at… the natural next step"; it is in fact the baseline that dominates the contribution.

**The metric-direction error, which is worse [CRITICAL].** `_scores` calls `f1_score(y, …)` with the default `pos_label=1`, and `y = passed`. Recomputing the identical pairs on the failure class:

| | F1 (fail class) |
|---|---|
| raw, fixed 0.5 | 0.421 |
| percentile, fixed 0.5 | **0.350** |
| constant "alert everyone" | 0.546 |

**On the class an early-warning system alerts for, the percentile transform destroys 0.071 F1 rather than recovering 0.132, and both are beaten by alerting on everybody.** Every F1 sentence in the abstract, Section V-C and the conclusion inverts on this recomputation. No model uses `class_weight`, so at a fixed 0.5 threshold each model simply tracks the majority class of its source — which is why the F1 matrix is organised by source institution: UKZN sources (pass rate 0.60–0.95) yield D3 F1 of 0.50–0.70, OULAD sources (0.34–0.73) yield 0.32–0.36. `corr(D3 F1 raw, source pass rate) = 0.360`; `corr(D3 F1 raw, target pass rate) = 0.068`. The metric tracks the source's base rate, not transfer.

**AUC side [MAJOR].** The percentile gain is not uniform: **41.2% of D3 pairs get a lower AUC** under percentiles than raw, and 35.0% get a lower F1. The mean gain of 0.020 averages a distribution straddling zero.

### Challenge 4 — Selection and composition: the conclusion is choice-dependent [CRITICAL]

**(a) The headline ladder is a three-institution ladder.** The 40 paired targets are OULAD 19, UKZN 15, KU Leuven 6. Excluded: **all 20 Oviedo** (single academic year ⇒ no D1 rung), **all 3 Zambia** (single course ⇒ no D2 rung), plus `ukzn_ISTN102_2018`. The restriction is stated; *which* institutions it deletes is not, and it deletes the two that carry the paper's most distinctive claims — the 0.21–0.95 prevalence spread and the D0 = 0.52 floor.

**(b) Unit of analysis is inconsistent between tables.** Recomputed three ways (gradient boosting):

| Aggregation | D0 AUC | D3 raw AUC | D3 raw F1 | D3 raw τ |
|---|---|---|---|---|
| paired-40, per target (Tables II–III) | 0.746 | 0.616 | 0.507 | 0.046 |
| all-64, per target | 0.689 | 0.599 | 0.480 | 0.035 |
| all-64, per pair (`aggregate.csv`, Table IV's "3,034 pairs") | 0.689 | 0.597 | 0.479 | 0.038 |

Tables II–III use row 1; Table IV uses row 3. The dissociation is asserted across metrics not measured on the same cohorts.

**(c) Leave-one-institution-out of the whole benchmark.** All defensible; the explanation headline moves by an order of magnitude.

| Benchmark | D3 AUC raw | D3 AUC pct | D3 F1 raw | D3 F1 pct | **D3 τ** |
|---|---|---|---|---|---|
| all five | 0.599 | 0.618 | 0.480 | 0.622 | **0.035** |
| drop KU Leuven | 0.607 | 0.619 | 0.478 | 0.606 | 0.019 |
| drop OULAD | 0.558 | 0.578 | 0.523 | 0.643 | **0.082** |
| drop Oviedo | 0.627 | 0.661 | 0.516 | 0.652 | 0.042 |
| drop UKZN | 0.595 | 0.612 | 0.416 | 0.575 | **0.008** |
| drop Zambia | 0.601 | 0.622 | 0.484 | 0.639 | 0.037 |

τ at D3 spans 0.008–0.082, a tenfold range, across single defensible composition choices. "τ ≈ 0.03" is a property of this particular five-way mix, not of cross-institution transfer.

**(d) Oviedo's 20-of-94 selection is a selection on the outcome.** "The 20 with the largest minority class are kept." Minority-class size is a function of the label distribution, so the retained Oviedo courses are systematically the largest and most class-balanced. Since prevalence shift is the paper's central explanatory variable, the sample entering that analysis has been pruned on a function of it. A size-based or random criterion would be neutral; this one is not.

**(e) Pseudo-replication [MAJOR].** `aggregate` bootstraps over *pairs* as if 3,034 D3 pairs were 3,034 independent observations; they are 64 targets × ~51 sources drawn from 5 institutions. Recomputed CI widths for D3 gradient-boosting raw AUC:

| Resampling unit | 95% CI | Width | Inflation |
|---|---|---|---|
| pairs (paper's method), n=3034 | [0.5924, 0.6009] | 0.0085 | 1.0× |
| target cohorts, n=64 | [0.5814, 0.6160] | 0.0346 | **4.1×** |
| institution pairs, n=20 | [0.5637, 0.6017] | 0.0380 | **4.5×** |

Every interval in the paper is roughly four times too narrow. Applying the correction to the headline percentile AUC gain (0.0204): the pair CI [0.0165, 0.0242] widens to [0.0117, 0.0340] under target-institution clustering — the *sign* survives, so the gain is real, but it is now nowhere near the "pre-registered 0.05 criterion". The F1 gain of 0.1435 has an institution-pair-clustered CI of [0.0708, 0.1667].

**(f) "Pre-registered" [MINOR].** The word appears twice. There is no pre-registration artefact in this repository; the only prior document is `side2026_paper_plan.md`, written by the same authors during the same work. Calling a self-authored working plan a pre-registration is not defensible at a double-blind venue.

### Challenge 5 — Label incoherence is unfalsifiable by this design [MAJOR]

The five definitions are: withdrawal-counts-as-failure (OULAD), gradebook total ≥ 50% (Oviedo), registrar code P* (UKZN), PASSED (KU Leuven), final exam ≥ 50 (Zambia). **Each institution has exactly one label definition, so label semantics and institution identity are perfectly collinear by construction.** No contrast in this benchmark separates "moved institution" from "changed label definition". The D3 effect is not identified as a transfer effect; it is identified as a joint institution-and-label effect, which is a different claim from the one the title makes.

I ran the only test the data admits and it is uninformative: restricting D3 to pairs where both endpoints use a registrar/exam label (UKZN, KU Leuven, Zambia) gives AUC 0.570 (n=324) against 0.600 (n=2,710) for mixed-semantics pairs. Homogenising the label makes transfer look *worse* — but the restriction also removes OULAD, by far the easiest target (as a target, D3 AUC 0.64–0.71 against 0.53–0.62 elsewhere), so the comparison is confounded by target difficulty and settles nothing. That is the point: it cannot be settled here. The Limitations paragraph concedes heterogeneity exists; it does not concede that the design cannot distinguish it from the effect being claimed.

The controls offered do not close this. Section V-F's withdrawal control runs **inside OULAD only, at D0 and D2** — it shows withdrawal inflates the *within-institution* signal; it says nothing about whether the D3 drop is a label artefact, because it never evaluates a D3 pair.

### Challenge 6 — Overgeneralisation

See the table in Section 3. The most consequential: a 0.746 that contradicts the table printed beneath it; "monotonically", false in 5 of 9 rows of the authors' own Table II; and "about two thirds", contradicting "44% to 47%" three pages earlier.

### Challenge 7 — The "so what" attack [MAJOR]

Strip the paper to what is not already known and what survives a baseline.

- *Prediction degrades with distance.* Known [7]–[10]. The addition is more institutions — real, but incremental.
- *Fixed thresholds break when base rates differ.* This is arithmetic. Schwerter et al. [10] already reported it. The paper's own Table I gives prevalences of 0.21–0.95, from which threshold collapse follows without an experiment.
- *A rank transform helps.* Percentile-within-group is rank normalisation, decades old, and Section V-D's mechanism story (removing platform scale) is what rank normalisation is for. Its measured mechanism here is prior matching, and it is beaten by a per-cohort threshold (Challenge 3).
- *Explanations do not transfer.* Against the correct within-cohort ceiling of 0.395, this reduces to "permutation-importance rankings of a GBM over seven collinear engagement features are unstable" — i.e. Tiukhova et al. [15], the paper's own citation, restated at longer range.

What is genuinely new and defensible is the **benchmark artefact** — 64 cohorts, five platforms, one schema, one relative cutoff — and the **within-cohort D0 range 0.85 → 0.52**, a real and useful rebuke to single-dataset reporting. That is a resource paper with one good finding. It is not a paper whose abstract can claim three separated failure modes and a fix.

### Challenge 8 (mine) — Student double-counting and the contamination gradient [CRITICAL]

**(a) "45,236 students" is enrolments, not students.** Over the 64 admitted cohorts at the 1/3 cutoff there are 45,158 enrolment rows and **35,529 distinct student identifiers** (21.3% duplication). Per institution: UKZN 7,254 rows / 3,904 distinct (46.2%), KU Leuven 3,939 / 2,126 (46.0%), Oviedo 3,789 / 3,092 (18.4%), OULAD 30,059 / 26,317 (12.4%), Zambia 0%.

**(b) The duplication is concentrated in exactly the rungs that define the ladder.**

| Rung | Pairs | Pairs sharing students | Mean fraction of target already in training | Max |
|---|---|---|---|---|
| D1 same course, other year | 78 | **72** | 0.123 | 0.831 |
| D2 other course, same institution | 916 | **324** | 0.036 | **0.938** |
| D3 other institution | 2,912 | 78 | 0.0001 | 0.015 |

Worst offenders: `oviedo_C190 → oviedo_C174` (93.8% of the target seen in training), `ukzn_ISTN3ND_2019 → ukzn_ISTN3SA_2019` (89.7%), `ukzn_ISTN103_2020 → ukzn_ISTN101_2020` (857 students, 85.7%), `ku_Globaleconom_1819 → ku_Globaleconom_1920` (566 students, 83.1% — repeat students in a same-course, different-year D1 pair). Contaminated pairs outscore clean ones at both rungs: D1 0.761 (n=57) vs 0.731 (n=21); D2 0.667 (n=123) vs 0.648 (n=793).

The UKZN D2 case is sharpest: the source model has memorised most of the target's students, in the *same academic year*, where one person's outcomes in two concurrent courses are strongly coupled. That is not "transfer to another course"; it is partly recall of individuals. Since D3 is the only rung where this is impossible, the reported D2→D3 cliff — the paper's central quantitative claim — is inflated by an amount the paper has not bounded.

### Challenge 9 (mine) — The frozen results do not reproduce [CRITICAL]

Contribution 1 is a reproducible benchmark. It does not currently reproduce.

| Source | Cohorts | Zambia cohorts | Zambia 2020 |
|---|---|---|---|
| `f33/cohorts.csv` (frozen; paper's Table I) | **64** | 3 (2019, 2020, 2021) | n=76, pass 0.211 |
| `run_f33.log` (log of the f33 run) | **63** | 2 (2020, 2021) | n=65, pass 0.246 |
| Re-running the released pipeline on the released caches today | **63** | 2 (2020, 2021) | n=65, pass 0.246 |

`datasets/cache/zambia_ICT1110_2019.parquet` does not exist; only 2020 and 2021 are present. `f33/pairs.csv` has 36,864 rows = 64² × 9, so the frozen ladder was genuinely computed on 64 cohorts — from an input state the repository no longer contains and the f33 log does not describe. The f25 and f50 logs both report 64, so the primary configuration is the odd one out. Downstream:

- Table I's "Zambia | 3 | 183" (= 55+76+52) is not reproducible; the current state gives 2 cohorts, 117 students.
- Section III-A's "Zambia's single course moves from 0.64 to 0.21 to 0.39 across three consecutive years" — the motivating example for prevalence shift — uses a cohort that no longer exists and a middle value the log gives as 0.246.
- Section V-H's "All 64 cohorts survive both" is contradicted by the primary run's own log.

I cannot tell from the repository whether the caches were regenerated after the frozen run or whether the adapter is unstable. Either diagnosis is disqualifying for a benchmark contribution, and both are fixable before submission.

### Challenge 10 (mine) — Undisclosed preprocessing changes the linear-model story [MAJOR]

`build_classification_model("logistic_regression")` returns `Pipeline([StandardScaler(), LogisticRegression(...)])`. Gradient boosting and random forest are unwrapped. So the "raw" logistic regression is already standardised — **using the source cohort's mean and standard deviation**, applied to the target. The "z-score representation" replaces that with the *target's* statistics.

The headline linear result — "recovers 0.089 AUC for a linear model", the paper's largest single AUC number — is therefore not a raw-versus-scaled comparison. It is source-statistics scaling versus target-statistics scaling: a textbook covariate-shift correction. Section IV-C describes only "logistic regression", and Section V-D explains the asymmetry by saying "a linear model is sensitive to feature scale directly", which is not true of the model actually run. A material undisclosed implementation detail on which a headline number depends.

### Challenge 11 (mine) — A stated methodological invariant is false in the authors' own data [MAJOR]

Section IV-B: *"For a tree model the percentile transform is monotone, so within a cohort it cannot change predictions; any gain at D1–D3 is therefore attributable to cross-cohort alignment alone, which is the property under test."* This is the argument licensing the causal reading of the fix.

At D0, gradient boosting, percentile versus raw, across 64 cohorts: **the two differ in 63 of 64 cohorts**, mean |Δ AUC| = 0.0055, **max 0.0490**. The mean violation is a quarter of the claimed D3 gain of 0.021; the maximum is more than double it. The invariance is asserted, not verified, and it does not hold. Relatedly, `represent()` computes the transform over the *entire* cohort including the CV test folds, so D0 is mildly transductive and not strictly comparable to D1–D3 either.

### Challenge 12 (mine) — Monotonicity, and the controls that do not control [MAJOR / MINOR]

**Monotonicity is false in 5 of 9 rows of Table II** (paired-40, per-target; D2 exceeds D1): GB percentile 0.720→0.725, GB z-score 0.722→0.723, LR percentile 0.752→0.753, LR z-score 0.758→0.760, RF z-score 0.736→0.736. Only the three raw rows and RF percentile are monotone. "All three model families lose discrimination monotonically" is contradicted by the table it cites.

**The feature-richness control (Table VII) is non-monotone and single-institution [MINOR].** D0−D2 gaps: 0.022 (7 features), 0.040 (11), 0.021 (17). The middle row is nearly twice the other two, so "richness buys accuracy, not portability" rests on the endpoints of a three-point curve whose interior contradicts it, in one institution, with no interval on a 0.001 difference.

**The pooled-source reversal (Section V-G) rests on Zambia [MINOR].** "An institution with little history is better served by borrowing than by learning from itself" is carried by 3 cohorts (2 in the current repository state), 183 students (117 now), whose within-cohort AUC is 0.521 — indistinguishable from chance. A conclusion drawn from a cohort where nothing is predictable at all.

**The cutoff sensitivity is not a replication [MINOR].** f25, f33 and f50 use the identical cohort set (verified: the three `cohorts.csv` cohort-id sets are equal) and merely shift the snapshot week within the same students' own timelines. The three rows of Section V-H are three highly correlated readings of one experiment, presented as robustness.

**Dangling citation [MINOR].** Reference [18] (Kapoor & Narayanan, leakage) appears in the reference list and is cited nowhere in the body. Given Challenge 8, the omission is unfortunate.

**Paper/code mismatch [MINOR].** Section III-D states the cutoff is week `⌈⅓ × course length⌉`. `cutoff_rows` computes `max(1, rint(fraction × n_weeks))` with `fraction = 0.33` — round-to-nearest of 0.33, not the ceiling of one third. For a 46-week course the paper says week 16 and the code takes week 15.

---

## 3. Overclaimed Sentences

| # | Quoted sentence | What the evidence supports | Suggested wording |
|---|---|---|---|
| 1 | "F1 at 0.5 drops from 0.809 to 0.507" / "the threshold fails much harder" (Abstract, V-C) | These are F1 scores for the **pass** class (`pos_label=1`, `y=passed`). On the failure class the same pairs give 0.421 → 0.350 under the "fix". A constant "predict everyone passes" scores 0.734, beating the repaired model in 63/64 targets. | State the positive class explicitly, report both classes, and report the majority-class baseline in the same table. If the fail-class numbers stand, the F1 claim must be withdrawn or inverted. |
| 2 | "restores cross-institution F1 to 0.639 uniformly across model families" (Abstract) | 0.639 is below the constant-classifier baseline of 0.734 and below a label-free per-cohort rank threshold on raw features (0.633 mean, winning 42/64 targets). | "…partially restores cross-institution pass-class F1 to 0.639, which remains below both a majority-class baseline and a per-cohort threshold applied to raw features." |
| 3 | "a fix that costs one line of preprocessing" (I) | Its measured mechanism is matching the source's own alert rate (r = 0.914 between target predicted-positive rate and source positive rate), and it is outperformed by a different one-line fix the paper positions as future work. | "…a one-line rank normalisation whose effect we trace to implicit prior matching, and which we benchmark against explicit per-cohort threshold calibration." |
| 4 | "Trained and tested inside its own cohort, the seven-feature model reaches ROC-AUC 0.746 on average" (V-A) | 0.746 is the paired-40 subset. The 64 cohorts in the table printed directly beneath average **0.689**. | "…reaches 0.689 over all 64 cohorts (0.746 over the 40 cohorts entering the paired ladder)." |
| 5 | "All three model families lose discrimination monotonically as the source moves away from the target (Table II)" (V-B) | False in 5 of 9 rows of Table II; D2 exceeds D1 for every percentile and z-score row except RF percentile. | "Discrimination falls sharply at D3 for all families; D1 and D2 are not reliably ordered, and under cohort-relative representations D2 slightly exceeds D1." |
| 6 | "recovers about two thirds of the lost F1 for every model family we tested" (VII) | Section V-C states 44%–47% for the same quantity; arithmetic on Table III gives 43.7% for GB. | "…recovers 44–47% of the lost pass-class F1…" — and reconcile with the abstract. |
| 7 | "covering 45,236 students" (Abstract, III-A) | 45,158 enrolment rows over 35,529 distinct identifiers; 46% duplication at UKZN and KU Leuven. | "…45,236 student-course enrolments from 35,529 distinct students." |
| 8 | "evaluated for all 4,096 ordered cohort pairs" / "D1 same course another year, D2 another course at the same institution" (I, IV-A) | 72/78 D1 and 324/916 D2 pairs share students between training and evaluation, up to 93.8% of the target. D3 is clean. | Add the overlap table, report D1/D2 both with and without contaminated pairs, and cite [18]. |
| 9 | "Re-expressing each feature as a percentile within the target cohort… recovers 0.089 AUC for a linear model" (Abstract) | 0.089 is the **z-score** gain (0.602→0.691); percentile gives 0.084. And the linear model is already `StandardScaler` + LR fitted on the source, so this is source- vs target-statistics scaling. | Attribute the number to z-scoring, and disclose the pipeline's scaler in Section IV-C. |
| 10 | "meeting the pre-registered success criterion" / "exceeding the pre-registered 0.05 criterion" (V-B, V-D) | No pre-registration artefact exists; the only prior document is the authors' own planning file. | "…exceeding the 0.05 threshold fixed in advance in our analysis plan" — or drop the term. |
| 11 | "A ranking over seven features is a rank statistic and is stable well below that size" (IV-F) | True of the *estimator* (self-agreement τ = 0.921) but not of the *ranking*: two models trained on halves of the same cohort agree at τ = 0.395. | Keep the sentence for the estimator, and add the resampling control, because it is the ceiling for Table IV. |
| 12 | "permutation-importance rankings of a transferred model agree with locally trained rankings at Kendall tau 0.03" / "Explanations lose everything" (Abstract, VI) | Against a within-cohort resampling ceiling of τ = 0.395, D3 retains ~10% of attainable agreement; the local baseline is additionally scored in-sample. | "…retain about a tenth of the agreement two models trained on halves of the same cohort achieve (τ 0.03 against a within-cohort ceiling of 0.40)." |
| 13 | "an institution with little history is better served by borrowing than by learning from itself" (V-G) | Rests on Zambia: 3 cohorts, 183 students, within-cohort AUC 0.521 — chance. Two of the three do not reproduce. | "…in the one institution with fewer than five cohorts, though its within-cohort AUC is near chance and the comparison is correspondingly weak." |
| 14 | "Richness buys accuracy, not portability" (V-F) | Three feature sets in one institution, D0−D2 gaps 0.022 / 0.040 / 0.021; the middle set has the largest gap. No intervals. | "In OULAD, the richest feature set does not shrink the D0–D2 gap, though the intermediate set widens it and the differences are within noise." |
| 15 | "Code, cohort definitions and frozen results are released" (Abstract) | The released code + caches produce 63 cohorts and 2 Zambia cohorts; `run_f33.log` agrees with that and not with the released 64-cohort artifacts. | Do not make this claim until the artifacts regenerate. |
| 16 | "one row per student at week ⌈⅓ × course length⌉" (III-D) | Code is `max(1, rint(0.33 × n_weeks))`. | State the implemented rule. |

---

## 4. What Would Save The Paper

Ordered by how fatal the objection is. Items 1–10 are, in my view, non-negotiable for acceptance.

**For Challenge 3 + overclaim 1 (metric direction and missing baselines) — CRITICAL.**
1. Recompute every F1 in the paper with the failure class as positive, and report both classes side by side. State the positive class in Section IV-C.
2. Add two baselines to every threshold table: the majority-class constant classifier, and a label-free per-cohort threshold (source-rate matching) applied to raw features. If the representation fix does not beat both, say so and reframe the contribution as *measurement* of threshold collapse rather than a fix for it.
3. Report the mechanism honestly: give the `corr(predicted positive rate, source positive rate) = 0.914` result and describe the transform as implicit prior matching. This is a better and more defensible paper than the current one; it just is not the paper currently written.

**For Challenge 8 (contamination) — CRITICAL.**
4. Compute student-identifier overlap for every source→target pair and publish the table. Re-report D1 and D2 restricted to zero-overlap pairs (21 clean D1 and 793 clean D2 pairs remain — enough). If the D2→D3 cliff shrinks, the headline degradation must be restated. Cite [18].

**For Challenge 9 (reproducibility) — CRITICAL.**
5. Regenerate f33 from the current caches, reconcile the Zambia discrepancy, and ship artifacts whose cohort count matches their own run log. Repair or drop Table I's Zambia row and the "0.64 to 0.21 to 0.39" sentence. Add a manifest of input file hashes.

**For Challenge 4 (composition) — CRITICAL.**
6. Name the excluded institutions in the captions of Tables II and III: "paired ladder; Oviedo and Zambia contribute no target cohort at all four distances." Report the all-64 per-target ladder alongside, and use one aggregation unit across Tables II, III and IV.
7. Add the leave-one-institution-out sensitivity table (τ at D3 spans 0.008–0.082). If the explanation headline is composition-dependent, the abstract must carry an interval, not a point.
8. Replace the Oviedo "largest minority class" rule with one that is not a function of the label — largest enrolment, or a seeded random draw — and confirm the ladder is unchanged.
9. Recompute every confidence interval with the target cohort (or target institution) as the resampling unit. Expect intervals roughly four times wider.

**For Challenge 1 (the explanation finding) — CRITICAL to the framing, though the finding itself survives.**
10. Add the within-cohort resampling control (train on disjoint halves, rank both on the cohort): τ = 0.395, J@3 = 0.530. Report D1/D2/D3 as fractions of that ceiling, not against an implicit 1.0.
11. Add the random-ranking baselines analytically: E[J@3] = 0.3029, E[τ] = 0, per-pair sd(τ) = 0.317. Put them as a row in Table IV.
12. Score the local baseline ranking out-of-sample (cross-fitted), so both sides of the comparison are measured in the same regime.
13. Keep my noise-floor table (τ = 0.921 self-agreement, insensitive to `n_repeats`) as a defence — a reviewer will ask, and the answer is good.
14. Stop assigning τ = 1.0 at D0 in `aggregate.csv`; measure it.

**For Challenges 5, 10, 11 — MAJOR.**
15. State plainly in Limitations that institution and label definition are perfectly collinear in this design, so the D3 effect is a joint institution-and-label effect and cannot be decomposed. Do not claim the withdrawal control bounds it — that control never evaluates a D3 pair.
16. Disclose the `StandardScaler` in the logistic-regression pipeline and re-describe the z-score result as source-statistics versus target-statistics scaling.
17. Either verify the tree monotone-invariance claim empirically (it fails: 63/64 cohorts differ, max 0.049) or delete the argument resting on it, and note that `represent()` is computed transductively over the whole cohort at D0.
18. Fix "monotonically", "two thirds", "45,236 students", "pre-registered", the `⌈⌉`/`rint` mismatch, and the dangling [18].

**If the authors can do only three things:** run item 1 (fail-class F1), item 2 (the two missing baselines), and item 4 (the overlap table). If the fail-class numbers hold as I computed them, contribution 4 has to go — and what remains, a public five-platform benchmark, the D0 range 0.85→0.52, and a properly ceilinged explanation-instability result, is still worth publishing, at a smaller claim.
