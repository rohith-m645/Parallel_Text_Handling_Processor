import streamlit as st
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
import smtplib
from email.message import EmailMessage
import sqlite3
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor
import os
from openpyxl import Workbook
import re

# ===============================
# CLEAN + TOKENIZE
# ===============================
def tokenize(text):
    return re.findall(r'\b\w+\b', str(text).lower())

def clean_text(text):
    text = str(text)
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    return text

# ===============================
# WORD LISTS (module-level for multiprocessing)
# ===============================
positive_words = set(["good","great","excellent","happy","amazing","love"])
negative_words = set(["bad","poor","terrible","hate","worst"])

refund_words   = ["refund","money back","return"]
delivery_words = ["late","delayed","not delivered","missing"]
damage_words   = ["broken","damaged","defective"]
service_words  = ["no response","rude"]
price_words    = ["expensive","overpriced"]
sarcasm_words  = ["yeah right","as if"]
spam_words     = ["spam","junk","promotion"]
scam_words     = ["scam","fraud","fake"]

# ===============================
# SCORE
# ===============================
def calculate_score(text):
    words = tokenize(text)
    score = 0
    for w in words:
        if w in positive_words:
            score += 1
        elif w in negative_words:
            score -= 1
    return score

# ===============================
# CLASSIFY
# ===============================
def classify(text, score):
    text = text.lower()
    if any(w in text for w in scam_words):     return "Scam Risk"
    if any(w in text for w in spam_words):     return "Spam"
    if any(w in text for w in refund_words):   return "Refund Issue"
    if any(w in text for w in delivery_words): return "Delivery Issue"
    if any(w in text for w in damage_words):   return "Product Damage"
    if any(w in text for w in service_words):  return "Customer Service"
    if any(w in text for w in price_words):    return "Price Complaint"
    if any(w in text for w in sarcasm_words):  return "Sarcasm"
    if score > 0:  return "Positive"
    elif score < 0: return "Negative"
    else:           return "Neutral"

# ===============================
# PROCESS BATCH (runs in separate process)
# ===============================
def process_batch(batch):
    results = []
    for line in batch:
        if line.strip():
            score = calculate_score(line)
            sentiment = classify(line, score)
            results.append((clean_text(line), score, sentiment))
    return results

# ===============================
# PAGE
# ===============================
st.set_page_config(page_title="Multi File Analyzer", layout="wide")
st.title("📃 Multi File Analyzer")

# ===============================
# SESSION
# ===============================
if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "results_df" not in st.session_state:
    st.session_state.results_df = None
if "small_file" not in st.session_state:
    st.session_state.small_file = None

