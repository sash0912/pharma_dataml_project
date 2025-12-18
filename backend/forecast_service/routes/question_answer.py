from fastapi import APIRouter, HTTPException
import sqlite3
from backend.forecast_service.db import DB_PATH
from backend.forecast_service.routes.drug_forecast import forecast_drug_logic

router = APIRouter(prefix="/ask", tags=["Question Answering"])


def extract_drug_name(question: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT drug_name FROM historical_demand")
    drugs = [d[0] for d in cursor.fetchall()]
    conn.close()

    for drug in drugs:
        if drug.lower() in question.lower():
            return drug

    raise HTTPException(status_code=400, detail="Drug name not found")


@router.post("")
def ask_question(payload: dict):
    question = payload.get("question", "").lower()

    if "next month" in question:
        drug = extract_drug_name(question)
        forecast = forecast_drug_logic(drug)

        return {
            "question": payload["question"],
            "answer": f"Estimated demand for {drug} next month is {forecast}",
            "source": "ML Forecast"
        }

    if "highest" in question:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT drug_name, AVG(qty) avg_qty
            FROM historical_demand
            GROUP BY drug_name
            ORDER BY avg_qty DESC
            LIMIT 1
        """)
        drug, avg = cursor.fetchone()
        conn.close()

        return {
            "question": payload["question"],
            "answer": f"{drug} has the highest average demand ({round(avg,2)})",
            "source": "Historical Analysis"
        }

    return {
        "question": payload["question"],
        "answer": "This question type is not supported yet.",
        "source": "Rule Engine"
    }
