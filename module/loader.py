"""
============================================================
 MODULE 1 — Text Breaker and Loader
------------------------------------------------------------
 Responsibilities:
   - Load TXT, CSV, XLSX, DOCX, PDF files
   - Tokenize text using regex patterns
   - Clean text (remove special/non-ASCII characters)
============================================================
"""

import re
import io
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
import streamlit as st


def tokenize(text):
    """Breaks a string into word tokens using regex."""
    return re.findall(r'\b\w+\b', str(text).lower())


def clean_text(text):
    """Removes control characters and non-ASCII content."""
    text = str(text)
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    return text


@st.cache_data
def read_file(file_name, file_bytes, ext):
    """
    Loads different file types into text content.
    Returns str for TXT/DOCX/PDF, DataFrame for CSV/XLSX.
    """
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
