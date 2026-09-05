# Reviewer 1 — Methodology, Statistics and Reproducibility

**Manuscript:** *What Transfers and What Does Not: Predictions, Thresholds and Explanations of Early-Warning Models Across Five Institutions* (SIDe 2026, Track 1, draft v1.0, 2026-09-05)
**Artifacts examined:** `data/artifacts/experiments/exp_014_transfer_ladder/{f25,f33,f50}`, `exp_015_feature_richness/f33`, `exp_016_shift_analysis/f33`
**Code examined:** `services/ml/src/experiments/{transfer_benchmark,run_transfer_ladder,run_shift_analysis,run_feature_richness_control,models,stability}.py`, `services/ml/src/benchmarks/{oulad,ku_leuven,ukzn,zambia,oviedo}_adapter.py`, `moodle_logs.py`, `services/ml/scripts/build_paper_tables.py`, `services/ml/tests/test_transfer_benchmark.py`
**Scope of this seat:** research design, leakage, sampling, statistical validity, effect sizes, uncertainty, reproducibility. I re-ran analyses against the frozen artifacts and against the live pipeline; every number below is computed, not quoted.

**Recommendation: Major Revision.** The benchmark is real, the pipeline is unusually clean on the leakage dimension the authors worried about, and the central negative result (explanations do not transfer) survives every test I could throw at it. But three of the paper's four headline numbers are estimator artifacts, one metric is on the wrong class and below its own trivial baseline, and the stated mechanism for the fix is contradicted by the authors' own regression output.

---

## 1. Summary of the Design

64 cohorts from five institutions are mapped onto one seven-feature engagement schema. Each cohort yields one row per student at week `max(1, round(f · n_weeks))`, `f ∈ {0.25, 0.33, 0.50}`. All 64² = 4,096 ordered (source, target) pairs are evaluated for 3 representations × 3 model families. Distance is categorical: D0 same cohort (5-fold CV), D1 same `module` different cohort, D2 same institution different `module`, D3 different institution. Aggregates are means over pairs (Tables II/III first average within target, then across the 40 targets that have all four distance classes; Table IV does not — see C7). Side analyses: pooled sources, few-shot, a shift regression (exp_016), a feature-richness control (exp_015).

Effort is visible in the right places: a full student × week grid so no student is silently dropped at the cutoff (`moodle_logs.py:108-111`), a relative cutoff so course lengths are commensurable, unsupervised representations that touch no labels, a stated `min_minority` admission rule, and honest disclosure of the permutation-importance compute settings. The problems are not in the plumbing; they are in the estimators and the framing built on top.

---

## 2. Verified Claims

**V1. The features contain no post-cutoff information.** `canonical_from_weekly` (`transfer_benchmark.py:66-80`) builds every feature from `groupby(student_id).cumsum()` over week-sorted rows, and `weeks_since_active` from a forward-fill of the last active week. Both are strict prefix operations, so the row at week *k* depends only on weeks ≤ *k*. `cutoff_rows` (`:83-86`) then selects exactly that row. `moodle_logs.build_cohort_frame:108-111` materialises the full `students × weeks` grid before merging activity, so a student silent at week *k* still has a row and is not selected out. I could find no path by which a post-cutoff observation reaches a feature. `tests/test_transfer_benchmark.py:26-33` pins this behaviour.

**V2. The representations use no labels.** `represent` (`:89-98`) computes rank/z-score column-wise on `X_raw` only. `Cohort.X` recomputes per cohort. The percentile fix is genuinely deployable without target labels, as claimed.

**V3. `n_repeats=3` is not the weak point.** I feared the paper's negative explanation result was manufactured by ranking noise. It is not. Refitting GB on 15 cohorts spanning all five institutions and re-running `_ranking` under three different seeds gives, at `n_repeats=3`, mean Kendall τ **0.924** and top-3 Jaccard **0.856** between repeated measurements of *the same model on the same data* (at `n_repeats=30`: 0.970 / 0.956). The measurement is reliable; attenuation toward zero is not what produces τ ≈ 0.03. The disclosure in Section IV-F is warranted. (This is the one place where I expected to find a fatal problem and did not.)

