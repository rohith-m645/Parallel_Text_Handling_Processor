"""
============================================================
 MODULE 4 — Text Storage Improver
------------------------------------------------------------
 Responsibilities:
   - Create and manage SQLite database
   - Optimized PRAGMA settings for fast bulk inserts
   - Cached connection reused across Streamlit reruns
============================================================
"""

import sqlite3
import streamlit as st


@st.cache_resource
def get_db_connection():
    """
    Creates an optimized SQLite connection.

    PRAGMA settings explained:
      journal_mode=WAL    → Allows simultaneous reads + writes
      synchronous=NORMAL  → Balanced speed and data safety
      cache_size=100000   → 100k pages stored in RAM cache
      temp_store=MEMORY   → Temp tables in RAM (faster sorting)

    @st.cache_resource keeps ONE connection alive
    for the entire app session — not recreated on reruns.
    """
    conn = sqlite3.connect("sentiment_results.db", check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=100000")
    conn.execute("PRAGMA temp_store=MEMORY")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sentiment_data (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            text      TEXT,
            score     REAL,
            sentiment TEXT
        )
    """)
    conn.commit()
    return conn


def bulk_insert(conn, rows):
    """
    Inserts a list of (text, score, sentiment) tuples into SQLite.
    Uses executemany for efficiency — single round trip to DB.
    """
    conn.executemany(
        "INSERT INTO sentiment_data (text, score, sentiment) VALUES (?,?,?)",
        rows
    )
    conn.commit()


def query_all(conn):
    """
    Fetches all records from sentiment_data table.
    Returns a list of (text, score, sentiment) tuples.
    """
    cursor = conn.execute("SELECT text, score, sentiment FROM sentiment_data")
    return cursor.fetchall()


def clear_table(conn):
    """
    Deletes all rows from sentiment_data (for fresh processing runs).
    """
    conn.execute("DELETE FROM sentiment_data")
    conn.commit()
