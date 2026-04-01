"""
============================================================
 PARALLEL TEXT HANDLING PROCESSOR
 Main Entry Point — Redesigned UI
============================================================
 Run with: streamlit run app.py
============================================================
"""

import streamlit as st

st.set_page_config(
    page_title="SentimentPro — Analytics Suite",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

from module.style import apply_theme, render_sidebar

apply_theme()
render_sidebar(active="")

# ── Session State Init ──
if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "results_df" not in st.session_state:
    st.session_state.results_df = None
if "small_file" not in st.session_state:
    st.session_state.small_file = None

# ── Home Page ──
st.markdown("""
<h1 style="margin-bottom:0.2rem;">📃 Parallel Text Processor</h1>
<p style="color:#7a7990; font-size:13px; font-family:'DM Mono',monospace; margin-bottom:1.8rem;">
    Upload a file · Run 1M-row parallel sentiment analysis · Export & Email
</p>
""", unsafe_allow_html=True)

# ── Stat Row — no deltas, unique border colours via CSS nth-child ──
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Row Limit",  "1,000,000")
with c2: st.metric("Formats",    "5 types")
with c3: st.metric("Max Upload", "1 GB")
with c4: st.metric("Engine",     "VADER")

st.divider()

st.markdown("""
<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; max-width:640px;">
    <div style="background:#16161f; border:0.5px solid rgba(255,255,255,0.07);
                border-radius:10px; padding:14px 16px;">
        <div style="font-family:'DM Mono',monospace; font-size:9px;
                    color:#7a7990; letter-spacing:0.1em; margin-bottom:5px;">PAGE 1</div>
        <div style="color:#f0eff8; font-size:13px; font-weight:500;">📂 Upload</div>
        <div style="color:#7a7990; font-size:11px; margin-top:3px;">Upload file and start processing</div>
    </div>
    <div style="background:#16161f; border:0.5px solid rgba(255,255,255,0.07);
                border-radius:10px; padding:14px 16px;">
        <div style="font-family:'DM Mono',monospace; font-size:9px;
                    color:#7a7990; letter-spacing:0.1em; margin-bottom:5px;">PAGE 2</div>
        <div style="color:#f0eff8; font-size:13px; font-weight:500;">📊 Results</div>
        <div style="color:#7a7990; font-size:11px; margin-top:3px;">View processed data table</div>
    </div>
    <div style="background:#16161f; border:0.5px solid rgba(255,255,255,0.07);
                border-radius:10px; padding:14px 16px;">
        <div style="font-family:'DM Mono',monospace; font-size:9px;
                    color:#7a7990; letter-spacing:0.1em; margin-bottom:5px;">PAGE 3</div>
        <div style="color:#f0eff8; font-size:13px; font-weight:500;">📈 Insights</div>
        <div style="color:#7a7990; font-size:11px; margin-top:3px;">Charts, scores and top texts</div>
    </div>
    <div style="background:#16161f; border:0.5px solid rgba(255,255,255,0.07);
                border-radius:10px; padding:14px 16px;">
        <div style="font-family:'DM Mono',monospace; font-size:9px;
                    color:#7a7990; letter-spacing:0.1em; margin-bottom:5px;">PAGE 4</div>
        <div style="color:#f0eff8; font-size:13px; font-weight:500;">📧 Email</div>
        <div style="color:#7a7990; font-size:11px; margin-top:3px;">Send report via Gmail SMTP</div>
    </div>
</div>
""", unsafe_allow_html=True)
