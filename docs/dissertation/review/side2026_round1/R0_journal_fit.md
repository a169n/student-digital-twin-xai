# R0 — Journal-Fit Review (seat: EIC / venue fit, originality, significance, shape)

**Venue:** SIDe 2026, IEEE, Astana — Track 1 "Computational Intelligence" (Explainable AI, fairness, bias mitigation, Trustworthy & Responsible AI). Hard limit 4–6 pages including references, IEEE two-column, double-blind, IEEE Xplore route.
**Manuscript:** `docs/dissertation/side2026_paper.md` (v1.0, 2026-09-05), with `docs/dissertation/side2026_tables.md` and five figure files in `docs/dissertation/figures/side2026/`.
**Measured length:** 4,716 words total — 312 abstract, 3,861 body (including four inline tables), 510 references. Seven further tables live in the supporting file; four figures exist.
**Scope of this seat:** venue fit, originality, significance, readership relevance, size and shape. Statistical validity and study design belong to another seat and are not adjudicated here, except where a design gap directly threatens the novelty claim.

---

## Summary of Submission

The paper builds a public benchmark of 64 real course cohorts from five universities on five different LMS platforms (45,236 students), reduces them all to a common seven-feature clickstream schema, and fixes the early-warning prediction point at one third of each course's length. It then trains a fixed classifier on every cohort and applies it to every other cohort, organising the 4,096 ordered pairs into a four-rung "transfer distance" ladder from within-cohort to cross-institution. The finding is that three distinct properties of the same model degrade at three different rates as distance grows: ranking ability loses about 0.13 AUC, a fixed 0.5 alerting threshold loses about a third of its F1, and permutation-importance rankings lose essentially all agreement with what a locally trained model would report (Kendall tau 0.03 at cross-institution distance). A label-free within-cohort percentile transform recovers a substantial part of the threshold failure and a smaller part of the discrimination failure, but does nothing for the explanation failure. Two controls argue that neither feature poverty nor OULAD's withdrawal labelling drives the result.

---

## Fit and Significance

**Does this belong in a Computational Intelligence / XAI track, or is it a learning-analytics paper wearing a CI badge?**

Honestly: right now it is about 80% learning-analytics benchmark paper and 20% trustworthy-AI paper, and the 20% is what earns it the track. Sections III (415 words), IV (340), V-A/B/C/D (694), V-F (177) and V-G (143) are a portability benchmark of the kind LAK or EDM publishes — the dataset harmonisation, the cohort admission rule, the calendar inference, the pooled-source comparison. The material that speaks to Track 1's stated topics is Section V-E (183 words, one three-row table), one paragraph of Section VI, and one paragraph of Section VII. That is roughly 400 words out of 3,861.

This is a framing problem, not a substance problem, and it is fixable — but it must be fixed, because a CI-track PC member reading this in the order written will spend four pages on cross-institution accuracy before reaching anything a Trustworthy-AI reviewer would call their own subject.

Two things do carry real weight for this readership once surfaced:

1. **The dissociation result.** "A transferred model may be safe to rank students with and unsafe to explain them with, and that these must be validated separately" (Section VII, line 206) is a trustworthy-AI claim of a kind the XAI-evaluation literature does not usually have the data to make: it requires many source/target pairs at graded distances, which is exactly what the benchmark supplies. This is the paper's reason to be at SIDe.
2. **The institution-level D0 spread.** The table in Section V-A: within-cohort AUC 0.845 at the Open University, 0.521 at the University of Zambia. An early-warning product validated on OULAD and sold to a Zambian institution would be near-useless there. That is a responsible-deployment finding with an equity dimension across four countries, and the manuscript spends one sentence on it (line 124) before moving on.

**What is missing for the track.** Track 1 explicitly lists fairness and bias mitigation. The benchmark spans the UK, Spain, Belgium, South Africa and Zambia and never once disaggregates performance by any student attribute, nor discusses whether the cross-institution AUC ordering has an equity reading. Gardner et al. [9] — cited in Related Work, line 41 — made fairness under transfer their central claim, so the omission is visible against the paper's own citation list. I do not demand a fairness analysis in 6 pages, but the paper must say why it is out of scope rather than silently skipping a headline topic of the track it targets.

