# S3 — Senior PC Member, Final Read Before the Accept/Reject Meeting

**Venue:** SIDe 2026, Astana. IEEE technical co-sponsorship (IEEE Kazakhstan Section), IEEE Xplore route. Track 1, Computational Intelligence. 4–6 pages including references, double-blind.
**Manuscript:** `docs/dissertation/side2026_paper.md` (round-2 draft, 4,009 words in file; **2,538 words of body prose** once abstract, title and references are removed).
**Date:** 2026-09-06. Four days to the deadline.

---

## Verdict and Confidence

**ACCEPT.** Confidence **0.85** that it is accepted if it is submitted in compliant IEEE format with the fixes in the "must-fix" list below. Confidence **0.55** if it is submitted as-is, because the dominant failure mode at this venue is not scientific — it is a chair's desk-check on length and format, plus three internal numerical contradictions that a careful second reviewer will find and that will read as carelessness rather than as small errors.

This is not a marginal paper for SIDe. It is a top-quartile submission that is currently at risk from mechanical problems, not from its science. Every hour between now and the deadline should go to compression, format, and the three error fixes — not to new analysis, new figures, or new framing beyond what is prescribed below.

**Must-fix before submission (all are 5-minute edits, all are things a reviewer will catch):**

1. **Section V-B contradicts Table II.** The text says "Random forest is the most robust family under raw features and gradient boosting the least." Table II raw-row D0−D3 losses are GBM 0.132, **LR 0.176**, RF 0.095. Logistic regression is the least robust under raw. As written the sentence inverts the very finding it uses to qualify [10]. Same sentence: "the gap is 0.09 to 0.13 depending on the estimator" excludes LR raw at 0.176 — say "0.09 to 0.18 across model families" or scope it to gradient boosting.
2. **The abstract misattributes a baseline.** "…agree at Kendall tau 0.338, against 0.026 across institutions and 0.303 expected from random rankings." 0.303 is the random **top-3 Jaccard**; random Kendall tau is 0.000 (your own Section V-E table). This is the single most quotable sentence in the paper and it is currently wrong. Fix to: "…0.026 across institutions, against a random-ranking expectation of 0.000."
3. **Student counts do not add up.** The manuscript says cohort rows sum to 45,158; Table I's institution column sums to 45,170 (3,951 + 30,059 + 3,789 + 7,254 + 117). Pick one and make the two files agree.
4. **Reference [21] (Friedman) is cited nowhere.** Delete it. That is one reference of space recovered and one integrity flag removed — round 1 already raised this.
5. **Only one figure or table is cited anywhere in the text** (line 110, "Table II, Fig. 2a"). Round 1 flagged exactly this and it is unfixed. Every surviving float must be referenced by number in prose, and figure numbering must start at Fig. 1.
6. **Double-blind hygiene.** "We release the benchmark, five institution adapters, and the frozen results" needs an anonymised artifact link (anonymous.4open.science or a figshare anonymous link) or it is an unverifiable claim; a de-anonymising GitHub URL in the camera-ready-in-waiting would be worse.
7. Minor: V-D reports percentile F1 0.348 where the round-1 recomputation recorded 0.350. Confirm which run is current and make the number match the released artifact.

---

## Where This Sits Among Competing Submissions

The realistic pool at a regional IEEE-co-sponsored conference in Central Asia, Track 1, is roughly:

| Band | Share of pool | What it looks like |
|---|---|---|
| A. Applied-ML case reports | ~55 % | "Random forest / CNN / LSTM for <task> on <one public or one local dataset>", 70–95 % accuracy reported, single split, no baseline beyond a second classifier, related work is a list. |
| B. Surveys and reviews | ~15 % | Narrative review of XAI or of student-performance prediction, no new data. |
| C. Systems and prototypes | ~15 % | A dashboard, an IoT pipeline, a chatbot, an LLM wrapper; engineering described, evaluation thin or absent. |
| D. Methodologically serious empirical work | ~10 % | Multi-dataset or multi-site evaluation, proper baselines, released artifacts, honest limitations. |
| E. Strong work slumming it | ~5 % | A group's second-tier paper, or a workshop-grade slice of a journal submission. |

