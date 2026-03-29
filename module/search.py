"""
============================================================
 MODULE 3 — Search Checker and File Saver
------------------------------------------------------------
 Responsibilities:
   - Export results to Excel (small 50k or full 1M)
   - Send email with Excel report via Gmail SMTP
   - Credentials loaded safely from .env file
============================================================
"""

import os
import smtplib
from email.message import EmailMessage
from openpyxl import Workbook
from dotenv import load_dotenv

load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD  = os.getenv("APP_PASSWORD")


def export_1M_excel(data, filename="FULL_1M_REPORT.xlsx"):
    """
    Exports up to 1,000,000 rows to Excel using write-only mode.

    write_only=True is critical for large exports:
      - Normal Workbook loads all data into RAM → crashes on 1M rows
      - write_only streams rows directly to disk → uses ~10x less memory

    Args:
        data     : list of [text, score, sentiment] rows
        filename : output Excel filename

    Returns:
        filename (str)
    """
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()
    ws.append(["Text", "Score", "Sentiment"])
    for row in data:
        ws.append(list(row))
    wb.save(filename)
    return filename


def export_small_excel(df, filename="report_small.xlsx", rows=50000):
    """
    Exports first N rows of DataFrame to Excel.
    Default 50k rows keeps file size under ~10MB (safe for email).

    Args:
        df       : pandas DataFrame with results
        filename : output Excel filename
        rows     : number of rows to export (default 50,000)

    Returns:
        filename (str)
    """
    df.head(rows).to_excel(filename, index=False)
    return filename


def send_email(receiver_email, attachment_path):
    """
    Sends an email with Excel report attached via Gmail SMTP SSL.

    Credentials loaded from .env:
      SENDER_EMAIL = your_email@gmail.com
      APP_PASSWORD = 16-char Gmail app password

    To generate App Password:
      1. myaccount.google.com → Security
      2. Enable 2-Step Verification
      3. Search 'App Passwords' → Create

    Args:
        receiver_email  : recipient email address
        attachment_path : path to Excel file to attach
    """
    if not SENDER_EMAIL or not APP_PASSWORD:
        raise ValueError("SENDER_EMAIL or APP_PASSWORD not set in .env file")

    msg = EmailMessage()
    msg["Subject"] = "📊 Sentiment Analysis Report"
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = receiver_email
    msg.set_content("Please find your sentiment analysis report attached.")

    with open(attachment_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=os.path.basename(attachment_path)
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
