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

### Workflows

- **Release Workflow**: `.github/workflows/release.yml` - Builds and publishes releases
- **CI Workflow**: `.github/workflows/ci.yml` - Continuous integration testing

### Release Artifact Naming

- `PDF2Office-v{version}-windows.zip` - Windows executable
- `PDF2Office-v{version}-macos.zip` - macOS app bundle
- `PDF2Office-v{version}-linux.tar.gz` - Linux binary

### Creating a Release

#### Quick Release (using helper script)

**macOS/Linux:**
```bash
./scripts/release.sh 1.1.0
```

**Windows:**
```powershell
.\scripts\release.ps1 1.1.0
```

This script will:
1. Update `APP_VERSION` in `metadata.py`
2. Commit the change
3. Create and push tag `v1.1.0`
4. Trigger GitHub Actions to build and release

#### Manual Release

1. Update `APP_VERSION` in `pdf2office/metadata.py`
2. Commit: `git commit -am "Bump version to v1.1.0"`
3. Create tag: `git tag v1.1.0`
4. Push: `git push origin main && git push origin v1.1.0`

When pushing a tag like `v1.0.0`, the workflow automatically:
- Builds for Windows, macOS, and Linux
- Creates a GitHub Release with all binaries
- Uploads zipped platform bundles as release assets

See [.github/WORKFLOWS.md](.github/WORKFLOWS.md) for detailed documentation.

## 5. In-app auto-update (GitHub Releases)

The app can check `releases/latest` and download the best matching asset for the current OS.

1. Set `APP_GITHUB_REPO` in `pdf2office/metadata.py` to your GitHub repo in `owner/repo` format.
2. Keep release tags in `vX.Y.Z` format (example: `v1.1.0`).
3. Attach installable assets to each GitHub release (for example `.exe`, `.dmg`, `.deb`, or `.zip` bundles named with `windows`, `macos`, or `linux`).

In the app:
- `Help > Check for Updates…` runs a manual check.
- If `AUTO_UPDATE_CHECK_ON_STARTUP = True`, it also checks silently after launch.
