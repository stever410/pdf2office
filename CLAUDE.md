# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## App Name

**PDF2Office** — a PDF table to Excel/Word converter with Vietnamese/English UI.

App metadata (name, version, author) lives in `pdf2office/metadata.py`:
```python
APP_NAME    = "PDF2Office"
APP_VERSION = "1.0.0"
APP_BUILD_BY = "stever410"
APP_GITHUB_REPO = "owner/repo"
APP_TITLE   = f"{APP_NAME} v{APP_VERSION} | build by {APP_BUILD_BY}"
```
`APP_TITLE` is imported by `main_app.py` and set as the window title. Update version/author there, not in the UI code.
`APP_GITHUB_REPO` powers in-app update checks (GitHub Releases API).

## Running the App

```bash
python3 pdf2office.py
```

Install dependencies first:
```bash
pip install pdfplumber openpyxl python-docx
```

The app performs a dependency check on startup and exits with install instructions if any are missing.

## Architecture

Multi-file package under `pdf2office/`. Entry point is `pdf2office.py`.

**Data flow:**
```
PDF file → PDFExtractor.extract() → list of raw tables
         → ExcelExporter / WordExporter → .xlsx / .docx
```

**Package structure:**

```
pdf2office/
  metadata.py          — APP_NAME, APP_VERSION, APP_TITLE constants
  bootstrap.py         — dependency check
  core/
    extractors.py      — PDFExtractor (pdfplumber), returns list[list[list[str]]]
  exporters/
    excel_exporter.py  — writes .xlsx (one sheet per table)
    word_exporter.py   — writes .docx (A4 landscape, one Word table per PDF table)
    theme.py           — color/style constants (unused by current exporters, kept for reference)
  ui/
    main_app.py        — App(tk.Tk) main window
```

**Key classes:**

- **`PDFExtractor`** — uses `pdfplumber` to extract all tables from a PDF, preserving table boundaries. Returns `list[list[list[str]]]` (list of tables → rows → cells).

- **`ExcelExporter`** — takes raw tables and writes one sheet per table to `.xlsx`. First row of each table is styled as a header (teal background).

- **`WordExporter`** — takes raw tables and writes each as a Word table in A4-landscape `.docx`. First row styled as teal header.

- **`App(tk.Tk)`** — simple tkinter window. User picks a PDF, chooses Excel or Word, clicks Convert, picks a save location. All UI text is in Vietnamese.

**Key data shape:**
```python
tables: list[list[list[str]]]  # tables → rows → cells
```

Both exporters consume this same shape.

## Internationalisation

`pdf2office/i18n.py` holds all UI strings for Vietnamese (`"vn"`) and English (`"en"`) in a `STRINGS` dict. `detect_lang()` reads `locale.getdefaultlocale()` and returns `"vn"` for Vietnamese locales, otherwise `"en"`.

`App` in `main_app.py` stores `self._lang` (initialised from `detect_lang()`) and uses `self._s(key)` to look up `STRINGS[self._lang][key]`. A **Language** menu in the menu bar lets the user switch at runtime; `_switch_lang(lang)` updates `self._lang` and calls `_apply_lang()` which patches all widget labels in-place.

To add a new string, add it to both `"vn"` and `"en"` in `STRINGS` and reference it via `self._s("your_key")`. Do not hard-code any display text in `main_app.py`.

## Settings

No settings persistence. Each session starts fresh.
