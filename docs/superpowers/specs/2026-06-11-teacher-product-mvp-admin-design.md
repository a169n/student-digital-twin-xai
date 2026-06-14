# Teacher Product MVP + Admin Console — Design

> **Status:** approved (2026-06-11). Approach A (two zones, shared shell, light real-product touches).
> **Commit policy:** user commits manually.

## Goal
Turn the existing OULAD-seeded Next.js dashboard from a "research prototype" into a polished, real-looking **teacher product MVP** (no auth), and add a **model & system admin console** that holds the deeper detail + the honest research framing. The frontend is already visually mature (coherent custom-CSS design system in `apps/web/app/globals.css`); this is mostly re-packaging + one new admin zone, reusing existing loaders/components and the OULAD-seeded API. No backend/ML changes.

## Decisions (from brainstorm)
- **Honesty placement:** teacher view = clean product (no `ResearchBanner`/`PlatformStatusStrip`, no research jargon). ALL honest detail (model metrics, circularity, F1≈0.86 not 1.000, "not causal", limitations) lives in `/admin` + a thin global footer "About the model" link. The defense narrative stays one click away.
- **Admin = model & system console:** eval metrics, OULAD benchmark, XAI global importance + dominance audit, data provenance/quality, full cohort analytics, prediction/explanation browser, limitations, about.
- **Product name:** keep "Student Digital Twin" (drop the "· Research Platform" subtitle, add tagline "Early-warning student analytics"). Easy to rename later.
- **Admin structure:** multi-tab sub-nav (Overview / Model & evaluation / Explainability / Data & provenance / About).

## Architecture
Reuse: the entire FastAPI + OULAD-seeded SQLite + all loaders in `apps/web/lib/platform/loaders.ts` (no new endpoints) + the existing component library + the CSS design system. Two route areas share the root layout but the admin area gets its own sub-nav/console chrome.

## Part 1 — Teacher product (de-prototype existing pages)
- **Nav / brand** (`apps/web/components/layout/nav.tsx`, `apps/web/app/layout.tsx`): brand → "Student Digital Twin" + tagline; links `Dashboard / Students / Predictions / Admin` (remove "Research"); add a static identity chip ("Ms. Carter · DDD 2013J", no auth). Add a global **Footer** component with the "About the model" link → `/admin/about` and a one-line model disclaimer.
- **Home** (`apps/web/app/page.tsx`): replace the research-intro hero with a task-driven product landing — greeting, key cohort numbers, primary CTAs (Open cohort dashboard / Find a student / This week's predictions), and a "students needing attention" preview list. Remove "frozen artifacts / read-only platform" copy.
- **Remove `ResearchBanner` and `PlatformStatusStrip`** from all teacher pages (`/`, `/dashboard`, `/students`, `/students/[id]`, `/predictions`). They move to admin.
- **Soften caveat copy** on `/students/[id]` (the "Reading guardrail" + explanation-panel interpretation/footer): replace research jargon with product-appropriate wording (e.g. "AI-assisted estimate — guidance, not a final judgment"; keep actual-grade as "recorded outcome"). Keep it short; full detail lives in admin.
- **Polish:** consistent product page headers, a subtle "Week 38" context indicator, graceful empty/null states (already mostly handled). No redesign of the working tables/charts.

## Part 2 — Admin console (`/admin`)
New route group `apps/web/app/admin/` with its own layout + sub-nav. Sections (all from existing loaders):
- **`/admin` (Overview):** system health (schema, last import, counts, source artifacts — the elevated `PlatformStatusStrip` data) + cohort rollup analytics (risk distribution, means, top-at-risk/improving, trends).
- **`/admin/model` (Model & evaluation):** lean Twin RMSE/Δ, OULAD benchmark grouped+temporal tables, classification F1 0.861 / ROC-AUC 0.953, the honest limitations, circularity disclosure, "not causal". (Re-packages current `/research-demo` evidence, expanded.)
- **`/admin/explainability`:** global feature importance + dominance audit + a browser of representative XAI cases (reuse `explanation-panel`).
- **`/admin/data` (Data & provenance):** schema version, import timestamp, source artifacts, counts, OULAD cohort info (DDD 2013J), null-field disclosures (no attendance/quiz).
- **`/admin/about`:** the public-first honest narrative (F1≈0.86 never 1.000, target circularity, model-behavior-not-causal) — the footer "About the model" target.
- **Console chrome:** admin sub-nav (tabs/sidebar) visually distinct from teacher chrome so it reads as a back-office console.
- **`/research-demo` → redirect to `/admin/model`** (preserve the old URL; the prior screenshots' page becomes the admin model tab).

## Components
Reuse: `cohort-cards`, `student-table`, `risk-badge`, `explanation-panel`, `timeline-chart`, `platform-status-strip` (now admin-only).
New: `Footer` (global), `AdminSubNav`, an admin section/stat panel or two, `IdentityChip` (header). Keep new files small and focused; follow existing CSS class conventions (`.section`, `.cohort-card`, etc.) — extend `globals.css` with admin-console classes, no new styling system.

## Out of scope
- Auth / real roles (static identity chip only).
- Real multi-course/multi-cohort (single DDD 2013J + a disabled/placeholder selector at most).
- Live retrain / `/predict` serving; interventions / what-if (stays deferred, matches the non-claim).
- New backend or ML endpoints; new datasets.
- Mobile-first redesign (keep existing responsive behavior).

## Verification (acceptance)
1. Teacher pages (`/`, `/dashboard`, `/students`, `/students/[id]`, `/predictions`) show NO "RESEARCH PROTOTYPE" banner, no `PlatformStatusStrip`, no research jargon; read as a real product; nav shows the new brand + Admin link + identity chip; footer has "About the model".
2. `/admin` exists with the 5 sections, each populated from real OULAD-seeded data; the honest detail (F1 0.861, circularity, not-causal, limitations) is present and correct there.
3. `/research-demo` redirects to `/admin/model`.
4. App builds and runs; `npm run build` / typecheck pass; no broken links; null fields (attendance/quiz) still render gracefully.
5. Screenshots of the new teacher home, dashboard, student detail, and the admin console captured for review.
6. No synthetic R²≈0.99 / F1=1.000 presented as a real capability anywhere; honesty intact in admin.
