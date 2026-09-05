# Editorial Decision and Revision Roadmap — SIDe 2026 round 1

**Manuscript:** *What Transfers and What Does Not: Predictions, Thresholds and Explanations of Early-Warning Models Across Five Institutions*
**Panel:** five role-separated seats (journal fit, methodology, domain, perspective, devil's advocate), each committed without sight of the others.
**Date:** 2026-09-05

## Decision: **MAJOR REVISION**, and the revision changes what the paper claims

All five seats returned Major Revision or worse; the devil's advocate argued for rejection. The panel converged, independently, on one defect that invalidates a central claim, and the recomputations behind it were reproduced by the authors before this decision was written. The benchmark and one of the three findings survive. The other two do not.

---

## 1. Consensus findings (three or more seats, independently)

### C-1. The decision metric was computed on the wrong class — **four seats**
`transfer_benchmark._scores` called `f1_score(y, …)` with scikit-learn's default `pos_label=1`, and `y` is `passed` in every adapter. Every F1 in the abstract, Table III, Sections V-C and V-H and the Conclusion therefore measured identification of students who **pass** — the class an early-warning system never alerts on.

Consequences, recomputed and confirmed:
- A constant "everyone passes" rule scores F1 0.765 on the paired targets and beats the percentile-repaired transferred model in 100 % of cohorts.
- On the failing class the claimed repair **reverses**: 0.421 raw against 0.350 percentile, and both lose to "alert everyone" at 0.546.

**Verdict: the paper's second headline finding is withdrawn as stated.** Fixed in code: the metric suite now reports F1 on the failing class, recall and precision at a fixed 20 % flag budget, Brier score, calibration-in-the-large, and the trivial-rule baseline beside every F1.

### C-2. The headline ladder is not the five-institution benchmark — **two seats, verified**
Requiring a target to appear at all four distances structurally excludes every Oviedo cohort (one academic year, so no D1) and every Zambia cohort (one course, so no D2). The paired-40 set is OULAD 19, UKZN 15, KU Leuven 6. On all 64 targets the D0−D3 gap is 0.090, not 0.131.

**Remedy:** report both estimators side by side and state plainly which institutions each contains. The five-institution claim belongs to the benchmark, not to the headline number.

### C-3. The stated mechanism is contradicted by the authors' own artifact — **two seats, verified**
The paper says the percentile transform works by removing sensitivity to platform click scale. In `exp_016_shift_analysis/regression.csv` the correlation with click-scale shift **rises** (0.067 → 0.077); what falls is distribution-shape shift. The shift analysis also loaded only three of the five institutions.

**Remedy:** retract the click-scale sentence, restate on shape, rerun the analysis over all five institutions.

---

## 2. Devil's Advocate CRITICAL issues — adjudicated individually

Per the panel's iron rule, each is recorded with its outcome.

| # | Challenge | Adjudication |
|---|---|---|
| DA-1 | The dissociation is estimator variance, not transfer | **Rejected, and the challenger says so.** Same-model self-agreement is τ = 0.921 and is insensitive to `n_repeats` (0.924 / 0.952 / 0.957 at 3 / 10 / 30). The finding is not noise. |
| DA-1b | But the ceiling is not 1.0 | **Upheld.** Two models on disjoint halves of the *same* cohort agree at τ = 0.395, J@3 = 0.530. Cross-institution agreement retains ≈ 10 % of attainable agreement. The claim must be restated against this ceiling, and the in-sample local baseline against the out-of-sample transferred one must be equalised. |
| DA-3 | The fix is accidental prior matching, and a threshold beats it | **Upheld.** Percentile features force each cohort's marginals to Uniform[0,1], so the transferred model reproduces its source's alert rate (corr 0.914 against 0.424 raw). A one-line label-free source-rate threshold on raw features scores 0.633 against percentile's 0.622 and wins 42 of 64 targets. |
| DA-4 | The conclusion is choice-dependent | **Upheld.** Leave-one-institution-out moves cross-institution τ from 0.008 to 0.082. Sensitivity to composition must be reported, not hidden. |
| DA-8 | Student double-counting and a contamination gradient | **Upheld and reproduced.** 72 of 78 D1 pairs and 324 of 916 D2 pairs share students between training and evaluation, up to 93.8 % of the target; D3 is clean at 1.5 %. Distinct students are 35,529, not the 45,236 claimed. The D2→D3 drop is partly a leakage cliff. |
| DA-9 | The frozen results do not reproduce | **Upheld at the time of review; now resolved.** The artifact/code mismatch was the Zambia label fix landing after the frozen run. All artifacts are being regenerated from current code. |
| DA-misc | Monotone-invariance claim false; "monotonically" false in 5 of 9 rows; logistic regression silently wrapped in a scaler | **Upheld.** All three are wording or specification errors and must be corrected. |

No CRITICAL was bypassed.

---

## 3. Single-seat findings that must still be answered

- **Fairness (perspective seat).** The manuscript's defence that demographics are unavailable is false for the two largest institutions: OULAD ships `gender`, `region`, `imd_band`, `age_band`, `disability`; UKZN ships `GENDER`, `RACE`, `QUINTILE`, means-tested-aid flags and matric points. At a track that names fairness and bias mitigation, no disaggregation is indefensible — and a click-volume risk score is partly a device-and-connectivity score.
- **Missing literature with a settled vocabulary (perspective and domain seats).** The central result already has a name in clinical prediction modelling: external validation separating discrimination from calibration, the calibration hierarchy, and a model-updating ladder in which intercept-only recalibration is tried before refitting. The paper's negative few-shot result may be an artefact of refitting all coefficients on 25 students. Prevalence shift is also called an open problem when label-free estimators have existed since 2002.
- **Gap claim (b) is falsified as written (domain seat).** Within-course differential features have been used to mitigate cross-dataset disparity, and the Oviedo release itself ships normalised event-percentage variables, so "raw counts" is a partly artificial baseline.
- **Gap claim (a) needs narrowing (domain seat).** At least one multi-institution harmonised benchmark exists and is uncited.
- **Gap claim (c) survives.** No prior work compares a transferred model's explanation against a locally trained model's. This is the paper's real contribution.
- **Citation integrity (domain seat).** The "only four datasets" figure is not stated in the cited census and must be reattributed as the authors' own analysis of its public inventory. Permutation importance must be cited to Fisher, Rudin and Dominici rather than Breiman. One reference is uncited. Two author lists were wrong and have been corrected.
- **Venue and length (journal-fit seat).** 4,700 words against a six-page limit, no figure was cited anywhere in the text, and the sole novel contribution arrives third of five on page five.

---

## 4. Required reframing

The honest paper that survives this review is **a benchmark plus negative results**, not a benchmark plus a fix.

**Keep and lead with:**
1. The benchmark: 63 cohorts, five institutions, five platforms, four countries, all public, with adapters released.
2. Institution-dependence of the signal itself: within-cohort ROC-AUC ranges from 0.85 to 0.52. A single-dataset study cannot observe this and routinely reports one point of that range as the state of the art.
3. Explanation agreement collapses with transfer distance, restated against the 0.395 attainable ceiling, with the noise floor (0.921) reported so the reader can see it is not estimator variance.

**Report as negative results, prominently:**
4. The authors' own cohort-relative representation does **not** repair the decision rule on the class that matters, and a simpler label-free source-rate threshold beats it.
5. Adding labelled target students does not close the gap — with the caveat that the refit strategy was not the recalibration ladder the clinical literature would use.

**Report as methodological warnings, which is where much of the paper's value now lies:**
6. F1 on the majority class is an easy, invisible error that flatters a model; always print the trivial-rule baseline.
7. Within-institution "cross-course" evaluation is contaminated by shared students, up to 94 % of a target cohort. Report per-pair overlap or the near rungs of any such ladder are inflated.

**Delete:** the click-scale mechanism claim, the word "monotonically", the demographics-unavailable defence, and the pooled-source and few-shot sections if space demands.

---

## 5. Roadmap, in dependency order

1. ~~Correct the metric suite; rerun~~ — code fixed, run in progress.
2. ~~Close the Zambia backward label leak~~ — done; Zambia now contributes two cohorts.
3. ~~Correct two wrong author attributions~~ — done against Crossref.
4. Land the contamination audit as a released artifact and report clean-pair results (`exp_017`).
5. Rerun the shift analysis over all five institutions and restate the mechanism on distribution shape.
6. Add the source-rate-threshold baseline and report that it beats the proposed transform.
7. Restate the explanation finding against the disjoint-halves ceiling, and equalise in-sample versus out-of-sample scoring.
8. Add fairness disaggregation for OULAD and UKZN, or state precisely why not.
9. Reframe against the clinical external-validation literature and adopt its vocabulary.
10. Fix the citation integrity items; verify all references against Crossref uniformly.
11. Recount students as distinct identifiers.
12. Widen the bootstrap to cluster on target cohort.
13. Rewrite around the surviving claims, then compress to six pages.
