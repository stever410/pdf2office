# GitHub Actions Workflow Guide

This repository includes automated GitHub Actions workflows for building and releasing PDF2Office.

## Workflows

### 1. CI Workflow (`.github/workflows/ci.yml`)

**Triggers on:**
- Push to `main` or `develop` branch
- Pull requests to `main` or `develop` branch

**What it does:**
- Tests building on Windows, macOS, and Linux
- Runs code quality checks
- Verifies metadata configuration

**Status:** View build status in the "Actions" tab of your repository.

### 2. Release Workflow (`.github/workflows/release.yml`)

**Triggers on:**
- Pushing a version tag (e.g., `v1.0.0`, `v1.2.3`)
- Manual trigger from GitHub UI (workflow_dispatch)

**What it does:**
- Builds executables for Windows, macOS, and Linux
- Creates a GitHub Release with all binaries
- Uploads artifacts as release assets

## How to Create a Release

### Option 1: Using Version Tags (Recommended)

1. **Update the version** in `pdf2office/metadata.py`:
   ```python
   APP_VERSION = "1.1.0"  # Update this
   ```

2. **Commit and push** your changes:
   ```bash
   git add pdf2office/metadata.py
   git commit -m "Bump version to 1.1.0"
   git push origin main
   ```

3. **Create and push a tag**:
   ```bash
   git tag v1.1.0
   git push origin v1.1.0
   ```

4. **Wait for the workflow** to complete (5-15 minutes). The release will automatically appear in the "Releases" section.

### Option 2: Using GitHub Web Interface

1. Go to your repository on GitHub
2. Click on "Releases" (right sidebar)
3. Click "Draft a new release"
4. Click "Choose a tag" → type `v1.1.0` → click "Create new tag"
5. GitHub will automatically trigger the release workflow

### Option 3: Manual Trigger (Testing)

1. Go to "Actions" tab in your repository
2. Select "Release" workflow
3. Click "Run workflow" dropdown
4. Select branch and click "Run workflow"

This creates a development build without creating a tag or release.

## Release Artifacts

Each release includes three archives:

- **`PDF2Office-v{version}-windows.zip`** - Windows executable
  - Contains `PDF2Office.exe` and dependencies
  
- **`PDF2Office-v{version}-macos.zip`** - macOS application
  - Contains `PDF2Office.app` bundle
  
- **`PDF2Office-v{version}-linux.tar.gz`** - Linux binary
  - Contains `PDF2Office` executable and dependencies

## Auto-Update Feature

The app includes auto-update checking that uses GitHub Releases:

- Configured in `pdf2office/metadata.py`:
  ```python
  APP_GITHUB_REPO = "stever410/pdf2office"
  AUTO_UPDATE_CHECK_ON_STARTUP = True
  ```

- On startup, the app checks the latest release via GitHub API
- Users are notified when a new version is available

## Troubleshooting

### Build fails on a specific platform

Check the workflow logs:
1. Go to "Actions" tab
2. Click on the failed workflow run
3. Click on the failed job (e.g., "Build for Windows")
4. Review the error logs

Common issues:
- Missing dependencies in requirements.txt
- Missing icon.png file
- PyInstaller spec file issues

### Release not created

Ensure:
- Tag format is correct: `v1.2.3` (must start with `v`)
- You have push permissions to the repository
- No duplicate tags exist

### macOS app not opening

Users may need to:
1. Right-click the app and select "Open"
2. Or run: `xattr -cr PDF2Office.app` to remove quarantine attribute

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- `v1.0.0` - Major.Minor.Patch
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes

## Local Testing

To test builds locally before releasing:

**Windows:**
```powershell
.\scripts\build_windows.ps1
```

**macOS/Linux:**
```bash
./scripts/build_posix.sh
```

## Advanced: Customizing the Release

Edit `.github/workflows/release.yml` to:
- Change release notes template
- Add checksums (SHA256)
- Add code signing (requires certificates)
- Modify archive formats
- Add additional platforms

## Security Notes

- GitHub Actions uses `GITHUB_TOKEN` automatically (no setup needed)
- For code signing, add secrets in repository Settings → Secrets
- Never commit private keys or certificates to the repository
