$ErrorActionPreference = "Stop"

Set-Location (Join-Path $PSScriptRoot "..")

$appId = python -c "from pdf2office.metadata import APP_ID; print(APP_ID)"
$appVersion = python -c "from pdf2office.metadata import APP_VERSION; print(APP_VERSION)"
$appBuildBy = python -c "from pdf2office.metadata import APP_BUILD_BY; print(APP_BUILD_BY)"

Write-Host "[1/3] Installing build dependencies..."
python -m pip install -r requirements-build.txt

Write-Host "[2/3] Building $appId v$appVersion (build by $appBuildBy)..."
python -m PyInstaller --noconfirm pdf2office.spec

Write-Host "[3/3] Build complete."
Write-Host "Output: dist/$appId/$appId.exe"
