# S1 — Statistics and Reproducibility Review (Round 2)

**Manuscript:** `docs/dissertation/side2026_paper.md` (rewrite)
**Tables:** `docs/dissertation/side2026_tables.md`
**Artifacts interrogated:** `exp_014_transfer_ladder/{f25,f33,f50}`, `exp_016_shift_analysis`, `exp_017_contamination`, `exp_018_explanation_ceiling`, `exp_019_threshold_transfer`, `exp_020_fairness`, `datasets/_candidates/oviedo/tables`
**Code read:** `services/ml/src/experiments/transfer_benchmark.py`, `run_transfer_ladder.py`, `run_explanation_ceiling.py`, `run_contamination_audit.py`, `services/ml/src/benchmarks/oviedo_adapter.py`

Every number below was recomputed from the released CSVs unless marked otherwise. Where I quote the paper I quote it verbatim.

---

## Summary

The rewrite is a better paper than the abstract's four bullet points suggest, and its two negative results (the flag-budget null and the F1/trivial-baseline hazard) are the most defensible things in it. But the paper's *positive* headline — "calibration collapses and a label-free percentile transform restores calibration-in-the-large almost exactly (−0.009)" — is, on the released data, **an arithmetic identity of the experimental design rather than an empirical finding**, and I can demonstrate that to three decimal places. Three further problems are serious enough to block acceptance in the current form:

1. **The calibration result is a theorem, not a measurement.** Under the percentile representation, per-pair calibration-in-the-large equals (source failure rate − target failure rate) with R² = 0.961. The D3 pair set is *exactly* closed under source/target swap, so the mean of that quantity is 0.000000 by construction at every rung. Mean |CIL| under percentile is **0.249**, not ~0. 78 % of D3 pairs still miscalibrate by more than 10 points. Nothing was restored.
2. **The paper's headline numbers do not reproduce from the released artifacts.** `aggregate.csv` gives D3 GB/raw AUC = 0.5945 and D1 = 0.7533; the paper says 0.597 and 0.715. `exp_017/clean_vs_all.csv` — which the paper quotes — gives 0.5969 and 0.7149 on the *same 2912 and 78 pairs*. Two artifacts of the same pipeline disagree. The D1 discrepancy (0.038) is larger than several effects the paper claims.
3. **The uncertainty is understated by 3.6× to 16×.** Clustering the bootstrap on institution — the level at which every headline claim is stated — the D3 raw CIL of +0.122 has a 95 % CI of **[−0.053, +0.325]**. The paper's central positive claim is not distinguishable from zero.

A fourth, less visible problem: **the explanation "ceiling" of 0.338 is estimated on one third of each cohort while the ladder trains on whole cohorts**, and the ceiling rises from 0.214 to 0.396 across cohort-size quartiles. The paper's most quoted negative claim rests on a statistic confounded with sample size.

I recommend **major revision** with a specific, cheap set of re-analyses that I believe the data can support.

---

## Claims That Survive

### (d) The percentile transform does not improve the decision at a 20 % flag budget — SURVIVES, and gets stronger

Recomputed from `exp_014/f33/pairs.csv`, gradient boosting, D3, n = 2912 paired pairs:

| | recall@20 | lift@20 | Brier | AUC |
|---|---|---|---|---|
| raw | 0.2712 | 1.3583 | 0.3626 | 0.5945 |
| percentile | 0.2732 | 1.3685 | 0.3223 | 0.6150 |

Paired Δrecall = **+0.0020**. Bootstrap intervals, four resampling schemes:

```
iid pairs              [-0.0014,+0.0054]   width 0.0068  (paper's scheme)
cluster: target        [-0.0038,+0.0080]   width 0.0118  x1.75
cluster: source        [-0.0106,+0.0137]   width 0.0244  x3.61
cluster: target inst.  [-0.0162,+0.0200]   width 0.0361  x5.35
```

Zero is inside every interval including the paper's own. This is a real null and it is robust. Good.

`exp_019/summary.csv` confirms the trivial-rule comparison exactly: D3 f1_fail_baseline = **0.5457** (paper: 0.546), best rule 0.4207 (raw, fixed 0.5), source-rate rule recovers percentile to 0.4147 (paper: 0.415) and *degrades* raw to 0.4057 (paper: 0.406); `beats_baseline_share` maxes at 0.2709 (paper: "no more than 27 %"). All four verbatim.

**One caveat the paper should add.** Recall@20 has an arithmetic ceiling of min(1, 0.20/prevalence). Averaged over D3 targets that ceiling is 0.582. So the transferred model attains **0.2712 / 0.582 = 46.6 %** of the attainable recall, against 0.3264 / 0.5786 = 56.4 % within cohort. The honest deployment framing is "half the headroom a perfect ranker would get at this budget", which is more informative and no less flattering than "36 % more than random".

### (g) Same-course pairs share students — the *audit* survives; the *correction* does not

`exp_017/f33/pair_overlap.csv`: **72 of 78** D1 pairs have contamination > 0. Verbatim. D3 is genuinely clean: 78 of 2912, max 0.0150. The audit itself is sound, valuable, and the correct thing to have done.

The 94 % figure is misattributed in the abstract. Max contamination is **0.8311 at D1** and **0.9375 at D2**. The abstract's "72 of 78 same-course transfer pairs share students between training and evaluation, up to 94 % of the target cohort" reads as though 94 % is a same-course figure; it is the D2 maximum. Section V-G's phrasing is defensible; the abstract's is not. (See below for why the quantitative correction fails.)

### (a) The signal is institution-specific — SURVIVES directionally, but the range is over-narrated

Recomputed D0 GB/raw from `pairs.csv` × `cohorts.csv`:

| Institution | k | mean | sd | min | max | median n |
|---|---|---|---|---|---|---|
| OULAD | 19 | 0.845 | 0.044 | 0.709 | 0.897 | 1614 |
| UKZN | 16 | 0.667 | 0.091 | 0.536 | 0.814 | 261 |
| KU Leuven | 6 | 0.611 | 0.028 | 0.586 | 0.653 | 718 |
| Oviedo | 20 | 0.606 | 0.136 | 0.384 | 0.953 | 131 |
| Zambia | 2 | 0.527 | 0.101 | 0.455 | 0.598 | 59 |

