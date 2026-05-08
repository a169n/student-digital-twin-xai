param()

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path -LiteralPath (Join-Path $scriptDir "..")).Path
$mlRoot = Join-Path $repoRoot "services\ml"
$apiRoot = Join-Path $repoRoot "apps\api"

Write-Host "Exporting UI research-demo payload from current data and frozen experiment artifacts..."
Push-Location $mlRoot
try {
    & python -m src.export.export_research_demo_payload
    if ($LASTEXITCODE -ne 0) {
        throw "UI payload export failed with exit code $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}

Write-Host "Importing UI payload into local SQLite application store..."
Push-Location $apiRoot
try {
    & python -m src.import_research_payload
    if ($LASTEXITCODE -ne 0) {
        throw "API seed import failed with exit code $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}

Write-Host "Done. The UI seed path is refreshed."
Write-Host "Note: this script does not rerun experiments or validate new hypotheses."
