# Product Requirements Document
## pdf2office Tool — Generic PDF Table Converter

**Version:** 2.0
**Date:** 2026-03-04
**Author:** Internal

---

## Implementation Status

| Feature | Status |
|---------|--------|
| Vietnamese price-list PDF → Excel/Word | ✅ Implemented (v1) |
| Generic PDF support (any column structure) | 🔲 Planned (v2) |
| Column Mapping Dialog | 🔲 Planned (v2) |
| Heuristic auto-detect for any PDF | 🔲 Planned (v2) |
| Ollama AI column detection | 🔲 Planned (v2) |
| Ollama Setup Wizard | 🔲 Planned (v2) |

> **Current state:** `pdf2office_tool.py` is v1 — it only works correctly with Vietnamese price-list PDFs that match a hardcoded 3-column structure (code / name / price). Loading any other PDF will likely produce incorrect or empty output. All v2 features below are requirements for the upcoming rewrite.

---

## 1. Overview

A desktop GUI application that converts tabular PDF data into formatted Excel and Word documents. Originally built for Vietnamese medical/dental price lists, v2 is reusable for **any text-based PDF containing tables** — invoices, catalogs, specs, etc. An optional local LLM (Ollama) can auto-detect column roles; the base app works fully without it.

---

## 2. Problem Statement

Sales staff receive product price lists as PDFs (e.g., Innovative Biomedical). These are difficult to filter, search, or embed in proposals. The v1 tool solved this for one specific Vietnamese format; v2 generalises to arbitrary tabular PDFs while adding AI-assisted column mapping.

---

## 3. Goals

| # | Goal |
|---|------|
| G1 | Load any text-based PDF and extract raw tabular data |
| G2 | Let the user map columns (ID, Name, Value, Group) via a dialog |
| G3 | Optionally use a local LLM (Ollama) to auto-suggest column mapping |
| G4 | Preview mapped data in interactive tabs with real-time search/filter |
| G5 | Export to Excel (.xlsx) and/or Word (.docx) |
| G6 | Auto-save beside the source PDF on load; manual Save As option |
| G7 | Provide guided Ollama install/setup within the app |

---

## 4. Non-Goals

- No cloud sync or remote access
- No PDF editing or annotation
- No support for image-only / scanned PDFs (text-based only)
- No multi-language UI (Vietnamese labels preserved for legacy workflow)
- No cloud LLM — Ollama local only

---

## 5. Users

- **Primary:** Sales staff at medical/dental supply companies
- **Secondary:** Office admins preparing client quotations
- **Extended (v2):** Any user needing to convert structured PDF tables to Excel/Word

---

## 6. Functional Requirements

### 6.1 PDF Loading
- FR-1: User selects a PDF via file dialog (Browse button)
- FR-2: `RawTableExtractor` extracts all tables from the PDF as raw 2D string lists using `pdfplumber`
- FR-3: Tables spanning multiple pages with matching headers are merged automatically
- FR-4: After extraction, `ColumnMappingDialog` opens for the user to map columns

### 6.2 Column Mapping
- FR-5: `ColumnMappingDialog` (modal) shows a preview of the first 8 rows and Comboboxes to assign each column a role: ID, Name, Value, Group-by, or Ignore
- FR-6: Heuristic auto-detect pre-populates the Comboboxes using header keyword matching (no LLM required)
- FR-7: "AI Detect" button sends headers + 5 sample rows to Ollama and fills Comboboxes with the suggested mapping
- FR-8: Live preview Treeview updates on every Combobox change

### 6.3 Preview Tabs
- FR-11: "Products" tab shows a Treeview table with column headers from the mapping
- FR-12: "Groups/Sets" tab shows group rows (bold, dark background) with indented child items
- FR-13: Both tabs populate automatically after mapping is applied

### 6.4 Search & Filter
- FR-14: Search bar filters the active tab in real-time
- FR-15: Match on ID OR Name (case-insensitive, partial match)
- FR-16: Clear button resets the filter

