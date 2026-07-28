"""Schema document definitions used by the text-to-SQL engine."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _load_documents() -> list[str]:
    data_file = Path(__file__).with_name("documents.json")
    with data_file.open("r", encoding="utf-8") as handle:
        payload: dict[str, Any] = json.load(handle)

    documents: list[str] = []
    for table in payload.get("tables", []):
        lines = [f"Table: {table['table']}", table.get("description", "")]
        lines.append("Columns:")
        for column in table.get("columns", []):
            lines.append(f"- {column['name']} : {column['description']}")
        documents.append("\n".join(lines))
    return documents


DOCUMENTS = _load_documents()
