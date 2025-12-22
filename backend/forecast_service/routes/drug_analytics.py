from fastapi import APIRouter
import sqlite3
from backend.forecast_service.db import DB_PATH

router = APIRouter(prefix="/analytics", tags=["Drug Analytics"])


# -----------------------------
# List all available drugs
# -----------------------------
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


# -----------------------------
# Drug trend with time control
# -----------------------------
@router.get("/drug/{drug_name}/trend")
def drug_trend(drug_name: str, months: int = 12):
    """
    Returns last N months of demand for a drug
    Default = 12 months
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, qty
        FROM historical_demand
        WHERE drug_name = ?
        ORDER BY date DESC
        LIMIT ?
    """, (drug_name, months))

    rows = cursor.fetchall()
    conn.close()

    # reverse so chart shows oldest → newest
    rows.reverse()

    return [
        {"date": r[0], "qty": r[1]}
        for r in rows
    ]
