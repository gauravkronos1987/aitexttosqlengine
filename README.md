# aitexttosqlengine

A prototype project that converts natural language questions into SQL queries using LangChain, OpenAI, and Chroma vector search.

## What this project does

- Builds a `Chroma` vector store from text documents describing database tables.
- Uses `OpenAIEmbeddings` to embed table and schema information.
- Defines a searchable tool for the agent to retrieve relevant schema details.
- Creates a LangChain agent with `ChatOpenAI` and guided instructions.
- Generates SQL queries from user questions and extracts them from model responses.
- Demonstrates a Postgres connection using `psycopg`.

## Key files

- `texttosql.ipynb` - original notebook reference for code and workflow.
- `pyproject.toml` - project metadata and installable package configuration.
- `main.py` - package entrypoint wrapper.
- `src/aitexttosqlengine/engine.py` - text-to-SQL agent and vector search logic.
- `src/aitexttosqlengine/db.py` - Postgres database schema initialization and sample data seeding.
- `src/aitexttosqlengine/cli.py` - command-line interface for generating SQL and initializing the database.

## Dependencies

This project requires Python 3.12+ and installs the following packages:

- `chromadb`
- `jupyter`
- `langchain`
- `langchain-chroma`
- `langchain-openai`
- `minsearch`
- `openai`
- `psycopg[binary]`
- `python-dotenv`
- `requests`

## Usage

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -e .
```

3. Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-key-here"
```

4. Run the package directly or use the installed CLI.

```bash
python -m aitexttosqlengine "What are the top customers by revenue?"
```

## Testing

Install test dependencies:

```bash
pip install -e .[dev]
```

Run the tests with pytest:

```bash
pytest
```

The test suite covers:

- SQL extraction logic in `src/aitexttosqlengine/engine.py`
- pretty table formatting in `src/aitexttosqlengine/cli.py`
- database header extraction in `src/aitexttosqlengine/db.py` using a mocked connection

Or, after installing the package, use the script:

```bash
aitexttosqlengine "What are the top customers by revenue?"
```

5. If you want to initialize and seed the default Postgres database:

```bash
aitexttosqlengine --init-db
```

6. Use the notebook as a reference for the original workflow and sample dataset.

## Example

The notebook includes an example question:

> "What are the top customers by revenue?"

The agent searches schema summaries and returns a SQL statement such as:

```sql
SELECT
  c.customer_id,
  c.name,
  SUM(o.amount) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_revenue DESC
LIMIT 10;
```

## Notes

- `texttosql.ipynb` is the current implementation prototype.
- The notebook also includes a helper function `findSql(query: str) -> str` to return the generated SQL query.
- If you connect to a Postgres database, update the connection string in the notebook before use.

## License

This repository currently has no license specified.
