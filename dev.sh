#!/usr/bin/env bash
# Launch the Student Digital Twin platform: FastAPI backend + Next.js frontend.
# Runs the API in the background and the web app in the foreground; stopping
# this script (Ctrl+C) also stops the API.
#
# Usage:
#   ./dev.sh           # start both
#   ./dev.sh --seed    # re-seed the API store first, then start both
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
api_dir="$root/apps/api"
web_dir="$root/apps/web"

# venv python: Windows (Git Bash) layout first, then POSIX
py="$api_dir/.venv/Scripts/python.exe"
[ -x "$py" ] || py="$api_dir/.venv/bin/python"
if [ ! -x "$py" ]; then
  echo "API virtualenv not found at '$py'. See RUNNING.md > 'One-time setup'." >&2
  exit 1
fi

if [ "${1:-}" = "--seed" ]; then
  echo "Seeding API store with OULAD demo data..."
  ( cd "$api_dir" && "$py" -m src.import_research_payload )
fi

echo "Starting backend (API)  -> http://localhost:8000"
( cd "$api_dir" && "$py" -m uvicorn src.main:app --port 8000 ) &
API_PID=$!
trap 'echo; echo "Stopping API ($API_PID)..."; kill "$API_PID" 2>/dev/null || true' EXIT INT TERM

echo "Starting frontend (Web) -> http://localhost:3000  (Ctrl+C to stop both)"
cd "$web_dir" && npm run dev
