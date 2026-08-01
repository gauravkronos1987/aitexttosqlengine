import os
import streamlit as st
import pandas as pd
import json

from aitexttosqlengine.engine import TextToSQLEngine
from aitexttosqlengine.db import DatabaseManager, resolve_database_url
from aitexttosqlengine.evaluation import evaluate
from aitexttosqlengine.search import SchemaSearcher
from pathlib import Path


# ---------------------------------------------------------------------------
# Setup (unchanged)
# ---------------------------------------------------------------------------
openai_key = st.secrets.get("OPENAI_API_KEY")
if openai_key:
    os.environ.setdefault("OPENAI_API_KEY", openai_key)

engine = TextToSQLEngine()
database_url = resolve_database_url(getattr(st, "secrets", None), os.environ)

if database_url:
    db_manager = DatabaseManager(database_url)
else:
    db_manager = None


PROJECT_ROOT = Path(__file__).resolve().parents[2]
METRICS_FILE = PROJECT_ROOT / "evaluation_metrics.json"


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
st.set_page_config(page_title="AI SQL Assistant", layout="wide")

page = st.sidebar.radio(
    "Navigation",
    ["SQL Assistant", "Monitoring Dashboard"],
)

if db_manager is None and page == "SQL Assistant":
    st.info("No database URL is configured. Database initialization is skipped; "
            "SQL execution will be unavailable until a database is configured.")


# ---------------------------------------------------------------------------
# Page 1: SQL Assistant (your existing logic)
# ---------------------------------------------------------------------------
def render_sql_assistant():
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
                    if db_manager is None:
                        st.info("Database execution is unavailable because no database URL "
                                "is configured in this deployment.")
                    else:
                        try:
                            if generatedsql.startswith("UPDATE"):
                                db_manager.execute(generatedsql)
                                st.success("Update executed!")
                            else:
                                headers, rows = db_manager.query(generatedsql)
                                st.success("Query executed!")
                                if rows:
                                    df = pd.DataFrame(rows, columns=headers)
                                    st.dataframe(df, use_container_width=True)
                                else:
                                    st.info("Query returned no results.")
                        except Exception as e:
                            st.error(f"Query failed: {e}")
                else:
                    st.error("Could not extract SQL from response.")


# ---------------------------------------------------------------------------
# Page 2: Monitoring Dashboard
# ---------------------------------------------------------------------------
def render_monitoring_dashboard():
    st.title("Evaluation Dashboard")
    
    metrics = load_evaluation_metrics()

    if metrics is None:
        st.warning(
            "Evaluation metrics are not available. "
            "Run the evaluation script first."
        )
        return

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Hit Rate",
        f"{metrics['hit_rate']:.2%}",
    )

    col2.metric(
        "MRR",
        f"{metrics['mrr']:.3f}",
    )

    col3.metric(
        "Evaluated Questions",
        metrics["evaluated_questions"],
    )

    st.caption(
        f"Last evaluated: {metrics['evaluated_at']}"
    )


def load_evaluation_metrics() -> dict | None:
    if not METRICS_FILE.exists():
        return None

    try:
        return json.loads(
            METRICS_FILE.read_text(encoding="utf-8")
        )
    except (json.JSONDecodeError, OSError):
        return None
# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
if page == "SQL Assistant":
    render_sql_assistant()
else:
    render_monitoring_dashboard()