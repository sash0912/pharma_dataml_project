import sqlite3
from datetime import datetime

DB_PATH = "backend/data/forecasts.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            lag_1 REAL,
            lag_3 REAL,
            lag_6 REAL,
            lag_12 REAL,
            rolling_mean_3 REAL,
            rolling_mean_6 REAL,
            rolling_std_3 REAL,
            predicted_qty REAL
        )
    """)

    conn.commit()
    conn.close()

def save_forecast(input_data: dict, prediction: float):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO forecasts (
            created_at,
            lag_1, lag_3, lag_6, lag_12,
            rolling_mean_3, rolling_mean_6, rolling_std_3,
            predicted_qty
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        input_data["lag_1"],
        input_data["lag_3"],
        input_data["lag_6"],
        input_data["lag_12"],
        input_data["rolling_mean_3"],
        input_data["rolling_mean_6"],
        input_data["rolling_std_3"],
        prediction
    ))
def save_drug_forecast(drug_name, predicted_qty, method):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO drug_forecasts (created_at, drug_name, predicted_qty, method)
        VALUES (datetime('now'), ?, ?, ?)
    """, (drug_name, predicted_qty, method))

    conn.commit()
    conn.close()


