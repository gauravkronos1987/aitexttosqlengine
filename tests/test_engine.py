from langchain_core.messages import AIMessage

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