**Relevance to the readership.** Adequate but not assumed. A general IEEE CI audience will not know what OULAD is, why a "module-presentation" is a cohort, or why one third of a course is a natural prediction point. The paper currently writes for LA specialists. Two sentences of framing in the Introduction fixes this, and they are worth the words.

---

## Originality Assessment

**Verdict: incremental in three of its four claimed contributions, genuinely novel in one — and the novel one is not currently the paper.**

Taken piece by piece:

- **Contribution 1, the five-institution public benchmark (Introduction, item 1).** Novel in assembly, not in kind. López-Zambrano [7] did 24 courses at one university; Riestra-González [13] did 532 courses at one university; Gardner [9] did four US institutions; Swamy [12] did 26 MOOCs. Being the first *public and multi-institution* version of this is a genuine service to the field, and the census statistic in [11] (four public datasets in the field carry activity + outcome + join key) makes the scarcity argument credible rather than self-serving. But "we harmonised five public datasets" is an artefact contribution, not a CI insight. Worth citing; not worth a headline at this venue.
- **Contribution 2, the transfer-distance ladder.** A useful organising device, not a new idea. Graded domain distance is standard practice in transfer learning; the contribution is instantiating it for LMS cohorts.
- **Contribution 3a, prediction degrades with distance.** Not novel. Schwerter et al. [10] reported exactly this, including the base-rate mechanism, and the manuscript says so at line 21. The paper's own §V-B partially *contradicts* [10] on the linear-versus-tree ordering, which is more interesting than the degradation itself and gets one clause.
- **Contribution 3b, the threshold fails harder than discrimination.** Well known in general ML as prior/prevalence shift, and the paper's own explanation ("a score calibrated to one prevalence is meaningless at another", line 132) is textbook. What is new is the *magnitude on real cohorts* — 37% of F1 against 17% of AUC. That is a quantification, not a discovery. Defensible to report, indefensible to headline.
- **Contribution 4, the label-free percentile fix.** Weakest originality claim in the paper. Within-cohort rank/quantile normalisation as a domain-alignment device is old and general (rank-gauss, quantile transformers, per-batch normalisation). §II line 41 claims "a within-cohort rescaling of the features themselves has not been tested" — that may be true *within learning analytics*, but the manuscript never says so, and as written it reads as a claim of ML novelty that will not survive a general CI reviewer.
- **Contribution 3c, explanation portability after transfer.** *This* is the novel piece. Tiukhova et al. [15] measured explanation instability across cohorts of models trained on those cohorts; nobody, as far as this reviewer knows, has asked whether the explanation a *transferred* model produces on a target agrees with the explanation a *locally trained* model on that same target would produce, at graded transfer distance, and nobody has shown that the transform which repairs the predictions leaves that agreement untouched (tau 0.026 under percentiles against 0.038 under raw counts, line 162). The dissociation — one fix, two properties, one repaired and one not — is clean, non-obvious, and the only thing here a Trustworthy-AI audience could not have predicted.

So: the paper is a repackaging of known distribution-shift results *plus* one genuinely novel explanation-transfer result, currently presented as the third of five contributions and arriving on what would be page 5. The revision must invert that ordering, or the paper does not have a novelty claim strong enough for the track.

**Caveat that bears on the novelty claim itself.** Table IV reports tau at D1, D2 and D3 but has no D0 row and no noise floor — no tau between two locally trained models on the same cohort with different seeds, no split-half agreement. With seven features, `n_repeats = 3`, and targets subsampled to 1,500 rows (§IV-F, line 104), some of the observed disagreement is estimator variance rather than transfer failure. Section V-E's own defence, that top-3 Jaccard 0.33 is "close to what random rankings would give" (line 162), cuts against the paper: it shows the metric *can* sit at chance, which is exactly why the reader needs to see where it sits when there is no transfer at all. I raise this as a significance matter rather than a statistics one: without that baseline the headline claim is not yet established, and the headline claim is the paper's only novelty.

---

## Strengths

