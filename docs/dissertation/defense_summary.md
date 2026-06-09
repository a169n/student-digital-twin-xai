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

The XAI phase used permutation importance and local median-replacement
perturbations. It found that the lean Twin remained teacher-meaningful and did
not collapse onto a single mastery feature. The top global feature was
`activity_score_to_date` with importance share `0.648`; `overall_mastery`
ranked second with share `0.178`. The method is explicitly model-behavior
explanation, not causal explanation and not SHAP.

## External Benchmark Result (Decisive)

The full nested ablation on real OULAD (`exp_006`, module `DDD 2013J`,
`67830` snapshots, `1938` students) is the decisive external evidence, and it
is a **mixed-to-null result**. Under a fixed-model (gradient boosting)
comparison, no Twin feature block beats the strong `B_lms_oulad` baseline by
more than `1.0` RMSE on either split. The largest gain is the mastery analogue
on the temporal-forward split (`9.561` → `9.180`, delta `-0.381`), but it is
`+0.061` worse on the student-grouped split; the full `C_twin_oulad` is within
`±0.025` RMSE of the baseline on both splits. Critically, the OULAD
classification target is genuinely predictive — best-model F1 `0.83`–`0.887`,
never `1.000` — which directly contrasts the synthetic `passed` saturation at
F1 `1.000` and confirms that the synthetic "mastery advantage" was an artifact
of a circular target that did not transfer to real data.

## Final Contribution

The contribution is **methodological and cautionary**, not a performance
claim: (i) a reproducible, leakage-aware protocol for constructing, ablating,
and explaining weekly student-state representations; (ii) a synthetic-to-real
demonstration that a circular target can manufacture an apparent feature-group
advantage that vanishes on genuine OULAD data; and (iii) an honest
mixed-to-null real-data finding, with explanation-stability / importance-
transfer analysis as the planned positive result on top of it. It does not
prove Digital Twin superiority, full external validity, or causal intervention
effects, and its external evidence rests on one OULAD module-presentation
pending replication on a second cohort.
