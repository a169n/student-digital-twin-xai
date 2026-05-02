# exp_001 vs exp_002 Comparison

## Purpose

This note compares the baseline experiment with the Twin subgroup ablation so
the research progression is easy to cite.

## What Changed

| area | `exp_001_baseline` | `exp_002_twin_ablation` |
| --- | --- | --- |
| Main question | Does full `C_twin` outperform simpler baselines? | Which Twin subgroups add value beyond `B_lms`? |
| Feature sets | `A_simple`, `B_lms`, `C_twin` | `B_lms`, four single-block additions, one compact combination, `C_twin_full` |
| Primary target | `final_grade` | `final_grade` |
| Secondary context | `passed` | `passed` |
| Primary split | student-grouped | student-grouped |
| Secondary split | temporal-forward with held-out students | temporal-forward with held-out students |
| Schema | `v1.2` | `v1.2` |

## Result Difference

`exp_001_baseline` showed that `C_twin` did not reliably outperform `B_lms`.
On the primary student-group split, best RMSE was:

- `B_lms`: `2.101`
- `C_twin`: `2.149`

`exp_002_twin_ablation` refined that result. On the same primary split:

- `B_lms`: `2.101`
- `B_lms_plus_mastery`: `1.894`
- `B_lms_plus_trends_mastery`: `1.973`
- `C_twin_full`: `2.149`

The ablation therefore improves scientific clarity: the full Twin set remains
unjustified, but the mastery block appears useful as a lean addition to the LMS
baseline.

## Interpretation

The current Twin layer is not useless, but it is too redundant in full form. The
best carry-forward candidate is `B_lms_plus_mastery`, not `C_twin_full`.

`passed` remains saturated with best F1 at `1.000` across feature sets, so it
should stay secondary until the dataset makes pass/fail classification less
trivial.

## Next Step

Before SHAP/XAI, review whether the generator and feature construction make
mastery too directly aligned with `final_grade`. If the relationship is
acceptable for the research prototype, use `B_lms_plus_mastery` as the lean
feature set for the first explanation phase.
