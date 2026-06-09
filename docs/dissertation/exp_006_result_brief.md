# exp_006 Result Brief — Real-Data Ablation and the Reframed Contribution

**Status:** decisive external result of the public-first pivot. One page, for the
supervisor conversation and the dissertation results chapter.

## What was run

The identical leakage-aware pipeline used on the synthetic data was applied to
**real OULAD** data — module-presentation `DDD 2013J`, **67,830 weekly snapshots
across 1,938 students** — as a **full nested A/B/C ablation** (`exp_006`):

- Feature sets: `A_simple_oulad`, `B_lms_oulad`, `B_lms_plus_trends_oulad`,
  `B_lms_plus_mastery_oulad`, `B_lms_plus_indices_oulad`, `C_twin_oulad`.
- Splits: student-grouped and temporal-forward, both reported.
- A **fixed-model (gradient boosting)** table to neutralize the model-flip
  artifact (best-model-per-cell can flatter a feature set).

## The result: mixed-to-null

Under the fixed-model comparison, **no Twin feature block beats the strong
`B_lms_oulad` baseline by more than 1.0 RMSE on either split.**

| Feature set | temporal-forward Δ RMSE | student-grouped Δ RMSE |
|---|---:|---:|
| `B_lms_plus_mastery_oulad` | **−0.381** | +0.061 |
| `B_lms_plus_indices_oulad` | −0.218 | +0.008 |
| `C_twin_oulad` (full) | +0.024 | −0.019 |
| `B_lms_plus_trends_oulad` | +0.077 | −0.048 |
| `A_simple_oulad` | +4.105 | +1.207 |

(Baseline `B_lms_oulad` RMSE: 9.561 temporal-forward, 12.660 student-grouped.)

- The best single gain (mastery, temporal-forward, −0.381 ≈ 4%) does not hold
  on the other split (+0.061 worse).
- The full `C_twin_oulad` is within ±0.025 RMSE of the baseline on both splits —
  **non-inferior, but not better**.
- `A_simple_oulad` is clearly worse, confirming the LMS behavioral layer carries
  the signal and the Twin engineering adds little on top of it.

**Classification is genuinely predictive: best-model F1 = 0.83–0.887, never
1.000.** This is the key contrast with the synthetic `passed` target, which
saturates at F1 = 1.000 because the synthetic `final_grade` is a deterministic
function of the features.

## Why this is a finding, not a failure

1. **Negative result that punctures hype.** "Digital twin in education" is largely
   conceptual in the literature. A careful, leakage-aware ablation showing that
   engineered twin blocks do **not** beat a competent LMS baseline on real data is
   a legitimate, citable contribution.
2. **The synthetic→real contrast is a mechanism story.** On synthetic data the
   mastery block *appeared* to help (RMSE −0.206, R²≈0.99, F1=1.000). That target
   is circular (a closed-form function of the features), so the gain was an
   artifact. Running the same pipeline on real, non-circular OULAD data, the
   advantage did not transfer. This is a concrete cautionary case: a circular
   target can manufacture an apparent representation advantage that vanishes on
   genuine data. That is more valuable than "no effect" — it explains *why* a
   false effect arose.

## Reframed contribution (what the dissertation now claims)

- A reproducible, **leakage-aware methodology** for constructing, ablating, and
  explaining weekly student-state representations.
- A **synthetic-vs-real cautionary demonstration** of circular-target artifacts.
- An **honest mixed-to-null real-data finding** on OULAD.
- **explanation-stability** analysis (`exp_007`, done): on real OULAD the
  importance rankings are regime-sensitive across splits (Kendall `tau`
  `0.55`-`0.79`, mean `0.67`, none `>= 0.90`) — the positive methodological
  result on top of the predictive null, extending Tiukhova et al. (2024).

It does **not** claim Digital Twin predictive superiority, full external
validity, or causal/intervention effects.

## Honest risk and the recommended next step

The dominant weakness is that the external evidence rests on **one OULAD
module-presentation**. A reviewer will ask whether the null is robust or
course-specific. The strongest mitigation is **replication on a second cohort**
(a further OULAD presentation via the same adapter, or an independent dataset
such as the KU Leuven 2026 release). The mixed-to-null result therefore *raises*
the value of a second real cohort from optional to recommended: "null replicates
across cohorts" turns the main weakness into a strength.

## Supervisor pitch (verbatim)

> On real OULAD data the Digital Twin feature blocks do not beat a strong LMS
> baseline (best-model F1 0.83–0.89; regression deltas within noise; mastery
> helps only on the forward-time split by ~4%). This contradicts the synthetic
> result, which we have shown was inflated by a circular target. I propose
> reframing the contribution as (1) a leakage-aware methodology, (2) a
> synthetic-vs-real cautionary demonstration, and (3) an explanation-stability /
> transfer analysis. My question: is one OULAD module sufficient, or should we
> add a second cohort (a further OULAD presentation or KU Leuven) to show the
> null is robust rather than course-specific?

## Artifacts

- Config: `services/ml/configs/experiments/exp_006_oulad_full_ablation.yaml`
- Results: `data/artifacts/experiments/exp_006_oulad_full_ablation/`
- Writeup: `docs/experiments/exp_006_oulad_full_ablation.md`
- Reconciled conclusions: `docs/dissertation/final_research_conclusions.md` (§5b, §6, §8)