Acceptance at venues of this shape typically lands between 40 % and 60 %, which means most of band A gets in. **This paper is band D, near the top of it.** Five institutions, four countries, 3,969 evaluated ordered pairs, released adapters, a contamination audit of the authors' own pipeline, a fairness disaggregation, and a vocabulary borrowed correctly from clinical prediction modelling — nothing else in the pool will have that. Against band A it is not close.

Which is exactly why the risk profile is inverted from a top-tier venue. Nobody here will reject it for insufficient novelty of method if it is framed properly. It gets rejected, if at all, because it arrived at 7.5 pages, or because a reviewer skimmed "two of them are negative" in the abstract and stopped.

---

## The Compression Plan

### The arithmetic first, because the premise is wrong in the authors' favour

The brief assumes ~4,100 words against a limit fitting ~2,800. That over-counts. Of the 4,009 words in the file, 369 are the abstract, 648 are the reference list (which is set in 8 pt and is measured in lines, not words), and 444 are table cells. **Body prose is 2,538 words.**

IEEE two-column letter, 10 pt: ~19 column-inches of text per page, ~57 words per column-inch, so 6 pages ≈ 114 column-inches. Fixed overheads: anonymous title block ~2, abstract + keywords ~6, 20 references at ~3 lines each ~8, section headings ~5 → 21 column-inches. That leaves 93 column-inches for body text and floats. At 2,538 words the body needs ~45. **The remaining 48 column-inches are what the floats have to fit into, and the current 6 inline tables plus 4 figure families need roughly 36 for the floats alone plus captions and IEEE float slack — which is how a paper with only 2,538 words of prose lands at 6.3–6.8 pages.**

Conclusion: **this is a float problem, not a prose problem.** Cut floats hard, trim prose lightly, and the paper fits with a quarter-page to spare. Do not gut the argument to save words you do not need to save.

### Section-by-section budget

Body prose target: **~1,990 words** (from 2,538). Abstract target: **200** (from 369). Floats: **2 figures, 3 tables**.