**V4. The sensitivity-to-cutoff table reproduces** for AUC and F1. Recomputing paired-40 means from `f25/f33/f50/pairs.csv` gives D0 AUC 0.726 / 0.746 / 0.777, D3 raw 0.602 / 0.616 / 0.644, D3 pct 0.638 / 0.637 / 0.677, F1 D0 0.801 / 0.809 / 0.836, F1 D3 raw 0.486 / 0.507 / 0.536, F1 D3 pct 0.636 / 0.639 / 0.655 — every cell matches Section V-H. All three runs carry `n_cohorts: 64`, so "all 64 cohorts survive both" is true. (The τ column does not reproduce; see C7.)

**V5. Counts and identifiers are right.** 64 cohorts, 45,236 students, 4,096 ordered pairs, 3,034 D3 pairs, 916 D2, 82 D1, 64 D0 — all confirmed from `pairs.csv`. The Zambia adapter never reads the `StudentName` column (`zambia_adapter.py:43,59`), as the privacy note claims.

**V6. exp_016's reported R² and correlations are traceable.** GB raw R² = 0.116, percentile R² = 0.062, `corr_d_shape` 0.283 → 0.189 all appear verbatim in `exp_016_shift_analysis/f33/regression.csv`. The numbers in Section V-D are the numbers in the artifact. (Their interpretation is another matter; see C3.)

---

## 3. Concerns

### [CRITICAL] C1 — F1 at 0.5 is measured on the *pass* class, and every configuration in the paper loses to a trivial baseline on it

`_scores` (`transfer_benchmark.py:159-163`) calls `f1_score(y, p >= 0.5)` with `y = passed`. The positive class is therefore **passing**, not being at risk. Section V-C reads this as "what that shift does to a deployed alerting rule" — but no early-warning system alerts on students predicted to pass. The metric on which the paper's second headline rests is computed on the complement of the class of interest.

Worse, it is not a metric that discriminates. For a constant "predict pass" classifier, F1 on the pass class is `2p/(1+p)`. Over the 40 paired targets (mean pass rate 0.635) that trivial baseline is **0.765**. Against it:

| Setting | Reported F1 | Trivial `2p/(1+p)` | Beats trivial in |
|---|---|---|---|
| D0 within cohort, raw | 0.809 | 0.765 | **47.5 %** of cohorts |
| D3 other institution, raw | 0.504 | 0.769 | **26.8 %** of pairs |
| D3 other institution, percentile ("the repair") | 0.640 | 0.769 | **19.3 %** of pairs |

The within-cohort model beats "always say pass" in fewer than half of its own cohorts, and the celebrated percentile repair leaves the model *further* below the trivial baseline than the raw model was at D0. The narrative "the threshold fails first / the transform repairs it most decisively" is therefore a story about movement inside a region that a one-line constant classifier dominates. This is the single most serious problem in the manuscript.

*Settling analysis:* recompute all threshold results with the fail class as positive, and report recall at a fixed alert budget (top-10 % / top-20 % of scores) and precision-at-budget alongside. Add the `2p/(1+p)` and "alert everyone" baselines to Table III. If the fix still recovers a real fraction of budgeted recall, the section survives and becomes much stronger; if not, it must be withdrawn.

### [CRITICAL] C2 — The pairing rule silently removes two of the five institutions from the headline estimate

`build_paper_tables.table_ladder:78-80` keeps targets with `nunique(distance) == 4`. Because Oviedo has 20 courses in a single academic year (no D1 partner) and Zambia has one course (no D2 partner), **all 20 Oviedo and all 3 Zambia cohorts are structurally excluded**, plus one UKZN cohort. The 40 paired targets are OULAD 19 / UKZN 15 / KU Leuven 6. Nearly half the estimator's weight is OULAD, the institution with by far the best within-cohort signal (D0 0.845 vs 0.521–0.667 elsewhere).

The consequences, recomputed per-target over all 64 targets:

| Estimator | D0 AUC | D3 AUC (raw) | D0−D3 | F1 D0 | F1 D3 (raw) | F1 D0−D3 |
|---|---|---|---|---|---|---|
| Paired 40 (paper) | 0.746 | 0.616 | **0.131** | 0.809 | 0.507 | **0.303** |
| All 64 targets | 0.689 | 0.599 | **0.090** | 0.736 | 0.480 | **0.256** |

The abstract's "0.746 → 0.616" and the conclusion's "about 0.13 AUC" are inflated by ~45 % relative to the five-institution benchmark the paper says it built. This is selection bias toward large, multi-year institutions — exactly the institutions whose signal is strongest.

