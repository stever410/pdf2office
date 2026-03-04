# GitHub Automation

This directory contains GitHub Actions workflows and documentation for automated builds and releases.

## Files

### Workflows

- **[`workflows/release.yml`](workflows/release.yml)** - Automated release workflow  
  Builds Windows, macOS, and Linux binaries and creates a GitHub Release when you push a version tag.

- **[`workflows/ci.yml`](workflows/ci.yml)** - Continuous integration workflow  
  Tests builds on all platforms for every push and pull request.

### Documentation

- **[`WORKFLOWS.md`](WORKFLOWS.md)** - Complete guide  
  Detailed documentation on how to use the workflows, create releases, and troubleshoot issues.

## Quick Start

### Create a Release

**Using the helper script:**
```bash
# macOS/Linux
./scripts/release.sh 1.1.0

# Windows
.\scripts\release.ps1 1.1.0
```

**Manual:**
```bash
git tag v1.1.0
git push origin v1.1.0
```

The GitHub Actions workflow will automatically build and publish the release.

### View Status

- **Actions**: https://github.com/stever410/pdf2office/actions
- **Releases**: https://github.com/stever410/pdf2office/releases

## What Gets Built

Each release includes:
- Windows: `PDF2Office-v{version}-windows.zip` (contains .exe)
- macOS: `PDF2Office-v{version}-macos.zip` (contains .app)
- Linux: `PDF2Office-v{version}-linux.tar.gz` (contains binary)

Build time: 5-15 minutes

## More Information

See [WORKFLOWS.md](WORKFLOWS.md) for complete documentation.
