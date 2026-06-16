from aitexttosqlengine.cli import format_table


def test_format_table_header_and_rows():
    headers = ["customer_id", "name", "total_revenue"]
    rows = [(1, "Alice", 1600.0), (2, "Bob", 950.0)]
    table = format_table(headers, rows)

    assert "| customer_id | name  | total_revenue |" in table
    assert "| 1           | Alice | 1600.0        |" in table
    assert "+-------------+-------+---------------+" in table
