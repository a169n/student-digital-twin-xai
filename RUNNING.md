# Running the platform locally (Backend + Frontend)

The app has two parts that run together:

| Part | Stack | Folder | URL |
|------|-------|--------|-----|
| **Backend (API)** | FastAPI + SQLite | `apps/api` | http://localhost:8000 (docs at `/docs`) |
| **Frontend (Web)** | Next.js 14 | `apps/web` | http://localhost:3000 |

Prerequisites: **Python 3.11+**, **Node 20+**, and **npm** (or pnpm). All commands are shown for **Windows PowerShell** from the repo root.

---

## 0. One command (run both) — recommended

A launcher script starts the backend **and** frontend together:

```powershell
# Windows (PowerShell) — opens API + Web in two windows
.\dev.ps1
.\dev.ps1 -Seed     # re-seed the OULAD data first, then start

# …or via npm from the repo root
npm run dev:all
```

```bash
# Git Bash / WSL / macOS / Linux — API in background, Web in foreground (Ctrl+C stops both)
./dev.sh
./dev.sh --seed
```

That's it — open **http://localhost:3000**. To run the two parts manually instead, use the steps below.

---

## 1. Backend (FastAPI) — terminal 1

```powershell
cd apps\api

# First run only: seed the local SQLite store from the OULAD demo payload
.\.venv\Scripts\python.exe -m src.import_research_payload
#  -> "Imported research platform seed: 150 students, 5250 weekly snapshots, 4 explanation cases"

# Start the API (reload on changes)
.\.venv\Scripts\python.exe -m uvicorn src.main:app --port 8000
```

Verify it's up: open http://localhost:8000/api/health (should return `{"status":"ok"}`) or http://localhost:8000/docs.

> The API auto-seeds on first start if the store is empty, so the seed step is optional — but running it explicitly guarantees fresh OULAD data. Data lives in `data/application/research_platform.sqlite` (gitignored, regenerable).

---

## 2. Frontend (Next.js) — terminal 2

```powershell
cd apps\web
npm run dev
```

Open **http://localhost:3000**.

> If port 3000 is busy, Next.js auto-picks 3001/3002 — watch the terminal for the actual `Local:` URL. The web app reads the API base from `apps/web/.env` (`NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api`).

---

## One-time setup (only if dependencies are missing)

The repo already includes the API virtualenv (`apps/api/.venv`) and web `node_modules`. If they are absent (fresh clone):

```powershell
# Backend deps (from repo root)
python -m venv apps\api\.venv
.\apps\api\.venv\Scripts\python.exe -m pip install -e services\ml -e apps\api

# Frontend deps
cd apps\web
npm install   # or: pnpm install
```

---

## Quick reference

```powershell
# Terminal 1 — API
cd apps\api ; .\.venv\Scripts\python.exe -m uvicorn src.main:app --port 8000

# Terminal 2 — Web
cd apps\web ; npm run dev
```

| What | Command |
|------|---------|
| Re-seed the API store (OULAD data) | `cd apps\api ; .\.venv\Scripts\python.exe -m src.import_research_payload` |
| API health check | `curl http://localhost:8000/api/health` |
| Rebuild the OULAD demo payload (advanced) | `cd services\ml ; python -m src.export.export_oulad_research_payload` |

---

## Troubleshooting

- **`[Errno 10048] only one usage of each socket address` (port 8000 busy):** an API is already running. Use it, or stop the other process (`netstat -ano | findstr :8000` then `taskkill /PID <pid> /F`).
- **Web shows "platform unavailable":** the API isn't running or isn't seeded — start the backend (step 1) and reload.
- **Bash users:** replace `.\.venv\Scripts\python.exe` with `./.venv/Scripts/python.exe`.

bash (Git Bash / WSL) equivalents:

```bash
# Terminal 1 — API
cd apps/api && ./.venv/Scripts/python.exe -m uvicorn src.main:app --port 8000
# Terminal 2 — Web
cd apps/web && npm run dev
```
