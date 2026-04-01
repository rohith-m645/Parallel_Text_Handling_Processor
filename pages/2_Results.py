"""
============================================================
 PAGE 2 — Results  (Redesigned UI)
------------------------------------------------------------
 - View processed data table (first 1,000 rows)
 - Download small Excel report (50k rows)
 - Generate and download full 1M Excel report
============================================================
"""

import streamlit as st
from module.search import export_small_excel, export_1M_excel
from module.style import apply_theme, render_sidebar

apply_theme()
render_sidebar(active="results")

# ── Guard ──
if not st.session_state.get("show_results"):
    st.markdown("""
    <div style="
        background: rgba(245,166,35,0.06);
        border: 0.5px solid rgba(245,166,35,0.3);
        border-radius: 10px; padding: 20px 24px; margin-top:2rem;
    ">
        <div style="font-family:'Syne',sans-serif; font-weight:600;
                    color:#f5a623; margin-bottom:4px;">No results yet</div>
        <div style="font-size:13px; color:#7a7990;">
            Go to the <strong style="color:#f0eff8;">Upload</strong> page and process a file first.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df = st.session_state.results_df

# ── Page Header ──
st.markdown("""
<h1 style="margin-bottom:0.25rem;">📊 Results</h1>
<p style="color:#7a7990; font-size:13px; font-family:'DM Mono',monospace; margin-bottom:1.5rem;">
    Processed data table — preview, filter and export
</p>
""", unsafe_allow_html=True)

# ── Summary Stats ──
total   = len(df)
pos     = len(df[df["Sentiment"] == "Positive"]) if "Sentiment" in df.columns else 0
neg     = len(df[df["Sentiment"] == "Negative"]) if "Sentiment" in df.columns else 0
neu     = total - pos - neg

c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Total Rows", f"{total:,}")
with c2: st.metric("Positive",   f"{pos:,}")
with c3: st.metric("Negative",   f"{neg:,}")
with c4: st.metric("Other",      f"{neu:,}")

st.divider()

# ── Data Preview ──
st.markdown(f"""
<div style="
    display:flex; align-items:center; justify-content:space-between;
    margin-bottom:0.75rem;
">
    <div style="font-family:'Syne',sans-serif; font-weight:600;
                color:#f0eff8; font-size:14px;">
        Preview — first 1,000 of {total:,} rows
    </div>
    <div style="font-family:'DM Mono',monospace; font-size:10px;
                color:#7a7990; letter-spacing:0.06em;">
        TEXT · SCORE · SENTIMENT
    </div>
</div>
""", unsafe_allow_html=True)

st.dataframe(
    df.head(1000),
    use_container_width=True,
    height=380
)

st.divider()

# ── Download Section ──
st.markdown("""
<div style="font-family:'Syne',sans-serif; font-weight:600;
            color:#f0eff8; font-size:14px; margin-bottom:1rem;">
    📥 Download Reports
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="
        background:#16161f; border:0.5px solid rgba(255,255,255,0.07);
        border-radius:10px; padding:16px; margin-bottom:12px;
    ">
        <div style="font-family:'DM Mono',monospace; font-size:10px;
                    color:#7a7990; letter-spacing:0.08em; margin-bottom:6px;">SMALL REPORT</div>
        <div style="color:#f0eff8; font-size:13px; margin-bottom:4px;">50,000 rows · Excel</div>
        <div style="font-size:11px; color:#7a7990;">Safe for email (~10 MB)</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⚙️ Generate Small Report (50k rows)", use_container_width=True):
        with st.spinner("Creating Excel file…"):
            small_file = export_small_excel(df, rows=50000)
            st.session_state.small_file = small_file

        with open(small_file, "rb") as f:
            st.download_button(
                "📥 Download Small Report",
                f,
                file_name=small_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

with col2:
    st.markdown("""
    <div style="
        background:#16161f; border:0.5px solid rgba(255,255,255,0.07);
        border-radius:10px; padding:16px; margin-bottom:12px;
    ">
        <div style="font-family:'DM Mono',monospace; font-size:10px;
                    color:#7a7990; letter-spacing:0.08em; margin-bottom:6px;">FULL REPORT</div>
        <div style="color:#f0eff8; font-size:13px; margin-bottom:4px;">1,000,000 rows · Excel</div>
        <div style="font-size:11px; color:#7a7990;">Write-only mode (~2 min)</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⚙️ Generate Full Report", use_container_width=True):
        with st.spinner("Building 1M row Excel… (~2 minutes)"):
            full_file = export_1M_excel(df.values.tolist())

        with open(full_file, "rb") as f:
            st.download_button(
                "📥 Download Full Report",
                f,
                file_name=full_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
