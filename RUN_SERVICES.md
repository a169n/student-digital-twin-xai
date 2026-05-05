# Run Services Locally (Web + API + ML)

This guide shows the recommended local startup flow for this monorepo on Windows.

## 1. Prerequisites

- Python 3.11+
- Node.js 20+
- `uv` installed (`pip install uv` or `pipx install uv`)
- `pnpm` installed (repo uses workspaces)

## 2. Python environment setup (recommended)

You can run Python services with `uv` only, but a local virtual environment is also fine.

### PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If script execution is blocked:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Command Prompt

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

After activation:

```powershell
python -m pip install --upgrade pip
python -m pip install -e .\services\ml
python -m pip install -e .\apps\api
```

## 3. ML service (generate/update research data)

From repository root:

```powershell
cd services\ml
python -m src.main --config configs/generator_v1_3_refined.yaml
```

Notes:
- `generator_v1_3_refined.yaml` is the explicit latest refined config.
- `generator_v1.yaml` is currently an alias that also points to v1.3 refined tuning.

This refreshes outputs under `data\raw`, `data\processed`, and `data\artifacts`.

## 4. API service (FastAPI)

From repository root:

```powershell
cd apps\api
uv sync
uv run python -m src.import_research_payload
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: `http://localhost:8000/docs`  
Base API path for web app: `http://localhost:8000/api`

## 5. Web app (Next.js)

From repository root:

```powershell
pnpm install
pnpm dev:web
```

Open: `http://localhost:3000`

If API is not on the default address, set `apps\web\.env`:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

## 6. Optional: run via Docker Compose

From repository root:

```powershell
docker compose up --build
```

This starts `web`, `api`, `ml`, and `postgres` services defined in `docker-compose.yml`.
