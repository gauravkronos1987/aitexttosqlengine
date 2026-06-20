
import os
import streamlit as st

from aitexttosqlengine.engine import TextToSQLEngine
from aitexttosqlengine.db import DatabaseManager

# Read secrets from Streamlit's secrets store (or fall back to defaults)
# Keys in .streamlit/secrets.toml: `open_api_key` and `database_url`.
openai_key = st.secrets.get("open_api_key")
if openai_key:
    os.environ.setdefault("OPENAI_API_KEY", openai_key)

database_url = st.secrets.get("database_url") or os.environ.get("DATABASE_URL")
if not database_url:
    # fallback used for local testing
    database_url = "postgresql://user:pswd@localhost:5432/faq"

engine = TextToSQLEngine()
db_manager = DatabaseManager(database_url)
# Initialize DB if possible, but don't crash the app on startup
try:
    db_manager.initialize_schema()
    db_manager.seed_data()
except Exception:
    st.warning("Database initialization or seeding failed; continuing without initialization.")

st.title("Natural Language SQL Assistant")

user_input = st.text_input("Enter your query:")
ask = st.button("Ask")

if ask:
    if not user_input:
        st.error("Please enter a query.")
    else:
        with st.spinner("Processing..."):
            generatedsql = engine.generate_sql(user_input)
            if generatedsql:
                st.write("**Generated SQL:**")
                st.code(generatedsql, language="sql")
                try:
                    headers, rows = db_manager.query(generatedsql)
                    st.success("Query executed!")
                    if rows:
                        import pandas as pd

                        df = pd.DataFrame(rows, columns=headers)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("Query returned no results.")
                except Exception as e:
                    st.error(f"Query failed: {e}")
            else:
                st.error("Could not extract SQL from response.")


