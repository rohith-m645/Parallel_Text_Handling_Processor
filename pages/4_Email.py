"""
============================================================
 PAGE 4 — Email Report  (Redesigned UI)
------------------------------------------------------------
 - Send Excel report via Gmail SMTP SSL
 - Credentials loaded from .env file
 - Clear error messages and setup guide
============================================================
"""

import smtplib
import os
import streamlit as st
from module.search import send_email, export_small_excel
from module.style import apply_theme, render_sidebar

apply_theme()
render_sidebar(active="email")

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
<h1 style="margin-bottom:0.25rem;">📧 Email Report</h1>
<p style="color:#7a7990; font-size:13px; font-family:'DM Mono',monospace; margin-bottom:1.5rem;">
    Send the Excel report as an attachment via Gmail SMTP
</p>
""", unsafe_allow_html=True)

# ── Info Banner ──
st.markdown("""
<div style="
    background: rgba(124,108,250,0.08);
    border: 0.5px solid rgba(124,108,250,0.25);
    border-radius: 8px; padding: 12px 16px;
    font-family:'DM Mono',monospace; font-size:12px;
    color: rgba(186,181,255,0.9);
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 1.5rem;
">
    ℹ️ &nbsp; The report (50,000 rows) will be sent as an Excel attachment via Gmail SMTP SSL (port 465).
</div>
""", unsafe_allow_html=True)

# ── Prepare small file ──
if not st.session_state.get("small_file"):
    with st.spinner("Preparing report file…"):
        small_file = export_small_excel(df, rows=50000)
        st.session_state.small_file = small_file

# ── Attachment Preview ──
small_file = st.session_state.small_file
file_size_mb = os.path.getsize(small_file) / 1_048_576 if small_file and os.path.exists(small_file) else 0

st.markdown(f"""
<div style="
    background:#16161f; border:0.5px solid rgba(255,255,255,0.07);
    border-radius:10px; padding:14px 18px; margin-bottom:1.5rem;
    display:flex; align-items:center; gap:14px;
">
    <div style="
        width:36px; height:36px; border-radius:8px;
        background:rgba(62,207,170,0.1);
        border:0.5px solid rgba(62,207,170,0.2);
        display:flex; align-items:center; justify-content:center;
        font-family:'DM Mono',monospace; font-size:9px; color:#3ecfaa;
    ">XLSX</div>
    <div style="flex:1;">
        <div style="font-size:13px; color:#f0eff8; font-weight:500;">report_small.xlsx</div>
        <div style="font-family:'DM Mono',monospace; font-size:10px; color:#7a7990;">
            50,000 rows &nbsp;·&nbsp; {file_size_mb:.1f} MB
        </div>
    </div>
    <div style="
        background:rgba(62,207,170,0.1); color:#3ecfaa;
        border:0.5px solid rgba(62,207,170,0.25); border-radius:6px;
        font-family:'DM Mono',monospace; font-size:10px;
        padding:4px 10px;
    ">ready</div>
</div>
""", unsafe_allow_html=True)

# ── Email Form ──
col_form, col_guide = st.columns([1, 1], gap="large")

with col_form:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif; font-weight:600;
                color:#f0eff8; font-size:14px; margin-bottom:1rem;">
        Send Email
    </div>
    """, unsafe_allow_html=True)

    receiver_email = st.text_input(
        "Receiver Email Address",
        placeholder="recipient@example.com",
        help="The Excel report will be sent to this address"
    )

    if st.button("📤 Send Email", type="primary", use_container_width=True):
        if not receiver_email:
            st.error("❌ Please enter an email address.")
        else:
            try:
                with st.spinner(f"Sending to {receiver_email}…"):
                    send_email(receiver_email, st.session_state.small_file)
                st.markdown(f"""
                <div style="
                    background:rgba(62,207,170,0.08);
                    border:0.5px solid rgba(62,207,170,0.3);
                    border-radius:8px; padding:14px 16px; margin-top:1rem;
                ">
                    <div style="color:#3ecfaa; font-weight:600; margin-bottom:2px;">
                        ✅ Email sent successfully
                    </div>
                    <div style="font-size:12px; color:#7a7990; font-family:'DM Mono',monospace;">
                        Delivered to {receiver_email}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            except smtplib.SMTPAuthenticationError:
                st.markdown("""
                <div style="
                    background:rgba(250,108,108,0.08);
                    border:0.5px solid rgba(250,108,108,0.3);
                    border-radius:8px; padding:14px 16px; margin-top:1rem;
                ">
                    <div style="color:#fa6c6c; font-weight:600; margin-bottom:6px;">
                        ❌ Authentication failed
                    </div>
                    <div style="font-size:12px; color:#c8c7d4;">
                        Wrong App Password in your <code style="background:rgba(255,255,255,0.06);
                        padding:1px 5px; border-radius:3px; color:#7c6cfa;">.env</code> file.
                    </div>
                    <ol style="font-size:12px; color:#7a7990; margin-top:8px; padding-left:1.2rem;">
                        <li>Go to myaccount.google.com/apppasswords</li>
                        <li>Revoke old password → Generate new one</li>
                        <li>Update APP_PASSWORD in your .env file</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)

            except FileNotFoundError:
                st.error("❌ Report file not found. Go to Results and generate the report first.")

            except Exception as e:
                st.markdown(f"""
                <div style="
                    background:rgba(250,108,108,0.08);
                    border:0.5px solid rgba(250,108,108,0.3);
                    border-radius:8px; padding:14px 16px; margin-top:1rem;
                ">
                    <div style="color:#fa6c6c; font-weight:600; margin-bottom:4px;">❌ Email failed</div>
                    <div style="font-family:'DM Mono',monospace; font-size:11px; color:#7a7990;">{e}</div>
                </div>
                """, unsafe_allow_html=True)

with col_guide:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif; font-weight:600;
                color:#f0eff8; font-size:14px; margin-bottom:1rem;">
        .env Configuration
    </div>

    <div style="
        background:#111118; border:0.5px solid rgba(255,255,255,0.07);
        border-radius:10px; padding:16px; font-family:'DM Mono',monospace;
        font-size:12px; line-height:2;
    ">
        <span style="color:#7c6cfa;">SENDER_EMAIL</span>=<span style="color:#3ecfaa;">your@gmail.com</span><br>
        <span style="color:#7c6cfa;">APP_PASSWORD</span>=<span style="color:#3ecfaa;">xxxx xxxx xxxx xxxx</span><br>
        <span style="color:#7c6cfa;">SMTP_HOST</span>=<span style="color:#3ecfaa;">smtp.gmail.com</span>
    </div>

    <div style="margin-top:1rem; font-size:12px; color:#7a7990; line-height:1.8;">
        <strong style="color:#f0eff8; font-family:'Syne',sans-serif;">
            How to get an App Password:
        </strong><br>
        1. Sign in to <span style="color:#7c6cfa;">myaccount.google.com</span><br>
        2. Security → Enable 2-Step Verification<br>
        3. Search <em>App Passwords</em> → Create<br>
        4. Copy the 16-char password into <code style="
            background:rgba(255,255,255,0.06); padding:1px 5px;
            border-radius:3px; color:#7c6cfa;">.env</code>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.markdown("""
<div style="font-family:'DM Mono',monospace; font-size:11px; color:#7a7990;">
    💡 Credentials are loaded from your <code style="background:rgba(255,255,255,0.06);
    padding:1px 5px; border-radius:3px; color:#7c6cfa;">.env</code> file.
    Never hardcode passwords in code.
</div>
""", unsafe_allow_html=True)
