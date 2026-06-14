# Teacher Product MVP + Admin Console Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the OULAD-seeded Next.js dashboard from a "research prototype" into a polished teacher product MVP (no auth) and add a model & system admin console (`/admin`) that holds the deeper detail and the honest research framing.

**Architecture:** Frontend-only re-packaging of an already-mature app (`apps/web`, Next.js App Router, custom-CSS design system in `apps/web/app/globals.css`). Reuse all existing loaders (`apps/web/lib/platform/loaders.ts`) and components — no backend/ML/endpoint changes. Teacher pages lose their research framing; a new `/admin` route group (own sub-nav + console chrome) absorbs the evidence/metrics/provenance and the honest caveats; a global footer links to "About the model".

**Tech Stack:** Next.js 14 App Router (server components + the one client `student-table`), TypeScript, plain CSS (`globals.css`, semantic class names like `.section`, `.cohort-card`, `.risk-badge`). Verification: `npm run typecheck` (tsc --noEmit), `npm run build`, visual checks via the running dev server. NOT pytest.

**Commit policy:** This repo does NOT auto-commit. Each task ends by staging (`git add`); the WORKER does NOT `git commit` (the user commits). Commit messages shown for the user's convenience.

**Honest-framing guardrails (carry into every task):** synthetic R²≈0.99 / F1=1.000 = artifact, never a real capability; teacher pages carry NO research jargon but the honest detail (target circularity, F1≈0.861 not 1.000, "model-behavior not causal", limitations) MUST be present and correct in `/admin`. "Digital Twin" = lean weekly state representation, not simulation.

---

## Pre-execution reads (every task)
Before editing a file, READ it in full to match the existing JSX structure, prop shapes, and CSS class conventions. Key references:
- `apps/web/app/layout.tsx`, `apps/web/components/layout/nav.tsx` — shell + nav.
- `apps/web/app/globals.css` — the design system (extend it; do NOT introduce Tailwind/CSS-modules).
- `apps/web/lib/platform/loaders.ts` + `apps/web/lib/platform/types.ts` — the data (loaders return typed objects; all data needed already exists).
- `apps/web/components/common/{research-banner,platform-status-strip,risk-badge}.tsx`, `apps/web/components/dashboard/{cohort-cards,student-table}.tsx`, `apps/web/components/student/{explanation-panel,timeline-chart}.tsx`.
- `apps/web/app/research-demo/page.tsx` — the evidence content to re-home into `/admin/model`.

## File / task map
| Task | Area | Files |
|---|---|---|
| 1 | Footer | Create `apps/web/components/layout/footer.tsx`; modify `layout.tsx`; extend `globals.css` |
| 2 | Nav + identity | Modify `nav.tsx`; create `apps/web/components/layout/identity-chip.tsx`; `globals.css` |
| 3 | Strip research framing | Modify `app/page.tsx`, `app/dashboard/page.tsx`, `app/students/page.tsx`, `app/students/[studentId]/page.tsx`, `app/predictions/page.tsx` |
| 4 | Product home | Modify `app/page.tsx` |
| 5 | Soften student caveats | Modify `app/students/[studentId]/page.tsx`, `components/student/explanation-panel.tsx` |
| 6 | Admin shell | Create `app/admin/layout.tsx`, `components/layout/admin-sub-nav.tsx`; `globals.css` |
| 7 | Admin Overview | Create `app/admin/page.tsx` |
| 8 | Admin Model & eval + redirect | Create `app/admin/model/page.tsx`; convert `app/research-demo/page.tsx` to a redirect |
| 9 | Admin Explainability | Create `app/admin/explainability/page.tsx` |
| 10 | Admin Data + About | Create `app/admin/data/page.tsx`, `app/admin/about/page.tsx` |
| 11 | Verify | typecheck/build + screenshots + honesty/links sweep |

---

## Task 1: Global Footer with "About the model" link

