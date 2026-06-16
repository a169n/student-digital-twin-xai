#!/usr/bin/env pwsh
<#
.SYNOPSIS
  Launch the Student Digital Twin platform: FastAPI backend + Next.js frontend.

.DESCRIPTION
  Starts the API (http://localhost:8000) and the web app (http://localhost:3000)
  in two separate PowerShell windows so each shows its own live logs.

.PARAMETER Seed
  Re-seed the API SQLite store from the OULAD demo payload before starting.
  (The API also auto-seeds on first start if the store is empty.)

.EXAMPLE
  .\dev.ps1
.EXAMPLE
  .\dev.ps1 -Seed
#>
param([switch]$Seed)

$ErrorActionPreference = "Stop"
$root   = $PSScriptRoot
$apiDir = Join-Path $root "apps\api"
$webDir = Join-Path $root "apps\web"
$py     = Join-Path $apiDir ".venv\Scripts\python.exe"

if (-not (Test-Path $py)) {
  Write-Error "API virtualenv not found at '$py'. See RUNNING.md > 'One-time setup'."
  exit 1
}

if ($Seed) {
  Write-Host "Seeding API store with OULAD demo data..." -ForegroundColor Cyan
  Push-Location $apiDir
  & $py -m src.import_research_payload
  Pop-Location
}

Write-Host "Starting backend (API)  -> http://localhost:8000" -ForegroundColor Green
Start-Process powershell -ArgumentList @(
  "-NoExit", "-Command",
  "Set-Location '$apiDir'; & '$py' -m uvicorn src.main:app --port 8000"
)

Write-Host "Starting frontend (Web) -> http://localhost:3000" -ForegroundColor Green
Start-Process powershell -ArgumentList @(
  "-NoExit", "-Command",
  "Set-Location '$webDir'; npm run dev"
)

Write-Host ""
Write-Host "Both services launched in separate windows." -ForegroundColor Cyan
Write-Host "Open http://localhost:3000  (close the two windows to stop)." -ForegroundColor Cyan
