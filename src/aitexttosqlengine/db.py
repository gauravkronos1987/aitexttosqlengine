from __future__ import annotations

import os
import re
import time
from pathlib import Path
from typing import Any, Mapping

import psycopg

DEFAULT_SEED_SQL_PATH = Path(__file__).resolve().parents[2] / "export_202607281151.sql"
DEFAULT_DDL_SQL_PATH = Path(__file__).resolve().parents[2] / "dvdrentalddl.sql"


def resolve_database_url(secrets: Any | None = None, env: Mapping[str, str] | None = None) -> str | None:
    env_map = os.environ if env is None else env

    if secrets is not None and hasattr(secrets, "get"):
        for key in ("DATABASE_URL", "database_url"):
            value = secrets.get(key)
            if value:
                return str(value)

    for key in ("DATABASE_URL", "database_url"):
        value = env_map.get(key)
        if value:
            return str(value)

    return None


class DatabaseManager:
    def __init__(self, dsn: str):
        start = time.perf_counter()
        self.conn = psycopg.connect(dsn, autocommit=True)
        elapsed = time.perf_counter() - start
        print(f"DB connect time: {elapsed:.3f}s")

    def initialize_schema(self) -> None:
        statements = self._ddl_statements()
        table_names = self._extract_table_names(statements)
        drop_statements = [f"DROP TABLE IF EXISTS {name} CASCADE;" for name in table_names]

        if drop_statements:
            self.conn.execute("\n".join(drop_statements))
        if statements:
            self.conn.execute("\n\n".join(statements))

    def _resolve_ddl_sql_path(self) -> Path | None:
        candidates = [
            DEFAULT_DDL_SQL_PATH,
            Path.cwd().resolve() / "dvdrentalddl.sql",
            Path.cwd().resolve() / "src" / "dvdrentalddl.sql",
            Path(__file__).resolve().parents[2] / "dvdrentalddl.sql",
            Path(__file__).resolve().parents[2] / "src" / "dvdrentalddl.sql",
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return None

    def _ddl_statements(self) -> list[str]:
        ddl_path = self._resolve_ddl_sql_path()
        if ddl_path is None or not ddl_path.exists():
            raise FileNotFoundError("DDL SQL file not found")
        return self._split_sql_statements(ddl_path.read_text(encoding="utf-8"))

    def _table_names_from_documents(self) -> list[str]:
        return self._extract_table_names(self._ddl_statements())

    def _build_create_statement(self, table_name: str) -> str:
        for statement in self._ddl_statements():
            if re.search(rf"CREATE\s+TABLE\s+(?:public\.)?(\"?{re.escape(table_name)}\"?)", statement, re.IGNORECASE):
                return statement.strip()
        return ""

    def _load_schema_definition(self, table_name: str) -> dict[str, Any] | None:
        statement = self._build_create_statement(table_name)
        if not statement:
            return None
        return {"table": table_name, "ddl": statement}

    def _extract_table_names(self, statements: list[str]) -> list[str]:
        table_names: list[str] = []
        for statement in statements:
            match = re.search(r"CREATE\s+TABLE\s+(?:public\.)?(\"[^\"]+\"|[A-Za-z0-9_]+)", statement, re.IGNORECASE)
            if match:
                table_name = match.group(1).strip('"')
                table_names.append(table_name)
        return table_names

    def _split_sql_statements(self, sql_text: str) -> list[str]:
        statements: list[str] = []
        for raw_statement in re.split(r";\s*\n", sql_text):
            statement = raw_statement.strip()
            if statement:
                statements.append(statement + ";")
        return statements

    def seed_data(self, sql_file: str | Path | None = None) -> None:
        path = self._resolve_seed_sql_path(sql_file)
        print("Inside db.py" ,path)
        if path is not None and path.exists():
            self._execute_sql_file(path)
            return

        self._execute_legacy_seed_data()

    def _resolve_seed_sql_path(self, sql_file: str | Path | None) -> Path | None:
        if sql_file is not None:
            candidate = Path(sql_file)
            if candidate.is_absolute() and candidate.exists():
                return candidate
            if not candidate.is_absolute():
                for base in self._candidate_base_directories():
                    resolved = base / candidate
                    if resolved.exists():
                        return resolved
            return candidate if candidate.exists() else None

        for candidate in self._candidate_seed_paths():
            if candidate.exists():
                return candidate
        return None

    def _candidate_base_directories(self) -> list[Path]:
        current = Path.cwd().resolve()
        module_root = Path(__file__).resolve().parents[2]
        return [current, module_root, current / "src", current / "src" / "aitexttosqlengine", module_root / "src"]

    def _candidate_seed_paths(self) -> list[Path]:
        return [
            DEFAULT_SEED_SQL_PATH,
            Path.cwd().resolve() / "export_202607281151.sql",
            Path.cwd().resolve() / "src" / "export_202607281151.sql",
            Path(__file__).resolve().parents[2] / "export_202607281151.sql",
            Path(__file__).resolve().parents[2] / "src" / "export_202607281151.sql",
            Path(__file__).resolve().parents[1] / "export_202607281151.sql",
        ]

    def _execute_sql_file(self, sql_file: Path) -> None:
        sql = sql_file.read_text(encoding="utf-8")
        statements = [statement.strip() for statement in sql.split(";") if statement.strip()]
        for statement in statements:
            self.conn.execute(statement)

    def _execute_legacy_seed_data(self) -> None:
        self.conn.execute("""
            INSERT INTO customers (customer_id, name, email, country) VALUES
                (1, 'Alice Johnson', 'alice@example.com', 'USA'),
                (2, 'Bob Smith', 'bob@example.com', 'Canada'),
                (3, 'Charlie Brown', 'charlie@example.com', 'UK'),
                (4, 'Diana Prince', 'diana@example.com', 'India'),
                (5, 'Ethan Hunt', 'ethan@example.com', 'Australia');

            INSERT INTO products (product_id, name, category, price) VALUES
                (101, 'Laptop', 'Electronics', 1200.00),
                (102, 'Smartphone', 'Electronics', 800.00),
                (103, 'Headphones', 'Accessories', 150.00),
                (104, 'Office Chair', 'Furniture', 250.00),
                (105, 'Coffee Maker', 'Home Appliances', 90.00);

            INSERT INTO orders (order_id, customer_id, order_date, amount) VALUES
                (1001, 1, '2025-01-10', 1200.00),
                (1002, 2, '2025-01-12', 800.00),
                (1003, 1, '2025-02-05', 150.00),
                (1004, 3, '2025-02-15', 250.00),
                (1005, 4, '2025-03-01', 1200.00),
                (1006, 5, '2025-03-10', 90.00),
                (1007, 2, '2025-03-15', 150.00),
                (1008, 4, '2025-04-01', 800.00),
                (1009, 1, '2025-04-12', 250.00),
                (1010, 3, '2025-05-05', 90.00);
        """)

    def execute(self, query: str):
        return self.conn.execute(query)

    def query(self, query: str):
        start = time.perf_counter()
        result = self.conn.execute(query)
        elapsed = time.perf_counter() - start
        print(f"DB query time: {elapsed:.3f}s")
        headers = [column.name for column in result.description] if result.description else []
        return headers, result.fetchall()

    def close(self) -> None:
        self.conn.close()