1. **The dissociation result is real and is the right shape for this venue.** Prediction portability and explanation portability being separate properties, established over 3,034 cross-institution pairs rather than anecdotally, is worth an IEEE page.
2. **The benchmark is large enough that the negative results are not dismissible.** 64 cohorts, 4,096 ordered pairs, five platforms in four countries. A reviewer cannot answer "you only tried two courses."
3. **The two controls in §V-F are the right controls, and they pre-empt rather than defend.** Feature richness raising D0 from 0.858 to 0.902 without shrinking the D0–D2 gap (0.022 versus 0.021) kills the obvious "your features are too crude" rebuttal, and the withdrawal-exclusion control (0.858 → 0.793) addresses a tautology that much of the OULAD literature never mentions. This is unusually honest work.
4. **The compute-settings disclosure in §IV-F** — stating `n_repeats = 3`, one model family for rankings, subsampled targets, and explicitly which reported numbers are and are not affected — is disclosure most submissions omit.
5. **Limitations (§VI) are candid**, particularly the concession that the population of suitable public datasets is small enough to bound generalisation, and that label semantics are not homogeneous across the five institutions.
6. **Internal arithmetic checks out where I spot-checked it.** 4,096 = 64²; 3,034 cross-institution pairs matches 4,096 minus the within-institution pairs implied by Table I; the 37%/17% comparison in §V-C is correct against Tables II and III.

---

## Concerns

### [CRITICAL] The paper is roughly 1.7x the hard page limit, and the overflow is structural, not stylistic

4,716 words plus seven tables plus four figures. A 6-page IEEE two-column paper holds roughly 900–1,000 words of body text per page; 18 references consume about 0.55 page; title block plus a 312-word abstract another 0.3. Table V alone (18 rows × 7 columns, in `side2026_tables.md`) would consume most of a column. No formatting trick closes this gap — material must be deleted, and the paper currently reads as though everything is load-bearing. See Compression Guidance. This is a rejection risk on submission mechanics alone, independent of scientific merit.

### [CRITICAL] The novel contribution is buried, and the title does not lead with it

The title — "What Transfers and What Does Not: Predictions, Thresholds and Explanations of Early-Warning Models Across Five Institutions" — puts explanations third of three, and the abstract does the same, reaching them at line 9 after 200 words of benchmark description. The Introduction's contribution list (lines 27–31) folds explanations into item 3 and does not name them in items 1, 2, 4 or 5. For a Track 1 submission whose only genuine novelty is the explanation dissociation, this is self-defeating framing: the paper as ordered invites the reading "learning-analytics benchmark, submitted to a CI track."

### [MAJOR] Not one figure is cited anywhere in the manuscript

A search for "Fig." across `side2026_paper.md` returns nothing. Four figure files exist (`fig2_ladder_{gbm,lr,rf}_f33`, `fig3_explanations_f33`, `fig4_fewshot_f33`, plus two heatmaps) and the text refers only to Tables II–VII. Either the figures are unnecessary — in which case the space they would have consumed is part of the compression budget, and say so — or the paper is missing its visual argument. In its current state this is a text-and-tables submission, and IEEE reviewers notice. Section V-E in particular carries the headline claim in 183 words with a three-row table and no figure, when `fig3_explanations_f33` is exactly the figure that claim needs.

### [MAJOR] The Conclusion overstates the fix by roughly 50% and contradicts the Results section

Section VII line 204: the percentile representation "recovers about two thirds of the lost F1 for every model family we tested." Section V-C line 134 says "between 44 % and 47 % of the loss." Both cannot be true, and neither matches Table III. Recomputing from Table III: gradient boosting loses 0.809 − 0.507 = 0.302 and recovers 0.639 − 0.507 = 0.132, i.e. 44%; logistic regression 0.828 → 0.489, recovering to 0.629, i.e. 41%; random forest 0.819 → 0.532, recovering to 0.642, i.e. 38%. The true range is 38–44%. "Two thirds" is wrong; "44–47 %" is wrong for two of three families. A discrepancy this size between a paper's own Results and its own Conclusion is the first thing a hostile reviewer checks and the fastest way to lose the room.

### [MAJOR] The abstract promises three model families where the headline result rests on one

The abstract says "Three model families are evaluated over all 4,096 ordered cohort pairs" and then, in the same paragraph, "Explanations do not transfer at all." Table IV has explanation rows for gradient boosting only; the logistic-regression and random-forest rows are blank, by the design decision disclosed at §IV-F line 104. The disclosure exists, but it is in Method and the abstract carries no qualifier, so the paper's strongest claim reads as three-family evidence and is one-family evidence. Name the model in that sentence.

### [MAJOR] "Explanations do not transfer at all" is an overclaim at D1 and D2

