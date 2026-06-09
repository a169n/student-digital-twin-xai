# Defense Summary

## Problem

The project addresses the need for a teacher-oriented educational analytics
prototype that can represent a student's evolving academic state, predict
end-of-course performance, and explain model behavior without becoming a full
LMS or overstating intervention claims.

## Method

The repository uses a versioned Student Digital Twin data model with weekly
snapshots at the grain `1 row = 1 student x 1 week`. The primary supervised
target is `final_grade`; `passed` is secondary context; `risk_level` remains a
teacher-facing heuristic and is not used as a supervised target.

The methodology proceeds through a fixed experiment sequence:

- `exp_001_baseline`: compare `A_simple`, `B_lms`, and full `C_twin`.
- `exp_002_twin_ablation`: decompose the Twin layer into feature blocks.
- `exp_003_mastery_validation`: validate the selected mastery block.
- `exp_004_xai_on_lean_twin`: explain the validated lean Twin candidate.
- `exp_005_public_benchmark_oulad`: stress-test the representation logic on
  OULAD (two-set transfer test).
- `exp_006_oulad_full_ablation`: full nested A/B/C ablation on real OULAD with
  fixed-model reporting — the decisive external evidence.
- `exp_007_xai_on_oulad`: real-data model-behavior explanation + an
  explanation-stability analysis across splits.
- `exp_008_faithfulness_probe`: controlled synthetic probe on known ground
  truth (importance recovers the weight ordering; proxy/redundancy illustration)
  — a methods appendix.
- `exp_009_oulad_ablation_bbb2013j`: second-cohort ablation on OULAD BBB 2013J.
- `exp_010_xai_on_oulad_bbb2013j`: second-cohort XAI on BBB 2013J, enabling a
  cross-cohort explanation-stability comparison with DDD.

## Key Result

The full Digital Twin representation was not justified. In `exp_001`, `C_twin`
did not improve over `B_lms` and deteriorated under the forward split. The
best internal candidate was the lean `B_lms_plus_mastery` subset, which
improved primary-split RMSE from `2.101` to `1.894` and improved several early
weekly snapshots. This candidate was validated with a redundancy caveat because
`overall_mastery` is very close to cumulative LMS score behavior. **This
synthetic improvement must be read with the circularity caveat below: the
synthetic `final_grade` is a deterministic function of the model's own
features, so the gain is an artifact, and it did not transfer to real OULAD
data (see the external benchmark result).**

## Explainability Result

The synthetic XAI phase (`exp_004`) used permutation importance and local
median-replacement perturbations. It found the lean Twin teacher-meaningful and
not collapsed onto a single mastery feature (top feature `activity_score_to_date`
share `0.648`; `overall_mastery` second at `0.178`). Model-behavior explanation,
not causal, not SHAP.

On real OULAD (`exp_007`) the same methods show the model leans on
assessment-discipline (`assessment_submission_rate_due_to_date`) and, once
included, the co-circular `overall_mastery_proxy`; the cleanest exogenous
signals (`is_unregistered_by_week`, VLE clickstream) are present but carry
modest weight. The explanation-stability analysis is itself a finding: the
importance rankings are **regime-sensitive** — Kendall `tau` between the
student-grouped and temporal-forward splits is `0.79` / `0.68` / `0.55` for the
three feature sets (mean `0.67`, none reaching `0.90`). Top-5 membership can be
stable (Jaccard `1.0` for the mastery/twin sets) while the order reorders. So
the model's "why" is not invariant to the evaluation scenario, extending
explanation-stability work (Tiukhova et al., 2024) to the transfer setting.

## External Benchmark Result (Decisive, Two Cohorts)

The full nested ablation runs on two real OULAD courses, and the result is
**heterogeneous, not uniform**. On `DDD 2013J` (`exp_006`, `67830` snapshots,
`1938` students), under a fixed-model (gradient boosting) comparison, no Twin
block beats the strong `B_lms_oulad` baseline by more than `1.0` RMSE on either
split (the largest gain is mastery on temporal-forward, `9.561` → `9.180`,
delta `-0.381`, but `+0.061` worse on the student-grouped split). On
`BBB 2013J` (`exp_009`, `80532` snapshots, `2237` students, richer assessment
structure), the mastery block **does** beat the baseline on temporal-forward by
`-1.026` RMSE (`6.311` → `5.284`) and `C_twin_oulad` by `-0.765`, but on the
student-grouped split every block stays within `0.087` (null, as on DDD), and
the trend/index blocks are null on both courses. Critically, the OULAD
classification target is genuinely predictive throughout — best-model F1
`0.83`–`0.93`, never `1.000` — which directly contrasts the synthetic `passed`
saturation at F1 `1.000` and confirms that the synthetic "mastery advantage"
was an artifact of a circular target. The honest cross-course statement is that
engineered Twin value is **course- and split-dependent**: it can help when the
assessment structure is rich and the evaluation is forward-in-time, but it does
not generalize across splits, blocks, or courses. The accompanying explanations
(`exp_007`, `exp_010`) are regime-sensitive within a course (Kendall `tau`
`0.55`–`0.79`) and partly course-specific across courses (`0.32`–`0.61`,
mean `0.52`).

## Final Contribution

The contribution is **methodological and cautionary**, not a performance
claim: (i) a reproducible, leakage-aware protocol for constructing, ablating,
and explaining weekly student-state representations; (ii) a synthetic-to-real
demonstration that a circular target can manufacture an apparent feature-group
advantage that fragments on genuine OULAD data; (iii) an honest two-cohort
finding that engineered Twin value is course- and split-dependent rather than
robust; and (iv) within-course and cross-course explanation-stability analyses
(`exp_007`, `exp_010`) showing importance rankings are regime-sensitive and
partly course-specific. It does not prove Digital Twin superiority, full
external validity, or causal intervention effects, and its external evidence
spans two OULAD courses from one institution.