The OULAD-vs-rest contrast is large and real. The bottom of the range is not. Zambia's 0.527 is the mean of two 5-fold-CV AUCs on 52 and 65 students (0.455, 0.598); on ~58 students with ~22 in the minority class the standard error of a single AUC is ≈ 0.08, so this is one draw with a ±0.16 interval. Oviedo's 0.606 has a within-institution sd of 0.136 across cohorts of median n = 131, with six cohorts at or below 0.51 and one at 0.953 — a spread consistent with a large share of pure estimation noise. Writing "ranges from 0.845 at the Open University to 0.527 at the University of Zambia" as the abstract's first result presents the noisiest endpoint of a 63-cohort scatter as a finding. The claim would be just as strong and honest as "OULAD 0.845 (19 cohorts, median n = 1614) versus 0.61–0.67 elsewhere, with the small-cohort institutions too noisy to order".

### (b) Discrimination degrades gradually — SURVIVES directionally, but not at the stated precision

D0−D3 gap, GB/raw, per pair = **0.0931**. Institution-clustered 95 % CI **[0.0345, 0.1545]**; still excludes zero, and stays out under an 18-way Bonferroni interval [0.0279, 0.1696]. The direction is safe.

The stated precision is not. The paper says "The gap is 0.09 to 0.13 depending on the estimator, and we report both rather than the flattering one." Its own Table II `D0-D3 loss` column runs **0.087 (LR/zscore) to 0.176 (LR/raw)**. 0.176 is not in "0.09 to 0.13". Across the nine (model × representation) cells on all 63 targets I get gaps from 0.049 (RF/zscore) to 0.115 (LR/raw), and only 6 of the 9 have institution-clustered intervals excluding zero:

```
model                rep         gap     lo95     hi95   loBonf18  hiBonf18
gradient_boosting    percentile  0.0735  0.0157   0.1445   0.0132   0.1628
gradient_boosting    raw         0.0931  0.0354   0.1510   0.0279   0.1696
gradient_boosting    zscore      0.0764  0.0122   0.1540   0.0009   0.1763
logistic_regression  percentile  0.0600  0.0140   0.0939  -0.0334   0.1006
logistic_regression  raw         0.1146  0.0208   0.2155   0.0047   0.2530
logistic_regression  zscore      0.0563  0.0085   0.0942  -0.0297   0.1037
random_forest        percentile  0.0509 -0.0098   0.1129  -0.0346   0.1272
random_forest        raw         0.0598  0.0073   0.1077  -0.0173   0.1112
random_forest        zscore      0.0494 -0.0108   0.1131  -0.0715   0.1368
```

### (e) Explanation rankings were weak before transfer — SURVIVES as a direction, fails as a number

The *ordering* floor 0.707 > D1 0.226 > D2 0.089 > D3 0.034 is monotone and robust. Instance-pair-clustered intervals:

```
D1 raw  tau=+0.2259  [+0.1762,+0.2875]  excludes 0
D2 raw  tau=+0.0889  [+0.0383,+0.1722]  excludes 0
D3 raw  tau=+0.0336  [+0.0034,+0.0669]  excludes 0 (barely)
D3 zscore tau=+0.0263 [-0.0172,+0.0785] INCLUDES 0
D3 pct  tau=+0.0183  [-0.0290,+0.0728]  INCLUDES 0
```

The claim "cross-institution agreement sits barely above the random baseline" is right. Everything else about this section is quantitatively broken — see below.

### exp_016 shift-decomposition numbers — REPRODUCE exactly

GB: `corr_d_scale` 0.0669 → 0.0774 (paper: "0.067 to 0.077"); `corr_d_shape` 0.2829 → 0.1892 (paper: "0.283 to 0.189"); `r2` 0.1156 → 0.0622 (paper: "0.116 to 0.062"). Clean.

One assertion in the same paragraph is not supported: "Prevalence shift, the largest component at D3". For GB/raw, `corr_d_prevalence` = 0.194 and `corr_d_shape` = 0.283. Shape has the *larger* correlation with AUC loss. If "largest" means largest magnitude of shift rather than largest association, say so; as written it contradicts the table it cites.

---

## Claims That Do Not Survive

### 1. [CRITICAL] The calibration finding is a near-identity of the design, not a result

**Claim (c):** "the within-cohort percentile representation removes that bias almost exactly, at every rung, without a single target label."

`represent()` maps each cohort's features to `x.rank(pct=True)`. Source and target are *both* mapped to Uniform[0,1] within themselves. The transferred model therefore sees, at test time, the same marginal feature distribution it was trained on, so its mean output on the target ≈ its mean output on the source ≈ the source base rate. Per-pair calibration-in-the-large is then forced to (source failure rate − target failure rate).

Measured, GB, D3, n = 2912:

| representation | corr(CIL, src_fail − tgt_fail) | R² | slope | MAE |
|---|---|---|---|---|
| raw | 0.7530 | 0.567 | 0.908 | 0.2000 |
| zscore | 0.9625 | 0.926 | 1.038 | 0.0605 |
| **percentile** | **0.9802** | **0.961** | **1.021** | **0.0423** |

And the pair set is *exactly* closed under source/target swap at every rung, so the mean of (src − tgt) is identically zero:

```
distance               n     mean(src_fail-tgt_fail)  closed-under-swap  meanCIL(pct)
D0_within_cohort      63     +0.000000                True               -0.00635
D1_same_module        78     +0.000000                True               +0.00049
D2_other_module      916     -0.000000                True               +0.00475
D3_other_institution 2912    -0.000000                True               -0.00544
```

That is the whole finding. The percentile transform converts CIL into a quantity whose pooled mean the design forces to zero, "at every rung", automatically. It would do so on random labels.

**What the transform actually achieves, measured on absolute error, which is the only honest summary of a signed quantity:**

| distance | mean \|CIL\| raw | mean \|CIL\| pct | change |
|---|---|---|---|
| D1 | 0.1031 | 0.0586 | −43.2 % |
| D2 | 0.1993 | 0.1483 | −25.6 % |
| **D3** | **0.3028** | **0.2486** | **−17.9 %** |

