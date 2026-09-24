# exp_026_gate_calibration: one gate threshold for everyone, or one per cohort?

> Research practice plan, week 1 (15–21 Sep 2026): "calibrating the threshold
> for showing an explanation". Post-processing only — no model is refit.

## Question

exp_025 gates a student's factor list on its own reproducibility: the list is
shown only if `self_tau_shap >= 0.80`. Pooled, that keeps 55.6 % of students
and raises retained SHAP–occlusion agreement from 0.346 to 0.410. The
institutions sit far apart before any gate (mean agreement 0.229 in OULAD,
0.573 in KU Leuven). Is that spread a threshold artifact, which a threshold
calibrated within each cohort would remove, or does it belong to the
institution, so that the spread itself is the result to report?

## Design

Gate signal: `self_tau_shap` (cheap, computable on the screen). Quality: agreement
of the shown SHAP list with a second method. Three regimes on the same students:

| regime | rule |
| --- | --- |
| global | keep `self_tau_shap >= t`, one `t` for every cohort |
| cohort_calibrated | keep the top `ceil(c·n)` of each cohort by `self_tau_shap`, seeded tie-break; label-free |
| oracle | same, ranked by the quality measure itself — the most any gate could retain at that coverage |

A random gate retains the no-gate mean (lift 0). The matched operating point is
the global gate at 0.80 against both ranked regimes at its pooled coverage
`c* = 0.5555`. Intervals are a 1,000-resample cluster bootstrap over cohorts
within institution. Zambia (2 cohorts, 40 students) is flagged and every spread
is also reported without it.

Code: `services/ml/src/experiments/run_gate_calibration.py`, tests
`services/ml/tests/test_gate_calibration.py`. Per-institution coverage–agreement
curves: `data/artifacts/experiments/exp_026_gate_calibration/f33_background/gate_calibration_curves.png`
(and the same figure for each `exp027_*` robustness run), drawn by
`services/ml/scripts/plot_gate_calibration.py --run <dir>`.

## Primary result (exp_025 `f33_background`, quality = SHAP vs occlusion)

Operating point, point [95 % cohort-cluster CI]:

| institution | global@0.80 coverage | retained τ | calibrated@c* retained τ | oracle@c* retained τ |
| --- | --- | --- | --- | --- |
| KU Leuven | 0.577 | 0.599 | 0.606 | 0.664 |
| OULAD | 0.591 | 0.310 | 0.320 | 0.437 |
| Oviedo | 0.570 | 0.569 | 0.552 | 0.635 |
| UKZN | 0.444 | 0.544 | 0.523 | 0.609 |
| Zambia (n = 40) | 0.150 | 0.638 | 0.536 | 0.599 |
| All | 0.556 [0.506, 0.604] | 0.410 [0.366, 0.451] | 0.419 [0.383, 0.456] | 0.519 [0.486, 0.551] |

- Calibration equalises coverage by construction: the cross-institution coverage
  spread falls from 0.441 to 0.018 (0.147 to 0.005 without Zambia, whose 15 %
  sets the headline figure).
- It does not equalise agreement: the retained-agreement spread is 0.287
  calibrated against 0.345 with no gate, and even the oracle leaves 0.227.
- Calibrated minus global, pooled: +0.009 [−0.011, 0.033]. No gain.
- The signal is informative within every large institution: within-cohort
  Spearman(`self_tau_shap`, agreement) 0.37–0.43, all intervals above 0. Pooled,
  the gate delivers 37 % (global) to 42 % (calibrated) of the oracle's lift; the
  difference is not significant and comes mostly from which institutions'
  students are shown, not from better ranking within a cohort.

The same holds at background sizes 20 and 200. Under `vary=model` and
`vary=both` the 0.80 threshold passes about 1 % of students or fewer, so the
matched operating point is not comparable there.

## Robustness: does the reading survive the choice of second method?

The quality measure above is exp_025's SHAP–occlusion agreement. exp_027 found
that occlusion attributions tie exactly in 58 % of student-repeats pooled (40 %
in OULAD to 96 % in KU Leuven), which the strict statistic breaks by feature
index, and added LIME as a third method. The same analysis was rerun on exp_027
inputs (`exp_026_gate_calibration/exp027_*`, summary in `robustness.csv`):

