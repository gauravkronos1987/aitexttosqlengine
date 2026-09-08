# Usage Guide

This guide provides comprehensive examples and use cases for the AI Text-to-SQL Engine.

## Table of Contents

- [Getting Started](#getting-started)
- [Web Interface Usage](#web-interface-usage)
- [Command Line Interface](#command-line-interface)
- [Python API](#python-api)
- [Common Use Cases](#common-use-cases)
- [Advanced Features](#advanced-features)
- [Best Practices](#best-practices)
- [Tips for Better Results](#tips-for-better-results)

## Getting Started

Before using the application, ensure you have:
1. Completed the setup (see [SETUP.md](SETUP.md))
2. Set your `OPENAI_API_KEY` environment variable
3. Configured your database connection (optional)

## Web Interface Usage

### Starting the Web Interface

```bash
streamlit run src/aitexttosqlengine/app.py
```

The application will open in your default browser at `http://localhost:8501`.

### SQL Assistant Tab

The SQL Assistant is the main interface for converting natural language to SQL.

#### Basic Workflow

1. **Enter your question** in the text input field
2. **Click "Ask"** button
3. **View the generated SQL** in the code block
4. **See the query results** in the data table (if database is connected)

#### Example Session

**Question 1:** "Show me all actors"
```sql
-- Generated SQL:
SELECT * FROM actor;
```

**Question 2:** "Which actors have the last name 'DAVIS'?"
```sql
-- Generated SQL:
SELECT first_name, last_name 
FROM actor 
WHERE last_name = 'DAVIS';
```

**Question 3:** "List all films with 'LOVE' in the title"
```sql
-- Generated SQL:
SELECT title, description, release_year 
FROM film 
WHERE title LIKE '%LOVE%';
```

### Evaluation Dashboard Tab

Monitor the system's retrieval performance:

1. **Click "Run Retrieval Evaluation"** to evaluate the current system
2. **View metrics:**
   - **Hit Rate**: Percentage of queries where relevant tables were found
   - **MRR**: Mean Reciprocal Rank - quality of ranking
   - **Evaluated Questions**: Number of test cases evaluated
3. **Check last evaluation timestamp**

## Command Line Interface

### Basic Query Execution

```bash
# Simple query
aitexttosqlengine "Show me all customers"

# Query with specific criteria
aitexttosqlengine "List all films released in 2006"

# Complex query
aitexttosqlengine "What are the top 10 customers by total payment amount?"
```

### Database Initialization

```bash
# Initialize database with DVD Rental schema and data
aitexttosqlengine --init-db

# Initialize with custom database connection
aitexttosqlengine --init-db --dsn "postgresql://user:pass@localhost:5432/mydb"
```

### Custom Database Connection

```bash
# Use custom DSN for queries
aitexttosqlengine "Show all rentals" --dsn "postgresql://user:pass@host:5432/db"
```

### Output Examples

**Successful Query:**
```
Generated SQL:

SELECT * FROM customer LIMIT 10;

Result:
+-------------+------------+-----------+-------+
| customer_id | first_name | last_name | email |
+-------------+------------+-----------+-------+
| 1           | MARY       | SMITH     | ...   |
| 2           | PATRICIA   | JOHNSON   | ...   |
+-------------+------------+-----------+-------+
```

**Query with No Results:**
```
Generated SQL:

SELECT * FROM actor WHERE last_name = 'NONEXISTENT';

Query executed successfully, but returned no rows.
```

## Python API

### Basic Usage

```python
from aitexttosqlengine.engine import TextToSQLEngine

# Initialize the engine
engine = TextToSQLEngine()

# Generate SQL from natural language
question = "Show me all actors with last name SMITH"
sql = engine.generate_sql(question)
print(sql)
# Output: SELECT * FROM actor WHERE last_name = 'SMITH';
```

### With Database Execution

```python
from aitexttosqlengine.engine import TextToSQLEngine
from aitexttosqlengine.db import DatabaseManager

# Initialize components
engine = TextToSQLEngine()
db = DatabaseManager("postgresql://localhost/dvdrental")

# Generate and execute query
question = "What are the top 5 films by rental count?"
sql = engine.generate_sql(question)

if sql:
    headers, rows = db.query(sql)
    
    # Print results
    print(f"Columns: {headers}")
    for row in rows:
        print(row)
else:
    print("Could not generate SQL")

# Close connection
db.close()
```

### Custom Configuration

```python
from aitexttosqlengine.engine import TextToSQLEngine

# Use different models
engine = TextToSQLEngine(
    embedding_model="text-embedding-3-small",
    llm_model="gpt-4",  # Use GPT-4 for better accuracy
    temperature=0.0     # Deterministic output
)

sql = engine.generate_sql("Complex query here")
```

### Batch Processing

```python
from aitexttosqlengine.engine import TextToSQLEngine
from aitexttosqlengine.db import DatabaseManager

engine = TextToSQLEngine()
db = DatabaseManager("postgresql://localhost/dvdrental")

# List of questions to process
questions = [
    "Show all actors",
    "List films from 2006",
    "Top 10 customers by payment",
]

results = []
for question in questions:
    sql = engine.generate_sql(question)
    if sql:
        headers, rows = db.query(sql)
        results.append({
            "question": question,
            "sql": sql,
            "row_count": len(rows)
        })

# Print summary
for result in results:
    print(f"Q: {result['question']}")
    print(f"SQL: {result['sql']}")
    print(f"Rows: {result['row_count']}\n")

db.close()
```

## Common Use Cases

### 1. Finding Records by Criteria

**Use Case:** Find specific records matching certain conditions

**Examples:**

```python
# Find actors by last name
"Which actors have the last name SMITH?"
# → SELECT first_name, last_name FROM actor WHERE last_name = 'SMITH';

# Find films by year
"Show me all films released in 2006"
# → SELECT * FROM film WHERE release_year = 2006;

# Find customers by country
"List all customers from Canada"
# → SELECT * FROM customer WHERE country = 'Canada';
```

### 2. Aggregation and Statistics

**Use Case:** Calculate totals, averages, counts

**Examples:**

```python
# Count records
"How many films are in the database?"
# → SELECT COUNT(*) FROM film;

# Sum amounts
"What is the total payment amount?"
# → SELECT SUM(amount) FROM payment;

# Average calculation
"What is the average film rental duration?"
# → SELECT AVG(rental_duration) FROM film;
```

### 3. Joining Tables

**Use Case:** Combine data from multiple related tables

**Examples:**

```python
# Customer rentals
"Show me all rentals for customer John Doe"
# → SELECT r.* FROM rental r 
#   JOIN customer c ON r.customer_id = c.customer_id
#   WHERE c.first_name = 'John' AND c.last_name = 'Doe';

# Film categories
"List all action films"
# → SELECT f.title FROM film f
#   JOIN film_category fc ON f.film_id = fc.film_id
#   JOIN category c ON fc.category_id = c.category_id
#   WHERE c.name = 'Action';

# Actor films
"What films has actor PENELOPE GUINESS appeared in?"
# → SELECT f.title FROM film f
#   JOIN film_actor fa ON f.film_id = fa.film_id
#   JOIN actor a ON fa.actor_id = a.actor_id
#   WHERE a.first_name = 'PENELOPE' AND a.last_name = 'GUINESS';
```

### 4. Top N Queries

**Use Case:** Find top/bottom records by some metric

**Examples:**

```python
# Top customers
"Who are the top 10 customers by total payment amount?"
# → SELECT c.customer_id, c.first_name, c.last_name, SUM(p.amount) as total
#   FROM customer c
#   JOIN payment p ON c.customer_id = p.customer_id
#   GROUP BY c.customer_id, c.first_name, c.last_name
#   ORDER BY total DESC
#   LIMIT 10;

# Most rented films
"What are the top 5 most rented films?"
# → SELECT f.title, COUNT(r.rental_id) as rental_count
#   FROM film f
#   JOIN inventory i ON f.film_id = i.film_id
#   JOIN rental r ON i.inventory_id = r.inventory_id
#   GROUP BY f.film_id, f.title
#   ORDER BY rental_count DESC
#   LIMIT 5;
```

### 5. Date Range Queries

**Use Case:** Filter records by date ranges

**Examples:**

```python
# Rentals in date range
"Show me all rentals from January 2025"
# → SELECT * FROM rental 
#   WHERE rental_date >= '2025-01-01' 
#   AND rental_date < '2025-02-01';

# Payments this year
"What is the total payment amount for 2025?"
# → SELECT SUM(amount) FROM payment 
#   WHERE EXTRACT(YEAR FROM payment_date) = 2025;
```

### 6. Pattern Matching

**Use Case:** Search for partial matches in text fields

**Examples:**

```python
# Films with keyword in title
"Find all films with 'LOVE' in the title"
# → SELECT title FROM film WHERE title LIKE '%LOVE%';

# Actors with name pattern
"Show actors whose first name starts with 'JO'"
# → SELECT * FROM actor WHERE first_name LIKE 'JO%';
```

## Advanced Features

### Schema Search

The system uses vector similarity search to find relevant tables:

```python
from aitexttosqlengine.search import SchemaSearcher

searcher = SchemaSearcher()

# Search for relevant tables
results = searcher.search("customer payments", k=3)

for doc in results:
    print(f"Table: {doc.metadata['table']}")
    print(f"Content: {doc.page_content[:100]}...")
```

### Evaluation

Run retrieval evaluation to measure system performance:

```python
from aitexttosqlengine.run_search_evaluation import run_evaluation

# Run evaluation on test dataset
run_evaluation()

# Results saved to evaluation_metrics.json
```

### Custom Instructions

Modify the agent's behavior by customizing instructions:

```python
from aitexttosqlengine.engine import TextToSQLEngine

engine = TextToSQLEngine()

# Override default instructions
custom_instructions = """
You are a PostgreSQL expert specializing in the DVD rental domain.
Always include column aliases for better readability.
Prefer explicit JOINs over implicit joins.
"""

engine.instructions = custom_instructions

sql = engine.generate_sql("Show customer rentals")
```

## Best Practices

### 1. Be Specific in Questions

**Good:**
- "Show me the first name and last name of actors with last name SMITH"
- "List film titles released in 2006 ordered by title"

**Less Effective:**
- "Show me actors"
- "Get some films"

### 2. Use Domain-Specific Terms

**Good:**
- "What is the total rental revenue?" (uses domain term "rental")
- "Show me customer payment history"

**Less Effective:**
- "How much money did we make?" (vague)
- "Show transactions" (ambiguous term)

### 3. Specify Sorting and Limits

**Good:**
- "Top 10 customers by payment amount"
- "List films ordered by title ascending"

**Less Effective:**
- "Show customers by payment" (unclear ordering)

### 4. Handle NULL Values

**Good:**
- "Show customers who have made payments"
- "Find films without a description"

### 5. Use Proper Date Formats

**Good:**
- "Rentals from January 2025"
- "Payments between 2025-01-01 and 2025-12-31"

**Less Effective:**
- "Rentals from last month" (relative dates may not work)

## Tips for Better Results

### Understanding the Database Schema

Before asking questions, understand what tables and columns exist:

**Available Tables in DVD Rental Database:**
- `actor` - Actor information
- `film` - Film catalog
- `customer` - Customer records
- `rental` - Rental transactions
- `payment` - Payment records
- `inventory` - Store inventory
- `category` - Film categories
- `film_actor` - Film-actor relationships
- `film_category` - Film-category relationships

### Common Pitfalls to Avoid

1. **Asking about non-existent tables**
   - ❌ "Show me all products" (no products table)
   - ✅ "Show me all films"

2. **Using wrong column names**
   - ❌ "Find customers by name" (ambiguous - first_name or last_name?)
   - ✅ "Find customers by first name"

3. **Ambiguous aggregations**
   - ❌ "Show customer totals" (total what?)
   - ✅ "Show total payment amount per customer"

4. **Complex multi-step logic**
   - ❌ "Show customers who rented action films but not comedies in 2025"
   - ✅ Break into simpler queries or be very explicit

### Iterative Refinement

If the first query isn't perfect:

1. **Review the generated SQL**
2. **Identify what needs adjustment**
3. **Rephrase your question** with more specifics
4. **Try again**

**Example:**

First attempt: "Show customer payments"
```sql
SELECT * FROM payment;  -- Too broad
```

Refined: "Show total payment amount per customer, ordered by amount descending"
```sql
SELECT customer_id, SUM(amount) as total_amount 
FROM payment 
GROUP BY customer_id 
ORDER BY total_amount DESC;  -- Better!
```

### Performance Considerations

For large databases:

1. **Always use LIMIT** for exploratory queries
   - "Show me 10 sample films"
   
2. **Be specific about columns** instead of SELECT *
   - "Show film title and release year" vs "Show all film data"

3. **Use indexes** (ensure your database has proper indexes)

4. **Avoid expensive operations** in questions
   - Be cautious with LIKE '%pattern%' on large tables

## Example Workflows

### Workflow 1: Customer Analysis

```python
# Step 1: Find high-value customers
"Who are the top 20 customers by total payment amount?"

# Step 2: Analyze their rental patterns
"Show rental history for customer ID 123"

# Step 3: Identify preferences
"What film categories does customer 123 rent most?"
```

### Workflow 2: Inventory Management

```python
# Step 1: Check inventory levels
"How many copies of each film do we have?"

# Step 2: Find popular films
"Which films have been rented more than 20 times?"

# Step 3: Identify gaps
"Which films have never been rented?"
```

### Workflow 3: Revenue Analysis

```python
# Step 1: Total revenue
"What is the total payment amount for all time?"

# Step 2: Revenue by period
"Show monthly revenue for 2025"

# Step 3: Revenue by category
"What is the total rental revenue per film category?"
```

## Troubleshooting Common Issues

### Issue: Generated SQL is incorrect

**Solution:**
- Make your question more specific
- Include table names if known
- Specify exact column names
- Review the database schema

### Issue: Query returns no results

**Solution:**
- Check if data exists: "How many records are in the table?"
- Verify filter criteria
- Check for case sensitivity in string comparisons

### Issue: Query is too slow

**Solution:**
- Add LIMIT clause to your question
- Be more specific to reduce join complexity
- Check database indexes

### Issue: "Could not extract SQL from response"

**Solution:**
- Rephrase your question more clearly
- Ensure question relates to database operations
- Check if OpenAI API is responding correctly

## Next Steps

- Review [EVALUATION.md](EVALUATION.md) to understand how the system is evaluated
- Check [ARCHITECTURE.md](ARCHITECTURE.md) to learn about the system design
- Explore the [tests/](tests/) directory for more code examples
- Experiment with your own questions and datasets

## Getting Help

If you need assistance:
1. Check the [SETUP.md](SETUP.md) for configuration issues
2. Review this guide for usage examples
3. Open an issue on GitHub with your question and example
4. Include the generated SQL and expected behavior

Happy querying! 🚀
