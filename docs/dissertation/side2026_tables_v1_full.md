# SIDe 2026 - result tables

Generated from `data\artifacts\experiments\exp_014_transfer_ladder\f33`.

## Table I. Benchmark composition

| Institution | Cohorts | Courses | Students | Students / cohort (min-max) | Pass rate (min-max) |
|---|---|---|---|---|---|
| KU Leuven | 6 | 2 | 3951 | 335-756 | 0.51-0.75 |
| OULAD | 19 | 6 | 30059 | 365-2498 | 0.34-0.73 |
| Oviedo | 20 | 20 | 3789 | 82-596 | 0.26-0.84 |
| UKZN | 16 | 8 | 7254 | 99-1113 | 0.60-0.95 |
| Zambia | 3 | 1 | 183 | 52-76 | 0.21-0.64 |
| **Total** | 64 | 37 | 45236 |  |  |

## Table II. Transfer ladder, ROC-AUC

_Paired over the 40 target cohorts present at all four distances._

| Model | Representation | D0 within cohort | D1 same course, other year | D2 other course, same inst. | D3 other institution | D0-D3 loss |
|---|---|---|---|---|---|---|
| Gradient boosting | percentile | 0.747 | 0.720 | 0.725 | 0.637 | 0.111 |
| Gradient boosting | raw | 0.746 | 0.728 | 0.710 | 0.616 | 0.131 |
| Gradient boosting | zscore | 0.746 | 0.722 | 0.723 | 0.629 | 0.117 |
| Logistic regression | percentile | 0.773 | 0.752 | 0.753 | 0.686 | 0.087 |
| Logistic regression | raw | 0.775 | 0.745 | 0.739 | 0.602 | 0.173 |
| Logistic regression | zscore | 0.775 | 0.758 | 0.760 | 0.691 | 0.085 |
| Random forest | percentile | 0.750 | 0.736 | 0.733 | 0.664 | 0.086 |
| Random forest | raw | 0.750 | 0.738 | 0.729 | 0.659 | 0.092 |
| Random forest | zscore | 0.751 | 0.736 | 0.736 | 0.664 | 0.087 |

## Table III. F1 at a fixed 0.5 threshold

| Model | Representation | D0 within cohort | D1 same course, other year | D2 other course, same inst. | D3 other institution |
|---|---|---|---|---|---|
| Gradient boosting | percentile | 0.810 | 0.801 | 0.780 | 0.639 |
| Gradient boosting | raw | 0.809 | 0.765 | 0.717 | 0.507 |
| Gradient boosting | zscore | 0.809 | 0.798 | 0.784 | 0.620 |
| Logistic regression | percentile | 0.824 | 0.812 | 0.794 | 0.629 |
| Logistic regression | raw | 0.828 | 0.764 | 0.752 | 0.489 |
| Logistic regression | zscore | 0.828 | 0.822 | 0.804 | 0.615 |
| Random forest | percentile | 0.819 | 0.810 | 0.789 | 0.642 |
| Random forest | raw | 0.819 | 0.791 | 0.751 | 0.532 |
| Random forest | zscore | 0.818 | 0.810 | 0.794 | 0.618 |

## Table IV. Explanation agreement with the local model

_Kendall tau and top-3 Jaccard between the transferred model's permutation-importance ranking on the target and the ranking of a model trained on that target._

| Model | Representation | D1 same course, other year tau | D1 same course, other year J@3 | D2 other course, same inst. tau | D2 other course, same inst. J@3 | D3 other institution tau | D3 other institution J@3 |
|---|---|---|---|---|---|---|---|
| Gradient boosting | percentile | 0.196 | 0.423 | 0.097 | 0.366 | 0.026 | 0.320 |
| Gradient boosting | raw | 0.217 | 0.418 | 0.089 | 0.372 | 0.038 | 0.336 |
| Gradient boosting | zscore | 0.186 | 0.430 | 0.121 | 0.373 | 0.035 | 0.326 |
| Logistic regression | percentile |  |  |  |  |  |  |
| Logistic regression | raw |  |  |  |  |  |  |
| Logistic regression | zscore |  |  |  |  |  |  |
| Random forest | percentile |  |  |  |  |  |  |
| Random forest | raw |  |  |  |  |  |  |
| Random forest | zscore |  |  |  |  |  |  |

