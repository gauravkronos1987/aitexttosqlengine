# Architecture Documentation

This document provides a comprehensive overview of the AI Text-to-SQL Engine's architecture, design decisions, and data flow.

## Table of Contents

- [System Overview](#system-overview)
- [Architecture Diagram](#architecture-diagram)
- [Core Components](#core-components)
- [Data Flow](#data-flow)
- [Technology Stack](#technology-stack)
- [Design Decisions](#design-decisions)
- [Database Schema](#database-schema)
- [Deployment Architecture](#deployment-architecture)
- [Security Considerations](#security-considerations)
- [Performance Optimization](#performance-optimization)

## System Overview

The AI Text-to-SQL Engine is a **Retrieval-Augmented Generation (RAG)** system that converts natural language questions into SQL queries. It combines vector search, language models, and agent-based reasoning to generate accurate database queries.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Streamlit  │  │     CLI      │  │    Python API        │  │
│  │   Web App    │  │   Interface  │  │                      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              TextToSQLEngine (engine.py)                 │   │
│  │  - Query Processing                                      │   │
│  │  - Agent Orchestration                                   │   │
│  │  - SQL Extraction                                        │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   Retrieval Layer        │  │   Generation Layer       │
│  ┌────────────────────┐  │  │  ┌────────────────────┐  │
│  │  Chroma Vector DB  │  │  │  │   OpenAI GPT       │  │
│  │  - Schema Docs     │  │  │  │   - SQL Generation │  │
│  │  - Embeddings      │  │  │  │   - Agent Logic    │  │
│  └────────────────────┘  │  │  └────────────────────┘  │
└──────────────────────────┘  └──────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data Layer                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              PostgreSQL Database                         │   │
│  │  - DVD Rental Schema                                     │   │
│  │  - Query Execution                                       │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Architecture Diagram

### Component Interaction Flow

```
User Question
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│ 1. Question Processing                                  │
│    - Receive natural language input                     │
│    - Validate and sanitize                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Schema Retrieval (RAG)                              │
│    ┌─────────────────────────────────────────────────┐ │
│    │ a. Embed question using OpenAI embeddings       │ │
│    │ b. Search Chroma vector DB                      │ │
│    │ c. Retrieve top-k relevant table schemas        │ │
│    └─────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Context Building                                     │
│    - Combine retrieved schemas                          │
│    - Format as context for LLM                          │
│    - Include instructions and constraints               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 4. SQL Generation (LangChain Agent)                    │
│    ┌─────────────────────────────────────────────────┐ │
│    │ a. Agent receives question + context            │ │
│    │ b. May perform additional searches              │ │
│    │ c. Generates SQL using GPT model                │ │
│    │ d. Returns response with SQL                    │ │
│    └─────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 5. SQL Extraction                                       │
│    - Parse LLM response                                 │
│    - Extract SQL from markdown/text                     │
│    - Validate SQL syntax                                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 6. Query Execution (Optional)                           │
│    - Connect to PostgreSQL                              │
│    - Execute SQL query                                  │
│    - Fetch and format results                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
                  Results
```

## Core Components

### 1. TextToSQLEngine (`engine.py`)

**Purpose**: Core engine that orchestrates the text-to-SQL conversion process.

**Key Responsibilities**:
- Initialize vector store with schema documents
- Create and manage LangChain agent
- Process natural language queries
- Extract SQL from LLM responses

**Key Methods**:
```python
class TextToSQLEngine:
    def __init__(self, embedding_model, llm_model, temperature):
        # Initialize vector store, LLM, and agent
        
    def generate_sql(self, query: str) -> str | None:
        # Main entry point for SQL generation
        
    def _build_search_tool(self):
        # Create search tool for agent
        
    def _extract_sql(self, text: str) -> str | None:
        # Extract SQL from LLM response
```

**Design Pattern**: Facade pattern - provides simple interface to complex subsystems

### 2. DatabaseManager (`db.py`)

**Purpose**: Manages all database operations including initialization, querying, and schema management.

**Key Responsibilities**:
- Establish and manage database connections
- Initialize database schema from DDL files
- Seed sample data
- Execute queries and return results
- Handle connection pooling and error recovery

**Key Methods**:
```python
class DatabaseManager:
    def __init__(self, dsn: str):
        # Initialize connection
        
    def initialize_schema(self) -> None:
        # Create tables from DDL
        
    def seed_data(self, sql_file: Path) -> None:
        # Load sample data
        
    def query(self, sql: str) -> tuple[list[str], list[tuple]]:
        # Execute query and return results
```

**Design Pattern**: Repository pattern - abstracts data access

### 3. SchemaSearcher (`search.py`)

**Purpose**: Provides semantic search over database schema documents.

**Key Responsibilities**:
- Initialize Chroma vector store
- Embed schema documents
- Perform similarity search
- Return relevant table information

**Key Methods**:
```python
class SchemaSearcher:
    def __init__(self):
        # Initialize vector store with embeddings
        
    def search(self, query: str, k: int = 2) -> list[Any]:
        # Search for relevant schemas
```

**Design Pattern**: Strategy pattern - encapsulates search algorithm

### 4. Streamlit App (`app.py`)

**Purpose**: Web-based user interface for the application.

**Key Features**:
- **SQL Assistant Page**: Interactive query interface
- **Evaluation Dashboard**: Performance metrics visualization
- Session state management
- Error handling and user feedback

**Architecture**:
```python
# Page routing
if page == "SQL Assistant":
    render_sql_assistant()
else:
    render_monitoring_dashboard()

def render_sql_assistant():
    # Handle user queries
    # Display SQL and results
    
def render_monitoring_dashboard():
    # Show evaluation metrics
    # Run evaluations
```

**Design Pattern**: MVC pattern - separates presentation from logic

### 5. CLI Interface (`cli.py`)

**Purpose**: Command-line interface for the application.

**Key Features**:
- Query execution from terminal
- Database initialization
- Custom DSN support
- Formatted table output

**Usage Pattern**:
```bash
aitexttosqlengine "query" [--dsn DSN] [--init-db]
```

### 6. Document Manager (`documents.py`)

**Purpose**: Manages schema document definitions and loading.

**Key Responsibilities**:
- Load schema definitions from JSON
- Parse DDL files
- Create LangChain Document objects
- Attach metadata (table names, etc.)

**Data Structure**:
```python
Document(
    page_content="Table: actor\nDescription: ...\nDDL: CREATE TABLE...",
    metadata={"table": "actor"}
)
```

### 7. Evaluation Module (`evaluation.py`)

**Purpose**: Measures system performance using retrieval metrics.

**Key Functions**:
```python
def hit_rate(relevance_total) -> float:
    # Calculate hit rate metric
    
def mrr(relevance_total) -> float:
    # Calculate MRR metric
    
def evaluate(ground_truth, search_function) -> dict:
    # Run full evaluation
```

## Data Flow

### Detailed Request Flow

#### 1. User Submits Question

```
User Input: "Which actors have the last name Smith?"
     │
     ▼
[Validation & Sanitization]
     │
     ▼
Processed Query: "Which actors have the last name Smith?"
```

#### 2. Schema Retrieval

```
Question → OpenAI Embeddings API
     │
     ▼
Question Vector: [0.123, -0.456, 0.789, ...]
     │
     ▼
Chroma Vector DB Search (Cosine Similarity)
     │
     ▼
Top-K Results:
  1. actor table (similarity: 0.95)
  2. film_actor table (similarity: 0.72)
```

#### 3. Context Assembly

```
Retrieved Schemas:
┌────────────────────────────────────────┐
│ Table: actor                           │
│ Description: Contains actor info...    │
│ DDL: CREATE TABLE public.actor (       │
│   actor_id integer NOT NULL,           │
│   first_name varchar(45) NOT NULL,     │
│   last_name varchar(45) NOT NULL,      │
│   ...                                  │
│ )                                      │
└────────────────────────────────────────┘
     │
     ▼
Combined Context for LLM
```

#### 4. Agent Processing

```
LangChain Agent:
┌────────────────────────────────────────┐
│ System Instructions:                   │
│ "You are a PostgreSQL expert..."       │
│                                        │
│ Context:                               │
│ [Retrieved schema documents]           │
│                                        │
│ User Question:                         │
│ "Which actors have last name Smith?"   │
└────────────────────────────────────────┘
     │
     ▼
OpenAI GPT API Call
     │
     ▼
LLM Response:
"```sql
SELECT first_name, last_name 
FROM actor 
WHERE last_name = 'Smith';
```"
```

#### 5. SQL Extraction

```
LLM Response → Regex Parsing
     │
     ▼
Extracted SQL:
"SELECT first_name, last_name FROM actor WHERE last_name = 'Smith';"
```

#### 6. Query Execution

```
SQL → PostgreSQL Database
     │
     ▼
Query Results:
┌────────────┬───────────┐
│ first_name │ last_name │
├────────────┼───────────┤
│ JOHN       │ SMITH     │
│ JANE       │ SMITH     │
└────────────┴───────────┘
     │
     ▼
Formatted Output to User
```

## Technology Stack

### Backend Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Language | Python | 3.12+ | Core implementation |
| Vector DB | Chroma | 1.5.9+ | Schema embeddings storage |
| LLM Framework | LangChain | 1.3.9+ | Agent orchestration |
| LLM Provider | OpenAI | GPT-4/GPT-3.5 | SQL generation |
| Embeddings | OpenAI | text-embedding-3-small | Vector embeddings |
| Database | PostgreSQL | 12+ | Data storage |
| DB Driver | psycopg | 3.3.4+ | Database connectivity |

### Frontend Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Web Framework | Streamlit | 1.58.0+ | Interactive UI |
| Data Display | Pandas | 3.0.3+ | Result formatting |

### Development Tools

| Tool | Purpose |
|------|---------|
| pytest | Unit testing |
| python-dotenv | Environment management |
| tqdm | Progress bars |
| Docker | Containerization |

## Design Decisions

### 1. RAG Architecture

**Decision**: Use Retrieval-Augmented Generation instead of fine-tuning.

**Rationale**:
- ✅ No need to fine-tune expensive models
- ✅ Easy to update with new schemas
- ✅ Transparent - can see what context is retrieved
- ✅ Cost-effective for inference
- ❌ Requires good retrieval quality

**Alternative Considered**: Fine-tuning GPT on SQL examples
- Rejected due to cost and inflexibility

### 2. Vector Database Choice: Chroma

**Decision**: Use Chroma for vector storage.

**Rationale**:
- ✅ Lightweight and easy to set up
- ✅ Good Python integration
- ✅ Sufficient for prototype/small-scale
- ✅ No external service dependencies
- ❌ May not scale to millions of documents

**Alternatives Considered**:
- Pinecone: Requires external service
- Weaviate: More complex setup
- FAISS: Lower-level, more manual

### 3. LangChain Agent Framework

**Decision**: Use LangChain agents for orchestration.

**Rationale**:
- ✅ Built-in tool calling support
- ✅ Easy to add search capability
- ✅ Handles conversation flow
- ✅ Well-documented
- ❌ Adds abstraction layer

**Alternative Considered**: Direct OpenAI API calls
- Rejected due to need for tool calling and agent logic

### 4. PostgreSQL Database

**Decision**: Use PostgreSQL as the target database.

**Rationale**:
- ✅ Industry-standard SQL database
- ✅ Rich feature set (JOINs, CTEs, etc.)
- ✅ Good Python support
- ✅ Free and open source
- ✅ DVD Rental sample database available

### 5. Multi-Interface Design

**Decision**: Provide Web UI, CLI, and Python API.

**Rationale**:
- ✅ Flexibility for different use cases
- ✅ Web UI for non-technical users
- ✅ CLI for automation/scripting
- ✅ API for integration
- ❌ More code to maintain

### 6. Evaluation-First Approach

**Decision**: Build evaluation framework from the start.

**Rationale**:
- ✅ Measure improvements objectively
- ✅ Catch regressions early
- ✅ Build confidence in system
- ✅ Guide optimization efforts

## Database Schema

### DVD Rental Database

The system uses the classic DVD Rental sample database:

```
┌─────────────────────────────────────────────────────────────┐
│                     Database Schema                          │
└─────────────────────────────────────────────────────────────┘

┌──────────┐     ┌──────────┐     ┌──────────┐
│  actor   │────▶│film_actor│◀────│   film   │
└──────────┘     └──────────┘     └──────────┘
                                        │
                                        ▼
                                  ┌──────────┐
                                  │inventory │
                                  └──────────┘
                                        │
                                        ▼
┌──────────┐     ┌──────────┐     ┌──────────┐
│ customer │────▶│  rental  │◀────│  staff   │
└──────────┘     └──────────┘     └──────────┘
     │                │                 │
     │                ▼                 │
     │          ┌──────────┐            │
     └─────────▶│ payment  │◀───────────┘
                └──────────┘

┌──────────┐     ┌──────────────┐     ┌──────────┐
│ category │────▶│film_category │◀────│   film   │
└──────────┘     └──────────────┘     └──────────┘
```

**Key Tables**:
- `actor`: Actor information
- `film`: Film catalog
- `customer`: Customer records
- `rental`: Rental transactions
- `payment`: Payment records
- `inventory`: Store inventory
- `category`: Film categories
- `film_actor`: Many-to-many relationship
- `film_category`: Many-to-many relationship

## Deployment Architecture

### Local Development

```
┌─────────────────────────────────────────┐
│         Developer Machine               │
│  ┌───────────────────────────────────┐  │
│  │  Python Virtual Environment       │  │
│  │  - Application Code               │  │
│  │  - Dependencies                   │  │
│  └───────────────────────────────────┘  │
│                  │                      │
│                  ▼                      │
│  ┌───────────────────────────────────┐  │
│  │  Local PostgreSQL                 │  │
│  │  - DVD Rental Database            │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Docker Deployment

```
┌─────────────────────────────────────────┐
│         Docker Host                     │
│  ┌───────────────────────────────────┐  │
│  │  App Container                    │  │
│  │  - Python 3.12                    │  │
│  │  - Application Code               │  │
│  │  - Streamlit Server               │  │
│  │  Port: 8501                       │  │
│  └───────────────────────────────────┘  │
│                  │                      │
│                  ▼                      │
│  ┌───────────────────────────────────┐  │
│  │  PostgreSQL Container (Optional)  │  │
│  │  - Database                       │  │
│  │  Port: 5432                       │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Streamlit Cloud Deployment

```
┌─────────────────────────────────────────────────────────┐
│              Streamlit Cloud                            │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Application Instance                             │  │
│  │  - Auto-deployed from GitHub                      │  │
│  │  - Secrets Management                             │  │
│  │  - HTTPS Endpoint                                 │  │
│  └───────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              External Services                          │
│  ┌──────────────────┐      ┌──────────────────────┐    │
│  │  OpenAI API      │      │  Cloud PostgreSQL    │    │
│  │  - Embeddings    │      │  (Supabase/Neon)     │    │
│  │  - GPT Models    │      │                      │    │
│  └──────────────────┘      └──────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## Security Considerations

### 1. API Key Management

**Best Practices**:
- ✅ Store keys in environment variables
- ✅ Use `.env` files for local development
- ✅ Never commit keys to version control
- ✅ Use secrets management in production
- ✅ Rotate keys regularly

### 2. SQL Injection Prevention

**Mitigations**:
- ✅ LLM generates SQL (not user input directly)
- ✅ Use parameterized queries where possible
- ✅ Validate generated SQL before execution
- ⚠️ Consider read-only database user for production

### 3. Database Access Control

**Recommendations**:
- Use least-privilege database accounts
- Restrict network access to database
- Enable SSL/TLS for database connections
- Implement connection pooling limits

### 4. Rate Limiting

**Considerations**:
- OpenAI API has rate limits
- Implement request throttling for production
- Cache common queries
- Monitor API usage

## Performance Optimization

### 1. Vector Search Optimization

**Current**:
- Retrieves top-2 schemas by default
- Uses cosine similarity

**Optimizations**:
- Adjust `k` parameter based on query complexity
- Implement caching for common queries
- Pre-filter by table relevance

### 2. Database Query Optimization

**Best Practices**:
- Ensure proper indexes on frequently queried columns
- Use EXPLAIN ANALYZE to profile queries
- Implement connection pooling
- Cache query results where appropriate

### 3. LLM Call Optimization

**Strategies**:
- Use smaller models (gpt-3.5-turbo) for simple queries
- Implement prompt caching
- Batch similar queries
- Monitor token usage

### 4. Caching Strategy

**Potential Caching Layers**:
```
Question → [Cache Check] → Vector Search → [Cache] → LLM → [Cache] → SQL
```

**Cache Candidates**:
- Vector search results (by question)
- Generated SQL (by question)
- Query results (with TTL)

## Future Enhancements

### Planned Improvements

1. **Query Optimization**
   - Analyze generated SQL for efficiency
   - Suggest index improvements

2. **Multi-Database Support**
   - Support MySQL, SQLite, etc.
   - Dialect-aware SQL generation

3. **Conversation Memory**
   - Remember context across queries
   - Support follow-up questions

4. **Feedback Loop**
   - Collect user feedback on SQL quality
   - Use feedback to improve system

5. **Advanced Evaluation**
   - SQL execution correctness
   - Result accuracy metrics
   - Latency tracking

## Conclusion

The AI Text-to-SQL Engine uses a modern RAG architecture combining vector search, language models, and agent-based reasoning. The modular design allows for easy extension and maintenance, while the evaluation framework ensures consistent quality.

Key architectural strengths:
- ✅ Modular and extensible
- ✅ Multiple interfaces (Web, CLI, API)
- ✅ Evaluation-driven development
- ✅ Production-ready deployment options

## Related Documentation

- [README.md](README.md) - Project overview
- [SETUP.md](SETUP.md) - Installation guide
- [USAGE.md](USAGE.md) - Usage examples
- [EVALUATION.md](EVALUATION.md) - Evaluation methodology

## References

- LangChain Documentation: https://python.langchain.com/
- Chroma Documentation: https://docs.trychroma.com/
- OpenAI API: https://platform.openai.com/docs
- PostgreSQL Documentation: https://www.postgresql.org/docs/
