from types import SimpleNamespace

import pytest

from aitexttosqlengine.db import DatabaseManager


def test_query_returns_headers_and_rows(monkeypatch):
    class DummyCursor:
        description = [SimpleNamespace(name="one")]

        def fetchall(self):
            return [(1,)]

    class DummyConnection:
        def __init__(self, **kwargs):
            assert kwargs.get("autocommit") is True

        def execute(self, query: str):
            assert query == "SELECT 1 AS one"
            return DummyCursor()

        def close(self):
            pass

    def dummy_connect(dsn: str, **kwargs):
        return DummyConnection(**kwargs)

    monkeypatch.setattr("aitexttosqlengine.db.psycopg.connect", dummy_connect)

    db = DatabaseManager("postgresql://user:pswd@localhost:5432/faq")
    headers, rows = db.query("SELECT 1 AS one")
    db.close()

    assert headers == ["one"]
    assert rows == [(1,)]
