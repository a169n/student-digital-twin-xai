# Benchmark Comparison

- Left: `v1_2_baseline` -> `C:\Users\a1byn\Desktop\dev\aitu\student-digital-twin-xai\tmp_dataset_v1_2_baseline`
- Right: `v1_3_refined` -> `C:\Users\a1byn\Desktop\dev\aitu\student-digital-twin-xai\tmp_dataset_v1_3_refined`

## Key Metrics
| Metric | Left | Right | Delta |
| --- | --- | --- | --- |
| `student_twin_snapshots_rows` | `1200` | `1200` | `0` |
| `risk_high_share` | `0.0975` | `0.1117` | `0.0142` |
| `risk_medium_share` | `0.3458` | `0.3358` | `-0.01` |
| `pass_rate` | `0.7368` | `0.7281` | `-0.0087` |
| `final_grade_mean` | `59.4668` | `58.8186` | `-0.6482` |
| `attendance_last_week_mean` | `0.565` | `0.5387` | `-0.0263` |
| `activity_last_week_mean` | `44.6507` | `44.0038` | `-0.6469` |
| `late_submission_rate` | `0.2662` | `0.2767` | `0.0105` |
| `missed_submission_rate` | `0.24` | `0.2367` | `-0.0033` |
| `high_risk_share_before_week_5` | `0.1125` | `0.1042` | `-0.0083` |
| `declining_final_week_risk` | `0.2493` | `0.3208` | `0.0715` |
| `improving_final_week_risk` | `0.2775` | `0.2257` | `-0.0518` |
| `trajectory_risk_ordering_valid` | `False` | `True` | `None` |
| `trajectory_grade_ordering_valid` | `False` | `True` | `None` |
| `trajectory_pass_ordering_valid` | `False` | `True` | `None` |

## Weekly Risk Shares
- Left: `{1: {'counts': {'low': 61, 'medium': 45, 'high': 14}, 'shares': {'low': 0.5083, 'medium': 0.375, 'high': 0.1167}}, 2: {'counts': {'low': 71, 'medium': 38, 'high': 11}, 'shares': {'low': 0.5917, 'medium': 0.3167, 'high': 0.0917}}, 3: {'counts': {'low': 65, 'medium': 39, 'high': 16}, 'shares': {'low': 0.5417, 'medium': 0.325, 'high': 0.1333}}, 4: {'counts': {'low': 64, 'medium': 43, 'high': 13}, 'shares': {'low': 0.5333, 'medium': 0.3583, 'high': 0.1083}}, 5: {'counts': {'low': 66, 'medium': 44, 'high': 10}, 'shares': {'low': 0.55, 'medium': 0.3667, 'high': 0.0833}}, 6: {'counts': {'low': 70, 'medium': 38, 'high': 12}, 'shares': {'low': 0.5833, 'medium': 0.3167, 'high': 0.1}}, 7: {'counts': {'low': 69, 'medium': 43, 'high': 8}, 'shares': {'low': 0.575, 'medium': 0.3583, 'high': 0.0667}}, 8: {'counts': {'low': 64, 'medium': 45, 'high': 11}, 'shares': {'low': 0.5333, 'medium': 0.375, 'high': 0.0917}}, 9: {'counts': {'low': 68, 'medium': 41, 'high': 11}, 'shares': {'low': 0.5667, 'medium': 0.3417, 'high': 0.0917}}, 10: {'counts': {'low': 70, 'medium': 39, 'high': 11}, 'shares': {'low': 0.5833, 'medium': 0.325, 'high': 0.0917}}}`
- Right: `{1: {'counts': {'low': 66, 'medium': 42, 'high': 12}, 'shares': {'low': 0.55, 'medium': 0.35, 'high': 0.1}}, 2: {'counts': {'low': 68, 'medium': 45, 'high': 7}, 'shares': {'low': 0.5667, 'medium': 0.375, 'high': 0.0583}}, 3: {'counts': {'low': 62, 'medium': 45, 'high': 13}, 'shares': {'low': 0.5167, 'medium': 0.375, 'high': 0.1083}}, 4: {'counts': {'low': 68, 'medium': 34, 'high': 18}, 'shares': {'low': 0.5667, 'medium': 0.2833, 'high': 0.15}}, 5: {'counts': {'low': 70, 'medium': 34, 'high': 16}, 'shares': {'low': 0.5833, 'medium': 0.2833, 'high': 0.1333}}, 6: {'counts': {'low': 67, 'medium': 39, 'high': 14}, 'shares': {'low': 0.5583, 'medium': 0.325, 'high': 0.1167}}, 7: {'counts': {'low': 65, 'medium': 40, 'high': 15}, 'shares': {'low': 0.5417, 'medium': 0.3333, 'high': 0.125}}, 8: {'counts': {'low': 67, 'medium': 39, 'high': 14}, 'shares': {'low': 0.5583, 'medium': 0.325, 'high': 0.1167}}, 9: {'counts': {'low': 66, 'medium': 42, 'high': 12}, 'shares': {'low': 0.55, 'medium': 0.35, 'high': 0.1}}, 10: {'counts': {'low': 64, 'medium': 43, 'high': 13}, 'shares': {'low': 0.5333, 'medium': 0.3583, 'high': 0.1083}}}`

