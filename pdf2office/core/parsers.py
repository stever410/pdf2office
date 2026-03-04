import re
from typing import List, Tuple

from .mapping import ColumnMapping


class GenericParser:
    """Apply a ColumnMapping to raw rows to produce (products, sets)."""

    SET_KEYWORDS = re.compile(r"bao\s*gồm|bộ|set|kit", re.IGNORECASE)

    @staticmethod
    def _parse_value(text: str) -> int:
        if not text:
            return 0
        cleaned = re.sub(r"[^\d]", "", str(text))
        return int(cleaned) if cleaned else 0

    @staticmethod
    def _is_value(text: str) -> bool:
        cleaned = re.sub(r"[^\d]", "", str(text or ""))
        return len(cleaned) >= 4

    def parse(self, raw_rows: List[List[str]], mapping: ColumnMapping):
        products: List[Tuple[str, str, int]] = []
        sets = []
        current_set = None

        def safe_get(row, idx):
            if idx is None or idx >= len(row):
                return ""
            return row[idx] or ""

        for index, row in enumerate(raw_rows):
            if index == mapping.header_row:
                continue

            name = safe_get(row, mapping.name_col)
            id_val = safe_get(row, mapping.id_col) if mapping.id_col is not None else ""
            value_raw = safe_get(row, mapping.value_col) if mapping.value_col is not None else ""
            group_val = safe_get(row, mapping.grouping_col) if mapping.grouping_col is not None else ""

            if not any(cell.strip() for cell in row):
                continue

            has_value = self._is_value(value_raw)

            if group_val and group_val != name:
                price = self._parse_value(value_raw)
                current_set = {"name": group_val, "price": price, "items": []}
                sets.append(current_set)
                continue

            if has_value:
                price = self._parse_value(value_raw)
                if (not id_val) and self.SET_KEYWORDS.search(name):
                    current_set = {"name": name, "price": price, "items": []}
                    sets.append(current_set)
                else:
                    if name:
                        products.append((id_val, name, price))
                    current_set = None
            else:
                if current_set is not None and name:
                    current_set["items"].append((id_val, name))

        return products, sets
