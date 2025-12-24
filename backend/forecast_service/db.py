import sqlite3
from datetime import datetime
import os

# Absolute-safe DB path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "forecasts.db")


def get_connection():
    conn = sqlite3.connect(
        DB_PATH,
        timeout=30,
        check_same_thread=False
    )
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # ----------------------------
    # Historical demand (ETL)
    # ----------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historical_demand (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            drug_name TEXT,
            date TEXT,
            qty INTEGER
        )
    """)

    # ----------------------------
    # Forecasts (USED BY KPIs)
    # ----------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            predicted_qty REAL
        )
    """)

    # ----------------------------
    # Drug-wise forecast history
    # ----------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drug_forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            drug_name TEXT,
            predicted_qty REAL
        )
    """)

    conn.commit()
    conn.close()


# --------------------------------------------------
# Used by /predict endpoint (generic ML forecasting)
# --------------------------------------------------
def save_forecast(predicted_qty: float):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO forecasts (created_at, predicted_qty)
        VALUES (?, ?)
    """, (datetime.utcnow().isoformat(), predicted_qty))

    conn.commit()
    conn.close()


# --------------------------------------------------
# Used by drug-wise forecast (AND KPI sync)
# --------------------------------------------------
def save_drug_forecast(drug_name: str, predicted_qty: float):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()

    # Save drug-level forecast
    cursor.execute("""
        INSERT INTO drug_forecasts (created_at, drug_name, predicted_qty)
        VALUES (?, ?, ?)
    """, (now, drug_name, predicted_qty))

    # 🔥 ALSO save to forecasts table (FOR KPI)
    cursor.execute("""
        INSERT INTO forecasts (created_at, predicted_qty)
        VALUES (?, ?)
    """, (now, predicted_qty))

    conn.commit()
    conn.close()
