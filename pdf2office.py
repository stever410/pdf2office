"""
pdf2office.py — PDF table → Excel / Word converter
Usage: python3 pdf2office.py
"""

import ctypes
import ctypes.util
import sys

from pdf2office.bootstrap import check_runtime_dependencies
from pdf2office.metadata import APP_ID, APP_NAME


def _set_process_identity() -> None:
    if sys.platform == "win32":
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)
        except Exception:
            pass
        return

    if sys.platform == "darwin":
        try:
            libc_path = ctypes.util.find_library("c")
            if libc_path:
                libc = ctypes.CDLL(libc_path)
                if hasattr(libc, "setprogname"):
                    libc.setprogname.argtypes = [ctypes.c_char_p]
                    libc.setprogname(APP_NAME.encode("utf-8"))
        except Exception:
            pass
        try:
            from Foundation import NSProcessInfo  # type: ignore

            NSProcessInfo.processInfo().setProcessName_(APP_NAME)
        except Exception:
            pass


def main() -> int:
    if not check_runtime_dependencies():
        return 1
    _set_process_identity()

    from pdf2office.ui.main_app import App

    App().mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
