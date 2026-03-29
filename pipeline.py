"""
============================================================
 PIPELINE — Parallel Processing Engine
------------------------------------------------------------
 Orchestrates the full 1M row processing pipeline:
   1. Inflate lines to 1,000,000
   2. Split into 50k batches
   3. Run batches in parallel across CPU cores
   4. Bulk insert results into SQLite
   5. Return results as DataFrame
============================================================
"""

import os
import pandas as pd
import streamlit as st
from concurrent.futures import ProcessPoolExecutor

from module.scorer  import process_batch
from module.storage import get_db_connection, bulk_insert

TARGET     = 1_000_000   # Total rows to process
BATCH_SIZE = 50_000      # Rows per parallel batch


def run_pipeline(lines):
    """
    Main pipeline — processes lines in parallel and saves to SQLite.

    Steps:
      1. Inflate input lines to TARGET (1,000,000) rows
      2. Split into batches of BATCH_SIZE (50,000)
      3. Submit each batch to a separate CPU process
      4. Collect results and buffer for DB insert
      5. Bulk insert every 200,000 rows (fewer commits = faster)
      6. Return full results as pandas DataFrame

    Args:
        lines : list of text strings from uploaded file

    Returns:
        pd.DataFrame with columns [Text, Score, Sentiment]
    """
    conn = get_db_connection()

    # ── Step 1: Inflate to 1M rows ──
    if len(lines) < TARGET:
        mult  = TARGET // len(lines)
        rem   = TARGET % len(lines)
        lines = lines * mult + lines[:rem]

    # ── Step 2: Split into batches ──
    batches   = [lines[i:i+BATCH_SIZE] for i in range(0, len(lines), BATCH_SIZE)]
    total     = len(batches)
    CPU_CORES = max(1, os.cpu_count() - 1)  # Leave 1 core free for UI

    # ── Step 3: Progress UI ──
    progress_bar = st.progress(0, text="Starting...")
    status_text  = st.empty()

    all_results = []

    # ── Step 4: Parallel processing ──
    # ProcessPoolExecutor creates real OS processes — bypasses Python GIL
    with ProcessPoolExecutor(max_workers=CPU_CORES) as executor:
        futures   = {executor.submit(process_batch, b): idx for idx, b in enumerate(batches)}
        completed = 0
        db_buffer = []

        for future in futures:
            result = future.result()
            all_results.extend(result)
            db_buffer.extend(result)
            completed += 1

            # ── Step 5: Bulk insert every 200k rows ──
            if len(db_buffer) >= 200_000:
                bulk_insert(conn, db_buffer)
                db_buffer.clear()

            # Update progress
            pct = int((completed / total) * 100)
            progress_bar.progress(pct, text=f"Processing... {completed}/{total} batches ({pct}%)")
            status_text.text(f"✅ Processed {min(completed * BATCH_SIZE, TARGET):,} rows")

    # Write remaining buffer
    if db_buffer:
        bulk_insert(conn, db_buffer)

    progress_bar.progress(100, text="Done!")
    status_text.text(f"✅ All {TARGET:,} rows saved to SQLite!")

    # ── Step 6: Return DataFrame ──
    return pd.DataFrame(all_results, columns=["Text", "Score", "Sentiment"])
