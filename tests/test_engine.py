from langchain_core.messages import AIMessage

from aitexttosqlengine.documents import DOCUMENTS, DOCUMENT_OBJECTS
from aitexttosqlengine.engine import TextToSQLEngine


def test_extract_sql_from_markdown_block():
    engine = object.__new__(TextToSQLEngine)
    sql = engine._extract_sql(
        "Here is the query:\n```sql\nSELECT * FROM customers;\n```\n"
    )
    assert sql == "SELECT * FROM customers;"


def test_extract_last_ai_message_returns_last_non_empty_response():
    engine = object.__new__(TextToSQLEngine)
    response = {
        "messages": [
            AIMessage(content=""),
            AIMessage(content="SELECT * FROM orders;"),
        ]
    }

    answer = engine._extract_last_ai_message(response)
    assert answer == "SELECT * FROM orders;"


def test_extract_sql_from_plain_sql_text():
    engine = object.__new__(TextToSQLEngine)
    sql = engine._extract_sql("SELECT title FROM film WHERE release_year = '2006';")
    assert sql == "SELECT title FROM film WHERE release_year = '2006';"


def test_documents_module_exposes_schema_definitions():
    assert any("Table: actor" in doc for doc in DOCUMENTS)
    assert any("Table: film" in doc for doc in DOCUMENTS)


def test_document_objects_include_table_metadata():
    actor_doc = next(doc for doc in DOCUMENT_OBJECTS if doc.metadata.get("table") == "actor")
    assert actor_doc.metadata["table"] == "actor"
    assert "Table: actor" in actor_doc.page_content
    assert "CREATE TABLE public.actor" in actor_doc.page_content