The abstract, the §V-E heading, and the Conclusion all use the unqualified form. Table IV gives tau 0.20 / Jaccard 0.42 at D1 and tau 0.10 / 0.37 at D2. Weak agreement is not zero agreement. The paper's own data support "explanation agreement decays fastest with distance and is indistinguishable from chance across institutions" — stronger, more precise, and equally publishable. Reserve "at all" for D3.

### [MAJOR] Double-blind compliance is not met, and the availability claim is unsupported

Line 3 carries a local project path (`data/artifacts/experiments/exp_014_transfer_ladder/f33/`) — a blinding risk and a drafting artefact. The abstract closes with "Code, cohort definitions and frozen results are released" and §VII line 206 with "We release the benchmark, the adapters for all five institutions, and the frozen results", with no URL anywhere in the paper. Under double-blind that URL must be an anonymised mirror; with no link at all, the release claim is an assertion the reviewer cannot check — and a public benchmark the reader cannot reach is precisely the failure mode the paper criticises in [12] at line 23. That irony will be noticed.

### [MINOR] Novelty of the percentile transform is claimed too broadly

§II line 41: "a within-cohort rescaling of the features themselves has not been tested". True of learning analytics; not true of ML. Scope the sentence ("has not been tested in this literature") or a CI reviewer who knows quantile normalisation will read it as an unread-literature signal.

### [MINOR] Two broken internal cross-references

Introduction contribution 5 (line 31) points the two controls at "Section V-E"; the controls are in §V-F, and §V-E is the explanation section. §III-C line 72 repeats the same error ("Section V-E shows the restriction does not drive the results"). Both should read V-F.

### [MINOR] Reference [18] is never cited

Kapoor & Narayanan, "Leakage and the reproducibility crisis," is in the reference list and nowhere in the body. Either cite it — §III-C's leakage-safe feature construction is the natural place and would be strengthened by it — or delete it and reclaim the line. In a 4–6 page paper an orphan reference is a wasted line and an IEEE Xplore production flag.

### [MINOR] The abstract conflates the two transforms

The abstract attributes both the F1 repair and "0.089 AUC for a linear model" to the percentile transform. Per §V-D line 138 and Table II, the 0.089 belongs to the z-score transform (LR raw 0.602 → z-score 0.691); percentile gives 0.084. Small, but the abstract is the most-read 300 words in the paper and should not misattribute its own result.

### [MINOR] The abstract is 312 words

IEEE conference abstracts run 150–250. 312 words in one unbroken paragraph containing fifteen numeric results is not readable, and in a paper fighting for space it is a free 130 words.

---

## Compression Guidance

Target for 6 IEEE pages with the floats recommended below: **about 2,500–2,700 words of body prose, three tables, two figures.** That means cutting roughly 30% of the prose *and* deleting four tables and two figures. Per section, against the measured word counts:

### Load-bearing — protect these, and give §V-E more space than it has

| Section | Now | Target | Why it survives |
|---|---|---|---|
| §V-E Explanations | 183 | **250 (grow it)** | The only novel contribution. Needs the D0/noise-floor row, `fig3`, and the dissociation stated as its own claim rather than a closing sentence. |
| §V-C Threshold failure | 155 | 130 | Largest measured effect and the one the fix repairs. Deployment-relevant. |
| §V-A Within-cohort baseline | 152 | 120 | The 0.845 → 0.521 institutional spread is a Responsible-AI result and should be promoted, not trimmed. Keep the five-row table; it can absorb Table I. |
| §V-F Feature-richness control | 177 | 90 | Kills the strongest reviewer objection. Compress Table VII to one sentence with three numbers; the table itself is expendable. |
| §VI Limitations | 333 | 220 | Candour is a strength and the label-heterogeneity concession pre-empts a reviewer. Cut the prose, not the concessions. |
| §IV-F Compute disclosure | 69 | 60 | Do not cut. Deleting a disclosure to save space is the worst trade available in this paper. |

### Expendable — cut with little loss

