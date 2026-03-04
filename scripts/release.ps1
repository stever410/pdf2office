# Release helper script for PDF2Office (Windows)
# Usage: .\scripts\release.ps1 [version]
# Example: .\scripts\release.ps1 1.1.0

param(
    [Parameter(Mandatory=$true)]
    [string]$Version
)

$ErrorActionPreference = "Stop"

Set-Location (Join-Path $PSScriptRoot "..")

# Validate version format (semantic versioning)
if ($Version -notmatch '^\d+\.\d+\.\d+$') {
    Write-Host "Error: Invalid version format" -ForegroundColor Red
    Write-Host "Version must be in format: MAJOR.MINOR.PATCH (e.g., 1.0.0)"
    exit 1
}

$newVersion = $Version

# Get current version from metadata
$currentVersion = python -c "from pdf2office.metadata import APP_VERSION; print(APP_VERSION)"

Write-Host ""
Write-Host "PDF2Office Release Helper" -ForegroundColor Blue
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Host "Current version: " -NoNewline
Write-Host $currentVersion -ForegroundColor Yellow
Write-Host "New version:     " -NoNewline
Write-Host $newVersion -ForegroundColor Green
Write-Host ""

# Check if there are uncommitted changes
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "⚠  Warning: You have uncommitted changes" -ForegroundColor Yellow
    git status --short
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne 'y' -and $continue -ne 'Y') {
        Write-Host "Aborted."
        exit 1
    }
}

# Check if tag already exists
$tagExists = git rev-parse "v$newVersion" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Error: Tag v$newVersion already exists" -ForegroundColor Red
    exit 1
}
$Error.Clear()
$LASTEXITCODE = 0

# Confirm before proceeding
Write-Host "This will:"
Write-Host "  1. Update APP_VERSION in metadata.py"
Write-Host "  2. Commit the change"
Write-Host "  3. Create and push tag v$newVersion"
Write-Host "  4. Trigger GitHub Actions to build and release"
Write-Host ""
$confirm = Read-Host "Proceed? (y/N)"
if ($confirm -ne 'y' -and $confirm -ne 'Y') {
    Write-Host "Aborted."
    exit 1
}

# Update version in metadata.py
Write-Host "[1/4] " -NoNewline -ForegroundColor Blue
Write-Host "Updating version in metadata.py..."
$metadataPath = "pdf2office\metadata.py"
$content = Get-Content $metadataPath -Raw
$content = $content -replace 'APP_VERSION = ".*"', "APP_VERSION = `"$newVersion`""
Set-Content -Path $metadataPath -Value $content -NoNewline

# Verify the change
$updatedVersion = python -c "from pdf2office.metadata import APP_VERSION; print(APP_VERSION)"
if ($updatedVersion -ne $newVersion) {
    Write-Host "Error: Version update failed" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Version updated to $newVersion" -ForegroundColor Green

# Commit the change
Write-Host "[2/4] " -NoNewline -ForegroundColor Blue
Write-Host "Committing version bump..."
git add pdf2office\metadata.py
git commit -m "Bump version to v$newVersion"
Write-Host "✓ Committed" -ForegroundColor Green

# Create tag
Write-Host "[3/4] " -NoNewline -ForegroundColor Blue
Write-Host "Creating tag v$newVersion..."
git tag -a "v$newVersion" -m "Release v$newVersion"
Write-Host "✓ Tag created" -ForegroundColor Green

# Push to GitHub
Write-Host "[4/4] " -NoNewline -ForegroundColor Blue
Write-Host "Pushing to GitHub..."
git push origin main
git push origin "v$newVersion"
Write-Host "✓ Pushed to GitHub" -ForegroundColor Green

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host "✓ Release process initiated!" -ForegroundColor Green
Write-Host ""
Write-Host "GitHub Actions is now building the release."
Write-Host "Monitor progress at:"
Write-Host "https://github.com/stever410/pdf2office/actions" -ForegroundColor Blue
Write-Host ""
Write-Host "Release will be available at:"
Write-Host "https://github.com/stever410/pdf2office/releases/tag/v$newVersion" -ForegroundColor Blue
Write-Host ""
Write-Host "This typically takes 5-15 minutes."