**Files:** Create `apps/web/components/layout/footer.tsx`; Modify `apps/web/app/layout.tsx`; extend `apps/web/app/globals.css`.

- [ ] **Step 1: Read** `apps/web/app/layout.tsx` (the shell — where nav + children render) and the top of `globals.css` (tokens + `.app-nav` classes) to match conventions.

- [ ] **Step 2: Create the Footer component** `apps/web/components/layout/footer.tsx` (server component):

```tsx
import Link from "next/link";

export function AppFooter() {
  return (
    <footer className="app-footer">
      <div className="app-footer__inner">
        <span className="app-footer__brand">Student Digital Twin</span>
        <span className="app-footer__note">
          AI-assisted early-warning analytics. Predictions and explanations describe model behavior,
          not causal truth.
        </span>
        <Link className="app-footer__link" href="/admin/about">
          About the model
        </Link>
      </div>
    </footer>
  );
}
```

- [ ] **Step 3: Render the footer in the root layout.** In `apps/web/app/layout.tsx`, import `AppFooter` and place it after the page `{children}` (outside `<main>` if the nav is similarly outside; match the existing structure). Wrap content so the footer sits at the bottom (use a flex column on the body/root container if not already).

- [ ] **Step 4: Add footer styles to `globals.css`** (follow existing token usage):

```css
.app-footer { border-top: 1px solid var(--border); background: var(--surface); margin-top: 40px; }
.app-footer__inner { max-width: 1200px; margin: 0 auto; padding: 16px 24px; display: flex; flex-wrap: wrap; gap: 12px; align-items: center; font-size: 12px; color: var(--muted); }
.app-footer__brand { font-weight: 600; color: var(--text); }
.app-footer__note { flex: 1 1 320px; }
.app-footer__link { color: var(--primary); text-decoration: none; }
.app-footer__link:hover { text-decoration: underline; }
```

- [ ] **Step 5: Verify** — `cd apps/web && npm run typecheck` passes; visit `/` and confirm the footer renders with the "About the model" link (the link target `/admin/about` is created in Task 10; until then it 404s — acceptable mid-plan).

- [ ] **Step 6: Stage** (no commit): `git add apps/web/components/layout/footer.tsx apps/web/app/layout.tsx apps/web/app/globals.css`

---

## Task 2: Rebrand nav + identity chip + nav links

**Files:** Modify `apps/web/components/layout/nav.tsx`; Create `apps/web/components/layout/identity-chip.tsx`; extend `globals.css`.

- [ ] **Step 1: Read** `apps/web/components/layout/nav.tsx` (current brand "Student Digital Twin · Research Platform" + links Dashboard/Students/Predictions/Research).

- [ ] **Step 2: Create the identity chip** `apps/web/components/layout/identity-chip.tsx` (static, no auth):

```tsx
export function IdentityChip() {
  return (
    <div className="identity-chip" aria-label="Signed in teacher">
      <span className="identity-chip__avatar" aria-hidden>MC</span>
      <span className="identity-chip__meta">
        <span className="identity-chip__name">Ms. Carter</span>
        <span className="identity-chip__role">DDD 2013J</span>
      </span>
    </div>
  );
}
```

- [ ] **Step 3: Update `nav.tsx`:** brand text → `Student Digital Twin` with a tagline `Early-warning student analytics` (drop "· Research Platform"); links → `Dashboard` (`/dashboard`), `Students` (`/students`), `Predictions` (`/predictions`), `Admin` (`/admin`) — REMOVE the `Research` (`/research-demo`) link. Render `<IdentityChip />` at the right end of the nav. Keep the existing `.app-nav*` class structure; add the tagline + chip within it.

- [ ] **Step 4: Add styles** to `globals.css`:

```css
.app-nav__tagline { display: block; font-size: 11px; color: var(--muted); font-weight: 400; }
.identity-chip { display: inline-flex; align-items: center; gap: 8px; padding: 4px 10px 4px 4px; border: 1px solid var(--border); border-radius: 999px; background: var(--surface); }
.identity-chip__avatar { width: 28px; height: 28px; border-radius: 999px; background: var(--primary-soft); color: var(--primary); font-size: 12px; font-weight: 600; display: inline-flex; align-items: center; justify-content: center; }
.identity-chip__meta { display: flex; flex-direction: column; line-height: 1.15; }
.identity-chip__name { font-size: 13px; font-weight: 600; color: var(--text); }
.identity-chip__role { font-size: 11px; color: var(--muted); }
```

- [ ] **Step 5: Verify** — typecheck passes; visit `/dashboard`: nav shows new brand + tagline, 4 links (no "Research"), identity chip on the right.

- [ ] **Step 6: Stage:** `git add apps/web/components/layout/nav.tsx apps/web/components/layout/identity-chip.tsx apps/web/app/globals.css`

---

## Task 3: Remove research framing from teacher pages

**Files:** Modify `apps/web/app/page.tsx`, `apps/web/app/dashboard/page.tsx`, `apps/web/app/students/page.tsx`, `apps/web/app/students/[studentId]/page.tsx`, `apps/web/app/predictions/page.tsx`.

- [ ] **Step 1: Read each page** and locate every usage of `ResearchBanner` and `PlatformStatusStrip` (imports + JSX) and any "research/frozen/read-only" lede copy.

- [ ] **Step 2: Remove** the `<ResearchBanner />` and `<PlatformStatusStrip ... />` elements and their imports from ALL FIVE teacher pages. Remove the now-unused `tryLoadPlatformStatus()` calls on these pages if they were ONLY feeding the status strip (keep them only if used elsewhere on the page). Do NOT delete the `research-banner.tsx` / `platform-status-strip.tsx` component files (PlatformStatusStrip is reused in admin).

- [ ] **Step 3: De-jargon the page ledes** (replace research-y copy with product copy), e.g.:
  - `/dashboard` lede: "Triage the imported cohort … latest Twin state." → "This week's view of every student's progress and risk. Open a student for their weekly trajectory and what's driving it."
  - `/predictions` note: "served from the platform store and seeded from the frozen lean Twin payload …" → "The model's current prediction for each student this week."
  - `/students` lede: keep product-plain ("Search and open any student.").
  Keep wording short and product-appropriate; do NOT introduce new claims.

- [ ] **Step 4: Verify** — typecheck passes; `cd apps/web && grep -rn "ResearchBanner\|PlatformStatusStrip\|RESEARCH PROTOTYPE\|frozen artifacts\|read-only research" app/page.tsx app/dashboard app/students app/predictions` returns NOTHING (all removed from teacher pages). Visit each page: no banner, no status strip, no research jargon.

- [ ] **Step 5: Stage:** `git add apps/web/app/page.tsx apps/web/app/dashboard apps/web/app/students apps/web/app/predictions`

---

## Task 4: Task-driven product home

**Files:** Modify `apps/web/app/page.tsx`.

- [ ] **Step 1: Read** `apps/web/app/page.tsx` (current research-intro hero + entry-card grid) and `apps/web/lib/platform/loaders.ts` (`tryLoadDashboard()` returns cohort + students).

- [ ] **Step 2: Rewrite the home page** as a teacher landing using `tryLoadDashboard()` only (drop `tryLoadResearchEvidence`/`tryLoadPlatformStatus` from home). Structure (reuse existing `.page`, `.section`, `.cohort-card`, `.entry-card`, `.watchlist` classes):
  - Greeting hero: `<h1>Welcome back, Ms. Carter</h1>` + sub: `DDD 2013J · Week {cohort.currentWeek} · {cohort.studentCount} students`.
  - Three primary CTA cards (links): "Open cohort dashboard" → `/dashboard`, "Find a student" → `/students`, "This week's predictions" → `/predictions`.
  - A "Students needing attention" preview: render `cohort.topAtRisk.slice(0, 5)` as a watchlist (name, predicted grade, risk badge via existing `RiskBadge`, link to `/students/{id}`).
  - If `!dashboard` → render the existing `PlatformUnavailableNotice` (import from `components/common/platform-unavailable`).
  - Remove all "frozen artifacts / read-only platform / FastAPI / SQLite projection" copy.