It also suppresses the most interesting fact in the dataset. Per-institution mean D0−D3 (all 64, raw, GB):

| KU Leuven | OULAD | Oviedo | UKZN | Zambia |
|---|---|---|---|---|
| +0.062 | +0.178 | +0.032 | +0.091 | **−0.037** |

At Zambia, cross-institution transfer **beats** the local model. That is consistent with the paper's own pooled-source finding (Section V-G) and is a genuinely publishable result which the headline estimator deletes.

*Settling analysis:* report the all-64 per-target estimate as primary and the paired-40 as a sensitivity check, or report both side by side with the institutional composition of each stated in the caption. The per-institution D0−D3 column above belongs in the paper.

### [CRITICAL] C3 — The stated mechanism for the fix is contradicted by the authors' own regression

The abstract and Section V-D both claim the percentile transform "works by removing sensitivity to platform click scale". `exp_016_shift_analysis/f33/regression.csv`, gradient boosting:

| Representation | corr `d_prevalence` | corr `d_scale` | corr `d_length` | corr `d_shape` | R² |
|---|---|---|---|---|---|
| raw | 0.194 | **0.067** | 0.228 | 0.283 | 0.116 |
| percentile | 0.202 | **0.077** | 0.125 | 0.189 | 0.062 |

`d_scale` has the *weakest* marginal association with loss of all four measures, and its correlation goes **up**, not down, under the percentile representation (0.067 → 0.077). Its partial coefficient is negative in both representations (β = −0.020 raw, −0.005 pct) — more click-scale shift, *less* loss. What actually falls is `d_shape` (0.283 → 0.189) and `d_length` (0.228 → 0.125). The paper cites the `d_shape` drop correctly one sentence later and then attributes the mechanism to click scale anyway.

Compounding this: `run_shift_analysis.build_cohorts:47` loads only `load_oulad`, `load_ku`, `load_ukzn`. Oviedo and Zambia are **absent from the entire mechanism analysis** — `loss_vs_shift.csv` contains 41 cohorts and 1,640 pairs per (model, representation), from three institutions, i.e. six ordered institution pairs. The module docstring still says "the ladder has only three institutions". Section V-D's shift-by-distance table and the sentence "frees it from the number of institutions" are therefore based on 3 of the 5 institutions, undisclosed.

*Settling analysis:* rerun exp_016 with all five loaders; restate the mechanism as removal of *distribution-shape* and *course-length* sensitivity, which the data supports; drop the click-scale claim from the abstract or demonstrate it with a scale-only ablation (e.g. per-cohort median normalisation alone).

### [MAJOR] C4 — Students appear in both the source and the target of D1/D2 pairs, and this is never disclosed

Recomputing student-ID intersections at the cutoff across cohorts of the same institution: **201 within-institution ordered pairs share students.**

| Institution | Rung | Pairs | Mean % of target students also in source | Max |
|---|---|---|---|---|
| KU Leuven | D1 | 4 | **79.4 %** | 83.1 % |
| Oviedo | D2 | 9 | 46.6 % | 89.6 % |
| UKZN | D2 | 66 | 17.9 % | 89.7 % |
| UKZN | D1 | 9 | 8.5 % | 19.7 % |
| Zambia | D1 | 3 | 14.9 % | 21.2 % |
| OULAD | D1 / D2 | 23 / 87 | 3.6 % / 2.5 % | 9.9 % / 44.8 % |

`ku_Accountancy_1819 → ku_Accountancy_1920` shares 79 % of the target cohort with the source. The KU Leuven D1 rung is, for practical purposes, testing on the training students.

To the authors' credit, this does **not** manufacture the monotone degradation: overlap correlates *positively* with loss (r = +0.043 at D1, +0.056 at D2), and removing overlapping pairs leaves D2 (0.651) and D3 (0.599) unchanged. But it destroys the D1 estimate: D1 has only 82 pairs benchmark-wide, of which **4** are overlap-free, and those 4 average AUC 0.615 against 0.715 for the rung as a whole. Any statement about D1 — including the τ = 0.20 in Table IV and the D1 column of every table — rests on 78 contaminated pairs.

