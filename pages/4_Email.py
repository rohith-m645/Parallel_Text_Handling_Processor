"""
============================================================
 PAGE 4 — Email Report
------------------------------------------------------------
 - Send small Excel report via Gmail SMTP
 - Credentials loaded from .env file
 - Shows clear error messages for common issues
============================================================
"""

import smtplib
import streamlit as st
from module.search import send_email, export_small_excel

st.header("📧 Email Report")

if not st.session_state.get("show_results"):
    st.warning("No results yet. Please go to Upload page and process a file first.")
    st.stop()

df = st.session_state.results_df

st.info("The report (50,000 rows) will be sent as an Excel attachment.")

# ── Ensure small file exists ──
if not st.session_state.get("small_file"):
    with st.spinner("Preparing report file..."):
        small_file = export_small_excel(df, rows=50000)
        st.session_state.small_file = small_file

# ── Email Input ──
receiver_email = st.text_input("📬 Enter Receiver Email Address")

if st.button("📤 Send Email"):
    if not receiver_email:
        st.error("❌ Please enter an email address.")
    else:
        try:
            with st.spinner("Sending email..."):
                send_email(receiver_email, st.session_state.small_file)
            st.success(f"✅ Email sent successfully to {receiver_email}!")

        except smtplib.SMTPAuthenticationError:
            st.error("❌ Wrong App Password. Check your .env file.")
            st.markdown("""
            **How to fix:**
            1. Go to https://myaccount.google.com/apppasswords
            2. Revoke old password → Generate new one
            3. Update `APP_PASSWORD` in your `.env` file
            """)

        except FileNotFoundError:
            st.error("❌ Report file not found. Please go to Results page and generate report first.")

        except Exception as e:
            st.error(f"❌ Email failed: {e}")

st.divider()
st.caption("💡 Credentials are loaded from your `.env` file. Never hardcode passwords in code.")
