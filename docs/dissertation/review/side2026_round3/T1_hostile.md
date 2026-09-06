# T1 — Third-round hostile review

**Seat:** adversarial methodologist, third panel.
**Scope:** `docs/dissertation/side2026_paper.md` (218 lines), `data/artifacts/experiments/exp_014` (f25/f33/f50) through `exp_020`, `services/ml/src`, and the raw institution caches under `datasets/`.
**Standing:** I have read both prior reports (eight seats). I do not restate their findings. Everything below is either a new computation or a correction to a prior seat's computation, and every claim carries the number that produced it. All figures recomputed from the shipped CSVs and parquet caches unless marked otherwise.

**Recommendation: REJECT as submitted.** Not because the paper is dishonest — it is unusually honest — but because after two rounds of subtraction the surviving quantity is a benchmark whose central object of study is never shown to beat a rule that requires no model, no training, no source cohort and no labels, and whose four-rung ladder has one rung that is a measurement artefact of the authors' own calendar inference and one that is a blend of a real effect with a null over cohorts where nothing is measurable.

---

## 1. What Eight Reviewers Missed

Eight seats audited the metrics, the estimator, the contamination, the labels-vs-institution collinearity, the weighting, the calibration mechanism, and the explanation floor. Not one of them asked the first question a methodologist asks of a predictive-modelling paper: **is the model better than not having a model?**

### H-1 [CRITICAL] There is no non-trivial baseline anywhere in the paper, and the model loses to the one it should have had

The paper has exactly one trivial baseline: `f1_fail_baseline`, the F1 of alerting everyone (`transfer_benchmark._scores:196`). That baseline is for a *classification threshold*. The paper's headline metrics are a *ranking* metric (AUC) and a *ranked budget* metric (recall at a 20 % flag), and neither has any baseline at all. Nobody supplied one.

Here is one. It uses no model, no training, no source cohort, no labels, and nothing the target institution does not already have on the day of prediction: **sort the target cohort by `cum_active_days` at the cutoff row and flag the bottom 20 %.** Recomputed over the same 63 cohorts, the same cutoff, the same rows:

| | mean ROC-AUC | mean recall@20 % |
|---|---|---|
| **No model — rank by `cum_active_days`** | **0.7130** | **0.3410** |
| Locally trained GB, 5-fold CV (paper D0) | 0.6915 | 0.3264 |
| Pooled within-institution GB (the "restored" positive) | 0.6857 raw / 0.6986 pct | — |
| Transferred GB, D3 raw (paper headline) | 0.5969 | 0.2724 |
| Transferred GB, D3 percentile (the "repair") | 0.6166 | 0.2732 |

The zero-parameter rule beats the paper's locally trained, cross-validated gradient-boosting model in **38 of 63 cohorts**, and beats the mean transferred model in **61 of 63**. At the pair level, a transferred model beats the target's own free rule in **265 of 2,912 D3 pairs (9.1 %)** under raw features and **337 of 2,912 (11.6 %)** under the percentile transform.

The paired-40 estimator, which the paper uses for its flattering headline, does not rescue it. On those 40 targets (19 OULAD, 15 UKZN, 6 KU Leuven):

| Paired-40 | AUC | recall@20 % |
|---|---|---|
| **No model — rank by `cum_active_days`** | **0.7626** | **0.3697** |
| Local GB D0 | 0.7462 raw / 0.7474 pct | 0.3592 |
| Transferred GB D3 | 0.6102 raw / 0.6325 pct | 0.2823 |

The free rule wins on the estimator the paper chose to report, on both metrics.

Per institution (mean D0 AUC, no-model vs locally trained GB):

| Institution | No model (`cum_active_days`) | Local GB D0 | Model's contribution |
|---|---|---|---|
| OULAD | 0.830 | 0.845 | **+0.015** |
| UKZN | 0.717 | 0.667 | −0.050 |
| KU Leuven | 0.655 | 0.611 | −0.044 |
| Oviedo | 0.631 | 0.606 | −0.025 |
| Zambia | 0.565 | 0.527 | −0.038 |

**The machine-learning apparatus adds value at exactly one of the five institutions, and at that one it adds 0.015 AUC.** Everywhere else it destroys signal relative to sorting students by how many days they logged in. Under student weighting the two are a dead heat (0.7820 no-model vs 0.7843 local) — a tie produced entirely by OULAD's 30,059 students dominating the average.

This is not a peripheral observation. It refits the paper's three surviving claims:

