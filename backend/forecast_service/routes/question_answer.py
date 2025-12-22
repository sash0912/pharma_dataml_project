from fastapi import APIRouter, HTTPException
import sqlite3

from backend.forecast_service.db import DB_PATH
from backend.forecast_service.routes.drug_forecast import forecast_drug_logic
from backend.forecast_service.llm_service import ask_llm

router = APIRouter(prefix="/ask", tags=["Question Answering"])


# ----------------------------
# Helper: extract drug name
# ----------------------------
def extract_drug_name(question: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT drug_name FROM historical_demand")
    drugs = [d[0] for d in cursor.fetchall()]
    conn.close()

    for drug in drugs:
        if drug.lower() in question.lower():
            return drug

    return ""


# ----------------------------
# MAIN ASK ENDPOINT
# ----------------------------
@router.post("")
def ask_question(payload: dict):
    question = payload.get("question", "").strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    q = question.lower()

    # ----------------------------
    # 1️⃣ Forecast-type question
    # ----------------------------
    if "next month" in q or "required" in q:
        drug = extract_drug_name(q)

        if not drug:
            return {
                "question": question,
                "answer": "Please specify a valid drug name.",
                "source": "Validation"
            }

        qty = forecast_drug_logic(drug)

        return {
            "question": question,
            "answer": f"Estimated demand for {drug} next month is approximately {qty}.",
            "source": "ML / Statistical Model"
        }

    # ----------------------------
    # 2️⃣ Highest / Most demanded
    # ----------------------------
    if "highest" in q or "most demanded" in q:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT drug_name, AVG(qty) AS avg_qty
            FROM historical_demand
            GROUP BY drug_name
            ORDER BY avg_qty DESC
            LIMIT 1
        """)

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "question": question,
                "answer": f"{row[0]} has the highest average demand ({round(row[1], 2)} units).",
                "source": "Historical Analytics"
            }

    # ----------------------------
    # 3️⃣ Fallback → LLM (Ollama)
    # ----------------------------
    llm_answer = ask_llm(question)

    return {
        "question": question,
        "answer": llm_answer,
        "source": "LLM (Ollama)"
    }
