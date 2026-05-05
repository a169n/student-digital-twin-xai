# API Service (FastAPI)

Backend service for the student digital twin research platform.

## Scope (Current)
- Health and platform status endpoints
- SQLite-backed application projection under `data/application/`
- Importer for `data/artifacts/research_demo/research_demo_payload.json`
- Teacher-facing read APIs for dashboard, students, Twin snapshots,
  predictions, explanations, interventions scope, and research evidence

The importer does not rerun models and does not modify frozen experiment
artifacts. It only refreshes the local application store used by the API.

## Seed the Application Store

From `apps/api`:

```bash
python -m src.import_research_payload
```

## Run

```bash
uv sync
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API also attempts to seed the store on startup when the SQLite database is
empty and the frozen research payload exists.
