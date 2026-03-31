"""
============================================================
 PAGE 4 — Email Report
============================================================
"""

import os
import smtplib
import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from dotenv import load_dotenv

load_dotenv()

st.header("📧 Email Report")


def send_email(receiver_email, file_path):
    sender   = os.getenv("SENDER_EMAIL")
    password = os.getenv("APP_PASSWORD")
    host     = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port     = int(os.getenv("SMTP_PORT", 587))

    msg = MIMEMultipart()
    msg["From"]    = sender
    msg["To"]      = receiver_email
    msg["Subject"] = "📊 Sentiment Analysis Report"
    msg.attach(MIMEText("Please find the sentiment analysis report attached.", "plain"))

    with open(file_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename=report.xlsx")
        msg.attach(part)

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver_email, msg.as_string())


# ── Check if results exist ──
if not st.session_state.get("show_results") or st.session_state.get("results_df") is None:
    st.warning("⚠️ No results yet. Please go to Upload page and process a file first.")

else:
    df = st.session_state.results_df

    st.info("The report (50,000 rows) will be sent as an Excel attachment.")

    # ── Generate small Excel if not done yet ──
    small_file = st.session_state.get("small_file")

    if not small_file or not os.path.exists(small_file):
        with st.spinner("Preparing report file..."):
            small_file = "report_small.xlsx"
            df.head(50000).to_excel(small_file, index=False)
            st.session_state.small_file = small_file

    # ── Email Form ──
    receiver_email = st.text_input("📬 Enter Receiver Email Address")

    if st.button("📤 Send Email"):
        if not receiver_email:
            st.error("❌ Please enter an email address.")
        else:
            try:
                with st.spinner("Sending email..."):
                    send_email(receiver_email, small_file)
                st.success(f"✅ Email sent to {receiver_email}!")

            except smtplib.SMTPAuthenticationError:
                st.error("❌ Wrong App Password. Check your .env file.")

            except OSError as e:
                st.error(f"❌ Network error: {e}\n\nMake sure you have internet access and port 587 is not blocked.")

            except Exception as e:
                st.error(f"❌ Email failed: {e}")

st.divider()
st.caption("💡 Credentials loaded from `.env` file. Never hardcode passwords.")