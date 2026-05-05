# Web App (Next.js)

Teacher-facing UI for the student digital twin research platform.

## Scope (Current)

- App Router structure
- Dashboard, roster, student Twin, prediction, and research evidence pages
- API-backed platform DTOs from FastAPI
- Clear unavailable state when the API or local application store is not ready
- Explicit placeholders for deferred Twin workspace and intervention workflow

## Data Source

The web app no longer reads `data/artifacts/research_demo/research_demo_payload.json`
directly. Runtime data flows through:

```text
frozen artifacts -> research demo payload -> SQLite application store -> FastAPI -> Next.js
```

Set `NEXT_PUBLIC_API_BASE_URL` when the API is not on `http://localhost:8000/api`.