### 6.5 Export
- FR-17: Format selector: Excel / Word / Both (radio buttons)
- FR-18: On mapping confirmation, auto-export is triggered to the same directory as the PDF
- FR-19: Auto-saved paths are shown in the status bar
- FR-20: Export button re-exports to the same auto-save paths
- FR-21: Save As… opens file dialog(s) for each selected format

### 6.6 Excel Output (.xlsx)
- FR-22: Sheet 1 — flat item list, teal header, alternating row shading, numeric value format `#,##0`
- FR-23: Sheet 2 — dark group header rows, indented item rows

### 6.7 Word Output (.docx)
- FR-24: A4 landscape orientation
- FR-25: Section 1 — 3-column table, teal header row, alternating row shading
- FR-26: Section 2 on new page — dark group headers, indented child rows

### 6.8 Ollama Integration
- FR-27: `OllamaClient` calls `http://localhost:11434` using stdlib `urllib.request` only (no `requests` dependency)
- FR-28: Model: `llama3.2:3b`; prompt uses Ollama's `format: "json"` mode
- FR-29: If Ollama is unavailable, "AI Detect" is disabled and the app remains fully functional
- FR-30: If Ollama is installed but not running, a "Start Ollama" button calls `subprocess.Popen(["ollama", "serve"])`
- FR-31: If model is not pulled, the app offers to pull it with a progress bar

### 6.9 Ollama Setup Wizard
- FR-32: `Help > Ollama Setup…` opens `OllamaInstallDialog`
- FR-33: Dialog shows platform-specific install command (brew / winget / curl), copyable via tkinter clipboard
- FR-34: Dialog shows step-by-step: Install → Pull model → Start service
- FR-35: Status indicators (green/red dots) refresh every 2s

---

## 7. Non-Functional Requirements

- NF-1: Single-file delivery (`pdf2office_tool.py`) — no project structure needed
- NF-2: Runs on macOS, Windows, Linux with Python 3.9+
- NF-3: On startup, check for missing dependencies and show install command if absent
- NF-4: UI must render Vietnamese characters correctly (UTF-8 throughout)
- NF-5: Search filter response < 100ms for up to 500 rows
- NF-6: No new pip dependencies beyond v1 (`pdfplumber`, `openpyxl`, `python-docx`); Ollama via stdlib only

---

## 8. UI Layout

```
┌──────────────────────────────────────────────────────────────────┐
│ [PDF: ________________________] [Browse]  [Remap Columns…]  [●]  │
├──────────────────────────────────────────────────────────────────┤
│ Search: [___________________] [Clear]  Format: ◉Excel ○Word ○Both │  AI: ● ready
├──────────────────────────────────────────────────────────────────┤
│  Tab: [Products] [Groups]                                        │
│  ┌────────────────────────────────────────────────────────┐      │
│  │ <id_label>  │ <name_label>              │ <value_label>│      │
│  │ ...         │ ...                       │ ...          │      │
│  └────────────────────────────────────────────────────────┘      │
├──────────────────────────────────────────────────────────────────┤
│ Auto-saved: file.xlsx | file.docx    [Export] [Save As…]        │
└──────────────────────────────────────────────────────────────────┘

Menu: Help > Ollama Setup…
```

### Column Mapping Dialog

