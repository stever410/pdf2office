import pdfplumber
from typing import List


class PDFExtractor:
    """Extract all tables from a PDF, preserving table boundaries."""

    def extract(self, pdf_path: str) -> List[List[List[str]]]:
        tables = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                for table in page.extract_tables():
                    cleaned = [
                        [str(cell).strip() if cell is not None else "" for cell in row]
                        for row in table
                        if any(cell for cell in row)
                    ]
                    if cleaned:
                        tables.append(cleaned)
        return tables

    def extract_text_pages(self, pdf_path: str) -> List[str]:
        pages: List[str] = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                pages.append(text.strip())
        return pages
