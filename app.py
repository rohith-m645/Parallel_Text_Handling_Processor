"""
============================================================
 PARALLEL TEXT HANDLING PROCESSOR
 Main Entry Point
============================================================
 Run with: streamlit run app.py
============================================================
"""

import streamlit as st

st.set_page_config(
    page_title="Parallel Text Processor",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📃 Parallel Text Handling Processor")
st.markdown("""
Welcome! Use the sidebar to navigate between pages.

| Page | Description |
|---|---|
| 📂 Upload | Upload your file and start processing |
| 📊 Results | View processed data table |
| 📈 Insights | View sentiment chart and summary |
| 📧 Email | Send report via email |
""")

# ── Session State Init (shared across all pages) ──
if "show_results" not in st.session_state:
    st.session_state.show_results = False

if "results_df" not in st.session_state:
    st.session_state.results_df = None

if "small_file" not in st.session_state:
    st.session_state.small_file = None