```
┌─ Map Columns ───────────────────────────────────────────────────┐
│  [AI Detect (Ollama)]  Status: "AI: ready" / "AI: offline"      │
│  ─────────────────────────────────────────────────────────────  │
│  Header row index:  [Spinbox 0-5]                               │
│  ID / Code column:  [Combobox: (none) | Col 0: "STT" | …]     │
│  Name column:       [Combobox: (required) Col 1: "Product" | …]│
│  Value column:      [Combobox: (none) | Col 2: "Price" | …]    │
│  Group-by column:   [Combobox: (none) | Col 3: "Category" | …] │
│  ─────────────────────────────────────────────────────────────  │
│  Preview (first 8 rows):                                        │
│  │ ID      │ Name                    │ Value        │           │
│  ─────────────────────────────────────────────────────────────  │
│  [AI reasoning — hidden until AI Detect clicked]                │
│                              [Cancel]  [Apply Mapping]          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. Technical Architecture

| Component | Class | Responsibility |
|-----------|-------|----------------|
| Raw extraction | `RawTableExtractor` | Extract all tables from PDF as raw 2D string lists |
| Data model | `ColumnMapping` (dataclass) | Column index → role mapping (id, name, value, group) |
| Structured parsing | `GenericParser` | Apply `ColumnMapping` to raw rows → `(products, sets)` |
| Legacy fallback | `_LegacyAutoDetect` | Vietnamese keyword-based detection (renamed from `PdfParser`) |
| Excel export | `ExcelExporter` | Write formatted `.xlsx` with two sheets |
| Word export | `WordExporter` | Write formatted `.docx` with two sections |
| Column mapping UI | `ColumnMappingDialog` | Modal dialog: Comboboxes + live preview + AI Detect button |
| LLM client | `OllamaClient` | REST calls to Ollama API via `urllib.request` |
| LLM install helper | `OllamaInstallHelper` | Platform detection + install instructions |
| Install wizard UI | `OllamaInstallDialog` | Step-by-step Ollama setup (install, pull, serve) |
| GUI | `App(tk.Tk)` | Main window, tabs, search, export controls, menubar |

### 9.1 Data Shapes

```python
# ColumnMapping (dataclass)
id_col: int | None       # column index for ID/code
name_col: int            # column index for name (required)
value_col: int | None    # column index for numeric value
extra_cols: list[int]    # additional pass-through columns
header_row: int          # row index to skip (usually 0)
grouping_col: int | None # rows with empty value become group headers
raw_headers: list[str]   # original PDF header strings

# Exporter inputs (unchanged from v1)
products: list[tuple[str, str, int]]  # (code, name, price_int)
sets:     list[dict]                  # {name, price, items: [(code, name)]}
```

### 9.2 Dependencies

| Library | Purpose | Install |
|---------|---------|---------|
| `tkinter` | GUI | Built-in |
| `ttk` | Styled widgets | Built-in |
| `urllib.request` | Ollama API calls | Built-in |
| `pdfplumber` | PDF table extraction | `pip install pdfplumber` |
| `openpyxl` | Excel file creation | `pip install openpyxl` |
| `python-docx` | Word file creation | `pip install python-docx` |
| Ollama | Local LLM runtime | Optional — `ollama.com/download` |

### 9.3 Ollama API

```
GET  http://localhost:11434/api/tags       → availability / installed models
POST http://localhost:11434/api/generate  → column mapping suggestion
     { model: "llama3.2:3b", format: "json", stream: false, prompt: "..." }
```

---

## 10. Acceptance Criteria

| # | Test | Pass Condition |
|---|------|----------------|
| AC-1 | Run `python3 pdf2office_tool.py` | Window opens, menubar shows `Help > Ollama Setup…` |
| AC-2 | Browse → select Innovative Biomedical PDF | `ColumnMappingDialog` opens with correct column headers |
| AC-3 | Apply mapping (id=col0, name=col1, value=col2) | ~196 products in Products tab |
| AC-4 | Check Groups tab | 3 sets with child items |
| AC-5 | Type "xoang" in search | Only matching rows visible |
| AC-6 | Select "Both" → load PDF | `.xlsx` and `.docx` auto-saved beside PDF |
| AC-7 | Select "Word" → Save As… | `.docx` saved to chosen path |
| AC-8 | Select "Excel" → Save As… | `.xlsx` saved to chosen path |
| AC-9 | Open `.xlsx` | Two sheets with correct formatting |
| AC-10 | Open `.docx` | A4 landscape, two sections, correct formatting |
| AC-11 | Missing dep on startup | Clear error message with `pip install` command |
| AC-12 | Load PDF with Ollama running | "AI Detect" enabled; clicking it populates Comboboxes |
| AC-13 | Load PDF without Ollama | "AI Detect" disabled; mapping and export work normally |
| AC-14 | `Help > Ollama Setup…` | Dialog opens, shows correct platform install command |
| AC-15 | Load a non-Vietnamese PDF | Heuristic auto-detect identifies columns; export works |

---

## 11. Delivery

- **File:** `/Users/ducngo/Documents/personal/pdf2office_tool.py`
- **Single file**, no external config, no database
- Self-contained: dependency check on startup
