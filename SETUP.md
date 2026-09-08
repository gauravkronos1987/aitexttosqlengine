# Setup Guide

This guide provides detailed instructions for setting up the AI Text-to-SQL Engine in various environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Database Setup](#database-setup)
- [Environment Configuration](#environment-configuration)
- [Docker Setup](#docker-setup)
- [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

- **Python 3.12 or higher**
  - Check version: `python --version`
  - Download from: https://www.python.org/downloads/

- **PostgreSQL** (optional for local development)
  - Version 12 or higher recommended
  - Download from: https://www.postgresql.org/download/

- **Git**
  - For cloning the repository
  - Download from: https://git-scm.com/downloads

### Required API Keys

- **OpenAI API Key**
  - Sign up at: https://platform.openai.com/
  - Navigate to API Keys section
  - Create a new secret key
  - Keep this key secure and never commit it to version control

## Local Development Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/aitexttosqlengine.git
cd aitexttosqlengine
```

### Step 2: Create Virtual Environment

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` in your terminal prompt indicating the virtual environment is active.

### Step 3: Install Dependencies

**For regular usage:**
```bash
pip install -e .
```

**For development (includes testing tools):**
```bash
pip install -e .[dev]
```

This will install all required packages:
- `chromadb` - Vector database for schema embeddings
- `langchain` - Agent orchestration framework
- `langchain-openai` - OpenAI integration for LangChain
- `langchain-chroma` - Chroma integration for LangChain
- `openai` - OpenAI API client
- `psycopg[binary]` - PostgreSQL database adapter
- `streamlit` - Web interface framework
- `python-dotenv` - Environment variable management
- `pandas` - Data manipulation for results display
- `tqdm` - Progress bars for evaluation

### Step 4: Verify Installation

```bash
# Check if the CLI is installed
aitexttosqlengine --help

# Or use the module directly
python -m aitexttosqlengine --help
```

## Database Setup

### Option 1: Use Sample DVD Rental Database

The project includes SQL files for the DVD Rental sample database.

**Initialize the database:**
```bash
aitexttosqlengine --init-db
```

This will:
1. Create all necessary tables (actor, film, customer, rental, etc.)
2. Load sample data from `export_202607281151.sql`
3. Set up foreign key relationships

### Option 2: Use Your Own PostgreSQL Database

**1. Create a new database:**
```sql
CREATE DATABASE your_database_name;
```

**2. Load your schema:**
```bash
psql -U your_username -d your_database_name -f your_schema.sql
```

**3. Update the connection string** (see Environment Configuration below)

### Option 3: Use Cloud Database

You can use cloud PostgreSQL services:
- **Supabase** (https://supabase.com/)
- **Neon** (https://neon.tech/)
- **AWS RDS**
- **Google Cloud SQL**
- **Azure Database for PostgreSQL**

Get the connection string from your provider and set it as `DATABASE_URL`.

## Environment Configuration

### Method 1: Using .env File (Recommended for Local Development)

Create a `.env` file in the project root:

```bash
# .env file
OPENAI_API_KEY=sk-your-openai-api-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/dvdrental
```

**Important:** Add `.env` to your `.gitignore` to prevent committing secrets:
```bash
echo ".env" >> .gitignore
```

### Method 2: Export Environment Variables

**On Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-your-openai-api-key-here"
$env:DATABASE_URL="postgresql://username:password@localhost:5432/dvdrental"
```

**On Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=sk-your-openai-api-key-here
set DATABASE_URL=postgresql://username:password@localhost:5432/dvdrental
```

**On macOS/Linux:**
```bash
export OPENAI_API_KEY="sk-your-openai-api-key-here"
export DATABASE_URL="postgresql://username:password@localhost:5432/dvdrental"
```

### Method 3: Streamlit Secrets (For Streamlit Cloud)

Create `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "sk-your-openai-api-key-here"
DATABASE_URL = "postgresql://username:password@host:5432/database"
```

## Docker Setup

### Build the Docker Image

```bash
docker build -t aitexttosqlengine .
```

### Run the Container

**Basic usage:**
```bash
docker run -p 8501:8501 \
  -e OPENAI_API_KEY="your-key" \
  -e DATABASE_URL="your-db-url" \
  aitexttosqlengine
```

**Using environment file:**
```bash
docker run -p 8501:8501 --env-file .env aitexttosqlengine
```

**With volume mounting (for development):**
```bash
docker run -p 8501:8501 \
  -v $(pwd)/src:/app/src \
  -e OPENAI_API_KEY="your-key" \
  -e DATABASE_URL="your-db-url" \
  aitexttosqlengine
```

Access the application at: `http://localhost:8501`

### Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=dvdrental
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Run with:
```bash
docker-compose up
```

## Streamlit Cloud Deployment

### Step 1: Prepare Your Repository

1. Ensure your code is pushed to GitHub
2. Create `.streamlit/secrets.toml` locally (don't commit it)
3. Add `requirements.txt` or ensure `pyproject.toml` is present

### Step 2: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `src/aitexttosqlengine/app.py`
6. Click "Advanced settings"
7. Add secrets:
   ```toml
   OPENAI_API_KEY = "your-key"
   DATABASE_URL = "your-database-url"
   ```
8. Click "Deploy"

### Step 3: Verify Deployment

- Wait for deployment to complete (usually 2-5 minutes)
- Test the application with sample queries
- Check the Evaluation Dashboard

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'aitexttosqlengine'"

**Solution:**
```bash
# Make sure you're in the project root directory
pip install -e .
```

#### 2. "OpenAI API Key not found"

**Solution:**
```bash
# Verify the environment variable is set
echo $OPENAI_API_KEY  # On macOS/Linux
echo %OPENAI_API_KEY%  # On Windows CMD
echo $env:OPENAI_API_KEY  # On Windows PowerShell

# If not set, export it again
export OPENAI_API_KEY="your-key"
```

#### 3. "Connection to database failed"

**Possible causes and solutions:**

- **PostgreSQL not running:**
  ```bash
  # Check if PostgreSQL is running
  # On macOS:
  brew services list
  # On Linux:
  sudo systemctl status postgresql
  # On Windows: Check Services app
  ```

- **Wrong connection string:**
  ```bash
  # Test connection with psql
  psql "postgresql://username:password@localhost:5432/dvdrental"
  ```

- **Database doesn't exist:**
  ```bash
  # Create the database
  createdb dvdrental
  # Or using psql:
  psql -U postgres -c "CREATE DATABASE dvdrental;"
  ```

#### 4. "Chroma DB initialization error"

**Solution:**
```bash
# Clear Chroma cache
rm -rf ./chroma_db  # On macOS/Linux
rmdir /s chroma_db  # On Windows

# Reinstall chromadb
pip uninstall chromadb
pip install chromadb
```

#### 5. "Streamlit command not found"

**Solution:**
```bash
# Ensure virtual environment is activated
# Then reinstall
pip install streamlit

# Or run directly with Python
python -m streamlit run src/aitexttosqlengine/app.py
```

#### 6. "SSL certificate verification failed" (OpenAI API)

**Solution:**
```bash
# Update certificates
pip install --upgrade certifi

# Or set environment variable to bypass (not recommended for production)
export CURL_CA_BUNDLE=""
```

### Getting Help

If you encounter issues not covered here:

1. Check the [GitHub Issues](https://github.com/yourusername/aitexttosqlengine/issues)
2. Review the [USAGE.md](USAGE.md) for usage examples
3. Check the [ARCHITECTURE.md](ARCHITECTURE.md) for system design details
4. Open a new issue with:
   - Your Python version
   - Operating system
   - Error message
   - Steps to reproduce

## Next Steps

After completing setup:

1. Read [USAGE.md](USAGE.md) for usage examples
2. Review [EVALUATION.md](EVALUATION.md) to understand metrics
3. Explore [ARCHITECTURE.md](ARCHITECTURE.md) for system design
4. Try the example queries in the README

## Verification Checklist

- [ ] Python 3.12+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] OpenAI API key configured
- [ ] Database connection working (if using database)
- [ ] CLI command works: `aitexttosqlengine --help`
- [ ] Streamlit app runs: `streamlit run src/aitexttosqlengine/app.py`
- [ ] Tests pass: `pytest` (if dev dependencies installed)

Congratulations! Your setup is complete. 🎉
