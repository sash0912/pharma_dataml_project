import sqlite3
from fastapi import APIRouter
from backend.forecast_service.db import DB_PATH

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# ---------------------------
# KPI SUMMARY (from forecasts)
# ---------------------------
@router.get("/summary")
def get_basic_analytics():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total_predictions,
            AVG(predicted_qty) AS avg_demand,
            MIN(predicted_qty) AS min_demand,
            MAX(predicted_qty) AS max_demand
        FROM forecasts
    """)

    row = cursor.fetchone()
    conn.close()

    return {
        "total_predictions": row[0] or 0,
        "average_demand": round(row[1], 2) if row[1] else 0,
        "min_demand": row[2] or 0,
        "max_demand": row[3] or 0
    }


# ---------------------------
# RECENT FORECAST TREND
# ---------------------------
@router.get("/trend")
def get_recent_trend(days: int = 7):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT created_at, predicted_qty
        FROM forecasts
        ORDER BY created_at DESC
        LIMIT ?
    """, (days,))

    rows = cursor.fetchall()
    conn.close()

    rows.reverse()

    return [
        {"date": r[0], "qty": r[1]}
        for r in rows
    ]


# ---------------------------
# DRUG LIST (from historical_demand)
# ---------------------------
@router.get("/drugs")
def list_drugs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT drug_name
        FROM historical_demand
        ORDER BY drug_name
    """)

    drugs = [r[0] for r in cursor.fetchall()]
    conn.close()

    return drugs


# ---------------------------
# DRUG DEMAND TREND (from historical_demand)
# ---------------------------
@router.get("/drug/{drug_name}/trend")
def drug_trend(drug_name: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, qty
        FROM historical_demand
        WHERE drug_name = ?
        ORDER BY date
    """, (drug_name,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {"date": r[0], "qty": r[1]}
        for r in rows
    ]