| Section | Current (prose / table) | Target prose | What goes |
|---|---|---|---|
| Abstract | 369 / — | **200** | Cut the four-findings enumeration to three sentences. Delete "and two of them are negative". Delete the two-hazards sentence (keep it in V-G only). Delete the mechanism detail. Fix the tau/Jaccard error (must-fix #2). |
| Keywords | — | unchanged | Reorder: explainable AI; trustworthy AI; fairness; model calibration; external validation; learning analytics; early warning. |
| I. Introduction | 341 / — | **280** | Compress the five contribution bullets to four (fold hazard bullet 4 into bullet 2). Rewrite bullet 3 per the negative-results section below. Keep the "three things can break" paragraph verbatim — it is the paper's best paragraph. |
| II. Related Work | 376 / — | **300** | Merge the "Prediction on public LMS data" and "Data scarcity" paragraphs into one of ~90 words. Keep "Portability", "External validation, borrowed" and "Explanation stability" intact; they carry the positioning. |
| III-A Five institutions | 140 / 125 | **110** prose, **1 merged table** | **Merge the institution table with the Section V-A results table** into one Table I: Institution \| Platform \| Country \| Cohorts \| Students \| D0 AUC (range). Drop the Outcome column into one prose sentence. Saves a whole float. |
| III-B Enrolment/calendars | 106 / — | **70** | Keep the Zambia backward-leak correction (2 sentences); compress the calendar inference to one. |
| III-C Schema and cutoff | 77 / — | **70** | Add one clause: the OULAD feature-richness control (17 features → D0 0.902, D0−D2 loss 0.021 vs 0.022 at 7 features). One sentence replaces Table VII entirely and pre-empts objection #3. |
| IV-A Ladder | 94 / — | **80** | Keep the paired-40 caveat; it is a round-1 concession and reviewers who read round-1-shaped critiques will look for it. |
| IV-B Representations | 19 / — | **15** | — |
| IV-C Metrics | 93 / — | **85** | Absorb IV-D here as one clause. |
| IV-D Compute settings | 28 / — | **0** | **Delete as a subsection.** One clause in IV-C: "permutation importance, 3 repeats, targets subsampled to 1,500 rows, affects no AUC, calibration or decision metric." |
| V-A Signal is institutional | 33 / 57 | **40**, table merged into III-A | Table absorbed above. |
| V-B Discrimination | 82 / — | **90** | Merge with V-C into one subsection "Discrimination degrades, calibration collapses". Fix must-fix #1 here. Cite Fig. 1. |
| V-C Calibration | 128 / 44 | **130**, **table cut** | The three numbers (0.691/0.597/0.617 AUC; −0.008/+0.119/−0.009 CITL; 0.197/0.361/0.322 Brier) go into two prose sentences. The shift-regression paragraph survives — it is the round-1 mechanism correction and dropping it looks evasive. |
| V-D Decision at flag budget | 155 / — | **110** | Keep: recall 0.272 → 0.274, lift 1.63 → 1.36, "all four rules lose to alerting everyone (0.546)". Cut the per-rule F1 enumeration to one clause. |
| V-E Explanations | 120 / 60 | **140**, **table kept** | Promote to first results subsection after V-A (see Track-Fit Fix). Expand slightly — this is the paper's only uncontested novel claim. |
| V-F Fairness | 82 / 67 | **80**, **table kept, trimmed to 3 columns** | Drop the "Gap, local / Gap, transferred" pair to one delta column, or drop the Gender row (0.035 → 0.038 is the least interesting). |
| V-G Two hazards | 134 / — | **110** | Keep both. This is the most cited-in-future part of the paper and costs no float. |
| V-H Sensitivity | 97 / 91 | **60**, **table cut** | **Delete the 9-column table.** It must span both columns and costs ~6 column-inches for a section whose entire message is "nothing moves". Replace with two sentences giving the ranges: D0 0.669–0.723, cross-institution gap 0.082–0.099, calibration bias +0.120 to +0.125 removed to within 0.01 at every cutoff, tau 0.026–0.038. |
| VI. Discussion + Limitations | 260 / — | **200** | Keep the clinical-updating-ladder paragraph in full. Compress limitations from eight sentences to five; keep label-collinearity, inferred calendars, Zambia, and the clustered-bootstrap caveat. |
| VII. Conclusion | 173 / — | **120** | Cut to: headline numbers, the release, one forward sentence. Delete the "two of our three original claims" paragraph — it repeats VI and is the sentence a skimmer quotes against you. |
| References | 21 refs | **19–20 refs** | Delete [21] (uncited). Optionally merge [4]/[6] — both are the same "applied ML + XAI on student data" point — recovering ~3 lines. |

**Totals:** 200 abstract + 1,990 body ≈ 2,190 words, 2 figures, 3 tables, 20 references. That lands at roughly 5.6 pages with float slack, which is where you want to be four days out.

### Floats: what survives, what is deleted

**Survives (2 figures):**
- **Fig. 1 = `fig2_ladder_gbm_f33`** (two panels: ROC-AUC and recall at a 20 % flag budget, by transfer distance).
- **Fig. 2 = `fig3_explanations_f33`** — only if the page count permits after typesetting. It is the first float to sacrifice; see below.

**Survives (3 tables):**
- **Table I** = merged benchmark composition + within-cohort AUC (III-A ∪ V-A).
- **Table II** = the explanation floor / ceiling / transferred / random baselines table (current V-E).
- **Table III** = fairness disaggregation, trimmed (current V-F).

**Deleted entirely:** `fig2_ladder_lr_f33`, `fig2_ladder_rf_f33` (the LR/RF story is one prose sentence), `fig4_fewshot_f33` (**orphaned — the few-shot section is no longer in the manuscript**), `figS_heatmap_raw_f33`, `figS_heatmap_percentile_f33`; and from `side2026_tables.md`, Tables II, III, IV, V, VI and VII in full (II is replaced by Fig. 1, III is F1-at-0.5 which the paper itself argues against reporting, IV is subsumed by the V-E table, V and VI are **orphaned** — pooled sources and few-shot are no longer in the manuscript, VII becomes one sentence in III-C). Also deleted: the current V-C calibration table and the V-H sensitivity table.

### The single figure and the single table that earn their space

**Figure: `fig2_ladder_gbm_f33`.** It is the only object in the paper that cannot be a table without costing more space than it saves. Table II of the tables file — 9 rows × 7 columns — would have to span both columns and would still not show the shape of the decay. The figure's two panels do the work of two tables: the upper panel is the discrimination ladder (the paper's spine), the lower panel is recall at the flag budget (the deployment consequence), and the reader sees in one glance that the first degrades gently and the second barely moves. That co-plotting *is* the argument.

