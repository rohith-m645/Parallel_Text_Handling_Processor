"""
============================================================
PIPELINE — Parallel Processing Engine
------------------------------------------------------------
Orchestrates the full processing pipeline:
1. Use actual uploaded rows (no forced inflation)
2. Split into 10k batches (memory-safe)
3. Run batches in parallel across CPU cores
4. Bulk insert results into SQLite
5. Return results as DataFrame
============================================================
"""

import os
import pandas as pd
import streamlit as st
from concurrent.futures import ThreadPoolExecutor  # Thread-safe for cloud (no ProcessPool)
from module.scorer import process_batch
from module.storage import get_db_connection, bulk_insert

MAX_ROWS   = 1_000_000   # Hard cap — never exceed 1M
BATCH_SIZE = 10_000      # Smaller batches = less RAM per batch


def run_pipeline(lines):
    """
    Main pipeline — processes uploaded lines and saves to SQLite.

    Steps:
      1. Cap rows at MAX_ROWS (don't inflate small files)
      2. Split into batches of BATCH_SIZE (10,000)
      3. Submit each batch to a thread pool
      4. Collect results and buffer for DB insert
      5. Bulk insert every 100,000 rows
      6. Return full results as pandas DataFrame

    Args:
        lines : list of text strings from uploaded file

    Returns:
        pd.DataFrame with columns [Text, Score, Sentiment]
    """

    conn = get_db_connection()

    # ── Step 1: Cap at MAX_ROWS — NO forced inflation ──
    # Only use what the user actually uploaded (up to 1M rows)
    lines = lines[:MAX_ROWS]
    total_rows = len(lines)

    # ── Step 2: Split into batches ──
    batches = [lines[i:i + BATCH_SIZE] for i in range(0, total_rows, BATCH_SIZE)]
    total_batches = len(batches)

    # Use threads instead of processes — safer on cloud free tier (no fork issues)
    MAX_WORKERS = max(1, min(4, os.cpu_count() or 1))

    # ── Step 3: Progress UI ──
    progress_bar = st.progress(0, text="Starting...")
    status_text  = st.empty()

    all_results = []
    db_buffer   = []
    completed   = 0

    # ── Step 4: Parallel processing with ThreadPoolExecutor ──
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_batch, b): idx for idx, b in enumerate(batches)}

        for future in futures:
            result = future.result()
            all_results.extend(result)
            db_buffer.extend(result)
            completed += 1

            # ── Step 5: Bulk insert every 100k rows ──
            if len(db_buffer) >= 100_000:
                bulk_insert(conn, db_buffer)
                db_buffer.clear()

            # Update progress bar
            pct = int((completed / total_batches) * 100)
            rows_done = min(completed * BATCH_SIZE, total_rows)
            progress_bar.progress(pct, text=f"Processing... {completed}/{total_batches} batches ({pct}%)")
            status_text.text(f"✅ Processed {rows_done:,} / {total_rows:,} rows")

    # ── Write any remaining buffer ──
    if db_buffer:
        bulk_insert(conn, db_buffer)

    progress_bar.progress(100, text="Done!")
    status_text.text(f"✅ All {total_rows:,} rows processed and saved!")

    # ── Step 6: Return DataFrame ──
    return pd.DataFrame(all_results, columns=["Text", "Score", "Sentiment"])