At D3, **89.2 %** of percentile pairs still have |CIL| > 0.05 and **77.9 %** have |CIL| > 0.10 (raw: 90.4 % and 81.7 %). Quantiles of D3 percentile CIL: q05 −0.478, q25 −0.235, median −0.005, q75 +0.227, q95 +0.466. The distribution is a wide symmetric smear centred on zero. That is not calibration; that is cancellation.

The cancellation is visible institution by institution. D3 CIL by target institution, GB:

| target | n | CIL raw | CIL pct | \|CIL\| pct |
|---|---|---|---|---|
| UKZN | 752 | **+0.4395** | **+0.3037** | 0.3100 |
| KU Leuven | 342 | +0.1735 | +0.0290 | 0.1820 |
| Oviedo | 860 | +0.0645 | −0.0838 | 0.2211 |
| OULAD | 836 | **−0.0730** | **−0.1742** | 0.2409 |
| Zambia | 122 | **−0.2326** | **−0.2990** | 0.3020 |

The abstract's "A transferred model over-predicts failure risk by 12 percentage points" is false at two of five institutions, where it *under*-predicts by 7 and 23 points. And the percentile transform makes OULAD and Zambia strictly worse.

This does not mean the section should be deleted. It means the section is measuring **prevalence shift**, which the paper itself half-recognises in V-C ("Prevalence shift... survives the transform untouched — which is precisely why it repairs calibration-in-the-large"). The correct claim is the opposite of the one made: the transform *does not touch* prevalence shift, and since post-transform CIL ≈ prevalence shift, the transform does not repair calibration at all. It only removes the *pooled mean* of a quantity that the ordered-pair design already averages to zero.

### 2. [CRITICAL] The Brier improvement does not come from the claimed mechanism

**Claim (c) continued:** percentile "improves the Brier score, so it is a recalibration device rather than a performance fix."

Per pair, exactly, `BS = Var(risk − fail) + CIL²`. Decomposing the D3 means:

| rep | mean BS | mean(CIL²) | = mean(CIL)² | + Var(CIL) | residual Var(risk−fail) |
|---|---|---|---|---|---|
| raw | 0.3626 | 0.1323 | 0.0149 | 0.1173 | 0.2304 |
| percentile | 0.3223 | 0.0877 | 0.0000 | 0.0877 | 0.2346 |

Paired over the same 2912 pairs: ΔBrier = **−0.0403** = ΔCIL² (**−0.0446**, 110 %) + Δresidual (**+0.0042**, −10 %).

Of that −0.0446, only **−0.0149 (33 %)** comes from the statistic the paper reports (the squared pooled mean). The other **−0.0297 (67 %)** comes from shrinking the *variance* of CIL across pairs — a quantity the paper never reports. So two thirds of the Brier gain is attributable to a mechanism the paper does not name, and the residual (refinement/sharpness) term actually gets slightly *worse*.

Simultaneously, the transform *is* a performance fix, contradicting the sentence quoted above:

| model | D3 AUC raw | D3 AUC pct | Δ |
|---|---|---|---|
| gradient boosting | 0.594 | 0.615 | **+0.020** |
| logistic regression | 0.598 | 0.650 | **+0.052** |
| random forest | 0.628 | 0.637 | +0.009 |

The paired ΔAUC of +0.0205 survives every clustering scheme (source-clustered [+0.0042, +0.0364]). The paper's own Table II shows LR raw 0.599 → LR percentile 0.684 at D3, +0.085. Calling a representation that buys 2 to 8.5 AUC points "a recalibration device rather than a performance fix" is not supportable from these artifacts.

**Also unreported: z-score does almost everything percentile does.** D3 GB: CIL +0.0093, Brier 0.3279, AUC 0.6107 — versus percentile −0.0054, 0.3223, 0.6150. The abstract and Section V-C present percentile as *the* transform; the artifacts show two of the three representations behave the same way, which is what you would expect if the mechanism is "any within-cohort standardisation removes the scale/shape component", not something specific to ranks.

### 3. [CRITICAL] The headline numbers do not reproduce from the released artifacts

`exp_014/f33/aggregate.csv` and `exp_017/f33/clean_vs_all.csv`, gradient boosting / raw, identical pair counts:

| distance | n_pairs | `aggregate.csv` | `clean_vs_all.csv` "all pairs" | paper |
|---|---|---|---|---|
| D0 | 63 | 0.6915 | 0.6915 | 0.691 |
| D1 | 78 | **0.7533** | **0.7149** | 0.715 |
| D2 | 916 | 0.6504 | 0.6513 | — |
| D3 | 2912 | **0.5945** | **0.5969** | 0.597 |

I re-derived `aggregate.csv` from `pairs.csv` directly (0.5945 / 0.3626 Brier) and confirmed the merge in `run_contamination_audit.recompute_clean` is row-preserving (35721 rows in, 35721 out). So `exp_017` was run against a different ladder output than the one released, and the paper quotes `exp_017`.

The same offset appears in the Section V-H sensitivity table at all three cutoffs:

| cutoff | artifact D0 | paper D0 | artifact D3 raw | paper | artifact D3 pct | paper | artifact CIL raw | paper | artifact CIL pct | paper |
|---|---|---|---|---|---|---|---|---|---|---|
| f25 | 0.669 | 0.669 | **0.585** | 0.587 | 0.615 | 0.616 | **+0.124** | +0.120 | **+0.002** | −0.001 |
| f33 | 0.691 | 0.691 | **0.594** | 0.597 | 0.615 | 0.617 | **+0.122** | +0.119 | **−0.005** | −0.009 |
| f50 | 0.723 | 0.723 | **0.621** | 0.624 | 0.651 | 0.654 | **+0.128** | +0.125 | **+0.003** | −0.000 |

A systematic +0.003 AUC / −0.003 CIL offset at every cutoff. D0 matches exactly; only the transfer rungs differ. Whatever the cause, **a reader who downloads the released benchmark and runs the analysis gets different numbers from the ones in the paper**, and for a paper whose stated contribution is "we release the benchmark and the frozen results so the next proposed fix can be measured against the same ladder", that is disqualifying until fixed. The D1 gap of 0.038 is larger than the entire percentile ΔAUC the paper reports.