- [ ] **Step 3: Verify** — typecheck passes; visit `/`: greeting with real cohort numbers (Week 38, 150 students), 3 CTA cards, top-5 at-risk preview with risk badges; no research copy.

- [ ] **Step 4: Stage:** `git add apps/web/app/page.tsx`

---

## Task 5: Soften student-detail caveats to product wording

**Files:** Modify `apps/web/app/students/[studentId]/page.tsx`, `apps/web/components/student/explanation-panel.tsx`.

- [ ] **Step 1: Read** both files; locate the "Reading guardrail" panel (`.panel--caveat` / `.latest-state__guardrail`) on the detail page and the interpretation/footer caveat inside `explanation-panel.tsx`.

- [ ] **Step 2: Replace research jargon with product wording** (keep it short; do not delete the safety message, just productize it):
  - "Reading guardrail" panel → a compact note: "Predicted grade is an AI-assisted estimate to guide attention — not a final judgment. The recorded outcome is shown for context only." (Remove "the model is not retrained from the UI", "read-only projection of frozen data", "retrospective evaluation evidence" jargon.)
  - `explanation-panel` interpretation/footer → "What's pushing this student's estimate up or down, per the model. A guide for conversation, not a cause." (Remove "model-behavior signal / permutation / no SHAP" research detail — that detail now lives in `/admin/explainability`.)

- [ ] **Step 3: Verify** — typecheck passes; visit `/students/124387`: the risk/explanation reads as product guidance, no research jargon; null fields (attendance/quiz) still render as "—".

- [ ] **Step 4: Stage:** `git add apps/web/app/students apps/web/components/student/explanation-panel.tsx`

---

## Task 6: Admin shell (layout + sub-nav + console chrome)

**Files:** Create `apps/web/app/admin/layout.tsx`, `apps/web/components/layout/admin-sub-nav.tsx`; extend `globals.css`.

- [ ] **Step 1: Read** `apps/web/app/layout.tsx` to see how the root layout wraps pages (the admin layout nests inside it).

- [ ] **Step 2: Create the admin sub-nav** `apps/web/components/layout/admin-sub-nav.tsx` (client component for active-link styling):

```tsx
"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const ADMIN_LINKS = [
  { href: "/admin", label: "Overview" },
  { href: "/admin/model", label: "Model & evaluation" },
  { href: "/admin/explainability", label: "Explainability" },
  { href: "/admin/data", label: "Data & provenance" },
  { href: "/admin/about", label: "About the model" }
];

export function AdminSubNav() {
  const pathname = usePathname();
  return (
    <nav className="admin-subnav" aria-label="Admin sections">
      {ADMIN_LINKS.map((link) => {
        const active = pathname === link.href;
        return (
          <Link
            key={link.href}
            href={link.href}
            className={active ? "admin-subnav__link admin-subnav__link--active" : "admin-subnav__link"}
            aria-current={active ? "page" : undefined}
          >
            {link.label}
          </Link>
        );
      })}
    </nav>
  );
}
```

- [ ] **Step 3: Create the admin layout** `apps/web/app/admin/layout.tsx`:

```tsx
import { AdminSubNav } from "@/components/layout/admin-sub-nav";

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="admin-shell">
      <header className="admin-shell__header">
        <div>
          <p className="admin-shell__eyebrow">Admin console</p>
          <h1 className="admin-shell__title">Model &amp; system</h1>
        </div>
      </header>
      <AdminSubNav />
      <div className="admin-shell__body">{children}</div>
    </div>
  );
}
```

- [ ] **Step 4: Add admin chrome styles** to `globals.css` (distinct, console-like but consistent with tokens):

