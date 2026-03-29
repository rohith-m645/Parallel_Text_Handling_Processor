"""
============================================================
 PAGE 3 — Insights
------------------------------------------------------------
 - Sentiment distribution bar chart
 - Category-wise count summary
 - Top positive and negative texts
============================================================
"""

import streamlit as st
import matplotlib.pyplot as plt

st.header("📈 Insights")

if not st.session_state.get("show_results"):
    st.warning("No results yet. Please go to Upload page and process a file first.")
    st.stop()

df      = st.session_state.results_df
summary = df["Sentiment"].value_counts()

# ── Summary Counts ──
st.subheader("Sentiment Category Counts")
col1, col2 = st.columns(2)

with col1:
    for k, v in summary.items():
        st.write(f"**{k}** : {v:,}")

with col2:
    # Horizontal bar chart
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(summary.index, summary.values, color="steelblue")
    ax.set_xlabel("Count")
    ax.set_title("Sentiment Distribution")
    plt.tight_layout()
    st.pyplot(fig)

st.divider()

# ── Score Distribution ──
st.subheader("Score Distribution")
fig2, ax2 = plt.subplots(figsize=(8, 3))
ax2.hist(df["Score"], bins=20, color="coral", edgecolor="black")
ax2.set_xlabel("Sentiment Score")
ax2.set_ylabel("Frequency")
ax2.set_title("Score Distribution")
plt.tight_layout()
st.pyplot(fig2)

st.divider()

# ── Top Positive & Negative Texts ──
col3, col4 = st.columns(2)

with col3:
    st.subheader("🟢 Top Positive Texts")
    top_pos = df[df["Sentiment"] == "Positive"].nlargest(5, "Score")[["Text", "Score"]]
    st.dataframe(top_pos, use_container_width=True)

with col4:
    st.subheader("🔴 Top Negative Texts")
    top_neg = df[df["Sentiment"] == "Negative"].nsmallest(5, "Score")[["Text", "Score"]]
    st.dataframe(top_neg, use_container_width=True)
