from fastapi import APIRouter
import sqlite3
import pandas as pd
import joblib

from backend.forecast_service.db import DB_PATH

router = APIRouter(prefix="/forecast", tags=["Drug Forecast"])

MODEL_PATH = "ml/models/xgboost_model.pkl"
model = joblib.load(MODEL_PATH)


@router.get("/drug/{drug_name}")
def forecast_drug(drug_name: str):
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        """
        SELECT date, qty
        FROM historical_demand
        WHERE drug_name = ?
        ORDER BY date
        """,
        conn,
        params=(drug_name,)
    )

    conn.close()

    # 🛑 If no data at all
    if df.empty:
        return {
            "drug_name": drug_name,
            "predicted_next_month_qty": 0,
            "method": "no_data",
            "note": "No historical data available"
        }

    df["date"] = pd.to_datetime(df["date"])

    # -----------------------------
    # 🧠 FALLBACK MODE (STATISTICAL)
    # -----------------------------
    if len(df) < 13:
        avg_qty = df["qty"].mean()
        trend = df["qty"].diff().mean()

        prediction = avg_qty + (trend if not pd.isna(trend) else 0)
        prediction = max(round(float(prediction), 2), 0)

        return {
            "drug_name": drug_name,
            "predicted_next_month_qty": prediction,
            "method": "statistical_fallback",
            "note": "Insufficient history for ML; used average + trend"
        }

    # -----------------------------
    # 🤖 ML MODE (FULL HISTORY)
    # -----------------------------
    df["lag_1"] = df["qty"].shift(1)
    df["lag_3"] = df["qty"].shift(3)
    df["lag_6"] = df["qty"].shift(6)
    df["lag_12"] = df["qty"].shift(12)

    df["rolling_mean_3"] = df["qty"].rolling(3).mean()
    df["rolling_mean_6"] = df["qty"].rolling(6).mean()
    df["rolling_std_3"] = df["qty"].rolling(3).std()

    df = df.dropna()

    latest = df.iloc[-1][[
        "lag_1",
        "lag_3",
        "lag_6",
        "lag_12",
        "rolling_mean_3",
        "rolling_mean_6",
        "rolling_std_3"
    ]]

    X = pd.DataFrame([latest])
    prediction = model.predict(X)[0]
    prediction = max(round(float(prediction), 2), 0)

    return {
    "drug_name": drug_name,
    "forecast": round(prediction, 2),
    "method": "ML"  
}

    