Also: `zambia_adapter.load_labels:51` groups by `student_id` only, with no year, and `build_all_cohorts:97` hands the same table to every year. A repeat sitter's label in 2019 is `max()` over all sittings including 2020 and 2021 — a label drawn from the future. UKZN gets this right (`ukzn_adapter.py:96` groups by `(student_id, subj, year)`); Zambia does not.

*Settling analysis:* report the overlap table; report D1 with and without overlapping pairs; fix the Zambia label grouping to `(student_id, year)` and rerun. Given 82 D1 pairs total, consider dropping the D1 rung to a disclosed limitation rather than a result.

### [MAJOR] C5 — "The threshold fails before discrimination does" reverses under a chance-anchored normalisation

Section V-C: "the threshold loses about 37 % of its F1 where discrimination loses 17 % of its AUC." Both are relative to zero, but AUC's null is 0.5, not 0. Anchored at chance:

- AUC: (0.746 − 0.616) / (0.746 − 0.500) = **53.1 %** of the above-chance signal lost.
- F1: 0.302 / 0.809 = **37.3 %**.

The ordering flips. The codebase already knows this: `run_feature_richness_control.summarise:195` computes `relative_drop_pct = 100 · drop / (D0 − 0.5)`. The paper uses the un-anchored version for the comparison that carries its headline. Combined with C1, "the threshold fails first" is not established.

### [MAJOR] C6 — Uncertainty: bootstrap over pairs is far too narrow, and no headline *difference* has a CI

`aggregate:360-382` resamples rows of `pairs` i.i.d. within (distance, representation, model). Each of the 3,034 D3 rows shares a target cohort with ~47 others and a source model with ~47 others; the effective number of independent units is nearer 64 (or 5) than 3,034. Also, `aggregate` produces CIs only for level means — never for D0−D3, never for percentile−raw, and never for F1 or τ at all — so every comparison the paper actually makes is reported without uncertainty.

I recomputed with a target-clustered bootstrap on per-target means (5,000 resamples, GB):

| Quantity | Estimate | Target-clustered 95 % CI |
|---|---|---|
| D0−D3 AUC, raw, paired 40 | +0.131 | [+0.109, +0.151] |
| D0−D3 AUC, raw, **all 64** | +0.090 | [+0.069, +0.111] |
| D3 percentile − raw, AUC | +0.021 | [+0.014, +0.028] |
| D0−D3 F1, raw, paired 40 | +0.303 | [+0.270, +0.339] |
| D3 percentile − raw, F1 | +0.132 | [+0.105, +0.160] |

Those survive. The honest clustering, however, is at institution level — the paper's claim is about moving between institutions, and there are five of them:

- D0−D3 AUC, all 64, **institution-clustered** 95 % CI: **[+0.028, +0.151]**.

The lower bound falls below the paper's own pre-registered 0.05 criterion. With five institutions, four of which are drawn from a population the paper itself says contains only four suitable public datasets, the cross-institution claim cannot be given the precision the manuscript implies.

*Settling analysis:* replace the pair-level bootstrap with a two-way (source-cluster × target-cluster) or at minimum target-clustered scheme; report paired CIs for every difference the paper asserts; report the institution-clustered CI for the D3 claim and state the 0.028 lower bound.

### [MAJOR] C7 — Table IV uses a different estimator than Tables II/III, and the τ column of Section V-H averages across representations

Section V opens: "ladder figures are means over ordered pairs, aggregated per target cohort and then restricted to the 40 target cohorts present at all four distances." `build_paper_tables.table_explanations:112-123` does neither — it is a flat mean over all pairs across all 64 targets. So Table IV's 0.038 / 0.336 is a different statistic from Table II's 0.616. Under the stated estimator, D3 τ (GB, raw, paired 40) is 0.049, not 0.038.

Section V-H's τ column (0.039 / 0.033 / 0.032) matched none of the three natural estimators. It reproduces only as **the mean of τ across the three representations** at each cutoff: (0.0465 + 0.0108 + 0.0604)/3 = 0.0392; (0.0263 + 0.0381 + 0.0348)/3 = 0.0331; (0.0363 + 0.0245 + 0.0352)/3 = 0.0320. Averaging over representations — which are separate experimental conditions, one of which is the paper's proposed intervention — is not a defensible estimator, and it manufactures the stability the sentence claims. Under the primary raw representation, D3 τ moves **0.011 → 0.038 → 0.025** across cutoffs, a 3.5× swing, not "stays at 0.032 to 0.039".

