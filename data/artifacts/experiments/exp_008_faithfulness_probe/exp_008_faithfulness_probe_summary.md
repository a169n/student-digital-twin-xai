# exp_008_faithfulness_probe: Controlled XAI faithfulness probe on synthetic generator oracle

> **Methods appendix.** This is a controlled probe on *known* ground truth.
> It is never primary evidence about learning, and recovering the importance
> ordering of a formula we designed is a controlled instrument, not a claim
> about real student outcomes.

## Objective

A controlled known-ground-truth probe of whether permutation/native importance recovers the generator's oracle weight ordering at the final course week (week 10), and how proxy/redundancy structure shapes importance. This is explicitly a methods appendix: recovering the ordering of a formula we designed is a controlled instrument, not a claim about real learning.


## Dataset / config

- Schema version: `v1.2`
- Dataset version: `v1_3_refined` / `generator_v1_3_refined.yaml`
- Config: `services/ml/configs/experiments/exp_008_faithfulness_probe.yaml`
- Final week used: `10` (114 rows, 114 students)

## Oracle-recovery probe

Feature set: exactly the 4 oracle features. Comparison: importance rank order vs oracle-weight rank order via Kendall tau.

**Oracle-ordering Kendall tau: `1.0000`**

| feature | oracle weight | oracle rank | importance share | importance rank |
| --- | ---: | ---: | ---: | ---: |
| avg_assignment_score_to_date | 0.55 | 1 | 0.631 | 1 |
| avg_quiz_score_to_date | 0.25 | 2 | 0.288 | 2 |
| attendance_rate_to_date | 0.10 | 3 | 0.042 | 3 |
| on_time_submission_rate_to_date | 0.10 | 4 | 0.039 | 4 |

Oracle weight order (desc): `['avg_assignment_score_to_date', 'avg_quiz_score_to_date', 'attendance_rate_to_date', 'on_time_submission_rate_to_date']`
Importance order (best-first): `['avg_assignment_score_to_date', 'avg_quiz_score_to_date', 'attendance_rate_to_date', 'on_time_submission_rate_to_date']`

*Note:* Ties at oracle_weight=0.10 (attendance_rate/on_time) make exact tail ordering ambiguous. Permutation importance reflects weight x feature-spread, not weight alone; partial recovery is expected and is the methodological point.

## Proxy demonstration (B_lms feature set)

`activity_score_to_date` importance share: `0.108` (rank 4 of 9 features).

activity_score_to_date enters base_score at +0.04 (submissions.py:83) as a latent-driven proxy under correlation. Importance attributed to it reflects proxy-correlation importance, not a direct formula coefficient.

## Redundancy diagnostic

| feature A | feature B | Pearson r |
| --- | --- | ---: |
| overall_mastery | avg_assignment_score_to_date | 0.9944 |

## Explicit caveats

- This probe uses a synthetic dataset where `final_grade` is a deterministic function of the 4 oracle features. Recovering the importance ordering is a controlled instrument; it cannot be generalized to claims about real learning.
- Permutation importance reflects weight multiplied by feature spread (variance × model sensitivity), not oracle weight alone. Partial or imperfect rank recovery is expected and is the methodological point.
- Ties in oracle weight (both attendance_rate and on_time at 0.10) make exact tail ordering ambiguous.
- SHAP: `false` (not a declared project dependency).

## Limitations

- The dataset is synthetic and final_grade is a deterministic weighted mean of the 4 oracle features. Importance-ordering recovery is a controlled instrument for methods validation only, not a claim about real learning.

- Permutation importance on a small held-out set (~28 rows) has high variance; the Kendall tau is indicative, not a definitive metric.

- SHAP is not used; this experiment uses documented sklearn permutation importance fallbacks only.

- The proxy feature set (B_lms) includes activity_score_to_date, which enters base_score via an indirect path (+0.04, submissions.py:83); importance attributed to it under correlation is a structural property of the data-generating process, not a calibration error.


## Next step

Use these findings in the methods appendix to document XAI faithfulness under known ground truth. Do not elevate to a headline experiment; report alongside exp_004/exp_007 as methodological context.