**Table: the explanation baselines table** (noise floor 0.707 / disjoint-halves ceiling 0.338 / transferred 0.026 / random 0.000, with J@3 beside it). Four rows, two columns, ~2 column-inches — the cheapest float in the paper and the one carrying the only contribution round 1 certified as unprecedented ("no prior work compares a transferred model's explanation against a locally trained model's"). It is also the paper's Track-1 anchor. Note the corollary: because these four numbers read perfectly as a table, **`fig3_explanations_f33` is largely redundant with it** and is therefore the correct thing to drop if typesetting comes in over six pages. Do not drop the table to keep the figure.

---

## Negative-Results Risk, and the Framing That Defuses It

At SIDe, "we found nothing" is a real rejection reason. Band-A reviewers evaluate against an implicit template — proposed method, table of accuracies, method wins — and a paper that says twice, in its own abstract, that its method failed does not fit that template. The current draft volunteers the vulnerability: the abstract contains "and two of them are negative", the Introduction advertises "Two honest negative results", and **two of eight results subsections are literally titled "Negative result:"**. A skimmer reads three "our method failed" signals before reaching any evidence.

None of this is a call for dishonesty. Every claim stays; every number stays; the Discussion keeps "two of our own hypotheses did not survive contact with the right baselines." What changes is that the *negativity* is not the headline — the *measurement* is. Reframe each negative as a quantity the field did not previously have:

| Current framing | Replacement framing (same facts) |
|---|---|
| "The transform does not improve the decision" (V-D title) | **"Recalibration is necessary but not sufficient"** — a label-free transform removes calibration bias entirely and moves recall at the flag budget by 0.002; we quantify the ceiling on what recalibration alone can buy. |
| "The explanations were never stable" (V-E title) | **"Explanation agreement has a low ceiling before transfer"** — we establish the first noise floor (0.707) and attainable ceiling (0.338) for permutation-importance agreement on engagement features, and show published stability numbers must be read against them. |
| Abstract: "Four results follow, and two of them are negative." | Delete the clause. State the four results. |
| Intro bullet 3: "Two honest negative results." | **"Two baselines that overturn intuitive claims"** — including one of our own. |
| Conclusion: "Two of our three original claims did not survive their own baselines." | Delete from the Conclusion; it already appears once in Section VI, which is where a self-critical sentence belongs. |

Rule of thumb for the rewrite: a negative result framed as "X does not work" reads as failure; framed as "we measure the ceiling on X, and it is here" reads as rigour. Say what you *established*, not what you *failed to establish*. The failure of your own transform is then a credibility signal buried in Section VI where a hostile skimmer will not weaponise it, and a careful reviewer will find it and be impressed.

---

## Title Recommendation

**Current:** "Discrimination Transfers, Calibration Does Not, and Explanations Were Never Stable: An Early-Warning Transfer Benchmark Across Five Institutions" — 18 words, three independent clauses, plus a subtitle.

Judgment for **this** venue: **too long, too clever, and one clause too negative.** "Explanations Were Never Stable" reads, to a reviewer scanning at speed, as the authors conceding their XAI contribution collapsed. "Discrimination Transfers" is worse: outside clinical prediction modelling, "discrimination" primarily means *unfair treatment*, and on a track that lists "fairness and bias mitigation", half your readers will parse the first two words of your title as "unfairness transfers between institutions" — which is *also* something your paper says, but not what that clause means. That ambiguity is a gift to a confused reviewer. Add that the three-clause form buries every indexable keyword past the colon, and IEEE Xplore search will not find this paper.