1. *"At a fixed flag budget the transferred model still finds a third more failing students than random selection, and that modest number is the honest case for deploying one."* (Conclusion, §V-D.) The honest case is the reverse. Against random (prevalence-rate) flagging the transferred model recovers 0.272; against the rule the institution already has for free it recovers **20 % fewer** failing students (0.272 vs 0.341). There is no deployment case here at all. An institution that adopts a transferred model in place of sorting its own students by login-days is strictly worse off.
2. *"The signal is a property of the institution"* (§V-A). Partly. It is also a property of a model that overfits seven collinear count features on 82–700 rows.
3. *"Permutation-importance rankings over these seven correlated features are weakly identified"* (§V-E). Correct, and now explained rather than merely observed. Within-institution, the first principal component of the seven standardised canonical features explains **54.1 % (UKZN), 55.1 % (Oviedo), 59.9 % (Zambia), 68.6 % (OULAD)** of the variance; PC1+PC2 explain 0.69–0.85. Pooled across all 63 cohorts under the percentile representation the model actually sees, the eigenvalue spectrum is **[0.750, 0.099, 0.064, 0.046, 0.024, 0.011, 0.006]** — one component carries three quarters of the variance. The feature space has roughly one and a half effective dimensions. Attributing importance across seven near-collinear coordinates of a one-dimensional construct is arbitrary before any transfer, which is why one coordinate reproduces the model.

Even the paper's own richness control makes the point: exp_015 reports OULAD D0 = 0.902 with 17 features including assessments. Sorting OULAD students by login-days scores 0.830. Eleven extra features, several of them assessment-derived, buy 0.07.

*What the paper must do:* add the single-feature ranking baseline to every table at every rung, or withdraw every claim that a model is worth transferring. If the benchmark's purpose is to let others measure a proposed fix, a benchmark whose reference configuration loses to a one-line rule is not a benchmark, it is a cautionary tale — which is a publishable paper, but a different one.

### H-2 [CRITICAL] The D1 rung measures the authors' calendar inference, not the passage of a year

Round 2's adversarial seat (S2 §2.6) raised the inferred calendar, tested whether it drives the result, and recorded a negative: UKZN D1 AUC by |Δ cutoff week| showed no monotone relation in cells of n ≤ 6, and Spearman(D0 AUC, inferred `n_weeks`) = −0.19 over 44 cohorts. **That test used the wrong statistic and had no power.** A week count is not comparable across a 13-week course and a 44-week one, and D0 level is not where the artefact lives — pair *mismatch* is.

The right statistic is scale-free: the share of a cohort's total activity already accumulated at its own cutoff row. That is the operational meaning of "how far into the course is the prediction point". Recomputed per cohort from the parquet caches:

| Institution | mean share of total clicks accumulated at the cutoff | cohort range |
|---|---|---|
| KU Leuven (published calendar) | **0.253** | 0.13 – 0.35 |
| Zambia (inferred) | 0.343 | 0.21 – 0.48 |
| UKZN (inferred) | 0.401 | **0.12 – 0.75** |
| Oviedo (inferred) | 0.460 | **0.01 – 0.87** |
| OULAD (published calendar) | **0.499** | 0.40 – 0.58 |

"One third of the course" means half the course has already happened at OULAD and a quarter of it at KU Leuven — a factor of two. Within UKZN alone it ranges from 12 % (`ISTN103_2020`) to 75 % (`ISTN101_2019`) of the course's activity. §III-C's "course lengths range from 14 to 46 weeks" is presented as a property of the courses; a 43-to-45-week "course" at Oviedo is an academic year with a June resit period inside the log span, and the 1/3 cutoff of it lands at the end of a first semester.