### 4. [CRITICAL] Uncertainty is understated by 3.6× to 16×, and the central claim loses significance

`aggregate()` bootstraps rows of `pairs.csv` i.i.d. Pairs share targets, sources, and institutions. Recomputed, GB, D3, 4000 resamples:

**D3 raw AUC (mean 0.5945)**
```
iid pairs             [0.5900, 0.5990]  width 0.0089   x1.00
cluster: target       [0.5787, 0.6109]  width 0.0323   x3.61
cluster: source       [0.5775, 0.6108]  width 0.0333   x3.73
cluster: inst. pair   [0.5634, 0.6257]  width 0.0623   x6.98
cluster: target inst. [0.5558, 0.6396]  width 0.0837   x9.38
```

**D3 raw calibration-in-the-large (mean +0.1222) — the paper's headline positive claim**
```
iid pairs             [+0.1101, +0.1344]  width 0.0244   x1.00
cluster: target       [+0.0617, +0.1831]  width 0.1214   x4.98
cluster: source       [+0.0576, +0.1828]  width 0.1252   x5.14
cluster: inst. pair   [-0.0278, +0.2653]  width 0.2931   x12.03
cluster: target inst. [-0.0529, +0.3252]  width 0.3781   x15.52  <-- INCLUDES ZERO
```

**D3 percentile CIL (mean −0.0054) — the claimed "restoration"**
```
iid pairs             [-0.0163, +0.0053]  width 0.0216   x1.00
cluster: target inst. [-0.1587, +0.1906]  width 0.3492   x16.20
```

Consequences:

- "A transferred model over-predicts failure risk by 12 percentage points" is a claim about *institutions*. Clustered at that level it is **not distinguishable from zero**. There are five institutions; the effective sample size for a between-institution claim is 5, and one of them (UKZN) supplies the entire effect.
- The "restoration to −0.009" is an equivalence claim with an institution-clustered interval of ±0.17. You cannot demonstrate equivalence with an interval 19× wider than the effect you are equating to zero.
- The paper's one-sentence limitation ("Bootstrap intervals resample pairs, which share target cohorts, so they are narrower than a fully clustered interval would be") is technically true and materially misleading: it implies a modest correction. The correction is 5× at cohort level and 15× at institution level, and it flips the sign of the paper's principal conclusion.

### 5. [MAJOR] The explanation ceiling is confounded with training-set size

`run_explanation_ceiling.cohort_reference_points` splits each cohort into an eval third and two training *sixths*: `rest_idx` is 2/3, split in half, so **each ceiling model trains on ~1/3 of the cohort**. The ladder trains on 100 % of a source cohort and 100 % of a target cohort. The ceiling is therefore measured with one third of the training data of the thing it is a ceiling for.

That confound is measurable in the artifacts. From `exp_018/f33/per_cohort.csv` (n = 315 cohort × seed):

```
corr(log n_students, ceiling_tau)       = +0.423
corr(log n_students, ceiling_full_tau)  = +0.294

n_students quartile   median n   strict ceiling   ladder-matched ceiling
(52, 140]                 107        0.023             0.214
(140, 335]                238        0.096             0.279
(335, 1113]               733        0.299             0.465
(1113, 2498]             1803        0.387             0.396
```

A 17× range in the strict ceiling across size quartiles. The pooled "ceiling = 0.338" is therefore a lower bound biased down by however much training data was withheld, and the paper's central rhetorical move — "We set out to show that transfer destroys explanations. It does not, because there was little to destroy" — is not established. Two models trained on *full* halves of a large cohort could plausibly agree far above 0.338. The experiment that settles this (train on true disjoint halves, i.e. `test_size=0`, ranking on the full cohort) is a two-line change and costs one re-run of exp_018 only.

**On the reviewer's specific question — is 0.338 the defensible choice or the flattering one?** It is the *conservative* one, and the paper deserves credit here. The stricter out-of-sample ceiling is 0.198; quoting it would make the negative claim look *stronger* (D3 tau 0.034 would then be 17 % of ceiling rather than 10 %). Quoting the higher number is the honest direction. My objection is not the choice between 0.338 and 0.198; it is that both are contaminated by the 1/3-training-sample artifact, so neither is the right comparator for the ladder.

There is a second, opposite asymmetry the paper should name: in the "ladder-matched" condition *both* half-models rank on data that includes their own training rows, whereas in the ladder the transferred model is strictly out-of-sample on the target. So the ladder-matched ceiling is measured under conditions *more* favourable than the transferred side of the comparison it anchors.

### 6. [MAJOR] Per-institution ceilings are heterogeneous and one is negative; pooling them is not defensible

Ladder-matched ceiling by institution (`ceiling_full_tau`), which is the 0.338 the paper quotes:

| institution | cohorts | strict ceiling | **ladder-matched ceiling** | floor |
|---|---|---|---|---|
| KU Leuven | 6 | 0.311 | **0.670** | 0.737 |
| UKZN | 16 | 0.175 | **0.361** | 0.631 |
| OULAD | 19 | 0.356 | **0.315** | 0.870 |
| Oviedo | 20 | 0.052 | **0.284** | 0.614 |
| **Zambia** | 2 | −0.000 | **−0.095** | 0.619 |

Zambia's two cohorts: `zambia_ICT1110_2020` ceiling −0.124, `zambia_ICT1110_2021` −0.067.

