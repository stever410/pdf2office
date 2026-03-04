import json
from typing import Optional

from pdf2office.core.mapping import ColumnMapping


class SettingsStore:
    def __init__(self, settings_path: str):
        self._settings_path = settings_path

    def load_last_mapping(self) -> Optional[ColumnMapping]:
        try:
            with open(self._settings_path, encoding="utf-8") as file:
                data = json.load(file)
            return ColumnMapping.from_dict(data["last_mapping"])
        except Exception:
            return None

    def save_last_mapping(self, mapping: ColumnMapping):
        try:
            with open(self._settings_path, "w", encoding="utf-8") as file:
                json.dump({"last_mapping": mapping.to_dict()}, file, indent=2)
        except Exception:
            pass