```css
.admin-shell { max-width: 1200px; margin: 0 auto; padding: 24px; }
.admin-shell__header { display: flex; align-items: flex-end; justify-content: space-between; gap: 16px; margin-bottom: 12px; }
.admin-shell__eyebrow { font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); margin: 0; }
.admin-shell__title { font-size: 26px; margin: 2px 0 0; }
.admin-subnav { display: flex; flex-wrap: wrap; gap: 4px; border-bottom: 1px solid var(--border); margin-bottom: 20px; }
.admin-subnav__link { padding: 8px 14px; font-size: 13px; color: var(--muted); text-decoration: none; border-bottom: 2px solid transparent; }
.admin-subnav__link:hover { color: var(--text); }
.admin-subnav__link--active { color: var(--primary); border-bottom-color: var(--primary); font-weight: 600; }
.admin-shell__body { display: flex; flex-direction: column; gap: 24px; }
```

- [ ] **Step 5: Verify** — typecheck passes (the `/admin` page itself comes in Task 7; until then `/admin` may 404, fine). Confirm no import errors.

- [ ] **Step 6: Stage:** `git add apps/web/app/admin/layout.tsx apps/web/components/layout/admin-sub-nav.tsx apps/web/app/globals.css`

---

## Task 7: Admin Overview (`/admin`)

**Files:** Create `apps/web/app/admin/page.tsx`.

- [ ] **Step 1: Read** `apps/web/lib/platform/loaders.ts` + `types.ts` for `tryLoadPlatformStatus()` (`PlatformStatus`: seeded, counts, schemaVersion, lastImportedAt, sourceArtifacts) and `tryLoadDashboard()` (`CohortSummary`). Read `components/common/platform-status-strip.tsx` and `components/dashboard/cohort-cards.tsx` to reuse.

- [ ] **Step 2: Create `apps/web/app/admin/page.tsx`** (server component) showing:
  - A "System health" section: render `<PlatformStatusStrip status={status} />` (reused) + a small grid of provenance facts (schema version, last imported, student/snapshot/case counts).
  - A "Cohort analytics" section: reuse `<CohortCards cohort={dashboard.cohort} />` (or render the `CohortSummary` means + `riskDistribution` low/medium/high counts + atRisk/lowMastery/lowActivity counts).
  - Use `Promise.all([tryLoadPlatformStatus(), tryLoadDashboard()])`; if either is null → `PlatformUnavailableNotice`.
  - Use existing `.section`, `.section__heading`, `.cohort-card` classes.

- [ ] **Step 3: Verify** — typecheck passes; visit `/admin`: system health (schema 1.0.0, 150 students / 5250 snapshots / 4 cases) + cohort analytics (risk mix 82/5/63); admin sub-nav shows "Overview" active.

- [ ] **Step 4: Stage:** `git add apps/web/app/admin/page.tsx`

---

## Task 8: Admin Model & evaluation (`/admin/model`) + research-demo redirect

**Files:** Create `apps/web/app/admin/model/page.tsx`; convert `apps/web/app/research-demo/page.tsx` to a redirect.

- [ ] **Step 1: Read** `apps/web/app/research-demo/page.tsx` fully (it already renders the evidence: hero metrics, claim guardrails, experiment timeline, lean Twin metrics, XAI dominance, representative cases, OULAD benchmark table, limitations) and the `ResearchSummary` type.

- [ ] **Step 2: Create `apps/web/app/admin/model/page.tsx`** by MOVING the research-demo evidence content here, focused on **Model & evaluation**: lean Twin RMSE/Δ, the OULAD benchmark grouped + temporal tables, classification framing (F1 0.861 / ROC-AUC 0.953 from the payload/timeline), the limitations panel, and the circularity + "not causal" disclosures. Keep the existing honest copy verbatim (it is correct). Drop the teacher-facing "Defense overview" hero framing in favor of an admin "Model & evaluation" heading. Reuse `tryLoadResearchEvidence()` + `tryLoadExplanationCases()`. (Explainability-specific global-importance/cases UI can stay minimal here and live fully in Task 9.)

