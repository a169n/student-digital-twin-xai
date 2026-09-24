# Teacher explanation-review screen — design

Date: 2026-09-24. Practice plan: week 6 ("teacher interface prototype"), built so
that week 7 (the feedback loop) extends it without rework.

## Intent

A screen that can be demonstrated in about two minutes at the defense and in the
practice report. It shows not only a student's risk and the factors behind it,
but the research result of weeks 1–3: whether this student's factor list can be
trusted. One screen over precomputed historical cases; no authentication, roles
or group analytics. English UI, like the rest of `apps/web`.

Success: open `/review`, click between cases from four institutions, see a
stable and an unstable explanation side by side in the list, read the
reliability scale without a legend lecture, record a teacher decision and see
it in the case history.

## Architecture

```text
services/ml  export_teacher_review_payload.py
      │  frozen JSON: data/artifacts/research_demo/teacher_review_payload.json
      ▼
apps/api     importer → SQLite (review_cases, review_decisions)
             domain/review: models · repository · service · router
      │  GET /api/review/cases · GET /api/review/cases/{id} · POST …/decisions
      ▼
apps/web     /review  (case list + case card), nav link "Explanation review"
```

## 1. Data export (ML)

New module `services/ml/src/export/export_teacher_review_payload.py`
(`uv run python -m src.export.export_teacher_review_payload`).

**Model and explanations.** exp_027's configuration: gradient boosting, 1/3
cutoff, background 50, 5 repeats, seed 0. The exporter mirrors the split and
background lines of `run_local_stability.cohort_students` (vary="background")
rather than refactoring that frozen-experiment code path, and is pinned to it by
the exp_027 check below. Per exported student:

- `risk` = P(not passing) = 1 − `predict_proba[:, 1]` (the exp_025/027 `p_risk`
  column is P(pass); the export fixes the orientation). `risk_rank_pct` = the
  student's midrank position in the cohort's evaluation students (ties share a
  midrank — many zero-activity students have identical risk); `flagged` =
  `risk_rank_pct >= 1 - transfer_benchmark.FLAG_RATE`, so the flag and the
  "higher than for X % of students" line always agree.
- `factors`: TreeSHAP (interventional, log-odds) with the repeat-0 background.
  Top 3 by |attribution|; `direction` = "raises_risk" when the attribution to
  P(pass) is negative, else "lowers_risk"; `share` = |attribution| / Σ|attribution|
  over the 7 features; `value` = the student's feature value; `course_median` =
  median of that feature over the cohort's evaluation students.
