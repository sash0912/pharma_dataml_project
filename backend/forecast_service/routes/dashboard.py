# routes/dashboard.py

from fastapi import APIRouter, HTTPException
import sqlite3
from backend.forecast_service.db import DB_PATH

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

# 1️⃣ List drugs in dataset
@router.get("/{dataset_id}/drugs")
def list_drugs(dataset_id: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT drug_name
        FROM dataset_demand
        WHERE dataset_id = ?
        ORDER BY drug_name
    """, (dataset_id,))

    drugs = [row[0] for row in cur.fetchall()]
    conn.close()

    if not drugs:
        raise HTTPException(status_code=404, detail="No drugs found")

    return drugs


# 2️⃣ Historical trend for a drug
@router.get("/{dataset_id}/drug/{drug_name}/history")
def drug_history(dataset_id: str, drug_name: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT date, qty
        FROM dataset_demand
        WHERE dataset_id = ? AND drug_name = ?
        ORDER BY date
    """, (dataset_id, drug_name))

    rows = cur.fetchall()
    conn.close()

    return [
        {"date": r[0], "qty": r[1]}
        for r in rows
    ]


# 3️⃣ Forecast for a drug
@router.get("/{dataset_id}/drug/{drug_name}/forecast")
def drug_forecast(dataset_id: str, drug_name: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT forecast_date, predicted_qty
        FROM dataset_forecasts
        WHERE dataset_id = ? AND drug_name = ?
    """, (dataset_id, drug_name))

    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Forecast not found")

    return {
        "forecast_date": row[0],
        "predicted_qty": row[1]
    }


# 4️⃣ Dataset analytics
@router.get("/{dataset_id}/analytics")
def dataset_analytics(dataset_id: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COUNT(*) as total_records,
            AVG(qty),
            MIN(qty),
            MAX(qty)
        FROM dataset_demand
        WHERE dataset_id = ?
    """, (dataset_id,))

    row = cur.fetchone()
    conn.close()

    return {
        "total_records": row[0],
        "average_demand": round(row[1], 2) if row[1] else 0,
        "min_demand": row[2] or 0,
        "max_demand": row[3] or 0
    }
