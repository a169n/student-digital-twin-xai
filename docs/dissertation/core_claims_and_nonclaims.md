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
- On real OULAD data, the full nested A/B/C ablation (`exp_006`, module
  `DDD 2013J`, fixed-model comparison) shows that no Twin feature block
  delivers a consistent advantage over a strong LMS baseline (no block better
  than `1.0` RMSE on either split; full `C_twin_oulad` within `±0.025`).
- The OULAD classification target is genuinely predictive (best-model F1
  `0.83`–`0.887`, never `1.000`), in direct contrast to the saturated
  synthetic `passed` target — evidence that the synthetic mastery advantage
  was an artifact of a circular target that did not transfer to real data.
- The synthetic-to-OULAD contrast is itself a cautionary methodological
  result: a circular target can manufacture an apparent feature-group
  advantage that disappears on genuine institutional data.
- On real OULAD (`exp_007`), the model-behavior explanations lean on
  assessment-discipline and the co-circular `overall_mastery_proxy`; the
  genuinely exogenous signals (`is_unregistered_by_week`, VLE clickstream) are
  present and interpretable but carry modest weight.
- The OULAD importance rankings are regime-sensitive: Kendall `tau` between the
  student-grouped and temporal-forward splits is `0.55`-`0.79` (none reaching
  `0.90`), so which features the model relies on, and in what order, depends on
  the evaluation scenario (extends Tiukhova et al., 2024).
- The real-data finding spans two OULAD courses and is **heterogeneous**: on
  `BBB 2013J` (`exp_009`) the mastery block beats the LMS baseline on the
  temporal-forward split by `-1.026` RMSE, whereas on `DDD 2013J` (`exp_006`) no
  block does; on the student-grouped split both courses are null and the
  trend/index blocks are null on both. Engineered Twin value is therefore
  course- and split-dependent, not robust.
- The explanations are partly course-specific: cross-cohort importance-ranking
  agreement (DDD vs BBB, `exp_010`) is Kendall `tau` `0.32`-`0.61` (mean `0.52`),
  below the within-course cross-split agreement and below a stability threshold.
- A second institution (KU Leuven, `exp_011`, engagement-only, classification of
  `PASSED`) extends the external check: engagement predicts passing only modestly
  (F1 `0.75`-`0.76`) and a richer engagement representation does not beat a
  minimal one (fixed-model F1 delta `-0.015`/`+0.000`), so feature-richness again
  fails to help robustly. The mastery ablation cannot be built on KU Leuven at
  all (no intermediate assessments, no continuous grade).
- A controlled synthetic faithfulness probe (`exp_008`) on known ground truth
  shows that, at the final course week, permutation importance recovers the
  generator's weight ORDERING (Kendall `tau` `1.0`), and illustrates how proxy
  correlation (`activity_score_to_date` importance `0.108`) and redundancy
  (`overall_mastery` vs `avg_assignment_score_to_date`, `r` `0.994`) shape
  importance. This is a methods instrument on a target we authored, not
  evidence about real learning.
- The final contribution is methodological and cautionary: a governed,
  leakage-aware pipeline for constructing, ablating, explaining, and
  externally testing a lean student-state representation, plus an honest
  two-cohort heterogeneous real-data finding and within- and cross-course
  explanation-stability results.

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
- It cannot claim a single uniform real-data verdict. The OULAD evidence spans
  two module-presentations (`DDD 2013J`, `BBB 2013J`) and is heterogeneous —
  neither a uniform null nor a uniform Twin benefit.
- It cannot claim a like-for-like institutional replication on KU Leuven. The
  KU Leuven check is engagement-only and classifies `PASSED`; it cannot test
  the mastery/Twin ablation and its task differs from OULAD, so its modest
  numbers must not be compared head-to-head with OULAD's assessment-driven
  results. Full external validity across institutions is not established.
- It cannot claim that the explanations are regime-invariant or that
  importance reflects causal mechanism. The OULAD rankings reorder across
  splits, and the methods describe model behavior, not causation.
