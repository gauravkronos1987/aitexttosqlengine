# AI Text-to-SQL Engine

An intelligent natural language to SQL query converter that leverages LangChain, OpenAI, and Chroma vector search to transform plain English questions into accurate PostgreSQL queries.

## 🎯 Problem Statement

Writing SQL queries requires technical expertise and knowledge of database schemas. This creates a barrier for non-technical users who need to extract insights from databases. This project solves that problem by allowing users to ask questions in natural language and automatically generating the corresponding SQL queries.

## 🚀 Live Demo

This application is deployed and live on **Streamlit Cloud**! Access the interactive web interface without any local setup required.

[🔗 Try the Live Demo](#) *(https://aitexttosqlengine-fsujahdyy5sx4mroydbja2.streamlit.app/)*

## ✨ Key Features

- **Natural Language Processing**: Convert plain English questions into SQL queries
- **Intelligent Schema Search**: Uses vector embeddings to find relevant database tables and columns
- **RAG-Based Architecture**: Retrieves schema context before generating queries
- **Multi-Interface Support**: Web UI (Streamlit), CLI, and Python API
- **PostgreSQL Integration**: Direct database connection and query execution
- **Evaluation Dashboard**: Monitor retrieval performance with Hit Rate and MRR metrics
- **Production Ready**: Includes Docker support, testing, and evaluation framework

## 📊 How It Works

1. **Schema Indexing**: Database table schemas are embedded using OpenAI embeddings and stored in a Chroma vector database
2. **Query Understanding**: User's natural language question is processed
3. **Context Retrieval**: Relevant table schemas are retrieved using semantic similarity search
4. **SQL Generation**: LangChain agent generates PostgreSQL query based on retrieved context
5. **Execution**: Query is executed against the database and results are returned
6. **Evaluation**: System performance is monitored using retrieval metrics

![System Architecture](docs/architecture-diagram.png) *(Add a diagram if available)*

## 📈 Evaluation Criteria

This project implements a comprehensive evaluation framework to measure system performance:

### Retrieval Metrics
- **Hit Rate**: 96.67% - Percentage of queries where relevant tables are retrieved
- **MRR (Mean Reciprocal Rank)**: 0.967 - Measures how highly relevant results are ranked
- **Evaluated Questions**: 120 test cases

These metrics are tracked in `evaluation_metrics.json` and can be viewed in the Evaluation Dashboard.

### Why These Metrics Matter
- **Hit Rate** ensures the system finds the right tables for user questions
- **MRR** measures the quality of ranking (finding relevant tables in top positions)
- Regular evaluation helps maintain and improve system accuracy

## 🚦 Quick Start

### Prerequisites
- Python 3.12 or higher
- PostgreSQL database (optional for local development)
- OpenAI API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/aitexttosqlengine.git
cd aitexttosqlengine
```

2. **Create a virtual environment**
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -e .
```

4. **Set up environment variables**
```bash
# Create a .env file or export directly
export OPENAI_API_KEY="your-openai-api-key-here"
export DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
```

For detailed setup instructions, see [SETUP.md](SETUP.md).

## 💻 Usage

### Option 1: Web Interface (Recommended)

Run the Streamlit application:

```bash
streamlit run src/aitexttosqlengine/app.py
```

The app provides two main features:
1. **SQL Assistant**: Enter natural language queries and get SQL + results
2. **Evaluation Dashboard**: Monitor system performance metrics

**Example Questions:**
- "Which actors have the last name Smith?"
- "List all films released in 2006"
- "What are the top 5 customers by total rental amount?"

### Option 2: Command Line Interface

```bash
# Generate and execute SQL from natural language
python -m aitexttosqlengine "Show me all customers from Canada"

# Initialize the database with sample data
aitexttosqlengine --init-db

# Use custom database connection
aitexttosqlengine "List all actors" --dsn "postgresql://user:pass@host:5432/db"
```

### Option 3: Python API

```python
from aitexttosqlengine.engine import TextToSQLEngine
from aitexttosqlengine.db import DatabaseManager

# Initialize the engine
engine = TextToSQLEngine()

# Generate SQL from natural language
sql = engine.generate_sql("What are the top 10 films by rental revenue?")
print(sql)

# Execute the query
db = DatabaseManager("postgresql://localhost/dvdrental")
headers, rows = db.query(sql)
print(headers)
print(rows)
```

For more examples and use cases, see [USAGE.md](USAGE.md).

## 🧪 Testing

Install test dependencies:

```bash
pip install -e .[dev]
```

Run the test suite:

```bash
pytest
```

The test suite includes:
- SQL extraction and parsing logic
- Database connection and query execution
- Table formatting utilities
- Schema document loading

Test coverage includes unit tests for all core components.

## 🐳 Docker Deployment

Build and run using Docker:

```bash
# Build the image
docker build -t aitexttosqlengine .

# Run the container
docker run -p 8501:8501 \
  -e OPENAI_API_KEY="your-key" \
  -e DATABASE_URL="your-db-url" \
  aitexttosqlengine
```

Access the application at `http://localhost:8501`

## 📁 Project Structure

```
aitexttosqlengine/
├── src/aitexttosqlengine/
│   ├── app.py              # Streamlit web interface
│   ├── engine.py           # Core text-to-SQL engine with LangChain
│   ├── db.py               # Database manager and initialization
│   ├── cli.py              # Command-line interface
│   ├── documents.py        # Schema document definitions
│   ├── search.py           # Schema search functionality
│   ├── evaluation.py       # Evaluation metrics (Hit Rate, MRR)
│   └── run_search_evaluation.py  # Evaluation runner
├── tests/                  # Test suite
├── texttosql.ipynb        # Original prototype notebook
├── dvdrentalddl.sql       # Database schema DDL
├── export_202607281151.sql # Sample data
├── evaluation_metrics.json # Latest evaluation results
├── dockerfile             # Docker configuration
└── pyproject.toml         # Project dependencies

```

## 📸 Screenshots

### SQL Assistant Interface
*(Add screenshot of the Streamlit interface showing a natural language query and generated SQL)*

### Evaluation Dashboard
*(Add screenshot of the evaluation metrics dashboard)*

### Example Query Results
*(Add screenshot showing query execution and results table)*

## 🎓 Example Use Cases

### 1. Finding Actors
**Question**: "Which actors have the last name Smith?"

**Generated SQL**:
```sql
SELECT first_name, last_name 
FROM actor 
WHERE last_name = 'Smith';
```

### 2. Film Analysis
**Question**: "List all films released in 2006 ordered by title"

**Generated SQL**:
```sql
SELECT title 
FROM film 
WHERE release_year = '2006' 
ORDER BY title;
```

### 3. Revenue Analysis
**Question**: "What are the top 10 customers by total rental amount?"

**Generated SQL**:
```sql
SELECT c.customer_id, c.first_name, c.last_name, SUM(p.amount) AS total_amount
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_amount DESC
LIMIT 10;
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY` (required): Your OpenAI API key
- `DATABASE_URL` (optional): PostgreSQL connection string
  - Format: `postgresql://user:password@host:port/database`
  - Default: `postgresql://postgres:postgres@localhost:5432/dvdrental`

### Streamlit Secrets

For Streamlit Cloud deployment, add secrets in `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your-key-here"
DATABASE_URL = "your-database-url"
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This repository currently has no license specified.

## 📚 Additional Documentation

- [SETUP.md](SETUP.md) - Detailed setup and installation guide
- [USAGE.md](USAGE.md) - Comprehensive usage examples and tutorials
- [EVALUATION.md](EVALUATION.md) - Evaluation methodology and metrics
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture and design decisions

## 🙏 Acknowledgments

This project uses:
- **LangChain** for agent orchestration
- **OpenAI** for embeddings and language models
- **Chroma** for vector storage
- **PostgreSQL** for database operations
- **Streamlit** for the web interface
- **DVD Rental Database** as sample data
