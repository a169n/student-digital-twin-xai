# Core Claims and Nonclaims

> Terminology: throughout, "Digital Twin" denotes a **lean, time-aware weekly
> state representation**. It does not denote a counterfactual/simulation engine;
> no such capability is implemented in this prototype.

## Claims the Dissertation Can Make

- The repository implements a research-oriented, teacher-facing educational
  analytics prototype grounded in Student Digital Twin and XAI framing.
- The canonical data model separates raw LMS-like data, weekly student twin
  snapshots, and prediction or explanation artifacts.
- The synthetic experiment line uses `final_grade` as the primary supervised
  target and treats `risk_level` as a teacher-facing heuristic rather than a
  supervised target.
- The full `C_twin` representation was not justified under the present setup.
- `B_lms_plus_mastery` was the best internal lean Twin candidate on the
  primary synthetic split.
- The mastery block improved several early weekly snapshots, supporting the
  early-warning framing within the controlled synthetic environment.
- `overall_mastery` is highly redundant with cumulative LMS performance and
  must be treated as a caveat.
- The lean Twin remained interpretable under permutation importance and local
  perturbation explanations in `exp_004`.
- The explanation methods describe model behavior and are useful for teacher
  interpretation under the current prototype scope.
- The OULAD benchmark is a public external stress test that produced mixed
  transfer evidence.
- The final contribution is methodological and structural: a governed pipeline
  for constructing, testing, validating, explaining, and stress-testing a lean
  student-state representation.

## Claims the Dissertation Cannot Make

- It cannot claim that the full Digital Twin outperformed the LMS baseline.
- It cannot claim that richer Twin features are generally better than LMS
  analytics features.
- It cannot claim that the custom synthetic dataset is better than OULAD.
- It cannot claim full external validity.
- It cannot claim validation on a local institutional cohort.
- It cannot claim that OULAD confirms the synthetic mastery advantage.
- It cannot claim that OULAD invalidates the synthetic result.
- It cannot claim causal explanation or causal intervention effects.
- It cannot claim that SHAP was used.
- It cannot claim that `passed` is a useful discriminating target in the
  synthetic experiments, because it saturates.
- It cannot claim that `overall_mastery` is independent of cumulative LMS
  performance.
- It cannot claim that scenario simulation or intervention recommendation is
  validated by the current experiment line.
- It cannot claim that synthetic predictive accuracy (R²≈0.99, F1=1.000) reflects
  learnable signal; the synthetic target is a deterministic function of the
  features and the scores are algebraic artifacts.
- It cannot claim a what-if / counterfactual / simulation capability: none is
  implemented (`services/ml/src/features/engineering.py` and
  `services/ml/src/explainability/xai.py` are stubs). The system is a lean,
  time-aware weekly state representation, not a simulation-capable digital twin.