- [ ] **Step 3: Convert `apps/web/app/research-demo/page.tsx` to a redirect:**

```tsx
import { redirect } from "next/navigation";

export default function ResearchDemoRedirect() {
  redirect("/admin/model");
}
```

- [ ] **Step 4: Update the research-demo test if present.** Check `apps/web` for a `test:research-demo` script / test file. If it asserts `/research-demo` content, point it at `/admin/model` (or update it to assert the redirect). Run `npm run test:research-demo` if it exists.

- [ ] **Step 5: Verify** — typecheck passes; visit `/admin/model`: lean Twin + OULAD benchmark + F1 0.861 + circularity + limitations all present and correct; visit `/research-demo` → redirects to `/admin/model`.

- [ ] **Step 6: Stage:** `git add apps/web/app/admin/model apps/web/app/research-demo`

---

## Task 9: Admin Explainability (`/admin/explainability`)

**Files:** Create `apps/web/app/admin/explainability/page.tsx`.

- [ ] **Step 1: Read** `tryLoadResearchEvidence()` (`xai`: method, shapUsed, `topGlobalFeatures[]`, `dominance` {topFeature, top1Share, averageLocalMasteryShare, outcome}, recommendation) and `tryLoadExplanationCases()` (`ExplanationSummary[]`); read `components/student/explanation-panel.tsx` to reuse for case rendering.

- [ ] **Step 2: Create `apps/web/app/admin/explainability/page.tsx`** (server component):
  - "Global feature importance" section: render `xai.topGlobalFeatures` as ranked rows (feature, importance share) using existing bar/row classes (`.contribution-row` or a simple table).
  - "Dominance audit" section: topFeature, top-1 share, average local mastery share, outcome (e.g. `acceptable_with_caveat`), and the `xai.method` ("permutation importance + perturbation; no SHAP") + `shapUsed=false`.
  - "Representative cases" browser: map `cases` → `<ExplanationPanel ... />` (reused) or compact cards linking to `/students/{studentId}`.
  - `Promise.all([tryLoadResearchEvidence(), tryLoadExplanationCases()])`; null → `PlatformUnavailableNotice`.

- [ ] **Step 3: Verify** — typecheck passes; visit `/admin/explainability`: global importance list, dominance audit (top feature + outcome), and the 4 representative cases render.

- [ ] **Step 4: Stage:** `git add apps/web/app/admin/explainability`

---

## Task 10: Admin Data & provenance + About

**Files:** Create `apps/web/app/admin/data/page.tsx`, `apps/web/app/admin/about/page.tsx`.

- [ ] **Step 1: Read** `tryLoadPlatformStatus()` (`sourceArtifacts`, schema, import date, counts) and `tryLoadResearchEvidence()` (`limitations[]`, `sourceArtifacts`).

- [ ] **Step 2: Create `apps/web/app/admin/data/page.tsx`** (Data & provenance): schema version, last imported timestamp, student/snapshot/case counts, the source-artifacts list (paths), the OULAD cohort identity (DDD 2013J), and a clear "null-by-design fields" note (no attendance / no quiz analog in OULAD). Use `tryLoadPlatformStatus()` + `tryLoadResearchEvidence()`.

- [ ] **Step 3: Create `apps/web/app/admin/about/page.tsx`** (About the model — the footer link target): a readable narrative of the honest framing, sourced from `tryLoadResearchEvidence().limitations` plus static copy: the demo runs on real OULAD DDD 2013J; pass-risk is a held-out classifier (F1 ≈ 0.861, ROC-AUC 0.953, never 1.000); the regression target is partially circular; Twin value is mixed-to-null; explanations are model-behavior, not causal; no SHAP; no intervention/what-if simulation. Render `limitations` as a list.

