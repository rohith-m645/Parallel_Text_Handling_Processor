"""
============================================================
 PAGE 1 — Upload & Process
------------------------------------------------------------
 - Upload TXT, CSV, XLSX, DOCX, PDF
 - Select file to process
 - Trigger 1M row parallel processing pipeline
============================================================
"""

import streamlit as st
import pandas as pd
from module.loader import read_file
from pipeline import run_pipeline

st.header("📂 Upload & Process")

# ── File Upload ──
uploaded_files = st.file_uploader(
    "Upload your file(s)",
    type=["txt", "csv", "xlsx", "docx", "pdf"],
    accept_multiple_files=True
)

lines = []

if uploaded_files:
    file_names    = [f.name for f in uploaded_files]
    selected_file = st.selectbox("Select file to process", file_names)

    for f in uploaded_files:
        if f.name == selected_file:
            ext     = f.name.split(".")[-1].lower()
            content = read_file(f.name, f.read(), ext)

            # Convert DataFrame rows to strings or split text into lines
            if isinstance(content, pd.DataFrame):
                lines = content.astype(str).agg(" ".join, axis=1).tolist()
            else:
                lines = content.splitlines()

    st.info(f"📄 **{selected_file}** loaded — {len(lines):,} lines found")

    # ── Process Button ──
    if st.button("🚀 Start Processing 1M Rows"):
        if not lines:
            st.error("No content found in file.")
        else:
            with st.spinner("Running parallel pipeline..."):
                df = run_pipeline(lines)

            # Save results to session state (shared across pages)
            st.session_state.results_df   = df
            st.session_state.show_results = True
            st.success("✅ Processing complete! Go to Results or Insights page.")

else:
    st.warning("Please upload a file to begin.")