### [MAJOR] C8 — The explanation claim needs a same-population ceiling, not an implicit ceiling of 1.0

Two corrections, in opposite directions.

**(a) 0.33 is not the random baseline.** For two uniformly random 3-subsets of 7 features, `|A ∩ B|` is hypergeometric and `J = i/(6−i)`:

| i | P(i) = C(3,i)·C(4,3−i)/35 | J |
|---|---|---|
| 0 | 4/35 = 0.1143 | 0.000 |
| 1 | 18/35 = 0.5143 | 0.200 |
| 2 | 12/35 = 0.3429 | 0.500 |
| 3 | 1/35 = 0.0286 | 1.000 |

E[J] = (0 + 3.6 + 6.0 + 1.0)/35 = 10.6/35 = **0.3029**, SD = 0.2077. The observed 0.3365 (raw, D3) is *above* chance, and detectably so: target-clustered CI [0.320, 0.352], institution-clustered [0.321, 0.366] — both exclude 0.3029. Similarly τ = 0.0381 has target-clustered CI [0.018, 0.059] and institution-clustered [0.013, 0.076], both excluding zero (under percentile, the institution-clustered CI [−0.002, 0.079] does include zero). So "no agreement" / "effectively uncorrelated" overstates: there is a small but real residual agreement, roughly 5 % of the available range above chance.

**(b) But the ceiling is not 1.0, which makes the paper's substantive point stronger than it argues.** I fitted two GB models on disjoint stratified halves of the *same* cohort, ranked both on the same data under the identical `_ranking` protocol, over 15 cohorts × 3 splits: mean τ = **0.424** (SD 0.332), mean J@3 = **0.569** (SD 0.292). Two models from an identical population agree at τ ≈ 0.42, not 1.0. Read against that ceiling, D3's 0.038 retains ~9 % of achievable agreement and D1's 0.217 retains ~51 %. That is a much better-posed claim than "0.03 versus 1.0", and it is the number a statistical referee will ask for.

Related asymmetry: the local ranking is computed from a model fitted on the full target and permuted **in-sample** (`run_ladder:223`), while the transferred ranking is computed **out-of-sample** on the same target (`:237`). The two rankings are not measured under the same regime, which biases the comparison toward disagreement by an unquantified amount. The half-split control above removes this and should replace the current baseline.

### [MAJOR] C9 — The few-shot "flat curve" is partly a composition artefact

The cap is fine: `run_fewshot:343` draws `_cap_rows` once per seed *outside* the `for k` loop, so k = 0 and k > 0 share the identical 8,000-row source. The docstring's defence is correct and I verified it. The problem is elsewhere — `:347` skips any (target, k) with `k >= t.n − 30`, so the set of cohorts averaged **changes with k**:

| Institution | k=0 | k=25 | k=50 | k=100 |
|---|---|---|---|---|
| Oviedo | 20 | 20 | 20 | **10** |
| UKZN | 16 | 16 | 16 | **14** |
| Zambia | 3 | **1** | — | — |

`table_fewshot:136` then takes a flat mean, so Table VI compares different cohort populations across columns. Recomputed on the cohorts common to every k:

| Institution | k=0 | k=25 | k=50 | k=100 |
|---|---|---|---|---|
| Oviedo (n=10, was 20) | 0.597 | 0.600 | 0.607 | 0.598 |
| Zambia (n=1, was 3) | 0.579 | 0.543 | — | — |

Section V-G's "at Oviedo 100 labelled students make it worse" is a reported drop of 0.032 (0.630 → 0.598) of which **0.023 is composition change**; the like-for-like drop is 0.009, well inside noise. The Zambia column compares three cohorts at k=0 against one at k=25. OULAD (0.778 → 0.828) and KU Leuven are unaffected and stand.

Secondary: `idx_eval = perm[k:]` means the evaluation set shrinks and changes as k grows, so even the clean rows compare AUCs measured on different populations. A fixed held-out set (`perm[max(ks):]` for all k) costs nothing and removes the confound.

### [MAJOR] C10 — The withdrawal control is not in the codebase, and the Oviedo control was never run

