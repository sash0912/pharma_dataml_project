from fastapi import APIRouter
import sqlite3
from backend.forecast_service.db import DB_PATH

router = APIRouter(prefix="/analytics", tags=["Drug Analytics"])


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
