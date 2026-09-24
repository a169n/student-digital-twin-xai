# exp_027_local_estimator_matrix: is exp_025's cross-estimator agreement a property of one pair?

> Research practice plan, week 2 (22–28 Sep 2026): "removing the dependence of
> the conclusion on one pair of methods". Deliverable: an agreement matrix over
> three local estimators on ~12k students.

## Question

exp_025 found that TreeSHAP and occlusion agree on a student's factor list at a
mean Kendall τ of about 0.35. Is that a general level of local-explanation
agreement, or a property of that particular pair?

## Design

Same cohorts, split, model, background draws and repeats as exp_025
`f33_background` (63 cohorts, 11,875 held-out students, gradient boosting,
5 repeats, background 50, seed 0); `f33_model` refits on bootstraps instead.
Estimators, each applied to the same model, students and background:

| estimator | what it is | role |
| --- | --- | --- |
| `shap` | interventional TreeSHAP, raw (log-odds) output | exp_025 |
| `occlusion` | feature set to the background median, change in P(pass) | exp_025 |
| `lime` | `LimeTabularExplainer` on the background, library defaults, 5,000 samples, fixed seed | **third method** |
| `kernelshap_prob` | `KernelExplainer` on P(pass), all 126 coalitions enumerated, `l1_reg=False` | control |

Why LIME and not KernelSHAP as the third method: with 7 features KernelSHAP
enumerates every coalition, so on the log-odds it reproduces TreeSHAP exactly
(the test enforces 1e-6; about 4e-8 was measured on real cohorts) — a
duplicate, not a third method. In probability space it is the exact
interventional Shapley value and differs from `shap` only by the output space,
which makes it a control for how much of the SHAP–occlusion gap is the link
function (occlusion works in probabilities).
`TreeExplainer(model_output="probability")` was not used: on real cohorts it
deviated from exact Shapley by up to about 0.1.

