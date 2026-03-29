# 📃 Parallel Text Handling Processor

A high-performance Streamlit application that processes large-scale text data using Python's multiprocessing capabilities. Designed for language experts and data workers to mine text efficiently without special NLP tools.

---

## 🎯 Project Overview

This system handles big text sets, runs tasks in parallel like sentiment scoring with rule-based rules, and builds searchable indexes. It supports batch processing via CSV files and provides automated email summaries.

---

## 🚀 Features

- ⚡ Parallel text processing using `ProcessPoolExecutor` (bypasses Python GIL)
- 📂 Upload TXT, CSV, XLSX, DOCX, or PDF files
- 🔁 Processes up to **1,000,000 rows** at a time
- 🧠 Rule-based sentiment scoring (no ML libraries needed)
- 🗄️ SQLite database with WAL optimization for fast storage
- 📊 Interactive sentiment distribution chart
- 📥 Download reports as Excel (50k preview or full 1M)
- 📧 Automated email summaries via Gmail SMTP

---

## 🧩 Modules

### Module 1 — Text Breaker and Loader
> *Breaks text using multi-tasking groups. Uses patterns for first filters.*

- `read_file()` — Loads TXT, CSV, XLSX, DOCX, PDF into text lines
- `tokenize()` — Breaks text into word tokens using regex patterns
- `clean_text()` — Removes special characters and non-ASCII content
- Data is split into batches of 50,000 lines for parallel processing
- `@st.cache_data` prevents re-loading the same file on every rerun

---

### Module 2 — Rule Checker and Scorer
> *Scores in tasks at the same time. Saves results in a simple database.*

- `calculate_score()` — Scores each text using positive/negative word lists
- `classify()` — Classifies text into 10 categories:
  - Positive, Negative, Neutral
  - Refund Issue, Delivery Issue, Product Damage
  - Customer Service, Price Complaint, Spam, Scam Risk, Sarcasm
- `ProcessPoolExecutor` runs scoring across all CPU cores simultaneously
- Results saved to **SQLite** with optimized PRAGMA settings:
  - `journal_mode=WAL` — faster concurrent writes
  - `synchronous=NORMAL` — balanced speed and safety
  - Bulk commits every 200,000 rows for efficiency

---

### Module 3 — Search Checker and File Saver
> *Lets you search and save to Excel files. Sends email summaries.*

- Results displayed in an interactive table (first 1,000 rows preview)
- Export to Excel:
  - **Small Report** — first 50,000 rows (~10MB)
  - **Full Report** — all 1,000,000 rows (write-only Workbook for memory efficiency)
- Email summary sent via Gmail SMTP with Excel report attached
- Sentiment summary counts shown for all categories

---

### Module 4 — Text Storage Improver
> *Builds and keeps good lists. Handles changes with little work.*

- SQLite database auto-created on first run
- `@st.cache_resource` keeps DB connection alive across reruns
- Session state (`st.session_state`) persists results across button clicks
- Word lists use Python `set()` for O(1) lookup speed
- Database schema supports incremental inserts without full rebuilds

---

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/parallel-text-processor.git
cd parallel-text-processor
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up Gmail credentials
Create a `.env` file in the project root:
```
SENDER_EMAIL=your_email@gmail.com
APP_PASSWORD=your_16_char_app_password
```

To generate a Gmail App Password:
1. Go to https://myaccount.google.com
2. Enable **2-Step Verification**
3. Search **App Passwords** → Create one

### 4. Run the app
```bash
streamlit run app.py
```

---

## 📦 Requirements

```
streamlit
pandas
python-docx
PyPDF2
openpyxl
matplotlib
python-dotenv
```

---

## 📁 Project Structure

```
Parallel_Text_Processor/
│
├── app.py
├── pipeline.py
├── .gitignore
│
├── module/
│   ├── __init__.py
│   ├── loader.py
│   ├── scorer.py
│   ├── search.py
│   ├── storage.py
│
├── pages/
│   ├── 1_Upload.py
│   ├── 2_Results.py
│   ├── 3_Insights.py
│   ├── 4_Email.py
│   ├── .env  

---

## 🗓️ Project Milestones

| Milestone | Weeks | Goal | Status |
|---|---|---|---|
| 1 — Setup & Planning | 1-2 | Tools setup, multiprocessing plan | ✅ Done |
| 2 — Text Breaker & Loader | 3-4 | Parallel file loading and batch splitting | ✅ Done |
| 3 — Rule Checker & Search Saver | 5-6 | Sentiment scoring, Excel export, email alerts | ✅ Done |
| 4 — Text Storage Improver | 7-8 | SQLite optimization, fast indexing | ✅ Done |

---

## ⚠️ Security Notes

- **Never commit your `.env` file to GitHub**
- If you accidentally expose your app password, revoke it immediately at https://myaccount.google.com/apppasswords
- `.gitignore` is included to prevent accidental credential commits

---

## 📄 License

MIT License — free to use and modify.