**Alternative A (recommended):**
> **Cross-Institution Transfer of Early-Warning Models: Discrimination, Calibration and Explanation Stability Across Five Universities**

**Alternative B:**
> **Explanations Do Not Transfer: A Five-Institution Benchmark for Trustworthy Early-Warning Models**

**Submit A.** It is 15 words, front-loads the topic, and carries "calibration", "explanation", "cross-institution" and "five universities" as indexable keywords that map directly onto Track 1's call. Nothing in it can be misread as a confession. B is the better title for a top-tier venue and the better title for the Q1 extension in 2027 — it is memorable and it states a finding — but at SIDe it leads with a negation and forfeits the descriptive-keyword advantage that a skim-reading regional PC rewards. Keep B's punch where it costs nothing: make "Explanations do not transfer" the first six words of the abstract's finding sentence.

---

## Track-Fit Fix

**Current composition of the 2,538-word body**, scored by whether a Track 1 reviewer would tag it Explainable/Trustworthy AI or generic learning analytics:

| Material | Words | Reads as |
|---|---|---|
| V-E explanations | 120 | XAI — core |
| V-F fairness | 82 | Trustworthy AI / fairness — core |
| V-C calibration + V-D decision | 283 | Trustworthy AI, *if framed that way*; currently framed as prediction quality |
| V-G hazards | 134 | Trustworthy AI / evaluation integrity, *if framed that way* |
| Everything else (data, method, ladder, discrimination, sensitivity, related work, intro) | ~1,900 | Learning analytics / applied ML |

So: **roughly 8 % is unambiguously XAI, ~16 % is XAI-or-fairness, and up to ~33 % can be read as Trustworthy AI with framing alone.** Right now the sole novel XAI contribution arrives **fifth of eight** results subsections, on what will be page 4 of 6 — the exact complaint round 1's journal-fit seat raised, and it is unfixed.

**The fix costs no new work and no new words. Reorder the results:**

1. **V-A** The signal is a property of the institution (unchanged, it is the setup).
2. **V-B** *(was V-E)* **Explanation agreement has a low ceiling before transfer** — the floor/ceiling/transferred/random table lands on page 2–3, where a Track 1 reviewer decides whether this is their paper.
3. **V-C** *(was V-B + V-C merged)* Discrimination degrades, calibration collapses, and a label-free transform restores calibration.
4. **V-D** *(was V-F)* Transfer costs the worst-served group most.
5. **V-E** *(was V-D)* Recalibration is necessary but not sufficient: the decision at a 20 % flag budget.
6. **V-F** *(was V-G)* Two hazards we created and then found.
7. **V-G** *(was V-H)* Sensitivity.

Then three sentence-level moves:

- **Introduction, paragraph 2, last sentence** — add: "All three failures are trustworthiness failures at the point of use: a miscalibrated score misleads the person setting a threshold, and an unstable importance ranking misleads the person reading the explanation."
- **Section VI, opening** — add one clause tying calibration to trustworthiness: an uncalibrated risk score presented to an advisor is not merely inaccurate, it is an unwarranted claim about a named student.
- **Keywords** — lead with explainable AI, trustworthy AI, fairness; put learning analytics last. This is what a track chair actually skims when assigning reviewers.

After the reorder, a Track 1 reviewer meets XAI content on page 2 and fairness on page 3. That is the difference between "wrong track, generic LA paper" and "on-track".

---

## Three Predicted Objections and Pre-emptions

**Objection 1 — "No novel method. This is only an evaluation; where is the contribution?"**
The most likely rejection sentence at this venue, and the current draft invites it by saying "We do not propose a new algorithm" in the Introduction with nothing defensive attached.
*Pre-emption (place as the final sentence of the abstract):* "The contribution is a released artifact and a measurement protocol — five institution adapters, 3,969 evaluated transfer pairs, and frozen results — in the tradition of external-validation studies that made clinical risk scores deployable [11], [12]."
Keep "we do not propose a new algorithm" in the Introduction, but follow it immediately with "we propose the experiment that a proposed algorithm must now pass."

