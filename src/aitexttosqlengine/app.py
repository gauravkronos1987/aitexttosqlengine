import streamlit as st

from aitexttosqlengine.engine import TextToSQLEngine
from aitexttosqlengine.db import DatabaseManager
from aitexttosqlengine.cli import format_table

engine = TextToSQLEngine()
db_manager = DatabaseManager("postgresql://user:pswd@localhost:5432/faq")

st.title("Course Assistant")

user_input = st.text_input("Enter your query:")

if st.button("Ask"):
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