## Trajectory Risk by Week
- Left: `{'consistently_at_risk': {1: 0.5135, 2: 0.5208, 3: 0.5372, 4: 0.5341, 5: 0.5264, 6: 0.5253, 7: 0.5276, 8: 0.5342, 9: 0.5347, 10: 0.5375}, 'declining': {1: 0.1789, 2: 0.171, 3: 0.1857, 4: 0.1981, 5: 0.1981, 6: 0.2067, 7: 0.2228, 8: 0.2351, 9: 0.2399, 10: 0.2493}, 'improving': {1: 0.3267, 2: 0.3114, 3: 0.3193, 4: 0.3241, 5: 0.3139, 6: 0.3005, 7: 0.2947, 8: 0.2968, 9: 0.29, 10: 0.2775}, 'stable_high': {1: 0.07, 2: 0.0765, 3: 0.08, 4: 0.0783, 5: 0.0738, 6: 0.0762, 7: 0.0825, 8: 0.0866, 9: 0.0938, 10: 0.0898}}`
- Right: `{'consistently_at_risk': {1: 0.5004, 2: 0.5076, 3: 0.5249, 4: 0.533, 5: 0.5343, 6: 0.5354, 7: 0.5387, 8: 0.5418, 9: 0.5404, 10: 0.5414}, 'declining': {1: 0.1895, 2: 0.209, 3: 0.2438, 4: 0.2457, 5: 0.2462, 6: 0.2638, 7: 0.2905, 8: 0.2941, 9: 0.3079, 10: 0.3208}, 'improving': {1: 0.2701, 2: 0.2707, 3: 0.2911, 4: 0.2771, 5: 0.2677, 6: 0.2619, 7: 0.2557, 8: 0.2489, 9: 0.2365, 10: 0.2257}, 'stable_high': {1: 0.0671, 2: 0.086, 3: 0.0879, 4: 0.0893, 5: 0.0818, 6: 0.0841, 7: 0.0858, 8: 0.0854, 9: 0.0892, 10: 0.0854}}`

## Outcome Ordering
- Left: `{'mean_final_grade': {'consistently_at_risk': 25.6883, 'declining': 67.4133, 'improving': 61.2917, 'stable_high': 88.3484}, 'pass_rate': {'consistently_at_risk': 0.0, 'declining': 1.0, 'improving': 1.0, 'stable_high': 1.0}, 'grade_ordering_expected': ['stable_high', 'improving', 'declining', 'consistently_at_risk'], 'pass_ordering_expected': ['stable_high', 'improving', 'declining', 'consistently_at_risk'], 'grade_ordering_valid': False, 'pass_ordering_valid': False}`
- Right: `{'mean_final_grade': {'consistently_at_risk': 25.6087, 'declining': 57.573, 'improving': 68.6769, 'stable_high': 88.7296}, 'pass_rate': {'consistently_at_risk': 0.0, 'declining': 0.9667, 'improving': 1.0, 'stable_high': 1.0}, 'grade_ordering_expected': ['stable_high', 'improving', 'declining', 'consistently_at_risk'], 'pass_ordering_expected': ['stable_high', 'improving', 'declining', 'consistently_at_risk'], 'grade_ordering_valid': True, 'pass_ordering_valid': True}`

## Warnings
- Left: `['Final-week risk ordering is weak or inverted; expected consistently_at_risk > declining > improving > stable_high.', 'Final-grade ordering is weak or inverted; expected stable_high > improving > declining > consistently_at_risk.', 'Pass-rate ordering is weak or inverted; expected stable_high >= improving > declining > consistently_at_risk.', 'Declining trajectories do not worsen early enough to support early-warning claims.']`
- Right: `[]`