**What a negative ceiling means.** Kendall tau between two rankings of 7 features has expectation 0 under independence. A ceiling of −0.095 means two models trained on disjoint subsamples of the *same* cohort produce rankings that are, on average, *anti*-correlated — i.e. the ranking carries no information whatever and the sign is sampling noise around zero. For Zambia (and near enough for Oviedo's strict ceiling of 0.052) the concept "attainable agreement" is undefined: there is no ceiling because there is no floor to rise from.

**Does that invalidate pooling?** Yes, for two independent reasons.

1. The ceiling table pools institutions where a ceiling exists (KU Leuven 0.670) with institutions where it demonstrably does not (Zambia −0.095), weighting by cohort count. The pooled 0.338 describes no institution: it sits between OULAD (0.315) and UKZN (0.361) purely because those two supply 35 of 63 cohorts.
2. Worse, the pooled ceiling (63 cohorts, equal weight) and the D3 tau it is compared against (2912 pairs, weighted 29.5 % Oviedo / 28.7 % OULAD / 25.8 % UKZN / 11.7 % KU Leuven / 4.2 % Zambia) are averages over **different populations**. Comparing 0.026 to 0.338 as if they were commensurable is not valid. A per-institution version of Table V-E (ceiling and D3 tau side by side, per target institution) is the fix and is computable from the released artifacts.

### 7. [MAJOR] The quoted explanation numbers are undocumented averages over representations

Section V-H reports "D3 tau" of 0.038 / 0.026 / 0.029 at cutoffs 1/4, 1/3, 1/2. The artifacts give:

| cutoff | raw | zscore | percentile | **mean of the three** | paper |
|---|---|---|---|---|---|
| f25 | 0.004 | 0.062 | 0.048 | **0.038** | 0.038 |
| f33 | 0.034 | 0.026 | 0.018 | **0.026** | 0.026 |
| f50 | 0.024 | 0.030 | 0.033 | **0.029** | 0.029 |

So the paper's tau is the mean over three representations, undisclosed. Three problems:

- The V-H stability claim ("explanation agreement stays between 0.026 and 0.038") is manufactured by that averaging. The underlying per-representation values run **0.004 to 0.062, a 15× range**, and the *raw* value — the representation used for every other headline number in the paper — is 0.004 at f25 and 0.034 at f33, an eightfold move across a nuisance parameter.
- You deploy one representation. A mean over three is not a quantity anyone can act on.
- It contradicts Section V-E, where the same 0.026 appears in a table whose other rows are raw-feature quantities, and Table IV, where raw = 0.034, zscore = 0.026, percentile = 0.018. A reader will take 0.026 for the raw number; it is the zscore number, and coincidentally also the three-way mean.

Under instance-pair clustering, the two representations nearest the quoted value **include zero** (zscore [−0.017, +0.079], percentile [−0.029, +0.073]); only raw excludes it, barely.

### 8. [MAJOR] "A feature ranking indistinguishable from random" is contradicted by the paper's own Jaccard column

Conclusion: "produces a feature ranking indistinguishable from random." Top-3 Jaccard, GB/raw, against the analytic random value of 0.3029:

| distance | J@3 |
|---|---|
| D1 | 0.4321 |
| D2 | 0.3719 |
| **D3** | **0.3339** |
| random | 0.3029 |
| ceiling | 0.4870 |

D3 J@3 exceeds random and declines monotonically with distance, exactly as tau does. The paper reports this column in Table IV and V-E and then draws its conclusion only from tau. Either the residual top-3 agreement is real (in which case "indistinguishable from random" is false) or the two metrics disagree and the paper should say why. As written the conclusion overstates.

### 9. [MAJOR] The contamination correction rests on 10 pairs from 6 courses, and Zambia composition explains half of it

**Claim (g) continued:** "Removing contaminated pairs lowers D1 from 0.715 to 0.656 and, with it, removes the artefact by which same-course transfer appeared to *beat* within-cohort performance."

The 10 "clean" D1 pairs, in full (`is_clean` = contamination < 1 %, not zero — a definition the paper does not state):

```
source                target                inst        n_target   auc    contam
oulad_BBB_2013B       oulad_BBB_2014J       OULAD          2292   0.8406  0.0065
oulad_BBB_2014J       oulad_BBB_2013B       OULAD          1767   0.8365  0.0085
oulad_FFF_2013B       oulad_FFF_2014J       OULAD          2365   0.9008  0.0089
ku_Globaleconom_1819  ku_Globaleconom_2021  KU Leuven       335   0.6085  0.0000
ku_Globaleconom_1920  ku_Globaleconom_2021  KU Leuven       335   0.6684  0.0000
ku_Globaleconom_2021  ku_Globaleconom_1819  KU Leuven       743   0.5783  0.0000
ku_Globaleconom_2021  ku_Globaleconom_1920  KU Leuven       681   0.6278  0.0000
ukzn_ISTN211_2019     ukzn_ISTN211_2021     UKZN            327   0.5517  0.0092
zambia_ICT1110_2020   zambia_ICT1110_2021   Zambia           52   0.4875  0.0000
zambia_ICT1110_2021   zambia_ICT1110_2020   Zambia           65   0.4388  0.0000
```

- n = 10 directed pairs from **6 undirected course-pairs**; effective sample size ≈ 6. Bootstrap 95 % CI on the clean mean: **[0.566, 0.748]** — it contains D0 (0.691) and it contains the contaminated D1 (0.715). The "drop" is not distinguishable from noise.
- **Composition, not decontamination, drives it.** Excluding the two Zambia pairs (52 and 65 students, D0 AUCs of 0.455 and 0.598) the clean D1 mean is **0.7016**, not 0.6539. Roughly 45 % of the reported 0.059 drop is the arrival of Zambia in the clean subset, which is absent from most of the contaminated 68. Comparing a 78-pair mean to a 10-pair mean with a completely different institutional mix is a composition change dressed as a bias correction. A within-institution paired comparison (contaminated vs clean pairs *at the same institution*) is the correct estimator and is computable from the released `pair_overlap.csv`.
- **The artefact is not removed.** The three clean OULAD D1 pairs average **0.859**, against OULAD's D0 mean of **0.845**. Contamination-free same-course transfer at OULAD still beats within-cohort performance. The sentence "removes the artefact by which same-course transfer appeared to beat within-cohort performance" is refuted by the paper's own clean subset.
- Note also that the paper quotes 0.715 for contaminated D1, which comes from the unreproducible `exp_017` run; the released `aggregate.csv` says **0.7533**, making the D1-over-D0 excess **+0.062** rather than +0.024. The two halves of this claim come from two different ladder runs.

### 10. [MAJOR] The fairness claim is a level effect, not a gap effect, and the ranking across attributes is a group-count artifact

`exp_020/f33/per_source.csv` is properly paired within target — credit for that. Recomputing the transferred-minus-local contrast per target:

| institution | attribute | targets | Δ(gap) | targets where gap widens | Δ(worst recall) | Δ(**best** recall) |
|---|---|---|---|---|---|---|
| OULAD | age_band | 19 | +0.0123 | 11/19 | −0.119 | −0.107 |
| OULAD | disability | 16 | **−0.0107** | 7/16 | −0.073 | −0.084 |
| OULAD | gender | 19 | +0.0030 | 12/19 | −0.117 | −0.114 |
| OULAD | highest_education | 19 | +0.0083 | 13/19 | −0.116 | −0.108 |
| OULAD | imd_band | 17 | **−0.0180** | 7/17 | −0.076 | −0.094 |
| UKZN | GENDER | 5 | +0.0036 | 2/5 | −0.488 | −0.485 |
| UKZN | QUINTILE | 3 | +0.0356 | 3/3 | −0.473 | −0.437 |
| UKZN | RACE | **1** | +0.0520 | 1/1 | −0.321 | −0.269 |

- **"Transfer costs the worst-served group most" is not supported.** The best-served group's recall falls by essentially the same amount as the worst-served group's in every case: OULAD gender −0.114 vs −0.117; age_band −0.107 vs −0.119; UKZN GENDER −0.485 vs −0.488. For **imd_band the worst group loses *less* than the best group** (−0.076 vs −0.094), and for disability likewise (−0.073 vs −0.084). Transfer costs everybody, roughly equally. The differential is at most 0.036 recall and is negative for the two attributes where the local disparity was widest.
- **The gap direction is a coin flip.** 5 of 8 attributes widen; a sign test on 8 gives p = 0.36. Per target, the best case (OULAD highest_education, 13/19) gives p = 0.17 two-sided. Nothing here is significant.
- **The paper's presentation hides the level effect.** "at UKZN, recall for the lowest school-quintile group falls from 0.65 locally to 0.18 after transfer" is true and dramatic; the unreported companion is that the *best* quintile group falls 0.78 → 0.34. The reader is invited to infer a fairness effect from what is a uniform collapse.
- **The cross-attribute ranking is an artifact of group count.** `groups` (median): imd_band 10, QUINTILE 4, highest_education 3, everything else 2. Mean gap by attribute: imd_band 0.164, QUINTILE 0.160, RACE 0.153, highest_education 0.064, GENDER 0.062, age_band 0.051, disability 0.044, gender 0.038. max−min recall over 10 groups is mechanically larger than over 2 purely from sampling noise; the paper's "Deprivation produces the widest disparity even locally" is fully explained by imd_band having five times as many groups as gender. The gap statistic must be either normalised for group count or replaced by a variance-based / pairwise-standardised measure before attributes can be ranked.
- **UKZN RACE rests on one target cohort and UKZN QUINTILE on three.** The paper's hedge ("The UKZN local figures rest on few cohorts and should be read as indicative; the transferred figures do not") is not adequate for n = 1: the transferred figure for RACE is 47 source cohorts scored on *the same single target*, so its apparent n of 47 is one cluster. The two claims in the abstract and V-F that carry the fairness contribution ("transfer widens the gap on the two South African attributes") rest on 3 targets and 1 target respectively.
- Three of eight attribute rows are omitted from the paper's table (OULAD age_band, disability, highest_education). Two of the three omitted rows would have *weakened* the claim (disability narrows). State the selection rule or report all eight.

### 11. [MAJOR] No multiplicity accounting anywhere, and one headline sits inside the noise of the search

The released ladder alone reports `4 distances × 3 representations × 3 models = 36` cells × 7 metrics = **252 metric cells per cutoff**, × 3 cutoffs = **756**. Add exp_016 (9 × 9 = 81), exp_019 (12 × 7 = 84), exp_020 (18 × 3 = 54), exp_018 (per-institution × 3 references). Roughly **1,000 reported quantities**. The only intervals in the artifacts are 36 unadjusted percentile bootstrap CIs on `auc_mean` in `aggregate.csv`; nothing else carries an interval at all, and the paper contains no correction, no pre-registration statement, and no distinction between confirmatory and exploratory analysis.

The concrete cost: under an 18-way Bonferroni interval, 3 of 9 (model × representation) D0−D3 gaps lose significance (RF/percentile, RF/zscore, LR/percentile — see the table in "Claims That Survive"). And the paper's Section V-B selects gradient boosting as its headline family after reporting all three, without saying it was chosen in advance.

Minimum acceptable fix: state that all analyses are exploratory, report intervals on every headline quantity, and use the *most conservative* cell rather than the illustrative one wherever the ordering across models flips (which it does: Table II shows RF the most robust family under raw and GB the least, so the headline "0.691 → 0.597" is the worst-case family).

### 12. [MAJOR] Oviedo cohort selection is not neutral, and it is the selection that maximises every headline

`oviedo_adapter.select_courses` sorts eligible courses by `minority = n × min(rate, 1−rate)` descending and takes the top 20. That is selection on **size × class balance jointly** — precisely the two properties that inflate measured AUC and suppress base-rate dispersion.

I recomputed the eligible pool directly from `datasets/_candidates/oviedo/tables/{mdl_grade_items,mdl_grade_grades}.csv` (the code path is `load_course_labels`, ~470k rows, cheap):

```
eligible courses (n>=50 & minority>=15): 94   [matches the paper's "94 eligible"]

                     count   mean n   median n   mean rate   sd(rate)   rate range        median |rate-0.5|   total students
SELECTED (top 20)       20    192.0      137.5       0.533      0.150    0.264 - 0.841           0.114              3,840
EXCLUDED (74)           74     88.8       76.0       0.556      0.218    0.072 - 0.893           0.202              6,574
```

Consequences, all determinable without a re-run:

- The excluded 74 courses are **half the size** and **76 % more class-imbalanced** than the selected 20, with a **45 % wider base-rate spread**.
- The excluded 74 contain **6,574 students against the selected 20's 3,840** — the benchmark uses 37 % of Oviedo's eligible students and 21 % of its eligible courses, chosen on the two axes that most affect the results.
- **Direction of the bias on discrimination:** Oviedo's D0 AUC is already 0.606 with sd 0.136 at median n = 131. Halving median n to 76 and moving median |rate−0.5| from 0.114 to 0.202 would push per-cohort AUC estimates further toward 0.5 (fewer minority-class events, noisier 5-fold CV). The within-cohort range in claim (a) would widen and the pooled D3 AUC would fall.
- **Direction of the bias on calibration:** the D3 CIL identity above says per-pair CIL ≈ source rate − target rate. The base-rate sd of the excluded pool is 0.218 vs 0.150, so per-pair |CIL| on Oviedo pairs would rise by roughly the ratio of base-rate spreads (~×1.45). The *pooled mean* would stay pinned near zero under percentile — because the swap symmetry is preserved under any selection — which is exactly the point of objection 1.
- **The stated justification does not justify the rule used.** The paper says the cap exists "so that the mean over pairs is not an Oviedo statistic" (and the code comment says the same). A **random** 20 of 94 serves that purpose exactly as well, without the selection-on-outcome-favourability. There is no defence in the manuscript for choosing the largest and best-balanced.

**On whether I could run the alternative:** the raw Oviedo tables are present (`datasets/_candidates/oviedo/` 2.3 GB, month tables + `mdl_log`), so a random-20 or smallest-20 re-selection is *technically* reproducible, but it requires re-streaming ~60 M log rows through `load_log_for_courses` and then re-running the full nine-block ladder plus the O(cohorts²) permutation-importance pass, which the code comments put at "tens of minutes" per block. The released artifacts contain only the 20 selected parquets and no per-course statistics for the other 74, so **the sensitivity analysis is not computable from the artifacts alone** — only the eligibility characterisation above is. That is itself a finding: for a paper whose contribution is a released benchmark, the selection is not auditable from what is released. Ship the eligible-94 table and either a random-20 arm or a documented justification.

Note also: Oviedo is **20 of 63 cohorts (32 %) and 29.5 % of the 2,912 D3 target pairs, but 8.4 % of the benchmark's students**, and it is the only institution whose label is a gradebook total rather than a registrar outcome (which the adapter docstring itself flags as "partly entailed by absence of activity"). A third of the pair-level weight comes from the least externally valid and most selection-biased eighth of the students.

---

## Additional Concerns

### [MAJOR] Every headline is an unweighted mean over pairs; the student-weighted version halves the effect

`aggregate()` and every table take a plain mean over pairs, so a 52-student Zambia cohort counts as much as a 2,498-student OULAD cohort. GB / raw / D3:

| metric | unweighted (paper) | weighted by n_target |
|---|---|---|
| AUC | 0.5945 | **0.6308** |
| calibration-in-the-large | **+0.1222** | **+0.0472** |
| Brier | 0.3626 | 0.3471 |
| recall@20 | 0.2712 | 0.2792 |

The abstract's "over-predicts risk by 12 percentage points" becomes **4.7 points** when weighted by the students who would actually be misclassified, and the D0−D3 AUC gap shrinks correspondingly. Neither weighting is wrong, but the paper never states which it uses or why, and the deployment-relevant one (students affected) is roughly half the reported effect. State the weighting and report both.

### [MINOR] `aggregate.csv` reports D0 explanation tau = 1.000

`transfer_benchmark.run_ladder` hardcodes `tau = 1.0; jac = 1.0` for D0 rows rather than computing them. Tables in the paper do not use these cells, so nothing is wrong in the manuscript — but the released `aggregate.csv` contains four rows asserting perfect explanation agreement within cohort, which a downstream user will read as a measured floor of 1.0 alongside the paper's measured floor of 0.707. Emit NaN or drop the rows.

### [MINOR] `exp_017/summary.csv` mixes two incompatible definitions in adjacent columns

`contaminated_pairs` counts `contamination > 0`; `clean_pairs` counts `contamination < 0.01`. So D1 shows 72 + 10 = 82 against 78 pairs, D2 shows 324 + 771 = 1095 against 916, D3 shows 78 + 2909 = 2987 against 2912. Nothing is miscomputed, but the table is unreadable and the paper's "clean" subset silently includes pairs with up to 0.99 % overlap (three of the ten OULAD/UKZN clean D1 pairs have 0.65–0.92 % overlap, i.e. 15–21 shared students). Report zero-overlap and <1 % as separate columns.

### [MINOR] Student-count inconsistency across the paper and artifacts

`cohorts.csv` sums to **45,170** (matching `side2026_tables.md` Table I); `exp_017/student_counts.csv` and paper Section III both say **45,158**. A 12-student discrepancy, trivial in itself, but it means the two artifacts were built from different cohort frames — consistent with the reproducibility problem in objection 3.

### [MINOR] Section IV-A says 3,969 ordered pairs; 63² = 3,969 and `pairs.csv` has 35,721 rows

3,969 × 9 (rep × model) = 35,721. Correct, but the distance counts (63 + 78 + 916 + 2912 = 3,969) should appear in the paper so a reader can check the design without loading the CSV.

### [MINOR] "The 40 targets present at all four distances" excludes both institutions that motivate the paper

Section IV-A states this. It should also state the consequence: the paired estimator excludes Oviedo and Zambia, so Table II describes a three-institution benchmark, and the "five institutions" of the title never appear together in the headline discrimination table. The paper reports all-target figures alongside, which is the right thing to have done — but the title's claim rests on the all-target column, and the flattering paired column (0.746 → 0.614) is the one in the table.

### [MINOR] The Table IV explanation columns are blank for six of nine rows

Only gradient boosting has permutation importances (documented in IV-D and in the code comment). Publishing a 9-row table with 6 empty rows invites a reader to think they are missing. Drop the rows or mark them "not computed".

---

## Concerns by Tag

**[CRITICAL]**
- C1. The calibration restoration is a design identity (percentile CIL = source rate − target rate, R² = 0.961; pair set exactly swap-symmetric so the mean is 0.000000 by construction at every rung). Mean |CIL| improves only 17.9 %; 78 % of pairs still miss by >0.10; the sign of the effect reverses at two of five institutions.
- C2. The Brier improvement is 67 % attributable to a mechanism the paper does not report (variance of CIL), only 33 % to the reported one; and the transform *does* improve discrimination (+0.020 GB, +0.052 LR), contradicting "recalibration device rather than a performance fix".
- C3. Headline D1 and D3 AUCs and all calibration numbers do not reproduce from the released artifacts; `aggregate.csv` and `exp_017/clean_vs_all.csv` disagree by 0.038 AUC at D1 on identical pair sets, and the paper quotes the latter.
- C4. Bootstrap intervals are 3.6–5× too narrow at cohort level and 9–16× too narrow at institution level; the headline +0.119 calibration bias has an institution-clustered CI of [−0.053, +0.325] and loses significance.

**[MAJOR]**
- M1. Explanation ceiling trained on 1/3 of each cohort; ceiling rises 0.214 → 0.396 across size quartiles (corr with log n = +0.29/+0.42). The "little to destroy" claim is not established.
- M2. Per-institution ceilings run −0.095 (Zambia) to 0.670 (KU Leuven); pooling them, and comparing the pool to a D3 tau averaged over a differently-composed population, is invalid.
- M3. The quoted D3 tau (0.026 / 0.038 / 0.029) is an undisclosed mean over three representations; per-representation values span 0.004–0.062, so the V-H stability claim is an averaging artifact.
- M4. "Indistinguishable from random" is contradicted by the paper's own top-3 Jaccard (0.334 vs random 0.303, monotone in distance).
- M5. The contamination correction rests on 10 pairs from 6 courses (CI [0.566, 0.748], contains both compared values); ~45 % of the drop is Zambia composition; and clean OULAD D1 (0.859) still beats OULAD D0 (0.845), refuting the stated conclusion.
- M6. Fairness: best-group recall falls as much as worst-group recall in every case (and *more* for imd_band and disability); gap widens in 5 of 8 attributes (sign test p = 0.36); the cross-attribute ranking tracks group count (10 groups → 0.164, 2 groups → 0.038); RACE has n = 1 target.
- M7. ~1,000 reported quantities, 36 unadjusted CIs, no correction, no confirmatory/exploratory split; 3 of 9 D0−D3 gaps fail an 18-way Bonferroni interval.
- M8. Oviedo's 20 of 94 are selected on size × balance jointly — the two properties that maximise AUC and minimise base-rate spread. Excluded 74 are half the size, 76 % more imbalanced, and contain more students (6,574) than the selected (3,840). Not auditable from the released artifacts.
- M9. Unweighted-over-pairs headlines; student-weighted calibration bias is +0.047, not +0.122.

**[MINOR]**
- m1. `aggregate.csv` D0 tau hardcoded to 1.0.
- m2. `exp_017/summary.csv` mixes >0 and <1 % definitions; counts exceed pair totals.
- m3. 45,170 vs 45,158 student count across artifacts.
- m4. Abstract attaches the 94 % contamination maximum (a D2 figure) to the same-course claim, where the maximum is 83 %.
- m5. "Prevalence shift, the largest component at D3" contradicts exp_016 (`corr_d_prevalence` 0.194 < `corr_d_shape` 0.283).
- m6. "The gap is 0.09 to 0.13 depending on the estimator" contradicts Table II's own range of 0.087–0.176.
- m7. Design pair counts (63/78/916/2912) not stated in the paper.
- m8. Paired-40 estimator structurally excludes the two institutions the title's "five" depends on; worth one more sentence.
- m9. Table IV has six blank rows.

---

## Recommendation

**Major revision.** The benchmark is a genuine contribution and the two negative results are the best-supported claims in learning-analytics transfer that I have seen from a single group. But the paper currently leads with a positive claim that the released data show to be an identity of its own design, quotes numbers that its released artifacts do not reproduce, and reports intervals roughly an order of magnitude too narrow for the level at which its claims are made.

What I think a defensible version looks like, in priority order — none of it requires new data and most requires no re-run:

1. **Rewrite Section V-C and the abstract's second result.** Report mean |CIL|, not mean CIL, and report CIL per target institution. Show the CIL ≈ (source rate − target rate) regression (R² = 0.961) explicitly and state that the pooled mean is zero by design. The correct claim is: *calibration transfer failure at D3 is essentially pure prevalence shift, the percentile transform does not touch it, and the transform's apparent success on pooled calibration-in-the-large is an averaging artifact of the ordered-pair design.* That is a more interesting and more citable finding than the current one, and it is what the data say.
2. **Fix the reproducibility gap (C3).** Regenerate every number in the paper from one frozen ladder run, or state which run each table came from and release both. Until this is done nothing in the paper can be checked.
3. **Cluster every interval on institution** (or, at minimum, on target cohort) and report the widened intervals in the tables, not in a limitations sentence. Drop or heavily hedge the claims that lose significance — principally the +0.119 calibration bias as an *institution-level* claim.
4. **Re-run exp_018 with full disjoint halves** (`test_size` → 0 on the eval split, or train each model on a true 50 % and rank on the full cohort) and report the ceiling **per institution**. Two lines of code, one cheap re-run, and it converts M1 and M2 from fatal to resolved. Report Zambia's negative ceiling explicitly and say what it means.
5. **Report the explanation tau per representation**, not averaged, at all three cutoffs.
6. **Replace the contamination correction** with a within-institution paired comparison, or report the 10-pair result with its interval and drop the claim that the artefact is removed.
7. **Fairness:** report Δ(best) beside Δ(worst) for all eight attributes, normalise or drop the cross-attribute disparity ranking, and mark RACE/QUINTILE as n = 1 and n = 3.
8. **Release the eligible-94 Oviedo table** and either add a random-20 arm or justify the selection rule against its stated purpose.
9. **Report both weightings** (per pair and per student) for the headline calibration and discrimination numbers.
10. Declare all analyses exploratory and state that no multiplicity correction was applied.

Items 1, 3, 5, 7, 9 and 10 are pure re-analysis of the released CSVs. Item 2 is a re-run of the existing pipeline. Item 4 is a two-line change plus one cheap re-run. Items 6 and 8 are scoping decisions. That is a realistic revision, and the resulting paper would be considerably stronger than the current one, because three of its four headline results would then be negative and all four would be true.

---

*Reproduction note: all computations in this report were run against the artifacts as of the review date using pandas 2.3.3 / numpy 2.4.3 / scipy 1.17.1. Bootstraps use 3,000–5,000 resamples with seeds fixed per analysis; cluster bootstraps resample whole clusters with replacement and concatenate. No project file outside this report was modified.*
