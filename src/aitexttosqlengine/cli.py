from __future__ import annotations

import argparse
import os
from typing import Sequence

from .db import DatabaseManager
from .engine import TextToSQLEngine


def format_table(headers: Sequence[str], rows: Sequence[tuple]) -> str:
    column_widths = [len(str(header)) for header in headers]
    for row in rows:
        for idx, value in enumerate(row):
            column_widths[idx] = max(column_widths[idx], len(str(value)))

    separator = "+" + "+".join("-" * (width + 2) for width in column_widths) + "+"
    header_row = "| " + " | ".join(str(header).ljust(width) for header, width in zip(headers, column_widths)) + " |"
    lines = [separator, header_row, separator]

    for row in rows:
        row_line = "| " + " | ".join(str(value).ljust(width) for value, width in zip(row, column_widths)) + " |"
        lines.append(row_line)

    lines.append(separator)
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Text-to-SQL engine CLI")
    parser.add_argument("query", nargs="?", help="Natural language question to convert into SQL")
    parser.add_argument("--dsn", default=os.getenv("DATABASE_URL", "postgresql://user:pswd@localhost:5432/faq"), help="Postgres DSN")
    parser.add_argument("--init-db", action="store_true", help="Initialize and seed the Postgres database")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.init_db:
        db = DatabaseManager(args.dsn)
        db.initialize_schema()
        db.seed_data()
        db.close()
        print("Database initialized and seeded.")
        return

    engine = TextToSQLEngine()

    if not args.query:
        print("Please provide a natural language query.")
        return

    sql = engine.generate_sql(args.query)
    if not sql:
        print("Could not extract SQL from the language model response.")
        return

    print("Generated SQL:\n")
    print(sql)
    print()

    try:
        db = DatabaseManager(args.dsn)
        headers, rows = db.query(sql)
        db.close()
    except Exception as exc:
        print("SQL execution failed:")
        print(exc)
        return

    if rows:
        print("Result:")
        print(format_table(headers, rows))
    else:
        print("Query executed successfully, but returned no rows.")
