# exp_028_local_sensitivity: which week-1/2 conclusions survive the cutoff and the model family?

> Research practice plan, week 3 (29 Sep – 5 Oct 2026): "sensitivity to design
> decisions — repeat the measurement at cutoffs 0.25 / 0.33 / 0.50 and on
> logistic regression and random forest instead of gradient boosting; separate
> properties of the data from properties of the configuration." Deliverables: a
> sensitivity table and the conditions under which the result holds.

## Design

A 3 × 3 grid — cutoff ∈ {0.25, 0.33, 0.50} of course length × model ∈
{gradient boosting, logistic regression, random forest} — with everything else
as exp_027 `f33_background`: 63 cohorts, 11,875 held-out students per config,
5 background draws of 50 rows, seed 0, estimators SHAP, occlusion, LIME and the
`kernelshap_prob` control, agreement as Kendall τ-b on |attribution| with 95 %
cohort-cluster intervals. Models, fixed and untuned (`models.py`): gradient
boosting 200 trees, depth 3, learning rate 0.05; logistic regression with
standard scaling, L2, C = 1; random forest 300 trees, unlimited depth,
min_samples_leaf 2.

`shap` keeps one meaning across families — the exact interventional Shapley
value on the model's raw output: TreeSHAP for the two tree ensembles, exact
KernelSHAP on `decision_function` (all 126 coalitions) for the logistic
regression, where it equals coef·(z − mean z) in scaled space. The random
forest's raw output is already the probability, so there `shap` coincides with
`kernelshap_prob` (τ-b 1.000 for every student in all three RF configs).
Forests grow the same trees as with `n_jobs=-1` but run single-threaded inside
each cohort worker: threaded prediction differs by ~1e-16 summation residues,
which would turn exact occlusion zeros into near-zeros.

Each config also gets exp_026's gate analysis for two quality measures
(SHAP–occlusion and SHAP–LIME τ-b).

Code: `services/ml/src/experiments/run_local_sensitivity.py`; outputs
`data/artifacts/experiments/exp_028_local_sensitivity/` (`sensitivity.csv`,
`conditions.csv`, one directory per config, `gate/`).

### Criteria, specified in code before the grid ran

The seven criteria below were written into the runner (with their thresholds)
before the full grid ran; a 3-cohort OULAD smoke run only exercised the
pipeline. They were not registered externally, they encode the week-1/2
conclusions, and the GBM@0.33 cell is byte-identical to exp_027 `f33_background`
— a replication by construction, so eight configs are genuine tests.

| id | claim from weeks 1–2 | rule |
| --- | --- | --- |
| C1 | every cross pair sits below both members' self-agreement | cross ci_high < min(self ci_low of the two members), all 3 pairs |
| C2 | occlusion–LIME is the lowest pair | smallest mean, and ci_high < ci_low of both SHAP pairs |
| C3 | occlusion ties do not drive SHAP–occlusion agreement | abs(τ-b − strict τ) < 0.03 |
| C4 | the output space explains little | abs(τ-b(kernelshap_prob, occl) − τ-b(shap, occl)) < 0.03; not evaluable for RF |
| C5 | the gate signal is informative within institutions | within-cohort Spearman ci_low > 0 in each of the four large institutions, both qualities |
| C6 | cohort calibration adds nothing over one global threshold | calibrated − global pooled ci_low ≤ 0, both qualities |
| C7 | LIME does not replicate the SHAP–occlusion institution spread | SHAP–LIME spread < 0.5 × SHAP–occlusion spread (no Zambia) |

## Sensitivity table (τ-b, student-weighted; full intervals in `sensitivity.csv`)

