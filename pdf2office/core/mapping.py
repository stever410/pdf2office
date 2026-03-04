from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ColumnMapping:
    name_col: int
    id_col: Optional[int] = None
    value_col: Optional[int] = None
    extra_cols: List[int] = field(default_factory=list)
    header_row: int = 0
    grouping_col: Optional[int] = None
    raw_headers: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name_col": self.name_col,
            "id_col": self.id_col,
            "value_col": self.value_col,
            "extra_cols": self.extra_cols,
            "header_row": self.header_row,
            "grouping_col": self.grouping_col,
            "raw_headers": self.raw_headers,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ColumnMapping":
        return ColumnMapping(
            name_col=data.get("name_col", 0),
            id_col=data.get("id_col"),
            value_col=data.get("value_col"),
            extra_cols=data.get("extra_cols", []),
            header_row=data.get("header_row", 0),
            grouping_col=data.get("grouping_col"),
            raw_headers=data.get("raw_headers", []),
        )