| quality measure (exp_027, background) | no-gate mean by institution (OULAD / UKZN / KU / Oviedo) | spread, no gate | calibrated − global, pooled | within-cohort ρ |
| --- | --- | --- | --- | --- |
| SHAP–occlusion, strict τ | 0.229 / 0.475 / 0.577 / 0.500 | 0.347 | +0.010 [−0.010, 0.033] | 0.41 |
| SHAP–occlusion, τ-b | 0.248 / 0.469 / 0.593 / 0.494 | 0.345 | +0.008 [−0.010, 0.030] | 0.40 |
| SHAP–LIME, τ-b | 0.425 / 0.361 / 0.385 / 0.399 | 0.064 | −0.020 [−0.037, −0.006] | 0.26 |

τ-b is undefined for 38 Oviedo students of one cohort whose occlusion
attribution is all zero; the τ-b occlusion row excludes them (n = 11,837,
c* = 0.557).

- Ties do not drive the spread: τ-b leaves it at 0.345.
- The spread is not invariant to the second method. It is large in both
  occlusion pairs and nearly vanishes for SHAP–LIME, where the institutions sit
  within 0.36–0.43 with overlapping intervals. The same holds under model
  refits (`f33_model`): SHAP–LIME spread without Zambia 0.078 against 0.349 for
  SHAP–occlusion.
- The institution order in each pair follows the second method's own
  reproducibility on that institution's data: occlusion's self-agreement is
  lowest in OULAD (0.639, against 0.71–0.79 in the other large institutions) and so is its agreement
  with SHAP; LIME's self-agreement is highest in OULAD (0.609) and so is its
  agreement with SHAP. The spread is an estimator × institution effect; with one
  alternative method and four large institutions it cannot be pinned on
  occlusion alone.
- Cohort calibration never helps. Against LIME it is worse than one global
  threshold when pooled (−0.020 [−0.037, −0.006]), although no single
  institution's interval excludes 0.
- The within-institution signal survives with LIME (ρ 0.14–0.36, every interval
  above 0), but is weaker.
- One tempting mechanism — occlusion agrees with SHAP where it zeroes more
  features — does not hold: the association exists between institutions
  (Spearman over the 63 cohort means 0.56) but reverses within cohorts (mean
  within-cohort student-level ρ −0.21). Computed from exp_027 `students.csv`.

## Decision

A calibrated threshold adds nothing over one global threshold, so the scheme
kept is **one global threshold** — but `t` is not portable: `t = 0.80` passes
29 %, 56 % and 75 % of students at background sizes 20, 50 and 200, and about
1 % under model refits. The rule is therefore to read `t` off the pooled
coverage–agreement curve of the deployed configuration (the curves above), not
to carry 0.80 across configurations.

The cross-institution spread is not reported as an institution property. What
is reported:

1. The gate is a within-institution tool: its signal predicts agreement with
   either second method in every large institution, and one global threshold is
   at least as good as a per-cohort one.
2. Institution-level agreement levels depend on which second method defines
   them and must not be compared across institutions without naming it — the
   local counterpart of the SIDe 2026 paper's finding for global rankings.

Update after week 3 (exp_028_local_sensitivity): the gate's within-institution
signal (point 1) holds at every cutoff and for every model family in each of the
four large institutions. "One global threshold is at least as good" holds
against LIME everywhere, but against occlusion at the 0.50 cutoff per-cohort
calibration gains about 0.02. LIME collapsing the spread is clear only for GBM
at the 0.25 and 0.33 cutoffs. What holds throughout (post hoc, four large
institutions) is point 2's mechanism: OULAD has the lowest occlusion and the
highest LIME self-agreement in every configuration, and is lowest for
SHAP–occlusion and highest (8 of 9) for SHAP–LIME.

Note: the practice plan quotes the spread as 0.24–0.58; the artifacts give
0.229–0.573.

## Limitations

- Zambia's two cohorts make its bootstrap degenerate; it is flagged throughout.
- `c*` is held at its point estimate across bootstrap replicates, so the
  calibrated-minus-global interval is conditional on `c*`; an independent
  re-run that recomputed `c*` per replicate reached the same reading.
- exp_027 is a fresh run of exp_025's configuration and matches it closely but
  not exactly: `self_tau_shap` differs for 9.9 % of students (mean absolute
  difference 0.003) and the strict `cross_tau` for 30 % (pooled 0.346 against
  0.348); 127 students change gate status. The differences concentrate on
  students with tied occlusion attributions, so the strict tie-broken statistic
  is not reproducible across builds. The robustness rows use exp_027 throughout
  and are internally consistent.
- `p_risk`, `flagged` and `margin` in exp_025's `students.csv` are inverted
  (`p_risk` is P(pass)); no number here uses them. See the TODO(ml) in
  `run_local_stability.py`.