- `reliability`: `self_tau` = mean pairwise Kendall τ of the 5 SHAP rankings
  (exp_025's `self_tau_shap`); `threshold` = 0.80 (`run_local_stability.GATE_TAU`);
  `verdict` = "stable" if `self_tau >= threshold` else "unstable";
  `recomputations` = the top factor of each of the 5 repeats (so the card can
  show "top factor: active days ×3, clicks ×2").
- `scale_context` (payload level): coverage at the threshold and pooled
  retained SHAP–occlusion agreement with and without the gate, read from
  `exp_026_gate_calibration/exp027_f33_background__cross_tau/summary.csv` —
  the exp_026 run on the same students as the cases (about 0.56, 0.41 vs
  0.35); never hard-coded.
- `context`: institution, course code, `week` (cutoff week) of `n_weeks`,
  cohort pass rate, cohort size, mean within-cohort model AUC on the held-out
  third.

**Validation (hard).** Each exported student's `self_tau` must equal the value
in `exp_027_local_estimator_matrix/f33_background/students.csv` for the same
`(cohort_id, student_row)`; the export aborts otherwise.

**Case selection (deterministic, recorded in the payload).** For each of the
four large institutions (OULAD, KU Leuven, UKZN, Oviedo; Zambia excluded, 40
students): among flagged students, the four closest to the 90th, 65th, 35th
and 10th percentiles of `self_tau` within that institution's flagged students;
plus one student from the lower half of the course's risk ranking closest to the
75th percentile of `self_tau` there. `self_tau` ties are broken by a seeded
shuffle (seed 0) so the picks spread over courses. Students without a defined
`self_tau` are never picked. 20 cases, no student twice.

**Pseudonymity.** `case_id` and `display_name` are institution prefix + index
(`OU-1`, `KU-3`, `UK-2`, `OV-4`); raw student ids never enter the payload.
The Zambia name column is never read (institution excluded anyway).

**Feature labels** (plain language, in the payload):

| feature | label |
| --- | --- |
| cum_clicks | Total clicks so far |
| cum_active_days | Active days so far |
| cum_content_clicks | Course-material clicks so far |
| cum_social | Forum activity so far |
| cur_clicks | Clicks this week |
| active_weeks | Active weeks so far |
| weeks_since_active | Weeks since last activity |

**Payload shape** (JSON keys are camelCase, like the existing research
payloads; top level): `schema_version`, `generated_from`
(experiment ids, config), `selection_rule`, `scale_context`, `feature_labels`,
`cases[]` with `case_id`, `display_name`, `context`, `risk`, `risk_rank_pct`,
`flagged`, `factors[3]`, `reliability`, `features` (all 7 values with course
medians). Week 7 will add `variants` per case; not produced now.

## 2. API (`apps/api/src/domain/review/`)

- **Storage.** `ReviewCaseRecord` (`review_cases`: `case_id` PK, `institution`,
  `payload_json`) and `ReviewDecisionRecord` (`review_decisions`: `id`,
  `case_id` FK, `action`, `factor` nullable, `note`, `created_at`) in
  `src/db/models.py`. A new importer function loads the payload into
  `review_cases` (replacing existing cases; decisions are kept); it is called
  from `src/import_research_payload.py` when the review payload exists.
  Decisions are append-only.
- **Endpoints** (router mounted at `/review`):
  - `GET /api/review/cases` → list: `case_id`, `display_name`, `institution`,
    `course`, `risk`, `flagged`, `verdict`, `self_tau`, `latest_decision`.
  - `GET /api/review/cases/{case_id}` → the full case plus `decisions[]`
    (newest first) and the payload-level `scale_context`/`feature_labels`.
  - `POST /api/review/cases/{case_id}/decisions` body `{action, factor?, note?}`
    → the stored decision.
- **Validation.** `action` ∈ {`contact_student`, `keep_monitoring`,
  `no_action_needed`, `factor_looks_wrong`} — marked `TODO(domain)`: a
  placeholder set, not a validated taxonomy. `factor` required iff action is
  `factor_looks_wrong` and must be one of the case's three shown factors; `note`
  ≤ 1000 characters. Unknown case → 404; invalid body → 422.
- **Tests** (`apps/api/tests/test_review_routes.py`, TestClient, temporary
  SQLite): list, case, valid decision, 404, 422 for bad action, missing factor,
  factor not among the case's three.

## 3. Web (`apps/web/app/review/`)

Two-pane layout: case list on the left (filters: institution, verdict; each
row shows pseudonym, institution, risk, verdict chip, a mark if a decision
exists), case card on the right. Nav link "Explanation review" in
`components/layout/nav-links.tsx`. Existing shadcn components and styling.

Case card, top to bottom:

1. **Header**: display name · institution · course · week k of n; "72 % risk of
   not passing · top 20 % of this course"; cohort pass rate and model AUC.
2. **Explanation reliability**: horizontal 0–1 scale with a tick at the
   threshold, a marker at the student's `self_tau`, verdict chip ("Stable
   explanation" / "Unstable explanation") and one sentence of meaning.
   Disclosure "About this scale": what self-agreement is (5 recomputations), and
   the `scale_context` numbers.
3. **Why flagged**: three rows — label, direction (↑ raises risk / ↓ lowers
   risk), value vs course median, a bar of `share`. When unstable: rows muted,
   a warning ("This list changes when it is recomputed — do not act on single
   factors"), and a disclosure "What 5 recomputations showed" listing the top
   factor counts.
4. **Teacher decision**: four actions (radio), factor select shown for "factor
   looks wrong", note, Save (POST); decision history below. Errors from the API
   shown inline.
5. **Disclaimer**: reuse `components/student/xai-disclaimer.tsx`.

If the API is unreachable the page shows an explicit error card — never
fallback or invented data. Bars show only the exported `share` values.
Decisions are posted by a Next.js server action, so the browser never calls the
API directly and the API needs no CORS opening. As built: the factor section is
titled "What drives this prediction" (calm cases are not flagged), the verdict is
a teal/amber chip rather than a red badge, and the scale shows two labelled
zones ("List changes" / "List repeats") split at the threshold. Screenshots:
`docs/superpowers/specs/assets/teacher-review-*.png`.

**Tests.** `pnpm typecheck` and `pnpm lint`; a `node --test` test for the
data-shaping helpers (verdict chip text, direction label, formatting),
following `tests/research-demo.test.js`.

## 4. Verification and demo

- ML: `tests/test_teacher_review_export.py` on a synthetic cohort — risk
  orientation, direction sign flip, top-3 ordering by |attribution|, `share`
  sums over 7 features to 1, deterministic selection, no raw id in the output;
  plus the hard exp_027 `self_tau` check during the real export.
- API: the route tests above.
- End to end: rebuild SQLite, run API and web, open `/review`, walk a stable and
  an unstable case, save a decision, reload and see it in history; screenshots
  for the practice report.

## Out of scope

Authentication and roles; group analytics; week 7 masking and later-week
re-display; translations; changing frozen experiment artifacts (exp_025/027
`p_risk` stays as is — the export computes risk itself).
