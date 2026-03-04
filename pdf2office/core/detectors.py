import re
from typing import List

from .mapping import ColumnMapping


class HeuristicDetector:
    ID_KW = re.compile(r"mã|code|sku|id|stt|no\.", re.IGNORECASE)
    NAME_KW = re.compile(r"tên|name|product|description|desc", re.IGNORECASE)
    VALUE_KW = re.compile(r"giá|price|value|amount|cost", re.IGNORECASE)
    GROUP_KW = re.compile(r"nhóm|loại|category|group", re.IGNORECASE)

    def detect(self, headers: List[str]) -> ColumnMapping:
        id_col = name_col = value_col = group_col = None

        for index, header in enumerate(headers):
            if id_col is None and self.ID_KW.search(header):
                id_col = index
            elif name_col is None and self.NAME_KW.search(header):
                name_col = index
            elif value_col is None and self.VALUE_KW.search(header):
                value_col = index
            elif group_col is None and self.GROUP_KW.search(header):
                group_col = index

        if name_col is None:
            used = {id_col, value_col, group_col}
            for index in range(len(headers)):
                if index not in used:
                    name_col = index
                    break

        if name_col is None:
            name_col = 0

        return ColumnMapping(
            name_col=name_col,
            id_col=id_col,
            value_col=value_col,
            grouping_col=group_col,
            raw_headers=headers,
        )