## Table V. Pooled sources

| Model | Representation | Source pool | KU Leuven | OULAD | Oviedo | UKZN | Zambia |
|---|---|---|---|---|---|---|---|
| Gradient boosting | percentile | P_in_leave_one_cohort_out | 0.647 | 0.858 | 0.604 | 0.689 | 0.536 |
| Gradient boosting | percentile | P_out_other_institutions | 0.625 | 0.784 | 0.617 | 0.685 | 0.630 |
| Gradient boosting | raw | P_in_leave_one_cohort_out | 0.636 | 0.859 | 0.586 | 0.650 | 0.543 |
| Gradient boosting | raw | P_out_other_institutions | 0.615 | 0.636 | 0.577 | 0.634 | 0.589 |
| Gradient boosting | zscore | P_in_leave_one_cohort_out | 0.651 | 0.858 | 0.605 | 0.698 | 0.473 |
| Gradient boosting | zscore | P_out_other_institutions | 0.631 | 0.727 | 0.621 | 0.672 | 0.661 |
| Logistic regression | percentile | P_in_leave_one_cohort_out | 0.665 | 0.854 | 0.625 | 0.715 | 0.567 |
| Logistic regression | percentile | P_out_other_institutions | 0.646 | 0.841 | 0.626 | 0.686 | 0.641 |
| Logistic regression | raw | P_in_leave_one_cohort_out | 0.654 | 0.859 | 0.620 | 0.698 | 0.571 |
| Logistic regression | raw | P_out_other_institutions | 0.635 | 0.827 | 0.619 | 0.691 | 0.610 |
| Logistic regression | zscore | P_in_leave_one_cohort_out | 0.662 | 0.859 | 0.620 | 0.714 | 0.581 |
| Logistic regression | zscore | P_out_other_institutions | 0.651 | 0.842 | 0.628 | 0.696 | 0.641 |
| Random forest | percentile | P_in_leave_one_cohort_out | 0.630 | 0.850 | 0.624 | 0.682 | 0.534 |
| Random forest | percentile | P_out_other_institutions | 0.607 | 0.761 | 0.610 | 0.669 | 0.603 |
| Random forest | raw | P_in_leave_one_cohort_out | 0.602 | 0.848 | 0.579 | 0.618 | 0.524 |
| Random forest | raw | P_out_other_institutions | 0.562 | 0.654 | 0.555 | 0.577 | 0.577 |
| Random forest | zscore | P_in_leave_one_cohort_out | 0.639 | 0.850 | 0.621 | 0.682 | 0.538 |
| Random forest | zscore | P_out_other_institutions | 0.614 | 0.684 | 0.609 | 0.674 | 0.604 |

## Table VI. Few-shot calibration on the target cohort

| Labelled target students (k) | KU Leuven | OULAD | Oviedo | UKZN | Zambia |
|---|---|---|---|---|---|
| 0 | 0.614 | 0.778 | 0.617 | 0.674 | 0.604 |
| 25 | 0.619 | 0.799 | 0.624 | 0.676 | 0.543 |
| 50 | 0.621 | 0.815 | 0.630 | 0.671 |  |
| 100 | 0.624 | 0.828 | 0.598 | 0.667 |  |

## Table VII. Feature-richness control (OULAD only, gradient boosting)

| Feature set | Features | D0 within cohort | D1 same course | D2 other course | D0-D2 loss |
|---|---|---|---|---|---|
| A_engagement_plus_assessment | 17 | 0.902 | 0.893 | 0.881 | 0.021 |
| E_rich_engagement | 11 | 0.861 | 0.856 | 0.821 | 0.040 |
| S_shared7 | 7 | 0.858 | 0.854 | 0.836 | 0.022 |
