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
  OULAD.

## Key Result

The full Digital Twin representation was not justified. In `exp_001`, `C_twin`
did not improve over `B_lms` and deteriorated under the forward split. The
best internal candidate was the lean `B_lms_plus_mastery` subset, which
improved primary-split RMSE from `2.101` to `1.894` and improved several early
weekly snapshots. This candidate was validated with a redundancy caveat because
`overall_mastery` is very close to cumulative LMS score behavior.

## Explainability Result

The XAI phase used permutation importance and local median-replacement
perturbations. It found that the lean Twin remained teacher-meaningful and did
not collapse onto a single mastery feature. The top global feature was
`activity_score_to_date` with importance share `0.648`; `overall_mastery`
ranked second with share `0.178`. The method is explicitly model-behavior
explanation, not causal explanation and not SHAP.

## External Benchmark Result

OULAD complicated the internal finding. On the primary grouped OULAD split,
`B_lms_plus_mastery_oulad` was slightly worse than `B_lms_oulad`
(`12.724` versus `12.658` RMSE). On the secondary temporal-forward split, it
was better (`9.161` versus `9.566` RMSE). This means external transfer remains
unresolved.

## Final Contribution

The contribution is a disciplined lean Twin + XAI research prototype and
experiment governance package. It demonstrates how to construct, test,
validate, explain, and externally stress-test a teacher-oriented student-state
representation. It does not prove full Digital Twin superiority, full external
validity, or causal intervention effects.
