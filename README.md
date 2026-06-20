# aitexttosqlengine

A prototype project that converts natural language questions into SQL queries using LangChain, OpenAI, and Chroma vector search.

## 🚀 Live Deployment

This application is now deployed and live on **Streamlit Cloud**! You can access the interactive web interface directly without any local setup required.

## What this project does

- Builds a `Chroma` vector store from text documents describing database tables.
- Uses `OpenAIEmbeddings` to embed table and schema information.
- Defines a searchable tool for the agent to retrieve relevant schema details.
- Creates a LangChain agent with `ChatOpenAI` and guided instructions.
- Generates SQL queries from user questions and extracts them from model responses.
- Executes queries and returns formatted results through an interactive web interface.
- Demonstrates a Postgres connection using `psycopg`.
- Provides a user-friendly Streamlit web interface for querying databases with natural language.

## Key files

- `texttosql.ipynb` - original notebook reference for code and workflow.
- `pyproject.toml` - project metadata and installable package configuration.
- `main.py` - package entrypoint wrapper.
- `src/aitexttosqlengine/engine.py` - text-to-SQL agent and vector search logic.
- `src/aitexttosqlengine/db.py` - Postgres database schema initialization and sample data seeding.
- `src/aitexttosqlengine/cli.py` - command-line interface for generating SQL and initializing the database.
- `src/aitexttosqlengine/app.py` - interactive Streamlit web interface for the Course Assistant.

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
- `streamlit` - for the interactive web interface

## Usage

### Web Interface (Streamlit Cloud)

The easiest way to use this application is through the live Streamlit Cloud deployment. Simply visit the deployed URL and start asking natural language questions about your database.

### Local Installation

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

### Running Locally

**Option A: Web Interface**

Run the Streamlit app locally:

```bash
streamlit run src/aitexttosqlengine/app.py
```

The application will open in your browser. You can then enter natural language queries in the text input field and click "Ask" to get SQL queries and results.

**Option B: Command Line**

Use the installed CLI:

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

## Database Initialization

If you want to initialize and seed the default Postgres database:

```bash
aitexttosqlengine --init-db
```

## Notes

- Use the notebook (`texttosql.ipynb`) as a reference for the original workflow and sample dataset.
- For the Streamlit Cloud deployment, secrets are managed through Streamlit's secrets management system.
- The application supports both local and cloud database connections via environment variables.

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
