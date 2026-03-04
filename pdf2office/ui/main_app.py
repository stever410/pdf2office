import os
import sys
import threading
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from pdf2office.core.extractors import PDFExtractor
from pdf2office.exporters.excel_exporter import ExcelExporter
from pdf2office.exporters.word_exporter import WordExporter
from pdf2office.i18n import STRINGS, detect_lang
from pdf2office.metadata import (
    APP_GITHUB_REPO,
    APP_NAME,
    APP_TITLE,
    APP_VERSION,
    AUTO_UPDATE_CHECK_ON_STARTUP,
    AUTO_UPDATE_TIMEOUT_SEC,
)
from pdf2office.services.updater import GitHubReleaseUpdater, ReleaseInfo


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self._palette = {
            "bg": "#F3F3F5",
            "surface": "#FFFFFF",
            "surface_alt": "#FAFAFB",
            "text": "#161616",
            "text_muted": "#5E5E66",
            "border": "#D9D9E0",
            "accent": "#FF3B30",
            "accent_hover": "#FF5C53",
            "accent_pressed": "#E3342C",
            "accent_disabled": "#F2A7A3",
            "subtle_hover": "#F0F0F3",
            "subtle_pressed": "#E5E5EA",
            "disabled_text": "#8A8A93",
        }
        self._icon_image: tk.PhotoImage | None = None
        self._icon_image_small: tk.PhotoImage | None = None
        self.title(APP_NAME)
        self.iconname(APP_NAME)
        try:
            self.tk.call("tk", "appname", APP_NAME)
        except tk.TclError:
            pass
        self.resizable(False, False)
        self._configure_theme()
        self._set_app_icon()
        self._pdf_path: str | None = None
        self._lang = detect_lang()
        self._updater = None
        if APP_GITHUB_REPO.strip():
            self._updater = GitHubReleaseUpdater(
                repo=APP_GITHUB_REPO,
                current_version=APP_VERSION,
                timeout_sec=AUTO_UPDATE_TIMEOUT_SEC,
            )
        self._checking_updates = False
        self._downloading_update = False
        self._build_ui()
        if self._updater and AUTO_UPDATE_CHECK_ON_STARTUP:
            self.after(1500, lambda: self._check_for_updates(manual=False))

    # --- i18n helper ---

    def _s(self, key: str, **kwargs) -> str:
        s = STRINGS[self._lang][key]
        return s.format(**kwargs) if kwargs else s

    # --- Build UI ---

    def _configure_theme(self):
        self.configure(bg=self._palette["bg"])
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("App.TFrame", background=self._palette["bg"])
        style.configure("Card.TFrame", background=self._palette["surface"])

        style.configure(
            "Title.TLabel",
            background=self._palette["bg"],
            foreground=self._palette["text"],
            font=("TkDefaultFont", 14, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=self._palette["bg"],
            foreground=self._palette["text_muted"],
        )
        style.configure(
            "App.TLabel",
            background=self._palette["bg"],
            foreground=self._palette["text"],
        )
        style.configure(
            "Status.TLabel",
            background=self._palette["bg"],
            foreground=self._palette["text_muted"],
        )

        style.configure(
            "App.TEntry",
            fieldbackground=self._palette["surface"],
            background=self._palette["surface"],
            foreground=self._palette["text"],
            bordercolor=self._palette["border"],
        )
        style.map(
            "App.TEntry",
            fieldbackground=[("readonly", self._palette["surface"])],
            foreground=[("readonly", self._palette["text"])],
        )

        style.configure(
            "App.TLabelframe",
            background=self._palette["surface_alt"],
            bordercolor=self._palette["border"],
            relief="solid",
        )
        style.configure(
            "App.TLabelframe.Label",
            background=self._palette["surface_alt"],
            foreground=self._palette["text"],
            font=("TkDefaultFont", 10, "bold"),
        )

        style.configure(
            "App.TRadiobutton",
            background=self._palette["surface_alt"],
            foreground=self._palette["text"],
        )

        style.configure(
            "App.TButton",
            background=self._palette["surface"],
            foreground=self._palette["text"],
            bordercolor=self._palette["border"],
            padding=(10, 5),
        )
        style.map(
            "App.TButton",
            background=[
                ("active", self._palette["subtle_hover"]),
                ("pressed", self._palette["subtle_pressed"]),
            ],
            foreground=[("disabled", self._palette["disabled_text"])],
        )

        style.configure(
            "Accent.TButton",
            background=self._palette["accent"],
            foreground="#FFFFFF",
            padding=(16, 7),
            borderwidth=0,
        )
        style.map(
            "Accent.TButton",
            background=[
                ("disabled", self._palette["accent_disabled"]),
                ("pressed", self._palette["accent_pressed"]),
                ("active", self._palette["accent_hover"]),
            ],
            foreground=[("disabled", "#FFFFFF")],
        )

    @staticmethod
    def _resource_path(name: str) -> Path:
        bundle_root = getattr(sys, "_MEIPASS", None)
        if bundle_root:
            return Path(bundle_root) / name
        return Path(__file__).resolve().parents[2] / name

    def _set_app_icon(self):
        icon_path = self._resource_path("icon.png")
        if not icon_path.exists():
            return
        try:
            self._icon_image = tk.PhotoImage(file=str(icon_path))
            self.iconphoto(True, self._icon_image)

            target_px = 44
            scale_x = max(1, self._icon_image.width() // target_px)
            scale_y = max(1, self._icon_image.height() // target_px)
            self._icon_image_small = self._icon_image.subsample(scale_x, scale_y)
        except tk.TclError:
            self._icon_image = None
            self._icon_image_small = None

    def _build_ui(self):
        self._build_menu()

        root = ttk.Frame(self, padding=20, style="App.TFrame")
        root.pack(fill="both", expand=True)

        header = ttk.Frame(root, style="App.TFrame")
        header.pack(fill="x", pady=(0, 14))

        if self._icon_image_small:
            ttk.Label(header, image=self._icon_image_small, style="App.TLabel").pack(
                side="left", padx=(0, 10)
            )

        title_wrap = ttk.Frame(header, style="App.TFrame")
        title_wrap.pack(side="left", fill="x", expand=True)
        ttk.Label(title_wrap, text=APP_TITLE, style="Title.TLabel").pack(anchor="w")
        ttk.Label(title_wrap, text=f"v{APP_VERSION}", style="Subtitle.TLabel").pack(anchor="w")

        # File row
        file_frame = ttk.Frame(root, style="App.TFrame")
        file_frame.pack(fill="x", pady=(0, 12))

        self._file_label = ttk.Label(file_frame, text=self._s("file_label"), style="App.TLabel")
        self._file_label.pack(side="left")
        self._path_var = tk.StringVar()
        ttk.Entry(
            file_frame,
            textvariable=self._path_var,
            width=52,
            state="readonly",
            style="App.TEntry",
        ).pack(
            side="left", padx=(6, 6)
        )
        self._browse_btn = ttk.Button(
            file_frame,
            text=self._s("browse_btn"),
            command=self._browse,
            style="App.TButton",
        )
        self._browse_btn.pack(side="left")

        # Format
        self._fmt_frame = ttk.LabelFrame(
            root, text=self._s("format_label"), padding=(12, 6), style="App.TLabelframe"
        )
        self._fmt_frame.pack(fill="x", pady=(0, 12))

        self._fmt_var = tk.StringVar(value="excel")
        ttk.Radiobutton(
            self._fmt_frame,
            text="Excel (.xlsx)",
            variable=self._fmt_var,
            value="excel",
            style="App.TRadiobutton",
        ).pack(side="left", padx=(0, 16))
        ttk.Radiobutton(
            self._fmt_frame,
            text="Word (.docx)",
            variable=self._fmt_var,
            value="word",
            style="App.TRadiobutton",
        ).pack(side="left")

        # Convert button
        self._convert_btn = ttk.Button(
            root,
            text=self._s("convert_btn"),
            command=self._convert,
            state="disabled",
            style="Accent.TButton",
        )
        self._convert_btn.pack(pady=(0, 10))

        # Status
        self._status_var = tk.StringVar(value=self._s("status_initial"))
        ttk.Label(root, textvariable=self._status_var, wraplength=440, style="Status.TLabel").pack()

    def _build_menu(self):
        menubar = tk.Menu(self)

        self._lang_menu = tk.Menu(menubar, tearoff=False)
        self._lang_var = tk.StringVar(value=self._lang)
        self._lang_menu.add_radiobutton(
            label="Tiếng Việt", variable=self._lang_var, value="vn",
            command=lambda: self._switch_lang("vn"),
        )
        self._lang_menu.add_radiobutton(
            label="English", variable=self._lang_var, value="en",
            command=lambda: self._switch_lang("en"),
        )

        menubar.add_cascade(label=self._s("menu_language"), menu=self._lang_menu)
        self._menu_index_language = menubar.index("end")

        self._help_menu = tk.Menu(menubar, tearoff=False)
        self._help_menu.add_command(
            label=self._s("menu_check_updates"),
            command=self._check_for_updates_manual,
        )
        menubar.add_cascade(label=self._s("menu_help"), menu=self._help_menu)
        self._menu_index_help = menubar.index("end")

        self.config(menu=menubar)
        self._menubar = menubar

    # --- Language switch ---

    def _switch_lang(self, lang: str):
        if lang == self._lang:
            return
        self._lang = lang
        self._apply_lang()

    def _apply_lang(self):
        # Menu
        self._menubar.entryconfig(self._menu_index_language, label=self._s("menu_language"))
        self._menubar.entryconfig(self._menu_index_help, label=self._s("menu_help"))
        self._help_menu.entryconfig(0, label=self._s("menu_check_updates"))
        # Widgets
        self._file_label.config(text=self._s("file_label"))
        self._browse_btn.config(text=self._s("browse_btn"))
        self._fmt_frame.config(text=self._s("format_label"))
        self._convert_btn.config(text=self._s("convert_btn"))
        # Status — only update non-transient messages
        current = self._status_var.get()
        for key in ("status_initial", "status_ready"):
            for other_lang in STRINGS:
                if current == STRINGS[other_lang][key]:
                    self._status_var.set(self._s(key))
                    return

    def _check_for_updates_manual(self):
        self._check_for_updates(manual=True)

    def _check_for_updates(self, manual: bool):
        if self._checking_updates or self._downloading_update:
            return
        if not self._updater:
            if manual:
                messagebox.showinfo(self._s("updates_title"), self._s("updates_not_configured"))
            return

        self._checking_updates = True
        if manual:
            self._status_var.set(self._s("status_checking_updates"))

        def run():
            try:
                release = self._updater.check_for_update()
                error = None
            except Exception as exc:
                release = None
                error = str(exc)
            self.after(0, lambda: self._on_updates_checked(manual=manual, release=release, error=error))

        threading.Thread(target=run, daemon=True).start()

    def _on_updates_checked(self, manual: bool, release: ReleaseInfo | None, error: str | None):
        self._checking_updates = False
        if error:
            if manual:
                self._restore_idle_status()
            if manual:
                messagebox.showerror(
                    self._s("updates_title"),
                    self._s("updates_checking_error", msg=error),
                )
            return

        if not release:
            if manual:
                self._restore_idle_status()
            if manual:
                messagebox.showinfo(
                    self._s("updates_title"),
                    self._s("updates_none", version=APP_VERSION),
                )
            return

        note_text = self._short_release_notes(release.body)
        if release.asset:
            msg = self._s(
                "updates_prompt_download",
                latest=release.version,
                current=APP_VERSION,
                asset=release.asset.name,
            )
        else:
            msg = self._s(
                "updates_prompt_open_page",
                latest=release.version,
                current=APP_VERSION,
            )
        if note_text:
            msg += f"\n\n{self._s('updates_release_notes')}:\n{note_text}"

        should_continue = messagebox.askyesno(self._s("updates_title"), msg)
        if not should_continue:
            self._restore_idle_status()
            return

        if release.asset:
            self._download_update_asset(release)
        else:
            self._restore_idle_status()
            webbrowser.open(release.html_url)

    def _download_update_asset(self, release: ReleaseInfo):
        if not self._updater or not release.asset:
            return

        self._downloading_update = True
        self._status_var.set(self._s("status_downloading_update", name=release.asset.name))
        download_dir = Path.home() / "Downloads"

        def run():
            try:
                path = self._updater.download_release_asset(release=release, dest_dir=download_dir)
                error = None
            except Exception as exc:
                path = None
                error = str(exc)
            self.after(0, lambda: self._on_update_downloaded(path=path, error=error))

        threading.Thread(target=run, daemon=True).start()

    def _on_update_downloaded(self, path: Path | None, error: str | None):
        self._downloading_update = False
        if error:
            self._restore_idle_status()
            messagebox.showerror(
                self._s("updates_title"),
                self._s("updates_download_error", msg=error),
            )
            return
        if not path:
            return

        self._status_var.set(self._s("status_update_downloaded", name=path.name))
        should_open = messagebox.askyesno(
            self._s("updates_title"),
            self._s("updates_downloaded", path=str(path)),
        )
        if not should_open:
            return

        try:
            assert self._updater is not None
            self._updater.open_download(path)
        except Exception as exc:
            messagebox.showerror(
                self._s("updates_title"),
                self._s("updates_open_error", msg=exc),
            )
        finally:
            self._restore_idle_status()

    @staticmethod
    def _short_release_notes(body: str) -> str:
        lines = [line.strip() for line in body.splitlines() if line.strip()]
        if not lines:
            return ""
        return "\n".join(lines[:5])

    def _restore_idle_status(self):
        self._status_var.set(self._s("status_ready" if self._pdf_path else "status_initial"))

    # --- Actions ---

    def _browse(self):
        path = filedialog.askopenfilename(
            title=self._s("browse_title"),
            filetypes=[("PDF files", "*.pdf"), (self._s("all_files"), "*.*")],
        )
        if path:
            self._pdf_path = path
            self._path_var.set(path)
            self._convert_btn.config(state="normal")
            self._status_var.set(self._s("status_ready"))

    def _convert(self):
        if not self._pdf_path:
            return

        fmt = self._fmt_var.get()
        ext = ".xlsx" if fmt == "excel" else ".docx"
        default_name = Path(self._pdf_path).stem + ext
        filetypes = (
            [("Excel files", "*.xlsx")] if fmt == "excel" else [("Word files", "*.docx")]
        )

        out_path = filedialog.asksaveasfilename(
            title=self._s("save_title"),
            defaultextension=ext,
            initialfile=default_name,
            filetypes=filetypes,
        )
        if not out_path:
            return

        self._convert_btn.config(state="disabled")
        self._status_var.set(self._s("status_converting"))
        self.update()

        def run():
            try:
                extractor = PDFExtractor()
                tables = extractor.extract(self._pdf_path)

                if fmt == "excel":
                    if not tables:
                        self.after(0, lambda: self._done(self._s("status_no_tables"), error=True))
                        return
                    ExcelExporter().export(tables, out_path)
                else:
                    if tables:
                        WordExporter().export(tables, out_path)
                    else:
                        text_pages = extractor.extract_text_pages(self._pdf_path)
                        WordExporter().export_text(text_pages, out_path)

                msg = self._s("status_done", name=os.path.basename(out_path))
                self.after(0, lambda: self._done(msg))
            except Exception as exc:
                msg = self._s("status_error", msg=exc)
                self.after(0, lambda: self._done(msg, error=True))

        threading.Thread(target=run, daemon=True).start()

    def _done(self, msg: str, error: bool = False):
        self._status_var.set(msg)
        self._convert_btn.config(state="normal")
        if error:
            messagebox.showerror(self._s("error_title"), msg)