- [ ] **Step 4: Verify** — typecheck passes; visit `/admin/data` (provenance + null-field note) and `/admin/about` (honest narrative with F1 0.861 / circularity / not-causal). Confirm the footer "About the model" link now resolves to `/admin/about`.

- [ ] **Step 5: Stage:** `git add apps/web/app/admin/data apps/web/app/admin/about`

---

## Task 11: Verification — build, screenshots, sweeps

**Files:** none (verification); may capture screenshots to `docs/dissertation/figures/screenshots/`.

- [ ] **Step 1: Typecheck + build.** `cd apps/web && npm run typecheck && npm run build`. Both must pass with no errors. Fix any type/build error introduced.

- [ ] **Step 2: Research-jargon sweep (teacher pages).** Run from `apps/web`:
`grep -rn "RESEARCH PROTOTYPE\|frozen artifacts\|read-only research\|ResearchBanner\|PlatformStatusStrip" app/page.tsx app/dashboard app/students app/predictions`
Expected: NO matches (all research framing removed from teacher pages).

- [ ] **Step 3: Honesty-present sweep (admin).** Confirm the honest detail lives in admin:
`grep -rn "0.861\|circular\|not causal\|never\|1.000" app/admin` → expect matches (F1 0.861, circularity, not-causal, "never 1.000" present in admin/model + admin/about).

- [ ] **Step 4: Run the app and capture screenshots** (API + web must be running; API on :8000, web on :3000/3001). Capture: new teacher home `/`, `/dashboard`, `/students/124387`, and admin `/admin`, `/admin/model`, `/admin/explainability`, `/admin/about`. Save to `docs/dissertation/figures/screenshots/` (e.g. `product-01-home.png`, `product-02-dashboard.png`, `admin-01-overview.png`, `admin-02-model.png`, …).

- [ ] **Step 5: Link check.** Click through nav (Dashboard/Students/Predictions/Admin), the admin sub-nav (all 5 tabs), the footer "About the model" link, and `/research-demo` (must redirect to `/admin/model`). No 404s, no broken null rendering.

- [ ] **Step 6: Stage any screenshots:** `git add docs/dissertation/figures/screenshots`

---

## Self-review notes
- **Spec coverage:** spec Part 1 (de-prototype) → Tasks 2 (nav/brand/chip), 3 (strip framing), 4 (product home), 5 (soften caveats), 1 (footer "About" link); Part 2 (admin) → Tasks 6 (shell), 7 (overview), 8 (model + redirect), 9 (explainability), 10 (data + about); honesty placement → caveats removed from teacher (Task 3/5), present in admin (Tasks 8/9/10) + verified (Task 11 steps 2-3); `/research-demo` redirect → Task 8; verification/screenshots → Task 11. All spec sections covered.
- **No placeholders:** every task names exact files, the exact copy/JSX skeletons, the loaders to call, and concrete verification greps/visits. UI tasks that depend on existing JSX carry an explicit "read the file first and match conventions" instruction (appropriate for UI re-packaging — the data shapes + class names are specified).
- **Type/name consistency:** reused names verified against the Explore map — loaders `tryLoadDashboard`/`tryLoadPlatformStatus`/`tryLoadResearchEvidence`/`tryLoadExplanationCases`/`tryLoadStudentDetail`; components `RiskBadge`/`CohortCards`/`ExplanationPanel`/`PlatformStatusStrip`/`PlatformUnavailableNotice`; new components `AppFooter`/`IdentityChip`/`AdminSubNav` used consistently across tasks; admin routes `/admin`,`/admin/model`,`/admin/explainability`,`/admin/data`,`/admin/about` consistent between the sub-nav (Task 6), the pages (Tasks 7-10), the footer link (Task 1 → `/admin/about`), and the redirect (Task 8).
- **No tests in pytest sense:** verification is typecheck/build/grep/visual (frontend). The one existing `test:research-demo` is handled in Task 8 step 4.
