"""
============================================================
 PAGE 3 — Insights  (Redesigned UI)
------------------------------------------------------------
 - Sentiment distribution bar chart  (dark theme)
 - Score histogram                   (dark theme)
 - Top positive and negative texts
 - Category breakdown table
============================================================
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from module.style import apply_theme, render_sidebar

apply_theme()
render_sidebar(active="insights")

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

df      = st.session_state.results_df
summary = df["Sentiment"].value_counts()
total   = len(df)

# ── Dark chart style ──
DARK_BG    = "#16161f"
DARK_AX    = "#1e1e2a"
TEXT_COLOR = "#c8c7d4"
MUTED      = "#7a7990"
ACCENT     = "#7c6cfa"
GREEN      = "#3ecfaa"
RED        = "#fa6c6c"
AMBER      = "#f5a623"

PALETTE = {
    "Positive":         GREEN,
    "Negative":         RED,
    "Neutral":          ACCENT,
    "Refund Issue":     AMBER,
    "Delivery Issue":   "#85b7eb",
    "Product Damage":   "#f09595",
    "Customer Service": "#ed93b1",
    "Price Complaint":  "#ef9f27",
    "Scam Risk":        "#e24b4a",
    "Safety Issue":     "#fa6c6c",
    "Spam":             "#888780",
    "Sarcasm":          "#b4b2a9",
}

def get_color(label):
    return PALETTE.get(label, ACCENT)

def style_ax(ax, fig):
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_AX)
    ax.tick_params(colors=MUTED, labelsize=10)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.title.set_color(TEXT_COLOR)
    for spine in ax.spines.values():
        spine.set_edgecolor((1.0, 1.0, 1.0, 0.07))  # Changed from "rgba(255,255,255,0.07)"
        spine.set_linewidth(0.5)
    ax.grid(axis="x", color=(1.0, 1.0, 1.0, 0.04), linewidth=0.5)  # Changed from "rgba(255,255,255,0.04)"
    ax.set_axisbelow(True)

# ── Page Header ──
st.markdown("""
<h1 style="margin-bottom:0.25rem;">📈 Insights</h1>
<p style="color:#7a7990; font-size:13px; font-family:'DM Mono',monospace; margin-bottom:1.5rem;">
    Sentiment distribution, score histogram and top texts
</p>
""", unsafe_allow_html=True)

# ── KPI Row ──
c1, c2, c3, c4 = st.columns(4)
pos_count = summary.get("Positive", 0)
neg_count = summary.get("Negative", 0)
neu_count = summary.get("Neutral",  0)
avg_score = df["Score"].mean() if "Score" in df.columns else 0

with c1: st.metric("Positive",  f"{pos_count:,}")
with c2: st.metric("Negative",  f"{neg_count:,}")
with c3: st.metric("Neutral",   f"{neu_count:,}")
with c4: st.metric("Avg Score", f"{avg_score:+.2f}")

st.divider()

# ── Row 1: Sentiment bar + Score histogram ──
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif; font-weight:600;
                color:#f0eff8; font-size:14px; margin-bottom:0.75rem;">
        Sentiment Distribution
    </div>
    """, unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(6, max(3, len(summary) * 0.55)))
    colors  = [get_color(k) for k in summary.index]
    bars    = ax.barh(summary.index, summary.values, color=colors, height=0.55)

    # Value labels
    for bar, val in zip(bars, summary.values):
        ax.text(
            bar.get_width() + max(summary.values) * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{val:,}", va="center", ha="left",
            color=TEXT_COLOR, fontsize=9,
            fontfamily="monospace"
        )

    ax.set_xlabel("Count", fontsize=10)
    style_ax(ax, fig)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif; font-weight:600;
                color:#f0eff8; font-size:14px; margin-bottom:0.75rem;">
        Score Distribution
    </div>
    """, unsafe_allow_html=True)

    if "Score" in df.columns:
        fig2, ax2 = plt.subplots(figsize=(6, 3.5))

        n, bins, patches = ax2.hist(df["Score"], bins=25, edgecolor="none")

        # Colour by sentiment zone
        bin_centers = 0.5 * (bins[:-1] + bins[1:])
        for patch, center in zip(patches, bin_centers):
            if center > 0:
                patch.set_facecolor(GREEN)
                patch.set_alpha(0.75)
            elif center < 0:
                patch.set_facecolor(RED)
                patch.set_alpha(0.75)
            else:
                patch.set_facecolor(ACCENT)
                patch.set_alpha(0.75)

        ax2.axvline(x=0, color=MUTED, linewidth=0.8, linestyle="--")
        ax2.axvline(x=avg_score, color=AMBER, linewidth=1.2, linestyle="-",
                    label=f"avg {avg_score:+.2f}")
        ax2.legend(fontsize=9, facecolor=DARK_AX, edgecolor="none",
                   labelcolor=TEXT_COLOR)
        ax2.set_xlabel("Sentiment Score", fontsize=10)
        ax2.set_ylabel("Frequency", fontsize=10)

        style_ax(ax2, fig2)
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

st.divider()

# ── Category Breakdown ──
st.markdown("""
<div style="font-family:'Syne',sans-serif; font-weight:600;
            color:#f0eff8; font-size:14px; margin-bottom:0.75rem;">
    Category Breakdown