- **§V-G Pooled sources and few-shot calibration (143 words, Tables V and VI, `fig4_fewshot_f33`) — cut entirely.** The single largest space win: Table V is 18×7 and would eat most of a column, Table VI adds another, `fig4` a third float. The findings are also the paper's weakest — "few-shot helps far less than expected," with Oviedo getting *worse* at k = 100 and Zambia's k = 50 and k = 100 cells empty in Table VI. None of it is part of the three-failure-mode story, and the "Zambia is better served by borrowing" observation rests on three cohorts totalling 183 students. Replace with one sentence in §VI: adding up to 100 labelled target students does not close the residual gap, so it is not a label-scarcity problem. Saves roughly a page and a quarter.
- **§V-H Cutoff sensitivity (199 words plus an 8-column table) — compress to about 45 words, drop the table.** The result is "nothing changes"; one sentence with the two ranges carries it (cross-institution AUC loss 0.124–0.133 and tau 0.032–0.039 at cutoffs of ¼, ⅓ and ½). Seven columns to report a passed robustness check is not a use of an IEEE column.
- **§III-B Enrolment, calendars and privacy (101 words) — compress to about 30.** The calendar-inference rule and the enrolment intersection are one clause each. Keep the Zambia personal-names disclosure — it is an ethics point and it is cheap.
- **§II Related Work (307 → 200).** Merge the "Prediction and explanation on public LMS data" paragraph into two sentences; it exists only to establish that single-cohort reporting is the norm. Keep [7]–[10] and [15] at one clause each, and keep the gap statement.
- **§I Introduction (534 → 320).** The five-item contribution list is the problem. Items 1 and 2 (benchmark, ladder) are apparatus and belong in one item; item 5 (controls) is due diligence, not a contribution, and belongs in Results. Restructure to three items, explanations first.
- **Abstract (312 → 180).** Cut the per-institution cohort breakdown (it is Table I), cut the two-control sentence entirely, cut the shift-regression clause. Lead with the dissociation.
- **§V-D mechanism analysis (287 → 170).** Keep the three-row shift table — it is what turns "a trick that worked" into a mechanism, and it is what licenses the good argument at line 150 that the finding is about measured distance rather than institution identity. Cut the R² prose: 11.6% versus 6.2% of pair-level variance is a weak number that invites attack for little return.
- **§VII Conclusion (272 → 130).** Currently restates the whole Results section. Two paragraphs suffice: the dissociation, and what a practitioner must therefore validate separately.

### Float budget

Keep: the five-row institution table from §V-A (merged with Table I), Table II (AUC ladder, trimmed to the primary model plus one robustness row), Table IV (explanations — the headline), `fig2_ladder_gbm_f33`, `fig3_explanations_f33`.
Drop: Tables III, V, VI and VII (fold their key numbers into prose), `fig2_ladder_{lr,rf}`, `fig4_fewshot`, both heatmaps. Note that Table III carries the *threshold* result, which is load-bearing — but three numbers per family in a sentence carry it, and the ladder figure already shows the F1 panel.

### One reframing that costs nothing and buys the track

Retitle around the dissociation rather than the benchmark. The current title is accurate — I have no factual objection to it — but it is a survey title. Something shaped like "Predictions Transfer, Explanations Do Not: ..." names the novel result in four words and tells a Track 1 chair why the paper is theirs. The benchmark then becomes the method that makes the claim possible, which is what it actually is.

---

## Recommendation

**Major Revision.**

The underlying work is sound, unusually honest, and contains one result — that a transferred early-warning model's predictions and its explanations fail at different rates and are not repaired by the same intervention — that genuinely belongs at a Trustworthy AI track and that I have not seen made with this much evidence. That result is worth publishing. But the submission in front of me is not yet that paper. It is a learning-analytics portability benchmark with the novel finding installed as its third contribution, at 1.7x the hard page limit, with no figure cited anywhere in the text, with a Conclusion that overstates its own central fix by fifty per cent against its own Results section, with the headline explanation claim resting on one model family the abstract does not name and lacking the within-cohort baseline that would separate transfer failure from estimator noise, and with a release claim pointing at no reachable artefact under a double-blind policy. None of these is fatal and all are fixable inside the deadline: the compression is mostly deletion of the weakest section (§V-G, worth over a page on its own), and the reframing is an ordering change rather than new work. But the volume of correction required is beyond what "Minor Revision" describes, and the arithmetic contradiction between §V-C, §VII and Table III would on its own sink the paper with any reviewer who checks it. Fix the framing, fix the numbers, add the explanation baseline or explicitly bound the claim without it, cut to length, and this becomes an accept.
