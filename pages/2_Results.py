"""
============================================================
 PAGE 2 — Results
------------------------------------------------------------
 - View processed data table (first 1,000 rows)
 - Download small Excel report (50k rows)
 - Generate and download full 1M Excel report
============================================================
"""

import streamlit as st
from module.search import export_small_excel, export_1M_excel

st.header("📊 Results")

if not st.session_state.get("show_results"):
    st.warning("No results yet. Please go to Upload page and process a file first.")
    st.stop()

df = st.session_state.results_df

# ── Preview Table ──
st.subheader(f"Preview — First 1,000 of {len(df):,} rows")
st.dataframe(df.head(1000), use_container_width=True)

st.divider()

# ── Small Excel Download (50k rows) ──
st.subheader("📥 Download Reports")

col1, col2 = st.columns(2)

with col1:
    if st.button("Generate Small Report (50k rows)"):
        with st.spinner("Creating Excel..."):
            small_file = export_small_excel(df, rows=50000)
            st.session_state.small_file = small_file  # Save for email page

        with open(small_file, "rb") as f:
            st.download_button(
                "📥 Download Small Report",
                f,
                file_name=small_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

with col2:
    # ── Full 1M Excel Download ──
    if st.button("⚙️ Generate Full 1M Report"):
        with st.spinner("Building 1M row Excel... (~2 minutes)"):
            full_file = export_1M_excel(df.values.tolist())

        with open(full_file, "rb") as f:
            st.download_button(
                "📥 Download Full 1M Report",
                f,
                file_name=full_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