</div>
""", unsafe_allow_html=True)

cat_df = summary.reset_index()
cat_df.columns = ["Category", "Count"]
cat_df["Share %"] = (cat_df["Count"] / total * 100).round(2)
cat_df = cat_df.sort_values("Count", ascending=False)
st.dataframe(cat_df, use_container_width=True, hide_index=True, height=280)

st.divider()

# ── Top Positive & Negative ──
col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div style="
        background:#16161f; border:0.5px solid rgba(62,207,170,0.2);
        border-top:2px solid #3ecfaa;
        border-radius:10px; padding:16px; margin-bottom:1rem;
    ">
        <div style="font-family:'DM Mono',monospace; font-size:10px;
                    color:#3ecfaa; letter-spacing:0.08em; margin-bottom:10px;">
            TOP POSITIVE TEXTS
        </div>
    """, unsafe_allow_html=True)

    top_pos = df[df["Sentiment"] == "Positive"].nlargest(5, "Score")[["Text", "Score"]]
    if not top_pos.empty:
        for _, row in top_pos.iterrows():
            truncated = str(row["Text"])[:80] + "…" if len(str(row["Text"])) > 80 else str(row["Text"])
            st.markdown(f"""
            <div style="
                display:flex; justify-content:space-between; align-items:center;
                padding:7px 0; border-bottom:0.5px solid rgba(255,255,255,0.04);
            ">
                <span style="font-size:12px; color:#c8c7d4; flex:1; margin-right:12px;">{truncated}</span>
                <span style="
                    font-family:'DM Mono',monospace; font-size:10px;
                    background:rgba(62,207,170,0.12); color:#3ecfaa;
                    padding:2px 8px; border-radius:4px; flex-shrink:0;
                ">{row['Score']:+.2f}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:#7a7990; font-size:12px;'>No positive results found.</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="
        background:#16161f; border:0.5px solid rgba(250,108,108,0.2);
        border-top:2px solid #fa6c6c;
        border-radius:10px; padding:16px; margin-bottom:1rem;
    ">
        <div style="font-family:'DM Mono',monospace; font-size:10px;
                    color:#fa6c6c; letter-spacing:0.08em; margin-bottom:10px;">
            TOP NEGATIVE TEXTS
        </div>
    """, unsafe_allow_html=True)

    top_neg = df[df["Sentiment"] == "Negative"].nsmallest(5, "Score")[["Text", "Score"]]
    if not top_neg.empty:
        for _, row in top_neg.iterrows():
            truncated = str(row["Text"])[:80] + "…" if len(str(row["Text"])) > 80 else str(row["Text"])
            st.markdown(f"""
            <div style="
                display:flex; justify-content:space-between; align-items:center;
                padding:7px 0; border-bottom:0.5px solid rgba(255,255,255,0.04);
            ">
                <span style="font-size:12px; color:#c8c7d4; flex:1; margin-right:12px;">{truncated}</span>
                <span style="
                    font-family:'DM Mono',monospace; font-size:10px;
                    background:rgba(250,108,108,0.12); color:#fa6c6c;
                    padding:2px 8px; border-radius:4px; flex-shrink:0;
                ">{row['Score']:+.2f}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:#7a7990; font-size:12px;'>No negative results found.</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