Section V-F's "lowers within-cohort AUC from 0.858 to 0.793 across the twelve original cohorts" appears nowhere in the repository except as a bullet in `docs/dissertation/side2026_paper_plan.md:234`. There is no script, no flag in the exp_014/exp_015 pipelines, and no artifact. `oulad_adapter.py:84` hard-codes `NEGATIVE_FINAL_RESULTS = {"Fail", "Withdrawn"}` with no exclusion path. For a paper whose contribution is a released reproducible benchmark, the control that answers its most obvious objection is the one result that cannot be reproduced from what is released.

The Oviedo control is worse: `oviedo_adapter.drop_zero_grades` exists (`:77, :85, :164`) but no artifact shows it was ever run, and the paper's wording — "its adapter exposes the same control" — is technically true while reading, in context, as if the objection were closed. It is not. Note also that `select_courses:85` applies `drop_zero_grades` *before* ranking by minority-class size, so running it would select a different 20 courses; the control as implemented is not comparable to the main run and needs a fixed-cohort variant.

On the substance: the concern is well-founded. A student who never opens the LMS has zero cumulative clicks *and*, at Oviedo, a zero gradebook total by construction. `cum_clicks = 0` at the cutoff nearly entails the label. 9.9 % of Oviedo students is a large enough share to move a cohort's AUC materially.

*Settling analysis:* add `--drop-withdrawn` / `--drop-zero-grades` flags to `run_transfer_ladder`, freeze both controls as artifacts, and report the Oviedo control with the course set held fixed to the main run's 20.

### [MINOR] C11 — Section IV-B's monotone-invariance argument is empirically false

The paper argues: "For a tree model the percentile transform is monotone, so within a cohort it cannot change predictions; any gain at D1–D3 is therefore attributable to cross-cohort alignment alone." Checked against `f33/pairs.csv`, D0 per cohort:

| Model | max abs(D0 pct − D0 raw) | mean | cohorts exactly equal |
|---|---|---|---|
| Gradient boosting | **0.0490** | +0.0013 | 1 / 64 |
| Random forest | **0.0113** | +0.0003 | 0 / 64 |

Two distinct causes, both reproduced directly:

1. **GB in-sample predictions *are* exactly invariant** (verified: percentile, log1p and ×10⁶ all give `allclose == True`), but D0 is scored by cross-validation. A tree's split threshold is the midpoint of two adjacent *training* values; under a nonlinear monotone map that midpoint lands somewhere else relative to unseen points. Out-of-sample predictions therefore change — and every prediction in this paper is out-of-sample.
2. **Random forest is not invariant even in-sample**: percentile gives max |Δp| = 0.035 and log1p 0.040, while a pure linear rescale (×10⁶) gives exactly 0. So the non-invariance is specific to *nonlinear* monotone maps under RF's internal float32 split handling.

Practically the paper's conclusion still holds — the D0 artifact averages +0.0013 for GB against a D3 gain of +0.021 (16×) — but the stated justification is wrong and a referee will test it. Replace the a-priori argument with the measured D0 delta used as an explicit null for the tree-model gain.

### [MINOR] C12 — Cohort admission at Oviedo is label-informed and ranked

`oviedo_adapter.select_courses:86-90` ranks all ~94 eligible courses by `n × min(rate, 1−rate)` and keeps the top 20 — i.e. the largest and most class-balanced. This is a label-derived selection stronger than the uniform `min_minority ≥ 15` rule applied elsewhere, and it biases the Oviedo pass-rate range in Table I and its AUC estimates upward. Disclose the selection rule in the paper (currently only "the 20 with the largest minority class") and report a random-20 sensitivity check.

### [MINOR] C13 — Course length is inferred from data that post-dates the prediction point

For the three Moodle institutions, `n_weeks` is the span between the first and last week with ≥ 10 % active students (`moodle_logs.py:87-94`), and for KU Leuven it is `max(week_number)` (`run_transfer_ladder.py:64`) — despite Section III-B saying KU Leuven ships a calendar. The cutoff week is `round(f · n_weeks)`, so the prediction point is set using activity observed after it. This does not leak into a feature and is a defensible design given the datasets, but it should be stated as a deployment gap: at deployment you do not yet know how long a course will run from its log. A robustness pass with the cutoff fixed at absolute weeks would bound it.

### [MINOR] C14 — Internal inconsistency in the F1 recovery figure

Section V-C: "between 44 % and 47 % of the loss". Conclusion: "recovers about two thirds of the lost F1 for every model family we tested." The correct figure for GB is (0.639 − 0.507)/(0.809 − 0.507) = **43.7 %**. The conclusion is wrong; fix it there.

