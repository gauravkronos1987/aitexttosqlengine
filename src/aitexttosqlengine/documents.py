"""Schema document definitions used by the text-to-SQL engine."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from langchain_core.documents import Document


def _load_schema_payload() -> dict[str, Any]:
    data_file = Path(__file__).with_name("documents.json")
    with data_file.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_ddl_definitions() -> dict[str, str]:
    ddl_candidates = [
        Path(__file__).resolve().parents[2] / "dvdrentalddl.sql",
        Path.home() / "dvdrentalddl.sql",
    ]

    ddl_path = next((candidate for candidate in ddl_candidates if candidate.exists()), ddl_candidates[0])
    ddl_text = ddl_path.read_text(encoding="utf-8")

    pattern = re.compile(
        r"CREATE TABLE\s+(?:public\.)?(?P<name>\"[^\"]+\"|[A-Za-z0-9_]+)\s*\((?P<body>.*?)\);",
        re.IGNORECASE | re.DOTALL,
    )

    definitions: dict[str, str] = {}
    for match in pattern.finditer(ddl_text):
        table_name = match.group("name").strip('"')
        body = match.group("body").strip()
        definitions[table_name] = f"CREATE TABLE public.{table_name} (\n{body}\n);"
    return definitions


def _infer_relationships(table_name: str, columns: list[dict[str, Any]]) -> list[str]:
    relationships: list[str] = []
    for column in columns:
        column_name = str(column.get("name", ""))
        if not column_name.endswith("_id") or column_name == f"{table_name}_id":
            continue

        target_name = column_name[:-3]
        if target_name.startswith("manager_"):
            target_name = "staff"
        elif target_name.startswith("staff_"):
            target_name = "staff"
        elif target_name.startswith("customer_"):
            target_name = "customer"
        elif target_name.startswith("payment_"):
            target_name = "payment"
        elif target_name.startswith("rental_"):
            target_name = "rental"
        elif target_name.startswith("inventory_"):
            target_name = "inventory"
        elif target_name == "manager_staff":
            target_name = "staff"

        relationships.append(f"- {column_name} -> {target_name}.{column_name}")

    return relationships or ["- No explicit relationships documented."]


def _build_document_objects() -> list[Document]:
    payload = _load_schema_payload()
    ddl_definitions = _load_ddl_definitions()
    documents: list[Document] = []

    for table in payload.get("tables", []):
        table_name = str(table["table"])
        columns = table.get("columns", [])
        ddl = ddl_definitions.get(table_name, "")
        column_text = "\n".join(
            f"- {column['name']} ({column.get('type', 'unknown')}): {column.get('description', '')}"
            for column in columns
        )
        relationship_text = "\n".join(_infer_relationships(table_name, columns))

        page_content = f"""
Table: {table_name}

Description:
{table.get('description', '')}

DDL:
{ddl}

Columns:
{column_text}

Relationships:
{relationship_text}
""".strip()

        documents.append(  Document(
        page_content=page_content,
        metadata={
            "table": table_name,
            "description": table.get("description", ""),
            "column_count": len(columns),
            "columns": [column["name"] for column in columns],
        },
    ))

    return documents


DOCUMENT_OBJECTS = _build_document_objects()
DOCUMENTS = [document.page_content for document in DOCUMENT_OBJECTS]
