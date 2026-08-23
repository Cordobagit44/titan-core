[CmdletBinding()]
param(
    [string]$Remote = "origin",
    [string]$Branch = "main",
    [switch]$RunChecks
)

$ErrorActionPreference = "Stop"

function Stop-Sync {
    param([string]$Message)

    Write-Host ""
    Write-Host "TITAN sync stopped: $Message" -ForegroundColor Yellow
    exit 1
}

function Invoke-CheckedCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Command,
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "'$Command $($Arguments -join ' ')' failed with exit code $LASTEXITCODE."
    }
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Stop-Sync "Git is not available in this terminal."
}

$repositoryRoot = (& git rev-parse --show-toplevel 2>$null)
if ($LASTEXITCODE -ne 0 -or -not $repositoryRoot) {
    Stop-Sync "the current folder is not inside a Git repository."
}

Push-Location $repositoryRoot.Trim()
try {
    $pendingChanges = @(& git status --porcelain --untracked-files=all)
    if ($LASTEXITCODE -ne 0) {
        Stop-Sync "Git could not inspect the working tree."
    }
    if ($pendingChanges.Count -gt 0) {
        Write-Host "Local changes found:" -ForegroundColor Yellow
        $pendingChanges | ForEach-Object { Write-Host "  $_" }
        Stop-Sync "commit, stash, or discard these changes before synchronizing."
    }

    $currentBranch = (& git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $currentBranch) {
        Stop-Sync "the repository is in detached HEAD state."
    }
    if ($currentBranch -ne $Branch) {
        Stop-Sync "switch to '$Branch' first. Current branch: '$currentBranch'."
    }

    & git remote get-url $Remote *> $null
    if ($LASTEXITCODE -ne 0) {
        Stop-Sync "remote '$Remote' is not configured."
    }

    Write-Host "Fetching $Remote/$Branch..." -ForegroundColor Cyan
    Invoke-CheckedCommand git fetch --prune $Remote $Branch

    $remoteRef = "$Remote/$Branch"
    & git rev-parse --verify $remoteRef *> $null
    if ($LASTEXITCODE -ne 0) {
        Stop-Sync "remote branch '$remoteRef' was not found after fetch."
    }

    $counts = ((& git rev-list --left-right --count "HEAD...$remoteRef") -split "\s+")
    if ($LASTEXITCODE -ne 0 -or $counts.Count -ne 2) {
        Stop-Sync "Git could not compare the local and remote branches."
    }

    $localAhead = [int]$counts[0]
    $remoteAhead = [int]$counts[1]

    if ($localAhead -gt 0) {
        Stop-Sync "local '$Branch' has $localAhead commit(s) not present on '$remoteRef'. Review them manually."
    }

    if ($remoteAhead -gt 0) {
        Write-Host "Applying $remoteAhead remote commit(s) with fast-forward only..." -ForegroundColor Cyan
        Invoke-CheckedCommand git merge --ff-only $remoteRef
    }
    else {
        Write-Host "Local '$Branch' is already current." -ForegroundColor Green
    }

    if ($RunChecks) {
        if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
            Stop-Sync "uv is required for validation but is not available in this terminal."
        }

        Write-Host "Running TITAN quality gates..." -ForegroundColor Cyan
        Invoke-CheckedCommand uv sync --frozen
        Invoke-CheckedCommand uv run ruff check .
        Invoke-CheckedCommand uv run ruff format --check .
        Invoke-CheckedCommand uv run mypy
        Invoke-CheckedCommand uv run pytest
    }

    Write-Host ""
    Write-Host "TITAN synchronization completed safely." -ForegroundColor Green
}
finally {
    Pop-Location
}
