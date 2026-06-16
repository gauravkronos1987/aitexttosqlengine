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

- `texttosql.ipynb` - main notebook demonstrating the text-to-SQL flow.
- `pyproject.toml` - project metadata and dependencies.
- `main.py` - placeholder entry point.

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

4. Open the notebook:

```bash
jupyter lab texttosql.ipynb
```

5. Run the notebook cells to:

- build the vector store from document descriptions,
- define the search tool,
- create the LangChain agent,
- invoke the agent with a natural language question,
- extract SQL from the agent response.

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
