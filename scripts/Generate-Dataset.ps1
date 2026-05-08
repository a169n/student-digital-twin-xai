param(
    [ValidateSet("small", "default", "large", "xlarge")]
    [string]$Preset = "default",
    [int]$Seed = 42,
    [switch]$SkipParquet
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path -LiteralPath (Join-Path $scriptDir "..")).Path
$mlRoot = Join-Path $repoRoot "services\ml"

$presets = @{
    small = @{
        NumStudents = 48
        NumWeeks = 10
        NumGroups = 2
        AssignmentsPerWeek = 2
        SessionsPerWeek = 2
    }
    default = @{
        NumStudents = 120
        NumWeeks = 10
        NumGroups = 3
        AssignmentsPerWeek = 2
        SessionsPerWeek = 2
    }
    large = @{
        NumStudents = 500
        NumWeeks = 12
        NumGroups = 8
        AssignmentsPerWeek = 2
        SessionsPerWeek = 2
    }
    xlarge = @{
        NumStudents = 1500
        NumWeeks = 14
        NumGroups = 16
        AssignmentsPerWeek = 2
        SessionsPerWeek = 2
    }
}

$selected = $presets[$Preset]

Write-Host "Generating synthetic dataset with preset '$Preset' and seed $Seed"
Write-Host "  students: $($selected.NumStudents)"
Write-Host "  weeks: $($selected.NumWeeks)"
Write-Host "  groups: $($selected.NumGroups)"
Write-Host "  assignments/week: $($selected.AssignmentsPerWeek)"
Write-Host "  sessions/week: $($selected.SessionsPerWeek)"

$arguments = @(
    "-m", "src.main",
    "--config", "configs/generator_v1_3_refined.yaml",
    "--seed", "$Seed",
    "--num-students", "$($selected.NumStudents)",
    "--num-weeks", "$($selected.NumWeeks)",
    "--num-groups", "$($selected.NumGroups)",
    "--assignments-per-week", "$($selected.AssignmentsPerWeek)",
    "--sessions-per-week", "$($selected.SessionsPerWeek)"
)

if ($SkipParquet) {
    $arguments += "--skip-parquet"
}

Push-Location $mlRoot
try {
    & python @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Dataset generation failed with exit code $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}
