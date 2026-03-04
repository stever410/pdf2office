# PDF2Office

Desktop app to convert table data from PDF files into Excel (`.xlsx`) or Word (`.docx`).

`PDF2Office` is a cross-platform Tkinter application focused on quick office-friendly export:
- Extracts tables from text-based PDFs with `pdfplumber`
- Exports merged table data to formatted Excel
- Exports tables (or text fallback) to Word
- Supports English and Vietnamese UI
- Can check/download new versions from GitHub Releases

![PDF2Office icon](icon.png)

## Features

- PDF -> Excel (`.xlsx`)
  - Merges tables across pages when headers repeat
  - Applies styled header, autosized columns, and frozen top row
- PDF -> Word (`.docx`)
  - Exports detected tables to a landscape table layout
  - Falls back to extracted page text when no tables are found
- In-app updates
  - `Help > Check for Updates...`
  - Optional startup auto-check via GitHub Releases
- Local desktop UI
  - No cloud requirement for core conversion

## Requirements

- Python `3.10+`
- OS: Windows, macOS, or Linux
- Runtime dependencies:
  - `pdfplumber`
  - `openpyxl`
  - `python-docx`

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run From Source

```bash
python pdf2office.py
```

The app will open a file picker workflow:
1. Choose a PDF.
2. Pick output format (Excel or Word).
3. Save to destination path.

## Build Standalone App

Builds are OS-specific and should be produced on each target OS.

- Windows:
  - `scripts\build_windows.bat`
  - or `powershell -ExecutionPolicy Bypass -File .\scripts\build_windows.ps1`
- macOS:
  - `./scripts/build_macos.sh`
- Linux:
  - `./scripts/build_linux.sh`

Detailed build guide: [BUILD.md](BUILD.md)

## Release Workflow

GitHub Actions workflows are included for CI and tagged releases:
- CI: `.github/workflows/ci.yml`
- Release: `.github/workflows/release.yml`

Create a release by pushing a semantic tag:

```bash
git tag v1.1.0
git push origin v1.1.0
```

Or use helper scripts:
- macOS/Linux: `./scripts/release.sh 1.1.0`
- Windows: `.\scripts\release.ps1 1.1.0`

Workflow docs: [.github/WORKFLOWS.md](.github/WORKFLOWS.md)

## Configuration

App metadata and update settings live in `pdf2office/metadata.py`:

- `APP_VERSION`
- `APP_BUILD_BY`
- `APP_GITHUB_REPO` (format: `owner/repo`)
- `AUTO_UPDATE_CHECK_ON_STARTUP`

Set `APP_GITHUB_REPO` to your repository to enable in-app update checks.

## Known Limitations

- Works best with text-based PDFs (not scanned image-only PDFs).
- Excel export requires detected tables; if no tables are found, Excel export is not produced.
- Word export can fall back to plain extracted text when table detection fails.

## Project Structure

```text
pdf2office/
  core/         # extraction + parsing utilities
  exporters/    # Excel and Word exporters
  services/     # updater/settings services
  ui/           # Tkinter app UI
scripts/        # build and release helper scripts
.github/        # CI/release workflows and docs
```

## License

Apache License 2.0. See [LICENSE](LICENSE).
