# End-User Build Guide (Windows, macOS, Linux)

This project is a desktop app (`tkinter`).

- App name: `PDF2Office`
- Version: `1.0.0`
- Build by: `stever410`

## Important

- Build on each target OS (no reliable cross-compiling for this app stack).
- Build outputs are platform-specific and not interchangeable.

## 1. Prerequisites

- Python 3.10+ in `PATH`
- `pip` available

## 2. Build commands

### Windows

```bat
scripts\build_windows.bat
```

or

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows.ps1
```

### macOS

```bash
./scripts/build_macos.sh
```

### Linux

```bash
./scripts/build_linux.sh
```

## 3. Build outputs

- Windows: `dist\PDF2Office\PDF2Office.exe`
- macOS: `dist/PDF2Office.app`
- Linux: `dist/PDF2Office/PDF2Office`

Ship:
- Windows/Linux: whole `dist/PDF2Office` folder
- macOS: `dist/PDF2Office.app`

## 4. Automated multi-platform builds (GitHub Actions)

Workflow:
- `.github/workflows/build-release-artifacts.yml`

Artifact naming format:
- `PDF2Office-v1.0.0-windows`
- `PDF2Office-v1.0.0-macos`
- `PDF2Office-v1.0.0-linux`

When pushing a tag like `v1.0.0`, the workflow now also uploads zipped platform bundles to the GitHub Release automatically.

## 5. In-app auto-update (GitHub Releases)

The app can check `releases/latest` and download the best matching asset for the current OS.

1. Set `APP_GITHUB_REPO` in `pdf2office/metadata.py` to your GitHub repo in `owner/repo` format.
2. Keep release tags in `vX.Y.Z` format (example: `v1.1.0`).
3. Attach installable assets to each GitHub release (for example `.exe`, `.dmg`, `.deb`, or `.zip` bundles named with `windows`, `macos`, or `linux`).

In the app:
- `Help > Check for Updates…` runs a manual check.
- If `AUTO_UPDATE_CHECK_ON_STARTUP = True`, it also checks silently after launch.