# ===============================
# DATABASE SETUP
# ===============================
@st.cache_resource
def get_db_connection():
    conn = sqlite3.connect("sentiment_results.db", check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")       # ✅ Faster writes
    conn.execute("PRAGMA synchronous=NORMAL")     # ✅ Balanced safety/speed
    conn.execute("PRAGMA cache_size=100000")      # ✅ More cache in RAM
    conn.execute("PRAGMA temp_store=MEMORY")      # ✅ Temp tables in RAM
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sentiment_data(
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            text      TEXT,
            score     REAL,
            sentiment TEXT
        )
    """)
    conn.commit()
    return conn

conn = get_db_connection()

# ===============================
# FILE READER
# ===============================
@st.cache_data
def read_file(file_name, file_bytes, ext):
    import io
    if ext == "txt":
        return file_bytes.decode("utf-8")
    elif ext == "csv":
        return pd.read_csv(io.BytesIO(file_bytes))
    elif ext == "xlsx":
        return pd.read_excel(io.BytesIO(file_bytes))
    elif ext == "docx":
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join([p.text for p in doc.paragraphs])
    elif ext == "pdf":
        reader = PdfReader(io.BytesIO(file_bytes))
        return "\n".join([p.extract_text() or "" for p in reader.pages])
    return ""

# ===============================
# SIDEBAR
# ===============================
st.sidebar.header("📁 Controls")

uploaded_files = st.sidebar.file_uploader(
    "Upload Files",
    type=["txt","csv","xlsx","docx","pdf"],
    accept_multiple_files=True
)

lines = []

if uploaded_files:
    file_names = [f.name for f in uploaded_files]
    selected_file = st.sidebar.selectbox("Select File", file_names)

    for f in uploaded_files:
        if f.name == selected_file:
            ext = f.name.split(".")[-1].lower()
            content = read_file(f.name, f.read(), ext)

            if isinstance(content, pd.DataFrame):
                lines = content.astype(str).agg(" ".join, axis=1).tolist()
            else:
                lines = content.splitlines()

process_btn = st.sidebar.button("🚀 Start Processing ")

# ===============================
# PROCESS 1 MILLION ROWS — OPTIMIZED
# ===============================
if process_btn and lines:

    # --- Inflate to 1 million ---
    TARGET = 1_000_000
    if len(lines) < TARGET:
        mult = TARGET // len(lines)
        rem  = TARGET % len(lines)
        lines = lines * mult + lines[:rem]

    progress_bar = st.progress(0, text="Starting...")
    status_text  = st.empty()

    CPU_CORES  = max(1, os.cpu_count() - 1)   # leave 1 core free for UI
    BATCH_SIZE = 50_000                         # larger batch = fewer overhead calls
    batches    = [lines[i:i+BATCH_SIZE] for i in range(0, len(lines), BATCH_SIZE)]
    total      = len(batches)

    all_results = []

    # ✅ Real multiprocessing — bypasses Python GIL
    with ProcessPoolExecutor(max_workers=CPU_CORES) as executor:
        futures = {executor.submit(process_batch, b): idx for idx, b in enumerate(batches)}

        completed = 0
        db_buffer = []      # accumulate rows before writing to DB

        for future in futures:  # as_completed not needed — we want ordered progress
            result = future.result()
            all_results.extend(result)
            db_buffer.extend(result)
            completed += 1

            # ✅ Write to DB in large chunks, commit only once per chunk
            if len(db_buffer) >= 200_000:
                conn.executemany(
                    "INSERT INTO sentiment_data (text,score,sentiment) VALUES (?,?,?)",
                    db_buffer
                )
                conn.commit()
                db_buffer.clear()

            pct = int((completed / total) * 100)
            progress_bar.progress(pct, text=f"Processing... {completed}/{total} batches ({pct}%)")
            status_text.text(f"✅ Processed {min(completed * BATCH_SIZE, TARGET):,} rows")

    # Write remaining buffer
    if db_buffer:
        conn.executemany(
            "INSERT INTO sentiment_data (text,score,sentiment) VALUES (?,?,?)",
            db_buffer
        )
        conn.commit()

    progress_bar.progress(100, text="Done!")
    status_text.text(f"✅ All {TARGET:,} rows saved to SQLite!")

    df = pd.DataFrame(all_results, columns=["Text","Score","Sentiment"])
    st.session_state.results_df = df
    st.session_state.show_results = True

# ===============================
# EXPORT LARGE EXCEL
# ===============================
def export_1M_excel(data):
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()
    ws.append(["Text","Score","Sentiment"])
    for row in data:
        ws.append(list(row))
    file_name = "FULL_1M_REPORT.xlsx"
    wb.save(file_name)
    return file_name

# ===============================
# RESULTS
# ===============================
if st.session_state.show_results:

    df = st.session_state.results_df

    st.subheader("📊 Preview (first 1,000 rows)")
    st.dataframe(df.head(1000), use_container_width=True)

    summary = df["Sentiment"].value_counts()

    st.subheader("📈 Summary")
    col1, col2 = st.columns(2)

    with col1:
        for k, v in summary.items():
            st.write(f"**{k}** : {v:,}")

    with col2:
        fig, ax = plt.subplots(figsize=(6,4))
        ax.barh(summary.index, summary.values, color="steelblue")
        ax.set_xlabel("Count")
        ax.set_title("Sentiment Distribution")
        st.pyplot(fig)

    # SMALL EXCEL (50k rows)
    small_file = "report_small.xlsx"
    df.head(50000).to_excel(small_file, index=False)
    st.session_state.small_file = small_file   # ✅ Save to session state

    with open(small_file, "rb") as f:
        st.sidebar.download_button(
            "📥 Download Small Report (50k)",
            f,
            file_name=small_file
        )

    # FULL 1M EXCEL
    if st.sidebar.button("⚙️ Generate Full data Excel"):
        with st.spinner("Building Excel file... this takes ~2 min for 1M rows"):
            file = export_1M_excel(df.values.tolist())
        with open(file, "rb") as f:
            st.sidebar.download_button(
                "📥 Download Excel",
                f,
                file_name=file
            )

    # EMAIL
    email = st.sidebar.text_input("Enter Email")

    if st.sidebar.button("Send Email"):

        msg = EmailMessage()
        msg["Subject"] = "Report"
        msg["From"] = "your_email@gmail.com"
        msg["To"] = email

        msg.set_content("Report Attached")

        with open(small_file,"rb") as f:
            msg.add_attachment(f.read(),
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=small_file)

        server = smtplib.SMTP_SSL("smtp.gmail.com",465)
        server.login("mrohith645@gmail.com","ldvs gulm kduk vnmw")
        server.send_message(msg)
        server.quit()

        st.success("Email Sent")