### [MINOR] C15 — D0 explanation agreement is asserted, not measured

`run_ladder:232-233` sets `tau = jac = 1.0` for D0 by construction. `build_paper_tables` notes this; the paper does not. Since the D0 *prediction* is cross-validated while the D0 *ranking* is a whole-cohort in-sample fit, the two D0 columns are not the same object. One sentence in Section IV-D fixes it.

### [MINOR] C16 — A trace of cross-institution ID collision

D3 pairs show a mean "student overlap" of 0.008 % — non-zero because student identifiers are not namespaced by institution (`UKZN "STUD…"` vs Oviedo integers vs OULAD integers). The magnitude is negligible and affects nothing, but any released code that joins on `student_id` should prefix it with the institution.

---

## 4. Reproducibility Assessment

**Strong.** Frozen CSV artifacts for three cutoffs, `run_metadata.json` with seed, fraction, admission thresholds, feature list, representations and models; one script per stage; a deterministic seed threaded through model construction, CV and permutation importance; a table builder that regenerates the manuscript's tables from the artifacts. I reproduced Tables I, II, III, V, VI, VII and the AUC/F1 rows of Section V-H from the frozen files without touching the raw data, and reproduced live pipeline behaviour (representation invariance, cohort membership, student overlap, few-shot composition) by importing the modules directly. That is better than most submissions in this literature.

**Gaps, roughly in order of severity:**

1. The withdrawal control (0.858 → 0.793) exists only in a planning document — no code, no flag, no artifact (C10).
2. The Oviedo zero-grade control has a flag but no run (C10).
3. Section V-H's τ column is produced by an estimator (mean over representations) that appears in no script and is stated nowhere (C7).
4. Table IV uses a different aggregation than Tables II/III, contradicting the Section V preamble (C7).
5. exp_016 silently runs on three institutions; its own docstring still describes the old three-institution design (C3).
6. `f25` and `f50` have no `fewshot.csv`, so the few-shot result is single-cutoff only — fine, but say so.
7. Test coverage is two functions (`test_transfer_benchmark.py`), covering only cumsum/recency and the cutoff. Nothing tests the pairing rule, the aggregation, the distance classification, or representation invariance — the four places where the bugs in this review actually live. Three small assertions (paired-target count by institution; `table_explanations` estimator matches `table_ladder`; D0 GB percentile ≈ raw within a stated tolerance) would have caught C2, C7 and C11 before submission.
8. No environment lock is referenced from the paper; `sklearn` 1.8.0 / `pandas` 2.3.3 in this checkout. Given C11 (float32 split behaviour) and the project's own history of an environment-sensitive result, pin the sklearn version in the release.

---

## 5. Recommendation

**Major Revision.**

The benchmark is a real contribution and the hardest thing to fake — five institutions, five platforms, one schema, released adapters — is done and done carefully. The leakage discipline in the feature construction is genuinely good (V1), the compute-saving settings the authors worried about are adequate (V3), and the paper's most novel claim, that explanation portability is a separate and worse-behaved property than prediction portability, survives every robustness check I applied and is in fact *understated* once measured against a same-population ceiling (C8b).

But the paper cannot be accepted in this form:

- **C1** puts the threshold narrative on the wrong class and below its trivial baseline. This is not a presentational fix; the section must be recomputed.
- **C2** means the abstract's headline numbers describe three institutions while claiming five, and inflate the effect by ~45 %.
- **C3** states a mechanism the authors' own regression contradicts, using an analysis run on 3 of 5 institutions without disclosure.
- **C5–C7** show that the comparative claims ("threshold fails first", "explanation agreement is stable across cutoffs") depend on non-standard or inconsistent estimators.
- **C10** leaves the paper's own key robustness control outside the released artifact.

None of these is unfixable, and several fixes make the paper better rather than weaker: the all-64 estimate surfaces Zambia's negative transfer gap; the half-split ceiling turns "τ = 0.03 versus 1.0" into a properly normalised effect size; the institution-clustered CI is the honest uncertainty for a claim about institutions. I would want to see the revision, including the recomputed threshold analysis with the fail class as positive and an alert-budget metric, before forming a view on acceptance.

If the authors can only address a subset, the priority order is **C1 > C2 > C3 > C10 > C6 > C9 > C7**.
