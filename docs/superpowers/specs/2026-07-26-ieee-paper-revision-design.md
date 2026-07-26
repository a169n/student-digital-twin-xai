# IEEE SIST 2026 paper revision — design

**Date:** 2026-07-26
**Artifact under revision:** `IEEE_Talgatov.docx` (submitted version preserved as
`IEEE_Talgatov_v1_submitted.docx`)
**Decision from reviewers:** *Revisions required*

## 1. Reviewer feedback, decomposed

| # | Reviewer item | Rating | Actionable reading |
|---|---|---|---|
| 2 | Conference requirements | Improve | IEEE template compliance, formatting |
| 4 | Abstract completeness | Improve | Abstract omits the system entirely |
| 7 | Analysis of subject area | Improve | Related Work lists work, does not analyse it |
| 8 | Used materials level | Moderate | Reference base thin on SE / reproducibility |
| 10a | *"expand the description of the technical implementation: system architecture, technologies used, interaction of components and deployment features"* | — | **Primary ask.** New Implementation section |
| 10b | *"reduce the volume of the description of the pedagogical context"* | — | Trim teacher-facing prose in I, VII, VIII |
| 10c | *"repeated figure legends (e.g. 'Fig. 1. Fig. 1.'), table formatting, presentation style of structure elements"* | — | Formatting pass |

The dominant, repeated ask is 10a. Everything else is secondary.

## 2. Root cause of 10a

The submitted paper describes the prototype as *"a monorepo with two
independently runnable services"*. The repository actually contains four runtime
components and a data plane. The engineering contribution was real but
undocumented. Verified against the working tree:

| Claim in submitted paper | Reality in repository |
|---|---|
| two services | Next.js web, FastAPI API, Python ML service, Postgres — 4 Compose services |
| *"web reads the frozen artifacts at request time"* | Web calls 9 REST routers on FastAPI; direct artifact reads happen only on the `/research-demo` route |
| not mentioned | Versioned schema contracts `schema_v0.1 … v1.2.yaml` used as a data contract |
| not mentioned | 13 experiment configs → 16 frozen artifact directories |
| not mentioned | exporter → JSON payload → importer → 5-table ORM projection |
| not mentioned | 26 ML test modules (~4.9k LOC), ruff + ESLint + pre-commit, uv + pnpm lockfiles, 3 Dockerfiles |

## 3. Chosen approach

**Approach A + one element of B.** Add a dedicated Implementation and Deployment
section and pay for the space by cutting two low-information figures and
compressing prose. Keep the title and the honest-evaluation framing intact, but
promote the engineering contribution to first position in the abstract and in the
Introduction's novelty list.

Rejected alternatives:

- *Restructure as a pure systems paper.* Would answer 10a most directly, but
  discards the methodological framing the same reviewer scored positively
  ("New methodology"). Too much risk for the gain.
- *Minimal compliance patch.* Fixes formatting and adds half a page. Likely reads
  as non-responsive to a request that was made twice in one comment. Invites a
  second revision round.

## 4. Target structure (6 pages, IEEE two-column)

| § | Section | Change |
|---|---|---|
| — | Abstract | Add architecture + reproducibility sentences; engineering contribution first |
| I | Introduction | −25% pedagogical framing; novelty list reordered, engineering as (1) |
| II | Related Work | Same length, denser: each theme gains an explicit analytical gap statement. +2 references |
| III | System Architecture | Rewritten to the real 4-component topology; read-only boundary as a reproducibility invariant; schema contracts. New Fig. 1 |
| IV | **Implementation and Deployment** | **New**, ~1.2 pages |
| V | Data and Experimental Design | Unchanged in substance; old Fig. 4 dropped |
| VI | Results | A–D kept; "Reading" paragraph compressed ~40%; old Fig. 7 dropped |
| VII | Discussion | Pedagogical paragraph trimmed; engineering-lessons point added |
| VIII | Limitations | Compressed ~30%, all substance retained |
| IX | Conclusion | Engineering contribution added to the summary |

Figures 7 → 5. Tables 2 → 3. Fallback if over length: merge Fig. 2 and Fig. 3
into one two-panel figure.

## 5. Content of the new Section IV

Only claims verifiable against the working tree.

- **A. Technology stack (Table III).** Next.js 14.2 / React 18.3 / TypeScript 5.5 /
  Tailwind 4; FastAPI + Pydantic v2 + SQLAlchemy 2.0 / SQLite; Python 3.11+,
  pandas 2.2, NumPy 2.1, scikit-learn 1.5+, PyArrow; Docker Compose, uv, pnpm,
  ruff, ESLint.
- **B. ML pipeline.** Dataset adapters (OULAD, KU Leuven) → weekly snapshot
  builder → feature-set registry with machine-checked forbidden-column
  enforcement (15 fields) → experiment runner → 13 configs → 16 frozen artifact
  directories.
- **C. Backend.** Domain-oriented router/service/repository triads across 8
  domains, 9 REST routers, 5-table ORM schema, pydantic-settings configuration,
  idempotent lifespan bootstrap.
- **D. Frontend.** App Router SSR, 11 routes, typed loaders, graceful degradation
  when the API is unavailable.
- **E. Component integration.** exporter → camelCase JSON payload → importer →
  SQLite projection (150 students / 5,250 snapshots / 4 explanation cases) →
  REST → SSR.
- **F. Deployment and reproducibility.** Three images plus Compose; pinned uv and
  pnpm lockfiles; pre-commit (ruff, ruff-format, ESLint); 26 ML test modules
  (~4.9k LOC); deterministic seeds; frozen artifacts. Stated honestly:
  single-host research deployment, no authentication, no production hardening —
  explicitly out of scope.

## 6. Reference additions

- Sculley et al., *Hidden Technical Debt in Machine Learning Systems*,
  NeurIPS 2015 — grounds the read-only boundary and data contracts as a response
  to ML system entanglement.
- Kapoor & Narayanan, *Leakage and the Reproducibility Crisis in ML-based
  Science*, Patterns 2023 — supports the leakage-aware pipeline claim.

## 7. Formatting fixes

1. Duplicated legends `Fig. 1. Fig. 1.` and `Fig. 2. Fig. 2.`
2. Table captions in IEEE form: caption above, roman numeral, small caps
3. Run-in italic *Abstract*— and *Keywords*—
4. Section heading style consistency
5. En-dash for ranges, true minus for negative deltas
6. Reference [6] missing volume and article number
7. Column-break cleanliness around full-width floats

## 8. Editing method

Paragraph-level edits inside `word/document.xml` through python-docx, preserving
the existing IEEE template run styles. New paragraphs are created by deep-copying
neighbouring paragraphs of the same style so template formatting is inherited
rather than reconstructed. The submitted file is preserved unmodified as
`IEEE_Talgatov_v1_submitted.docx`.

## 9. Out of scope

- Re-running any experiment or changing any reported number
- Changing the title or the paper's scientific framing
- User study of the interface (remains stated future work)
