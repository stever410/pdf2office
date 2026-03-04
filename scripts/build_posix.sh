#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

APP_ID="$(python3 -c 'from pdf2office.metadata import APP_ID; print(APP_ID)')"
APP_VERSION="$(python3 -c 'from pdf2office.metadata import APP_VERSION; print(APP_VERSION)')"
APP_BUILD_BY="$(python3 -c 'from pdf2office.metadata import APP_BUILD_BY; print(APP_BUILD_BY)')"

echo "[1/3] Installing build dependencies..."
python3 -m pip install -r requirements-build.txt

echo "[2/3] Building ${APP_ID} v${APP_VERSION} (build by ${APP_BUILD_BY})..."
python3 -m PyInstaller --noconfirm pdf2office.spec

echo "[3/3] Build complete."
case "$(uname -s)" in
  Darwin)
    echo "Output: dist/${APP_ID}.app"
    ;;
  Linux)
    echo "Output: dist/${APP_ID}/${APP_ID}"
    ;;
  *)
    echo "Output: dist/${APP_ID}"
    ;;
esac
