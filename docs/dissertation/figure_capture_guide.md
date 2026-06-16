# Figure capture & export guide — conference paper

Drafting scaffolding for `conference_paper_sist.md`. **Not part of the submission.**
It records how each figure is produced so they can be regenerated reproducibly.

Figures split into two kinds:

- **Inline Mermaid diagrams** — Fig. 1 (architecture / data-flow), Fig. 4 (nested
  feature-set ablation), Fig. 5 (experiment arc and verdict), Fig. 7 (explanation
  stability). Drawn, not captured.
- **Screenshots of the local web app** — Fig. 2 (cohort dashboard), Fig. 3
  (student detail), Fig. 6 (XAI explanation panel).

All screenshots come from the local web app. There is no login, but the data
pages require **two services**: the FastAPI backend (`apps/api`) serving on
`:8000` with its local SQLite projection seeded from the frozen research payload,
and the Next.js frontend (`apps/web`) on `:3000`. Without the API the pages render
an empty "Research platform data is not available yet" state.

## 0. Run the app (two services)

```bash
# from the repository root — first time only
pnpm install

# 1) API: serve on :8000 (auto-seeds the SQLite store on startup if empty;
#    or seed explicitly with `python -m src.import_research_payload`)
cd apps/api
uv sync
uv run python -m uvicorn src.main:app --host 127.0.0.1 --port 8000
#   NB: use `python -m uvicorn`, not the bare `uvicorn` console script — on
#   Windows the .exe may be blocked by an Application Control / WDAC policy.

# 2) Web: in a second terminal, from the repository root
pnpm dev   # Next.js on http://localhost:3000; reads the API via apps/web/.env
           # (NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api)
```

Then open `http://localhost:3000` in a browser. For clean, high-DPI figures:
maximise the window, set browser zoom to 100%, and use a 1440–1600 px wide
viewport. To capture a crisp PNG, use the browser DevTools device toolbar
(Ctrl+Shift+M) with a fixed width, or the OS screenshot tool (Win+Shift+S on
Windows). Save files under `docs/dissertation/figures/` and reference them in the
paper as `![Fig. n](figures/figN.png)`.

## Figs. 1, 4, 5, 7 — inline Mermaid diagrams (no screenshot needed)

These four are drawn diagrams embedded directly in the paper as fenced
` ```mermaid ` code blocks. They render automatically in GitHub and in VS Code
(with the *Markdown Preview Mermaid Support* extension). For a camera-ready raster
or vector export, paste the block into the [Mermaid Live Editor](https://mermaid.live)
and export PNG/SVG, or run `mmdc -i conference_paper_sist.md -o figures/figN.png`
(`@mermaid-js/mermaid-cli`). Save exports under `figures/` (e.g.
`figures/fig1_architecture.png`).

## Fig. 2 — Cohort dashboard

- Route: `http://localhost:3000/dashboard`
- Capture the full student table with the risk-level filter visible.
- Tip: apply the "high risk" filter for a second variant if you want to show
  filtering. Crop out browser chrome. Save as `figures/fig2_dashboard.png`.

## Fig. 3 — Student detail page

- Route: `http://localhost:3000/students` → click any student, **or** go directly
  to `http://localhost:3000/students/[studentId]` (pick a student id from the list
  or the dashboard URL).
- Capture (i) the row of summary cards and (ii) the weekly trajectory chart. If
  both do not fit in one frame, take two stacked screenshots and combine, or use a
  full-page capture (DevTools → Run command → "Capture full size screenshot").
- Choose a student with a visible trend (e.g. an at-risk or declining trajectory)
  for a more illustrative figure. Save as `figures/fig3_student_detail.png`.

## Fig. 6 — XAI explanation panel

- Same route as Fig. 3, scroll to the explanation panel below the timeline.
- Ensure the **XAI limitation notice** is visible in the frame — it is the point
  of the figure.
- Optional alternative/extra: the admin explainability view at
  `http://localhost:3000/admin/explainability`. Save as `figures/fig6_xai_panel.png`.

## Optional extra figures

Other routes you may screenshot if you expand the paper: `/predictions`,
`/twins`, `/interventions`, `/research-demo`, and the model/system console at
`/admin/model` and `/admin/data`.
