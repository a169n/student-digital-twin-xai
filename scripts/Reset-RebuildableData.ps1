param(
    [switch]$Apply
)

$ErrorActionPreference = "Stop"

function Get-RepoRoot {
    $scriptDir = Split-Path -Parent $PSCommandPath
    return (Resolve-Path -LiteralPath (Join-Path $scriptDir "..")).Path
}

function Test-IsUnderPath {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Parent
    )
    $normalizedPath = [System.IO.Path]::GetFullPath($Path).TrimEnd(
        [System.IO.Path]::DirectorySeparatorChar,
        [System.IO.Path]::AltDirectorySeparatorChar
    )
    $normalizedParent = [System.IO.Path]::GetFullPath($Parent).TrimEnd(
        [System.IO.Path]::DirectorySeparatorChar,
        [System.IO.Path]::AltDirectorySeparatorChar
    )
    if ($normalizedPath.Equals($normalizedParent, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $true
    }
    $parentWithSeparator = $normalizedParent + [System.IO.Path]::DirectorySeparatorChar
    return $normalizedPath.StartsWith($parentWithSeparator, [System.StringComparison]::OrdinalIgnoreCase)
}

function Assert-SafeDeleteTarget {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$RepoRoot
    )
    $resolved = (Resolve-Path -LiteralPath $Path).Path
    $experimentsRoot = Join-Path $RepoRoot "data\artifacts\experiments"
    if (-not (Test-IsUnderPath -Path $resolved -Parent $RepoRoot)) {
        throw "Refusing to delete outside repository root: $resolved"
    }
    if (Test-IsUnderPath -Path $resolved -Parent $experimentsRoot) {
        throw "Refusing to delete canonical experiment artifacts: $resolved"
    }
    return $resolved
}

function Add-DirectoryChildren {
    param(
        [System.Collections.Generic.List[string]]$Targets,
        [Parameter(Mandatory = $true)][string]$Directory,
        [switch]$KeepGitkeep
    )
    if (-not (Test-Path -LiteralPath $Directory)) {
        return
    }
    Get-ChildItem -LiteralPath $Directory -Force | ForEach-Object {
        if ($KeepGitkeep -and $_.Name -eq ".gitkeep") {
            return
        }
        [void]$Targets.Add($_.FullName)
    }
}

$repoRoot = Get-RepoRoot
$targets = [System.Collections.Generic.List[string]]::new()

Add-DirectoryChildren -Targets $targets -Directory (Join-Path $repoRoot "data\raw") -KeepGitkeep
Add-DirectoryChildren -Targets $targets -Directory (Join-Path $repoRoot "data\processed") -KeepGitkeep
Add-DirectoryChildren -Targets $targets -Directory (Join-Path $repoRoot "data\application")
Add-DirectoryChildren -Targets $targets -Directory (Join-Path $repoRoot "data\artifacts\research_demo")
Add-DirectoryChildren -Targets $targets -Directory (Join-Path $repoRoot "data\artifacts\eda")
Add-DirectoryChildren -Targets $targets -Directory (Join-Path $repoRoot "data\artifacts\reports")

$safeTargets = @()
foreach ($target in $targets) {
    if (Test-Path -LiteralPath $target) {
        $safeTargets += Assert-SafeDeleteTarget -Path $target -RepoRoot $repoRoot
    }
}

if ($safeTargets.Count -eq 0) {
    Write-Host "No rebuildable data targets found."
    exit 0
}

if (-not $Apply) {
    Write-Host "Dry run only. The following rebuildable targets would be removed:"
    $safeTargets | Sort-Object | ForEach-Object { Write-Host "  $_" }
    Write-Host ""
    Write-Host "Rerun with -Apply to delete these targets."
    exit 0
}

Write-Host "Removing rebuildable data targets:"
$safeTargets | Sort-Object | ForEach-Object {
    Write-Host "  $_"
    Remove-Item -LiteralPath $_ -Recurse -Force
}
Write-Host "Done. Canonical data/artifacts/experiments outputs were preserved."