**Objection 2 — "ROC-AUC of 0.60 is weak. These models are not good enough to draw conclusions from."**
A band-A reviewer accustomed to 0.95 accuracy on a single split will read 0.597 as incompetence rather than as the finding.
*Pre-emption (place in the abstract's second sentence and repeat verbatim in the Fig. 1 caption):* "Within-cohort performance matches published single-dataset results — 0.845 at the Open University — and the object of study is what happens to an ordinary, competently trained model when it is moved, not how high it can be pushed."
Putting it in the figure caption matters: a skimmer reads captions, and Fig. 1 is where the low numbers are most visible.

**Objection 3 — "Only seven features, no deep learning, no SHAP."**
*Pre-emption (one sentence at the end of Section III-C, plus a clause in IV-C):* "A feature-richness control on OULAD shows that 17 features including assessment data raise within-cohort AUC to 0.902 but leave the transfer loss unchanged (0.021 vs 0.022), so the schema is a floor on performance and not a confound for the transfer result; permutation importance rather than SHAP is used because the identifiability question we ask is the one [18] poses about permutation-based importance specifically."
This single sentence retires Table VII, the "your features are too thin" objection and the "why not SHAP" objection at once, and it belongs on page 2 where the reader forms the objection.

*(Bonus, cheap to cover: "Zambia has 117 students, that is not an institution." One clause in III-A — "Zambia contributes two cohorts and is reported as indicative throughout; no headline number depends on it" — already partly present in Limitations, but a skimmer never reaches Limitations.)*

---

## Route Recommendation

**Submit to SIDe 2026 now. Do not take the Springer STEAM-H chapter for this content.**

1. **The content fits.** Per the arithmetic above, this is a float problem, not a length problem. There is no scientific reason to buy extra pages, and buying them with a slower venue is paying for space you do not need.
2. **The Q1 extension is the real destination, and the conference paper is its prerequisite.** The extended-paper special issue with a 2027 deadline is where the pooled-source analysis, the few-shot ladder, the feature-richness control, the per-institution heatmaps, the full sensitivity grid and the shift regression belong — that is 5 of the 7 tables and 3 of the 4 figures you are cutting this week. **You are not deleting that material, you are staging it.** The 30–50 % new-material requirement most journals impose on conference extensions is already satisfied by what will not fit into six pages, which is a rare and lucky position.
3. **The Springer chapter is the worst of the three routes for this specific content.** It is slower, it is not indexed where learning-analytics and ML readers search, and — decisively — it consumes the same material the Q1 extension needs, creating a text-overlap problem between a book chapter and a journal article that is much harder to argue than the standard, well-understood conference→journal extension.
4. **Priority on the benchmark.** The paper's durable asset is the released five-institution benchmark. A dated IEEE Xplore record in October 2026 is what makes every later citation point at you rather than at whoever builds the second one.

Sequence: **SIDe 2026 (Sep 10) → camera-ready Oct 5 → Q1 extension during 2027.** Keep the Springer chapter as the fallback only if SIDe rejects, in which case the chapter's extra room is genuinely useful and the Q1 route is off the table anyway.

---

## Final Advice, in Five Sentences

Fix the three internal contradictions today — the inverted robustness claim in V-B, the tau/Jaccard error in the abstract, and the student count — because they are the only things in this paper that make a competent reviewer doubt the rest of it. Then cut floats, not argument: one merged Table I, the explanation baselines table, a trimmed fairness table, and `fig2_ladder_gbm_f33`, with everything else moved to the 2027 extension where it was always going to live. Retitle to "Cross-Institution Transfer of Early-Warning Models: Discrimination, Calibration and Explanation Stability Across Five Universities", delete every occurrence of the word "negative" from the abstract, introduction and subsection headings, and let the honesty stay in Section VI where it earns credit instead of inviting a skim-rejection. Move the explanation result from fifth to second so a Track 1 reviewer meets the XAI contribution on page 2 rather than page 4. This paper is better than most of what it is competing against at SIDe; the only way it loses is on length, format or a careless-looking number, so spend all four days there and none on new science.
