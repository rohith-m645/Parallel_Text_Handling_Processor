"""
============================================================
 PAGE 1 — Upload & Process  (Redesigned UI)
------------------------------------------------------------
 - Upload TXT, CSV, XLSX, DOCX, PDF
 - Select file to process
 - Trigger 1M row parallel processing pipeline
============================================================
"""

import streamlit as st
import pandas as pd
from module.loader import read_file
from module.style import apply_theme, render_sidebar
from pipeline import run_pipeline

apply_theme()
render_sidebar(active="upload")

# ── Page Header ──
st.markdown("""
<h1 style="margin-bottom:0.25rem;">📂 Upload & Process</h1>
<p style="color:#7a7990; font-size:13px; font-family:'DM Mono',monospace; margin-bottom:1.5rem;">
    Drop a file and run the 1M-row parallel sentiment pipeline
</p>
""", unsafe_allow_html=True)

# ── Stat Row ──

st.divider()

# ── File Upload ──
uploaded_files = st.file_uploader(
    "Drop your file here — or click to browse",
    type=["txt", "csv", "xlsx", "docx", "pdf"],
    accept_multiple_files=True,
    help="Supports TXT, CSV, XLSX, DOCX, PDF — up to 1 GB"
)

lines = []

if uploaded_files:
    file_names    = [f.name for f in uploaded_files]
    selected_file = st.selectbox("📄 Select file to process", file_names)

    for f in uploaded_files:
        if f.name == selected_file:
            ext     = f.name.split(".")[-1].lower()
            content = read_file(f.name, f.read(), ext)

            if isinstance(content, pd.DataFrame):
                lines = content.astype(str).agg(" ".join, axis=1).tolist()
            else:
                lines = content.splitlines()

    # ── File Info Card ──
    st.markdown(f"""
    <div style="
        background: #16161f;
        border: 0.5px solid rgba(255,255,255,0.07);
        border-radius: 12px;
        padding: 16px 20px;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 14px;
    ">
        <div style="
            width:38px; height:38px; border-radius:8px;
            background:rgba(62,207,170,0.1);
            border:0.5px solid rgba(62,207,170,0.25);
            display:flex; align-items:center; justify-content:center;
            font-family:'DM Mono',monospace; font-size:9px; color:#3ecfaa;
            font-weight:500;
        ">{selected_file.split('.')[-1].upper()}</div>
        <div>
            <div style="font-weight:500; color:#f0eff8; font-size:14px;">{selected_file}</div>
            <div style="font-family:'DM Mono',monospace; font-size:11px; color:#7a7990;">
                {len(lines):,} lines detected
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Process Button ──
    if st.button("🚀 Start Processing ", type="primary", use_container_width=True):
        if not lines:
            st.error("❌ No content found in file.")
        else:
            with st.spinner("Running parallel pipeline across CPU cores…"):
                df = run_pipeline(lines)

            st.session_state.results_df   = df
            st.session_state.show_results = True
            st.session_state.small_file   = None  # reset cached file

            st.success(f"✅ Processing complete — {len(df):,} rows analysed. Navigate to Results or Insights.")

else:
    # ── Empty state ──
    st.markdown("""
    <div style="
        background: rgba(124,108,250,0.04);
        border: 1.5px dashed rgba(124,108,250,0.2);
        border-radius: 12px;
        padding: 3rem 2rem;
        text-align: center;
        margin-top: 1rem;
    ">
        <div style="font-size:2rem; margin-bottom:1rem;">📁</div>
        <div style="font-family:'Syne',sans-serif; font-size:15px; font-weight:600;
                    color:#f0eff8; margin-bottom:6px;">No file uploaded yet</div>
        <div style="font-size:12px; color:#7a7990;">
            Supported: .txt &nbsp;·&nbsp; .csv &nbsp;·&nbsp; .xlsx &nbsp;·&nbsp; .docx &nbsp;·&nbsp; .pdf
        </div>
    </div>
    """, unsafe_allow_html=True)