Now the test S2 should have run. D1 loss (target's own D0 AUC minus the D1 pair AUC), gradient boosting, raw, split by whether the institution publishes its calendar:

| Target institution | calendar | n D1 pairs | mean \|Δ n_weeks\| | mean \|Δ click-share\| | **mean D1 loss** |
|---|---|---|---|---|---|
| OULAD | published | 46 | 2.52 | 0.040 | **+0.002** |
| KU Leuven | published | 12 | 0.00 | 0.088 | **+0.003** |
| UKZN | inferred | 18 | 6.78 | 0.257 | **+0.049** |
| Zambia | inferred | 2 | 7.00 | 0.268 | **+0.064** |

**The entire D1 degradation is at the institutions where the authors invented the calendar.** Where the calendar is published, transferring a model to the same course a year later costs nothing measurable. And within the inferred-calendar pairs, cutoff mismatch explains a third of the loss:

- inferred-calendar D1 targets (n = 20): r(|Δ click-share|, loss) = **+0.581**, R² = **0.337**
- published-calendar D1 targets (n = 58): r = −0.172, R² = 0.030
- all 78 D1 pairs: r = +0.550

For reference, exp_016's entire shift decomposition explains R² = 0.116 of AUC loss. A single artefact of the authors' own preprocessing explains three times as much of the D1 rung.

The mechanism is concrete and inspectable: `ukzn_ISTN211` is inferred at 37 weeks in 2019 and 19 in 2021 (cutoff week 12 vs 6); `ukzn_ISTN101` at 33/35/24 (weeks 11/12/8); `zambia_ICT1110` at 43/36 (weeks 14/12). S2 listed these same cohorts and then concluded they do not matter. They do.

D2 shows the same gradient: mean |Δ n_weeks| is 9.35 at Oviedo and 9.31 at UKZN against 2.11 at OULAD, and mean D2 loss is +0.068, +0.054 and +0.015 respectively.

**Honest counter-finding, which I record because it cuts against me:** at D3 the effect is negligible — r(|Δ click-share|, loss) = +0.084, R² = 0.007, and institution dummies alone explain R² = 0.233 while adding |Δ click-share| raises it only to 0.243. **The cross-institution gap is not a cutoff-mismatch artefact.** The claim is confined to D1 and D2, and it is fatal there and only there.

*Consequence for the paper.* §V-B's "discrimination degrades gradually" is a four-point curve whose second point is a preprocessing artefact and whose third is partly one. Combined with the contamination the authors themselves found (below), D1 as reported is uninterpretable in both directions at once — inflated by shared students, depressed by cutoff mismatch:

| Target institution | D1 pairs | mean student overlap | D1 loss, contaminated pairs | D1 loss, clean pairs |
|---|---|---|---|---|
| OULAD | 46 | 3.7 % | +0.001 (n=43) | +0.016 (n=3) |
| KU Leuven | 12 | **51.9 %** (max 83 %) | +0.022 (n=8) | −0.033 (n=4) |
| UKZN | 18 | 9.2 % | +0.037 (n=17) | +0.251 (n=1) |
| Zambia | 2 | 0 % | — | +0.064 (n=2) |

KU Leuven's apparent zero-loss D1 rests on pairs sharing half their students; the four clean pairs show a *gain*. The rung should be deleted or reported as three separate institution rows with the calendar provenance and the overlap stated in the same table.

### H-3 [CRITICAL] Round 1 demanded the withdrawal control; nobody ran it. I did, and it is the size of the paper's entire headline

Round 1's methodology seat (R1 C10) found that the withdrawal control existed only as a bullet in a planning document — "no script, no flag in the exp_014/exp_015 pipelines, and no artifact". The current manuscript has deleted the control rather than run it. It is still the single most obvious objection to a benchmark in which OULAD is 19 of 63 cohorts, 30,059 of 45,158 cohort-rows (66.6 %), and appears on one side of 1,672 of 2,912 D3 pairs (57.4 %).

From `datasets/oulad/studentInfo.csv` + `studentRegistration.csv`, restricted to the 19 benchmark cohorts:

- **9,864 of 16,188 OULAD "failures" (60.9 %) are `Withdrawn`, not `Fail`.**
- **6,766 of those 9,864 withdrawals (68.6 %) have `date_unregistration` on or before the cutoff day.** That is **22.5 % of all 30,059 OULAD students** carrying a label that is an administrative event which has already completed by the prediction week, and whose entire clickstream signature is "stopped clicking".
- 3,021 students have `date_unregistration ≤ 0` — they deregistered before the presentation started, have near-zero clicks throughout, and are labelled failures.

`_build_weekly_index` (`oulad_adapter.py:647-682`) computes `is_unregistered_by_week` and then does not use it to drop rows, so these students sit in the grid with zeroes.

Refitting D0 (GB, raw, 5-fold stratified CV, seed 42 — the exact paper pipeline, which reproduces 0.845 to three decimals):

| OULAD D0, mean over 19 cohorts | AUC | mean failure rate |
|---|---|---|
| As published | **0.845** | 0.513 |
| `Withdrawn` excluded (Pass/Distinction vs Fail) | **0.782** | 0.302 |
| Only pre-cutoff withdrawals excluded | **0.753** | — |

**Δ = 0.092.** The paper's entire headline effect — "an ordinary early-warning model loses about 0.1 ROC-AUC when it crosses an institutional boundary" (0.691 → 0.597, Δ = 0.094) — is the same magnitude as one label-definition choice at one institution. §III-A's disclosure ("Label definition and institution are perfectly collinear here") states that the two cannot be separated; it does not tell the reader that the label effect is as large as the transfer effect the paper is selling.

The consequences propagate through every headline, because OULAD dominates the source side:

| D3, gradient boosting | AUC raw | AUC pct | CIL raw | CIL pct | tau raw | tau pct |
|---|---|---|---|---|---|---|
| All 2,912 pairs (paper) | 0.5945 | 0.6150 | **+0.1222** | **−0.0054** | 0.0336 | 0.0183 |
| Excl. OULAD as source (2,076) | 0.5985 | 0.6122 | **+0.0408** | **−0.0714** | 0.0530 | 0.0549 |
| Excl. OULAD as target (2,076) | 0.5661 | 0.5934 | +0.2008 | +0.0625 | 0.0398 | 0.0321 |
| Excl. OULAD both sides (1,240) | 0.5536 | 0.5742 | +0.1174 | −0.0021 | **0.0765** | **0.1027** |

Three things fall out:

- **The calibration repair reverses.** With OULAD off the source side, raw miscalibration is +0.041 and the percentile transform drives it to −0.071. |CIL| goes from 0.041 to 0.071: the transform makes calibration-in-the-large **worse**. The abstract's "restores calibration-in-the-large almost exactly (−0.009)" is a statement about a source pool that is 29 % Open University.
- **Explanation agreement triples.** Without OULAD, cross-institution tau is 0.077 raw and 0.103 percentile, not 0.026/0.018. "A feature ranking indistinguishable from random" (Conclusion) is an OULAD-driven number.
- The AUC headline is the one thing that survives: 0.5945 → 0.5985 excluding OULAD sources.

*Required:* run the ladder with `--drop-withdrawn` as R1 asked, freeze it as an artifact, and report the benchmark with OULAD sources excluded as the primary robustness column, not as an afterthought.

### H-4 [CRITICAL] Thirty per cent of the benchmark has no measurable local signal, and on those cohorts transfer *improves* AUC

Nobody in either round computed a per-cohort interval. The paper's Table in §V-A reports institution means and ranges (Oviedo "0.384–0.953", Zambia "0.455–0.598") with no indication that most of that range is noise.

Recomputed: for each of the 63 cohorts, 5-fold cross-validated GB predictions (paper pipeline), then 2,000 bootstrap resamples of the students for a 95 % percentile interval on D0 AUC.

| Institution | cohorts | CI excludes 0.5 | mean CI width |
|---|---|---|---|
| OULAD | 19 | **19** | 0.045 |
| KU Leuven | 6 | **6** | 0.094 |
| UKZN | 16 | 11 | 0.165 |
| Oviedo | 20 | **8** | 0.181 |
| Zambia | 2 | **0** | 0.320 |
| **Total** | **63** | **44 (70 %)** | 0.123 |

- **19 of 63 cohorts (30 %) have a D0 AUC interval covering 0.5.** All 19 are non-OULAD. Of the 44 non-OULAD cohorts, only 25 (57 %) show a signal distinguishable from chance.
- **`oviedo_C2024_1415` has AUC 0.382, CI [0.298, 0.471]** — reliably *worse* than chance (P(AUC ≤ 0.5) = 0.993 under the bootstrap). A cohort where the model is dependably anti-predictive is in the benchmark and contributes equally to every mean the paper reports.
- **Neither Zambia cohort is distinguishable from chance** (0.597 [0.436, 0.745]; 0.459 [0.296, 0.626]). The abstract's dramatic range endpoint, "0.527 at the University of Zambia", is the average of two coin flips with a mean interval width of 0.320. §V-A's "0.455–0.598" range for Zambia is entirely inside sampling noise.
- The median non-OULAD CI width is **0.169** — **1.8× the paper's entire headline transfer gap of 0.094**. For 28 of the 44 non-OULAD cohorts a 0.09 movement is unmeasurable at the cohort level.

Now the question the brief asked: is the reported degradation measurable at all? Split the ladder by whether the target's own D0 signal is distinguishable from chance (GB):

| Target set | n targets | D0 AUC | D3 raw AUC | **gap** | D3 pct AUC | **gap** |
|---|---|---|---|---|---|---|
| Measurable D0 (CI excludes 0.5) | 44 | 0.7621 | 0.6202 | **+0.1419** | 0.6433 | +0.1187 |
| Not measurable | 19 | 0.5279 | 0.5345 | **−0.0066** | 0.5489 | **−0.0184** |

**On the 19 cohorts where nothing is predictable locally, transfer makes the model very slightly better.** The paper's 0.097 headline is a blend of a real 0.142 effect over 44 cohorts and a null (in fact a small negative) over 19, mixed in an undeclared 44:19 ratio determined by how many small Oviedo and UKZN courses passed a 50-student admission filter. 836 of the 2,912 D3 pairs (28.7 %) transfer *to* a cohort where no model works locally either.

That is a different paper from the one written. The correct statement is: where an engagement-only early-warning signal exists at all, crossing an institution costs about 0.14 AUC; at three of five institutions it does not exist in most cohorts, and there is nothing to lose.

### H-5 [CRITICAL] Round 2's own weighting finding is half-computed, and completing it reverses the paper's only positive result

S1 (round 2) found that every headline is an unweighted mean over pairs, recomputed D3 under student weighting, and concluded: "the D0−D3 AUC gap shrinks correspondingly … the deployment-relevant one is roughly half the reported effect."

**That conclusion is wrong, because S1 weighted D3 and left D0 unweighted.** Weighting both sides:

| Estimand | D0 AUC | D3 raw AUC | **gap** |
|---|---|---|---|
| Pair-mean (paper) | 0.6915 | 0.5945 | **0.0970** |
| Target-cohort mean | 0.6915 | 0.5969 | 0.0946 |
| **Student-weighted** | **0.7843** | **0.6308** | **0.1535** |
| **Institution-pair-weighted** (20 ordered institution pairs) | **0.6511** | **0.5698** | **0.0813** |

The effect is not "roughly half"; it is a range of **0.081 to 0.154**, a factor of 1.9, with the paper's number sitting in the middle. Student weighting makes the gap **58 % larger**, not smaller. Institution weighting — arguably the right estimand for a claim about crossing institutions, since the effective sample size for any cross-institution statement is five institutions and twenty ordered institution pairs, not 2,912 pairs — makes it 16 % smaller.

The damage is not to the AUC claim, which survives every weighting. It is to the calibration claim:

| Estimand | D3 CIL raw | D3 CIL percentile | does the transform help? |
|---|---|---|---|
| Pair-mean (paper) | +0.1222 | **−0.0054** | yes (0.122 → 0.005) |
| Institution-pair-weighted | +0.0845 | −0.0076 | yes |
| **Student-weighted** | **+0.0472** | **−0.0769** | **no (0.047 → 0.077)** |
| **Excl. OULAD as source** | **+0.0408** | **−0.0714** | **no (0.041 → 0.071)** |

**The paper's single defended positive claim — a label-free transform that restores calibration-in-the-large — reverses sign under two of four defensible estimands.** Under student weighting, the population of students who would actually be misclassified is *better* calibrated before the transform than after. The authors have already conceded that per-pair mean |CIL| falls only 0.303 → 0.249; the estimand analysis shows the pair-mean version is not merely weak but estimand-dependent in its direction.

### H-6 [MAJOR] Calibration-in-the-large averaged over a symmetric pair design is structurally blind to the thing it is supposed to measure

Here is why the pair-mean CIL behaves the way it does, which no seat has stated. Regressing per-pair CIL on the prevalence difference between source and target cohort, D3, GB, raw:

> **CIL = 0.908 × (source failure rate − target failure rate) + 0.1222**, r = 0.753, **R² = 0.567**

Under the percentile representation the same regression gives r = **0.980**. Prevalence shift is the whole story, as the paper's §V-C already half-says.

But the ladder evaluates **every ordered pair in both directions**. Therefore Σ(source failure rate − target failure rate) over all D3 pairs is exactly zero — the recomputed mean is **−0.0000**. The prevalence term cancels identically in the pair-mean, leaving only the intercept. **The pair-mean CIL is a statistic that cannot, by construction, see the component that explains 57 % of its own variance.** The "restoration from +0.119 to −0.009" is a statement about a residual intercept and nothing else.

That the intercept can be removed by a label-free intercept recalibration on the source base rate (which the authors verified beats the percentile transform: |CIL| 0.239 vs 0.249, Brier 0.310 vs 0.322) is now unsurprising: removing an intercept is all that is left to remove.

The per-source-institution decomposition shows the cancellation directly:

| Source institution | D3 pairs | mean failure rate | mean CIL |
|---|---|---|---|
| OULAD | 836 | 0.513 | **+0.325** |
| Zambia | 122 | 0.685 | +0.265 |
| Oviedo | 860 | 0.458 | +0.196 |
| KU Leuven | 342 | 0.348 | +0.092 |
| UKZN | 752 | 0.178 | **−0.196** |

*Required:* report mean |CIL| per pair (0.303 → 0.249) as the headline and delete "restores calibration-in-the-large almost exactly" from the abstract. A signed mean over an antisymmetric design is not a calibration result.

### H-7 [MAJOR] Both restored positive results are sample-size artefacts, and I ran the controls

The authors intend to restore two deleted findings: pooled within-institution training (0.686) nearly matching local training (0.691), and few-shot k = 100 (0.712) exceeding it. Both fail their controls.

**(a) Pooled ≈ local is a data-volume result.** The pooled model trains on the union of every other cohort at the institution — a mean of **11,774 rows** against a local 5-fold CV training fold of roughly **574** rows (0.8 × mean cohort size 717). A 20× data advantage is not a transfer finding.

I ran the size-matched control: cap the within-institution pool at 0.8 × n_target rows, label-stratified, same model, same seed, same evaluation.

| GB, mean over 63 targets | local D0 | pooled (full pool) | **pooled, size-matched** |
|---|---|---|---|
| raw | 0.6915 | 0.6857 | **0.6507** |
| percentile | 0.6922 | 0.6986 | **0.6509** |

Given the same number of training rows the local model gets, the pooled model **loses by 0.041 AUC** — a gap almost half the paper's entire cross-institution headline. Per institution the size-matched pool loses everywhere except OULAD, where it draws (0.841 vs 0.845) on a 29,000-row pool:

| Institution | local D0 (raw) | pooled size-matched (raw) |
|---|---|---|
| OULAD | 0.845 | 0.841 |
| UKZN | 0.667 | 0.625 |
| KU Leuven | 0.611 | 0.585 |
| Oviedo | 0.606 | 0.525 |
| Zambia | 0.527 | 0.502 |

**(b) The pooled comparison is also contaminated by the paper's own §V-G hazard, in a worse form.** `P_in_leave_one_cohort_out` pools every same-institution cohort, i.e. the union of all that target's D1 and D2 sources — precisely the pairs the authors flag as contaminated. From `exp_017/pair_overlap.csv`, the share of the target cohort's students already present in the pool (lower bound = largest single overlapping source; upper bound = sum, capped at 1):

| Institution | lower bound | upper bound |
|---|---|---|
| UKZN | **0.693** | 0.948 |
| KU Leuven | **0.659** | 0.765 |
| Oviedo | 0.388 | 0.396 |
| OULAD | 0.108 | 0.272 |
| Zambia | 0.000 | 0.000 |
| **All 63 targets** | **0.395** | 0.521 |

55 of 63 targets have some overlap; 15 have an upper bound of 1.0. §V-G says this hazard invalidates the D1/D2 rungs. The restored positive result is built on the union of those same rungs and nobody connected the two.

**Honest counter-finding:** I re-evaluated the pooled model on only the target students absent from the pool, and the effect is small — mean AUC moves 0.6857 → 0.6839 (raw) and 0.6986 → 0.6963 (percentile). It is material only at KU Leuven (0.636 → 0.576, raw) and Oviedo (0.587 → 0.566). **Contamination is not the driver here; training-set size is.** I record the null because it matters that the reader can tell which of my objections has a number behind it.

*Verdict on (a)+(b):* "pooling within an institution nearly matches local training" must be restated as "a model trained on 20× more data from the same institution nearly matches, and given equal data loses by 0.041." That is a sample-size result and belongs in a sentence, not a section.

**(c) Few-shot k = 100 does not exceed local training. It is a composition artefact.** `run_fewshot:347` skips any (target, k) with `k ≥ t.n − 30`, so the averaged cohort set shrinks with k: **63 targets at k = 0, 62 at k = 25, 61 at k = 50, 49 at k = 100.** Round 1's C9 identified this mechanism for a *flat* curve in an earlier run; the current claim is the opposite one and has not been rechecked against it.

On the balanced panel of the 49 targets present at every k:

| | k = 0 | k = 25 | k = 50 | k = 100 | local D0 (pct) on the same 49 |
|---|---|---|---|---|---|
| Reported (changing cohort set) | 0.6822 | 0.6927 | 0.6990 | **0.7123** | 0.6922 (all 63) |
| **Balanced panel (49 targets)** | 0.6951 | 0.7046 | 0.7094 | **0.7123** | **0.7099** |

**The reported +0.020 margin over local training collapses to +0.0024.** Few-shot adaptation with 100 target labels *reaches* local training; it does not exceed it. The 14 dropped cohorts are the small ones by construction (`k ≥ n − 30` selects on cohort size) — the same ones where the local model is weakest — so removing them raises the local reference by 0.018, which is roughly the whole claimed effect. Two further confounds remain unaddressed: `idx_eval = perm[k:]` means each k is scored on a different evaluation population, and local D0 is scored on all n by cross-validation while few-shot is scored on n − k held-out rows.

**Does the pooled source contribute anything at all?** I ran the missing arm: at k = 100, on the 49 eligible targets × 5 seeds, with all four configurations scored on the *identical* held-out rows.

| k = 100 control (49 targets × 5 seeds, same evaluation rows) | mean AUC |
|---|---|
| **No model — rank the held-out rows by `cum_active_days`** | **0.7301** |
| Pooled 4-institution source + 100 target labels | 0.7122 |
| Pooled source alone (k = 0) | 0.6950 |
| 100 target labels alone, no source | 0.6837 |

**Honest positive for the authors:** the pooled source is worth +0.029 over the 100 target labels alone, and the 100 labels are worth +0.017 over the pooled source alone. Few-shot adaptation is real and both ingredients contribute. That is a defensible sentence and it is the one the paper should write.

**But it does not escape H-1.** The best-performing configuration in the entire paper — a four-institution pooled source plus 100 labelled target students — scores 0.7122 against 0.7301 for sorting the same held-out students by login-days. Per institution the free rule wins at KU Leuven (0.653 vs 0.629) and UKZN (0.716 vs 0.666), ties at OULAD (0.830 vs 0.828) and Oviedo (0.606 vs 0.607). **Nothing the paper builds beats the baseline it never ran, at any rung, under any representation, with or without target labels.**

*Required:* fix the evaluation set to `perm[max(ks):]` for every k, report the balanced panel and the k-only arm, and state the claim as "100 target labels recover local performance, and the pooled source contributes 0.029 of that" — with the no-model baseline in the same table.

---

## 2. Challenge-by-challenge

### C1 — The cutoff [CRITICAL, partially sustained]
Established in H-2. **Sustained at D1 and D2, rejected at D3.** Inferred course length is systematically longer than the real teaching period at all three Moodle institutions (mean cutoff position of 0.457–0.465 of the last week with ≥ 25 % of students active, against 0.362 at OULAD and 0.322 at KU Leuven), and the 1/3 cutoff therefore lands at very different pedagogical moments — 25 % of the course's activity at KU Leuven, 50 % at OULAD. The D1 rung's entire degradation is confined to the inferred-calendar institutions and a third of it is explained by cutoff mismatch. The D3 gap is not explained by it (R² = 0.007).

**Supplementary structural point, new:** two of the seven canonical features have institution-specific supports fixed entirely by the cutoff week. `active_weeks` and `weeks_since_active` are both bounded above by the cutoff. Mean per-cohort maxima: KU Leuven 5.8, UKZN 8.25, Oviedo 11.15, OULAD 12.5, Zambia 13.0. **An OULAD-trained tree's splits on `active_weeks ∈ (6, 13)` are unreachable for every KU Leuven student.** This is a harder non-comparability than the accepted "KU Leuven social clicks are 99.9 % zero" point, because it is created by the paper's own relative-cutoff design rather than inherited from the platforms, and it is a mechanism for why the percentile transform helps AUC at D3 (0.597 → 0.617) while doing nothing for prevalence shift.

### C2 — The label [CRITICAL, sustained]
Established in H-3. 60.9 % of OULAD failures are withdrawals; 68.6 % of those were administratively complete before the prediction week; that is 22.5 % of OULAD's students and 15 % of the whole benchmark's student-rows. Removing them costs 0.092 AUC at OULAD — the size of the paper's headline. OULAD is on one side of 57.4 % of D3 pairs, and with it removed from the source side both the calibration repair and the explanation-collapse finding change materially (calibration reverses; tau triples).

### C3 — Is there a signal at all [CRITICAL, sustained and worse than posed]
Established in H-4. 19 of 63 cohorts have D0 intervals covering 0.5; one is reliably anti-predictive; both Zambia cohorts are noise; the median non-OULAD interval is 1.8× the headline gap. On the unmeasurable 19, transfer *improves* AUC by 0.007–0.018, so the reported degradation is a mixture of a 0.142 effect and a null in an undeclared ratio.

### C4 — Does the benchmark measure what it claims [CRITICAL, sustained]
Established in H-5. The estimand is never declared. The headline gap moves between 0.081 (institution-weighted) and 0.154 (student-weighted), and round 2's own partial computation reached the wrong conclusion by weighting one side only. The calibration headline reverses sign between estimands. Add to this that cohorts range 82–2,498 students and 19 of 63 come from one institution while 2 come from another: the effective independent sample for any cross-institution claim is five institutions.

### C5 — The surviving positive results [MAJOR, both defeated]
Established in H-7. Pooled ≈ local is a 20× data advantage (size-matched: −0.041) plus, at two institutions, a 66–69 % student overlap that reproduces the paper's own §V-G hazard. Few-shot k = 100 "exceeding" local is a 49-vs-63 cohort composition artefact; on the balanced panel the margin is +0.0024. The one genuinely positive residue, which I ran the control for and which the authors may keep: at k = 100 the pooled source is worth +0.029 over target labels alone. It still loses to the no-model rule (0.712 vs 0.730).

### C6 — Other things that would not survive a methodologist

**[CRITICAL] No baseline for the ranking metrics.** H-1. This is the finding.

**[MAJOR] The feature space has ~1.5 effective dimensions.** PC1 explains 0.541–0.686 of the standardised canonical feature variance within institution. The paper says permutation rankings are "weakly identified"; the correct statement is that seven near-collinear coordinates of a one-dimensional construct have no identified ordering at all, so §V-E's ceiling of 0.338 is not a property of the estimator or of the cohorts but of the schema. This is worth saying explicitly, because it means the finding generalises to any paper using these seven features, which is the paper's most transferable contribution and it is currently buried.

**[MAJOR] The D0 estimator is not the same estimator as D1–D3.** D0 is `cross_val_predict` over 5 folds — predictions pooled from five different models with five different calibrations — while every other rung is a single model applied out of sample. The pooled-fold Brier and CIL at D0 are therefore not commensurable with the Brier and CIL at D1–D3, and the "D0 CIL = −0.008" against which "+0.119" is contrasted is partly a property of stratified CV reproducing the cohort's own base rate. Every calibration comparison in §V-C compares an ensemble-of-five to a single fit.

**[MINOR] The fairness table's Race row is one cohort.** `exp_020/summary.csv` gives `UKZN, RACE, local, observations = 1`. §V-F reports "Race (UKZN) gap, local 0.102" beside three rows with 16–19 observations, with no indication that this one is a single cohort's single number. Given that S2 has already shown the local arm is a resubstitution fit, this row should be deleted rather than caveated.

**[MINOR] `n_weeks` for KU Leuven is `max(week_number)`, not the published calendar.** `run_transfer_ladder.py:64` uses the observed maximum despite the cache carrying `n_semester` and `course_week_progress`. It happens to agree (13/13/13, 15/15/15), so nothing moves — but §III-B implies a calendar is used and the code does not use it. Say what the code does.

---

## 3. What Is Left That Is True

Stripping everything that two prior panels and this one have removed, the following claims survive every check I ran and I would defend them in a rebuttal:

1. **The benchmark exists and the counts are right.** 63 cohorts, five institutions, five platforms, four countries, 45,158 cohort-rows, 35,529 distinct students, 21.3 % appearing more than once. Five adapters emitting one schema. Verified against `cohorts.csv`, `student_counts.csv` and the parquet caches. This is a real resource and nothing above touches it.

2. **The features are leakage-safe with respect to the cutoff.** Round 1 verified the cumsum construction; I re-derived the canonical frame independently and reproduced the shipped D0 AUCs to three decimals at OULAD. The prediction point contains no post-cutoff observation. (The OULAD *label* is a different matter — H-3 — but that is a label problem, not a feature-leakage problem.)

3. **Discrimination degrades across institutions, and it degrades under every estimand.** D0 → D3 raw: 0.097 (pair-mean), 0.095 (target-mean), 0.154 (student-weighted), 0.081 (institution-weighted), 0.142 (restricted to targets with measurable local signal), and 0.004 in the wrong direction on the 19 targets without one. The sign and the rough magnitude are robust; the precision the paper claims is not, and the estimand must be declared.

4. **Calibration degrades much more than discrimination does, and the degradation is prevalence shift.** CIL = 0.908 × Δprevalence + 0.122, R² = 0.567 raw and r = 0.980 under percentile. Mean per-pair |CIL| 0.303 raw. This is a real and useful finding. What is not true is that the pair-mean is the right way to report it or that the percentile transform repairs it.

5. **The percentile transform buys about 0.02 AUC at D3 and nothing at the decision.** 0.5945 → 0.6150; recall@20 0.2724 → 0.2732. Both hold under OULAD exclusion and student weighting. The AUC gain is small, real and correctly characterised in the paper as not a performance fix.

6. **Permutation-importance rankings over these seven features are weakly identified before transfer.** Ceiling 0.338 (ladder-matched), floor 0.707, random 0.000/0.303. Round 1 verified the estimator is not the cause; I add the reason (PC1 = 0.54–0.69). The specific number "0.026 at D3, indistinguishable from random" is OULAD-driven (0.077–0.103 without it) and must be restated, but the qualitative finding stands and is the paper's most transferable contribution.

7. **Few-shot adaptation genuinely works, at the size the paper claims.** At k = 100, scored on identical held-out rows: pooled + k = 0.7122, pooled alone = 0.6950, k alone = 0.6837. Both ingredients contribute. This is the only positive modelling result in the paper that survives its control, and the paper currently states it wrongly (as exceeding local training, which it does not).

8. **The two methodological hazards are real and worth publishing.** F1 on the majority class flatters every model; 72 of 78 same-course pairs share students, up to 94 % of the target. Both are audits of the authors' own pipeline and both generalise. The *correction* built on the second one (D1 0.715 → 0.656) does not survive — 10 clean pairs, and H-2 shows the residual is a calendar artefact — but the audit is the contribution, not the correction.

9. **The label/institution collinearity disclosure is correct and honestly stated**, and is now quantified: the label effect at OULAD alone is 0.092 AUC against a 0.094 transfer effect. The paper should promote this from a limitation to a result.

That is a resource paper with one solid negative empirical finding, one measurement decomposition, two reusable hazards, and a quantified warning that engagement-only early-warning models are not worth building at four of five institutions. It is publishable. It is not the paper that is written.

---

## 4. Verdict

**REJECT.** Resubmittable as a substantially different paper.

The paper survives its second panel by retreating to honesty: it reports its own failed hypotheses, discloses its own hazards, and frames itself as a benchmark rather than a method. That retreat is not far enough, because it left the benchmark's reference configuration unexamined. A benchmark whose default model loses to `sort by login-days` in 38 of 63 cohorts, and whose transferred model beats that rule in 9 % of cross-institution pairs, does not measure "what an ordinary early-warning model does when it leaves home". It measures what a gradient-boosting model overfitted to seven collinear count features on 82–700 rows does when it leaves home, and the interesting fact — that it should never have left, because it should never have been fitted — is nowhere in the manuscript.

Three things must happen before this is resubmittable:

1. **Add the no-model ranking baseline to every table at every rung** (H-1), and rewrite the contribution list around what it shows. If the paper's answer to "should I transfer a model?" is "no, and also you did not need one", that is a stronger and more publishable result than the one currently claimed, and it is what the data say.
2. **Run the withdrawal control and report OULAD-excluded columns as primary robustness** (H-3). It was demanded in round 1, deleted rather than run, and it moves the calibration and explanation headlines.
3. **Declare the estimand, report per-cohort intervals, and delete D1** (H-2, H-4, H-5). The ladder should be D0 / D2 / D3 with institution-level clustering, per-cohort intervals in §V-A, and an explicit statement that 19 of 63 cohorts have no measurable local signal and contribute a null to every mean.

The two positive results the authors intend to restore should not be restored in their current form (H-7). "Given equal training data, within-institution pooling loses 0.041" and "100 target labels recover local performance" are the true versions, and both are one sentence long.

Confidence: high on H-1, H-3, H-4, H-5, H-6, H-7(a) and H-7(c) — each rests on a computation I ran against the shipped data and, where a paper number was checkable, reproduced it first. Medium on H-2, which is confined to D1/D2 and contradicts a prior seat's negative test; I have given the reason the tests differ and recorded the D3 result that cuts against me. H-7(b)'s contamination arm is a recorded null.

---

### Reproduction notes

Every number above comes from one of:
- `data/artifacts/experiments/exp_014_transfer_ladder/f33/{pairs,pooled,fewshot,cohorts}.csv`
- `data/artifacts/experiments/exp_017_contamination/f33/pair_overlap.csv`, `exp_015`, `exp_018`, `exp_020` summaries
- `datasets/cache/*.parquet`, `datasets/ukzn/cache/*.parquet`, `datasets/oulad/{studentInfo,studentRegistration,courses}.csv`
- refits using `src.experiments.transfer_benchmark` and `src.experiments.models` at seed 42, fraction 0.33, unchanged from the paper's pipeline.

Recomputations that reproduce published numbers exactly, as a check on my pipeline: OULAD D0 mean 0.845; all-63 D0 raw 0.6915 / percentile 0.6922; D3 raw 0.5945 / percentile 0.6150; D3 raw CIL +0.1222; D3 recall@20 0.2724 / 0.2732; exp_017 contamination counts 72/78 and 324/916.
