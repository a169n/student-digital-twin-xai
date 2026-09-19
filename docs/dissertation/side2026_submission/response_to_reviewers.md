# Response to reviewers

Paper: *Reference Points for Explanation-Stability Claims: A Five-Institution Student-Risk Benchmark* (SIDe 2026)

We thank both reviewers. Every point raised by Reviewer 4 led to a change in the manuscript; the changes are listed below, point by point, with the section or figure where they appear. One of them (point 6) exposed an error in our own Table (now Table III), which we have corrected and describe in full.

## Reviewer 2

> The paper presents a useful study ... Overall, the work is well organized and makes a useful contribution to explainable AI and learning analytics.

We thank the reviewer for the assessment. No change was requested.

## Reviewer 4

### 1. "The manuscript states five platforms and four countries, but Table I lists three platforms and five countries; correct these inconsistencies."

The reviewer is right and Table I was correct. Three institutions run Moodle, one runs the OU VLE and one runs Toledo, so there are three platforms; and the five institutions are in the UK, South Africa, Belgium, Spain and Zambia, so there are five countries. We have corrected the abstract, contribution 1, the heading of Section III-A, the total row of Table I, Section VI and the conclusion to read "three platforms, five countries".

### 2. "The paper is not anonymised."

The submission is now anonymised: the author block is replaced by "Anonymous submission", and the repository link in the Reproducibility section is replaced by a note that an anonymised repository is linked from the submission record. No self-identifying text remains in the body; the one self-citation is cited in the third person, as the guidelines allow.

### 3. "Outcome definitions differ across institutions and are confounded with institution; limit cross-institution comparisons accordingly."

We agree, and we have made the restriction explicit rather than leaving it to the reader:

- Section III-A now states which numbers in the paper are cross-institution (the per-institution means of Table I, the variance share in Section V-A, and the bottom rung of Fig. 3) and that each is reported as a description of the corpus, not as an effect of institution.
- The same paragraph now states that the measurement result of Sections V-B and V-C rests only on comparisons within one cohort or one course, where the outcome definition is held fixed. This is the case by construction: the 78 course-year pairs of Table III are all same-course pairs.
- The caption of Table I and the variance-share sentence in Section V-A now carry the caveat directly, and the Limitations paragraph repeats it.

### 4. "Clarify whether repeated students were kept in different training and test folds for within-cohort validation."

Within a cohort a student contributes exactly one row (a student enrolled in two parallel sections of one course is deduplicated at cohort construction), so the folds of the 5-fold within-cohort cross-validation never share a student. Repetition is a cross-cohort matter: 22.5 % of students appear in more than one cohort, and Section V-D reports, per source–target pair, how many students the training cohort shares with the evaluation cohort. Section III-A now says this in two sentences.

### 5. "Report results for the logistic-regression and random-forest robustness checks, not only the gradient-boosting model."

Added as Table II, with a paragraph in Section V-A. The table gives mean within-cohort ROC-AUC per institution for gradient boosting, logistic regression and random forest on the shared schema, beside the zero-training rule, and a final row for cross-institution transfer on pairs that share no student. The ordering of institutions is identical under all three models; the models sit within 0.05 of one another at every institution but Zambia (117 students in two cohorts); logistic regression is the best overall (0.717 against 0.691 and 0.692). We have also corrected a sentence in Section V-B that described the explainer comparison as spanning "three model families": the explanation analyses use the gradient-boosting model only, because TreeSHAP is defined for tree ensembles and those analyses hold the model fixed while the estimator varies. Section IV now says so.

### 6. "Add statistical tests or confidence intervals for the explanation-stability differences, especially the claimed estimator effect."

Added throughout, and this request exposed an error in our own table, which we set out plainly.

**What was added.** Every agreement figure in the paper now carries a 95 % percentile bootstrap interval that resamples clusters rather than rows: cohorts for the floor, the ceiling and the between-estimator agreement (Section V-B, Fig. 3); target cohorts for the three transfer rungs (Fig. 3); and course-year pairs for everything in Table III. The estimator effect is a paired difference on the same 78 pairs, so it has a paired bootstrap interval and a Wilcoxon signed-rank test: the level differs by 0.252 (0.204–0.298; p < 0.001). The intervals are computed by a released script from the released per-pair files.

**What was wrong.** In the submitted version the "cost of one year" column was the mean self-agreement over all 63 cohorts minus the mean next-year agreement over the 78 course-year pairs. Those are different populations: the 78 pairs come from 16 courses at four institutions, and their cohorts have higher self-agreement than the 63-cohort mean. Computing the cost per pair, against the self-agreement of the cohorts in that pair, gives 0.129 (0.091–0.167) under SHAP and 0.173 (0.123–0.224) under permutation importance, not 0.083 and 0.089. The paired difference of −0.043 has an interval of −0.095 to 0.009 (p = 0.15), so the two estimators still measure an effect of one size as far as these pairs can tell, but the level shift of 0.252 is 1.7 times the mean effect, not three times. The abstract, Section V-C, Table III and the conclusion now carry the corrected figures, and the conclusion's claim is stated as "moves by more than the effect under study". The qualitative conclusion is unchanged; the quantitative one is weaker and, we believe, now right.

The Limitations paragraph states what the intervals do and do not price: they resample cohorts or pairs but not students within them, and pairs from one course family are not independent, so the Table III intervals are narrower than a family-clustered interval would be.

### 7. "Figures 1 and 2 are dense and difficult to read; enlarge labels and explain the reference-point comparisons more clearly."

Both figures were redrawn.

- The cohort figure (now Fig. 2) spans both columns and has two panels with 9 pt labels: (a) every cohort by size and pass rate, (b) the sorted within-cohort AUC with intervals. Panel (a) is new and answers point 8 as well.
- The agreement figure (now Fig. 3) spans both columns with 9 pt labels; the floor and the ceiling are named in their own bar labels and marked by dotted guides on the axis, the random baseline (τ = 0) is the axis origin rather than a zero-length bar, and every bar carries its interval. The opening paragraph of Section V-B now explains in order how each bar is read against the reference points and why the two cross-estimator bars are read against Table III instead; the caption itself was shortened accordingly.
- Table III was widened to both columns so that each estimate and its interval sit on one line.

### 8. "Add clearer figures and graphs to show the benchmark pipeline, cohort distribution."

Added. Fig. 1 is a schematic of the pipeline from the five releases through adapters, cutoff, cohort admission, models, source–target pairs and estimators to the reference points. Fig. 2(a) shows the cohort distribution: all 63 cohorts by size, pass rate and institution.

## Other changes

- The Terminology paragraph of Section III-B was shortened to keep the paper within six pages after the additions above.
- The Limitations paragraph previously said the 78 course-year pairs came from "six course families"; they come from 16 course families at four institutions, and the text now says so.