| config | AUC | self SHAP | self occl | self LIME | SHAP–occl | SHAP–LIME | occl–LIME | gate `c*` | gate lift (occl) | calibrated − global, occl | calibrated − global, LIME | within ρ occl / LIME |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.25 GBM | 0.667 | 0.792 | 0.679 | 0.578 | 0.357 | 0.402 | 0.141 | 0.54 | 0.077 | +0.001 [−0.012, 0.015] | −0.015 [−0.029, −0.005] | 0.34 / 0.23 |
| 0.25 LR | 0.714 | 0.825 | 0.787 | 0.662 | 0.524 | 0.644 | 0.363 | 0.65 | 0.090 | +0.002 [−0.021, 0.020] | −0.015 [−0.028, −0.004] | 0.68 / 0.49 |
| 0.25 RF | 0.683 | 0.789 | 0.683 | 0.668 | 0.367 | 0.431 | 0.114 | 0.53 | 0.106 | +0.005 [−0.008, 0.017] | −0.021 [−0.039, −0.007] | 0.44 / 0.34 |
| 0.33 GBM | 0.685 | 0.796 | 0.684 | 0.571 | 0.358 | 0.405 | 0.140 | 0.56 | 0.064 | +0.008 [−0.010, 0.030] | −0.020 [−0.037, −0.006] | 0.40 / 0.26 |
| 0.33 LR | 0.726 | 0.816 | 0.793 | 0.659 | 0.557 | 0.641 | 0.392 | 0.62 | 0.095 | +0.000 [−0.017, 0.017] | −0.009 [−0.018, −0.001] | 0.67 / 0.47 |
| 0.33 RF | 0.691 | 0.804 | 0.678 | 0.663 | 0.372 | 0.461 | 0.133 | 0.59 | 0.089 | +0.004 [−0.010, 0.016] | −0.020 [−0.035, −0.005] | 0.42 / 0.36 |
| 0.50 GBM | 0.731 | 0.807 | 0.678 | 0.608 | 0.362 | 0.452 | 0.160 | 0.59 | 0.033 | +0.024 [0.009, 0.039] | −0.021 [−0.038, −0.007] | 0.34 / 0.27 |
| 0.50 LR | 0.770 | 0.828 | 0.804 | 0.676 | 0.548 | 0.653 | 0.379 | 0.65 | 0.065 | +0.018 [0.005, 0.030] | −0.022 [−0.041, −0.010] | 0.67 / 0.43 |
| 0.50 RF | 0.744 | 0.817 | 0.672 | 0.674 | 0.379 | 0.505 | 0.170 | 0.62 | 0.064 | +0.025 [0.006, 0.042] | −0.034 [−0.054, −0.015] | 0.46 / 0.41 |

AUC is the mean within-cohort AUC of the fitted model on the held-out third;
no config falls below the 0.60 "weak model" flag. Cells are means over
students, so OULAD (57.5 %) weighs most. Averaging the five institutions
equally (`by_institution.csv`) changes one reading: for the tree ensembles
SHAP–occlusion is then *above* SHAP–LIME in all six configs (e.g. 0.33 GBM
0.453 vs 0.393), while for LR SHAP–LIME stays at or above it (0.575–0.597 vs
0.517–0.573). Which SHAP pair agrees more is a weighting choice; the other
conclusions below hold under both weightings.

## Conditions (`conditions.csv`)

| claim | 0.25 GBM | 0.25 LR | 0.25 RF | 0.33 GBM | 0.33 LR | 0.33 RF | 0.50 GBM | 0.50 LR | 0.50 RF |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | yes | no | yes | yes | no | yes | yes | no | yes |
| C2 | yes | yes | yes | yes | yes | yes | yes | yes | yes |
| C3 | yes | yes | yes | yes | yes | yes | yes | yes | yes |
| C4 | yes | yes | n/e | yes | yes | n/e | yes | yes | n/e |
| C5 | yes | yes | yes | yes | yes | yes | yes | yes | yes |
| C6 | yes | yes | yes | yes | yes | yes | no | no | no |
| C7 | yes | no | no | yes | no | no | no | no | no |

C7 ratios (SHAP–LIME / SHAP–occlusion spread): 0.31 and 0.18 for GBM at 0.25
and 0.33; 0.51 and 0.55 for GBM at 0.50 and RF at 0.25 (failing by a hair);
0.74–0.93 for RF at 0.33/0.50; above 1 for LR at 0.25 and 0.50.

## Properties of the estimators — hold in every configuration

- **C2, C3 in all nine configs; C4 in all six where it can be evaluated.**
  Occlusion and LIME are always the least compatible pair; occlusion ties never
  move SHAP–occlusion agreement by 0.03 (differences 0.007–0.016); the output
  space never explains it (differences −0.012 to +0.018).
- **SHAP's own reproducibility is a constant:** self τ-b 0.79–0.83 everywhere.
- **C5 in all nine configs:** within cohorts, SHAP's self-agreement predicts its
  agreement with either second method in each of the four large institutions.
  (Zambia, 2 cohorts and 40 students, is not part of the rule; its intervals
  include 0 in some configs.)

## Properties of the institutions' data — hold in every configuration

Descriptive and found after the grid ran, among the four large institutions:

- OULAD has the lowest occlusion self-agreement and the highest LIME
  self-agreement in all nine configs.
- Its position in the two SHAP pairs follows: lowest for SHAP–occlusion in all
  nine (KU Leuven highest in all nine), highest for SHAP–LIME in eight (second
  at 0.25 GBM). The two institution orders are never positively rank-correlated
  (Kendall τ between them 0 to −1).

