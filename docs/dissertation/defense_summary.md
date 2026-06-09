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
mixed-to-null real-data finding, with the explanation-stability analysis
(`exp_007`, regime-sensitive importance rankings) as the documented positive
result on top of it. It does not
prove Digital Twin superiority, full external validity, or causal intervention
effects, and its external evidence rests on one OULAD module-presentation
pending replication on a second cohort.
