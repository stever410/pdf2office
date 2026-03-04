# -*- mode: python ; coding: utf-8 -*-

import sys

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
from pdf2office.metadata import APP_ID, APP_NAME

hiddenimports = collect_submodules("pdf2office")
datas = [("icon.png", "."), *collect_data_files("certifi")]

# Exclude unnecessary modules to reduce bundle size
excludes = [
    # Testing frameworks
    "pytest", "unittest", "test", "tests", "_pytest",
    # Development tools
    "pip", "setuptools", "wheel", "distutils",
    # Unused standard library modules
    "pydoc", "curses", "turtle", "tkinter.test",
    # Common large packages not used
    "numpy", "pandas", "matplotlib", "scipy",
    "IPython", "jupyter", "notebook",
    # XML parsers we don't use
    "xml.dom.minidom", "xml.sax",
    # Other unused modules
    "asyncio", "multiprocessing", "concurrent.futures",
]

a = Analysis(
    ["pdf2office.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
    optimize=2,  # Python bytecode optimization level 2
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_ID,
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # Strip symbols on Linux/macOS to reduce size
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=True,  # Strip symbols from binaries
    upx=True,
    upx_exclude=[
        # Exclude problematic files from UPX compression
        "vcruntime140.dll",
        "python*.dll",
        "Qt*.dll",
    ],
    name=APP_ID,
)

# On macOS, produce a native .app bundle for end users.
if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name=f"{APP_NAME}.app",
        icon=None,
        bundle_identifier=None,
    )