So an institution's agreement level depends on how reproducible the chosen
second method is on that institution's data — the exp_026 reading, now across
the grid. With Zambia included, OULAD is highest for SHAP–LIME in six of nine.

## Properties of the configuration

- **The model family sets the level.** With logistic regression every cross cell
  is higher (SHAP–occlusion 0.52–0.56, SHAP–LIME 0.64–0.65, occlusion–LIME
  0.36–0.39, against 0.36–0.38, 0.40–0.50 and 0.11–0.17 for the tree ensembles).
  C1 fails for LR only through SHAP–LIME, whose interval overlaps LIME's own
  self-agreement (0.64 vs 0.66). Several things change together with the family
  — LR is also the best-AUC model and uses a different (exact kernel) SHAP
  algorithm on an additive model — so this is not attributed to linearity alone;
  within GBM, AUC rises from 0.667 to 0.731 across cutoffs while SHAP–occlusion
  stays at 0.357–0.362, which argues against predictive quality as the driver.
  The SHAP–occlusion institution spread also halves under LR (0.13–0.17 against
  0.28–0.35 for trees).
- **The cutoff leaves SHAP–occlusion flat but moves SHAP–LIME:** GBM
  SHAP–occlusion 0.357 / 0.358 / 0.362; SHAP–LIME rises by 0.05–0.07 for the
  tree ensembles (RF 0.431 → 0.505), mostly in OULAD. No cross cell moves by
  0.08 or more within a family.
- **At 0.50 the fixed threshold 0.80 retains less SHAP–occlusion agreement, and
  C6 flips for that quality.** The global gate's lift for SHAP–occlusion falls
  from 0.077 to 0.033 for GBM, while its lift for SHAP–LIME and the
  within-cohort signal do not decline. That is why per-cohort ranking overtakes
  the fixed threshold against occlusion at 0.50 (+0.018 to +0.025, lower bounds
  +0.005 to +0.009), in all three families. Against LIME, calibration is worse in
  all nine configs (−0.009 to −0.034, every interval below 0). Neither regime
  dominates; which is better depends on the second method.
- **C7 is a gradient, not a switch.** The collapse of the institution spread
  under LIME is clear only for GBM at 0.25 and 0.33 (ratios 0.31, 0.18); it is
  borderline for GBM at 0.50 and RF at 0.25, absent for RF at later cutoffs, and
  reversed for LR, partly because the occlusion spread itself shrinks there.

## Conditions of applicability

Within this grid — background-draw variation only, seven engagement features,
LIME at library defaults, these five institutions:

1. A student's local factor list depends on the explanation method. Occlusion–
   LIME agreement (0.11–0.39) is the lowest pair in every configuration, and for
   tree ensembles every pair stays below both methods' self-agreement.
2. SHAP's self-agreement predicts agreement with either second method within
   cohorts, in each of the four large institutions, at every cutoff and for
   every model family — the basis for a reproducibility gate.
3. Institution-level agreement depends on the second method, through that
   method's own reproducibility on the institution's data (post hoc, above), so
   levels must not be compared across institutions without naming it.

Needs qualification:

- "Every pair sits below self-agreement" — tree ensembles only; with LR the
  SHAP–LIME interval overlaps LIME's self-agreement.
- "One global threshold is at least as good as a per-cohort one" — holds against
  LIME everywhere and against occlusion at 0.25 and 0.33; at 0.50 against
  occlusion, per-cohort calibration gains about 0.02.
- "LIME collapses the institution spread" — GBM at early cutoffs.
- "SHAP agrees similarly with both second methods" — depends on how students are
  weighted and on the family.

## Limitations

- Only background draws vary; exp_027 showed that under model refits SHAP's
  self-agreement drops to the cross level, and `vary=model` was not repeated here.
- The calibrated-minus-global intervals hold `c*` at its point estimate (as in
  exp_026); the C6 flip at 0.50 rests on lower bounds 0.005–0.009 above zero
  (unchanged under a different bootstrap seed), and was not re-checked with `c*`
  recomputed per replicate.
- Comparisons across configs use unpaired point estimates, although the same
  students appear in every model at a cutoff.
- The thresholds (0.03, 0.5 ×, AUC 0.60) are conventions fixed in advance, not
  derived. Spreads use four large institutions without Zambia.
- τ-b is undefined for students whose occlusion attribution is all zero:
  38 in each 0.25/0.33 config, 54 at 0.50 GBM, 0 at 0.50 LR, 21 at 0.50 RF.
- `p_risk` / `flagged` / `margin` remain inverted in `students.csv` (TODO(ml));
  model AUC is computed with the correct orientation and no criterion uses them.
