import sqlite3
from backend.forecast_service.db import DB_PATH

def get_basic_analytics():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            COUNT(*) as total_predictions,
            AVG(predicted_qty) as avg_demand,
            MIN(predicted_qty) as min_demand,
            MAX(predicted_qty) as max_demand
        FROM forecasts
    """)

    row = cursor.fetchone()
    conn.close()

    return {
        "total_predictions": row[0],
        "average_demand": round(row[1], 2) if row[1] else 0,
        "min_demand": round(row[2], 2) if row[2] else 0,
        "max_demand": round(row[3], 2) if row[3] else 0
    }


def get_recent_trend(limit=7):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT created_at, predicted_qty
        FROM forecasts
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    rows.reverse()  

    return [
        {"date": r[0], "predicted_qty": r[1]}
        for r in rows
    ]