LIME's seed is fixed across repeats, which makes it reproducible for a given
(model, background). It does not freeze LIME's sampling across repeats: a new
background refits LIME's discretiser, so each repeat also draws new
perturbations, and LIME's diagonal and cross cells include some of its own
sampling noise. That noise alone is measured separately (`lime_seed_tau`: the
first repeat's model and background, seed + 1).

**Ties.** Occlusion attributions tie exactly in 58 % of student-repeats pooled
(40 % in OULAD to 96 % in KU Leuven): a feature moved to the median often
crosses no tree split. exp_025's statistic reads factor-list positions as
strict ranks, so those ties were broken by feature index. Every cell is
therefore reported twice: `tau_strict` (exp_025's statistic) and `tau_b`
(Kendall τ-b on |attribution|, ties kept). The other estimators rarely tie
(LIME ≈1 % pooled, 6.7 % in KU Leuven, mostly exact zeros; SHAP ≈0.1 %).

Code: `services/ml/src/experiments/run_estimator_matrix.py`, estimators in
`run_local_stability.py` (exp_025's default output is byte-identical to before,
verified on five institutions under every vary mode), τ-b helper
`stability.kendall_tau_scores`. Figure:
`data/artifacts/experiments/exp_027_local_estimator_matrix/estimator_matrix.png`
(`services/ml/scripts/plot_estimator_matrix.py`).

## Result: the 3×3 matrix (`f33_background`, τ-b, 95 % cohort-cluster CI)

| | SHAP | occlusion | LIME |
| --- | --- | --- | --- |
| **SHAP** | 0.796 [0.780, 0.811] | 0.358 [0.313, 0.410] | 0.405 [0.367, 0.439] |
| **occlusion** | | 0.684 [0.653, 0.717] | 0.140 [0.101, 0.184] |
| **LIME** | | | 0.571 [0.531, 0.606] |

Diagonal: self-agreement across background draws. Cells are means over
students, so OULAD (57.5 % of students) weighs most; averaging the five
institutions equally instead (`by_institution.csv`) gives SHAP–occlusion 0.453,
SHAP–LIME 0.393, occlusion–LIME 0.213. Control row (`kernelshap_prob`): vs SHAP
0.793, vs occlusion 0.361, vs LIME 0.408, self 0.784.

Per institution (τ-b):

| pair | OULAD | UKZN | KU Leuven | Oviedo | Zambia (n = 40) |
| --- | --- | --- | --- | --- | --- |
| SHAP–occlusion | 0.248 | 0.469 | 0.593 | 0.494 | 0.462 |
| SHAP–LIME | 0.425 | 0.361 | 0.385 | 0.399 | 0.397 |
| occlusion–LIME | 0.063 | 0.224 | 0.283 | 0.243 | 0.254 |

## Answers

1. **Across background draws, every pair sits far below both methods'
   self-agreement.** No cross cell's interval comes near a diagonal interval,
   under either weighting, so the dependence of a student's factor list on the
   chosen method no longer rests on SHAP–occlusion alone (under model refits the
   diagonal itself drops to the cross level — answer 6). The level is not a constant:
   SHAP agrees with either second method at a similar 0.36–0.41 (their
   intervals overlap, and which of the two is higher depends on how students
   are weighted), while occlusion–LIME is clearly lower (0.14).
2. **Ties are not what keeps agreement low.** τ-b moves SHAP–occlusion from
   0.348 to 0.358 and occlusion–LIME from 0.123 to 0.140; it lowers occlusion's
   self-agreement from 0.706 to 0.684, which the index tie-break had inflated.
3. **The output space explains almost none of the gap, pooled.** KernelSHAP in
   probabilities agrees with occlusion at 0.361, against 0.358 for TreeSHAP on
   log-odds; per institution the difference reaches about ±0.04 (UKZN 0.433 vs
   0.469). The link function changes a student's list about as much as a new
   background draw (SHAP vs `kernelshap_prob` 0.793, SHAP self 0.796).
4. **Institution effects depend on the pair.** SHAP–occlusion separates OULAD
   (0.248 [0.199, 0.291]) from every other institution; SHAP–LIME shows no
   detectable institution effect (0.36–0.43, overlapping intervals). See
   exp_026 for what this does to the week-1 conclusion.
5. **LIME's instability comes mostly from the background:** agreement across
   backgrounds is 0.571, while changing only the seed on the first repeat's
   model and background costs about 0.14 (seed-only floor 0.863).
6. **Under model refits (`f33_model`) the method matters as much as the model:**
   cross-agreement is similar (SHAP–occlusion 0.366, SHAP–LIME 0.430,
   occlusion–LIME 0.158), while SHAP's own agreement across refits drops to
   0.430 — the same level as its agreement with LIME.

## Limitations

- LIME is run with library defaults (quartile discretisation, default kernel
  width, 5,000 samples); settings are in `config.json`. A spot check on two
  cohorts found the LIME cells sensitive to the sample budget: ten times more
  samples raised SHAP–LIME by about 0.07 in one UKZN cohort and left an OULAD
  cohort unchanged.
- The fresh run matches exp_025 closely but not exactly: `p_risk` differs for
  0.5 % of students, `self_tau_shap` for 9.9 % (mean absolute difference 0.003),
  `self_tau_occlusion` for 20 % and the strict `cross_tau` for 30 % (pooled
  0.346 against 0.348). Beyond small platform-level differences in model
  fitting, the student-level differences concentrate on tied occlusion
  attributions: the strict tie-broken statistic is not reproducible across
  builds, which is one more reason to prefer τ-b.
- τ-b is undefined when a vector is constant; 60 of 11,875 students have no
  defined occlusion self-agreement and 38 no defined SHAP–occlusion value.
- `p_risk`, `flagged` and `margin` in `students.csv` are inherited from exp_025
  and inverted (`p_risk` is P(pass)); no agreement number uses them. See the
  TODO(ml) in `run_local_stability.py`.
