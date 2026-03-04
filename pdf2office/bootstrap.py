import sys


def check_runtime_dependencies() -> bool:
    missing = []

    try:
        import pdfplumber  # noqa: F401
    except ImportError:
        missing.append("pdfplumber")

    try:
        import openpyxl  # noqa: F401
    except ImportError:
        missing.append("openpyxl")

    try:
        import docx  # noqa: F401
    except ImportError:
        missing.append("python-docx")

    if not missing:
        return True

    print(f"Missing dependencies: {', '.join(missing)}")
    print(f"Install with: {sys.executable} -m pip install {' '.join(missing)}")
    return False
