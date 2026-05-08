param(
    [ValidateSet("small", "default", "large", "xlarge")]
    [string]$Preset = "default",
    [int]$Seed = 42,
    [switch]$Apply,
    [switch]$SkipParquet
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath

if (-not $Apply) {
    Write-Host "Dry run only. This would reset rebuildable data, generate '$Preset', and refresh the UI seed."
    Write-Host ""
    & (Join-Path $scriptDir "Reset-RebuildableData.ps1")
    Write-Host ""
    Write-Host "Rerun with -Apply to perform the rebuild."
    exit 0
}

& (Join-Path $scriptDir "Reset-RebuildableData.ps1") -Apply

$generateArgs = @("-Preset", $Preset, "-Seed", "$Seed")
if ($SkipParquet) {
    $generateArgs += "-SkipParquet"
}
& (Join-Path $scriptDir "Generate-Dataset.ps1") @generateArgs

& (Join-Path $scriptDir "Refresh-UiSeed.ps1")

Write-Host "Research data rebuild completed for preset '$Preset' with seed $Seed."
