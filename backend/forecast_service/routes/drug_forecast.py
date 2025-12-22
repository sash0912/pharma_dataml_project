from fastapi import APIRouter
import sqlite3
import pandas as pd
import joblib

from backend.forecast_service.db import DB_PATH, save_drug_forecast
  # ✅ ADD THIS

router = APIRouter(prefix="/forecast", tags=["Drug Forecast"])

MODEL_PATH = "ml/models/xgboost_model.pkl"
model = joblib.load(MODEL_PATH)


# ----------------------------
# CORE REUSABLE LOGIC FUNCTION
# ----------------------------
def forecast_drug_logic(drug_name: str) -> float:
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        """
        SELECT date, qty
        FROM historical_demand
        WHERE drug_name = ?
        ORDER BY date
        """,
        conn,
        params=(drug_name,),
    )

    conn.close()

    # No data
    if df.empty:
        return 0.0

    df["date"] = pd.to_datetime(df["date"])

    # Statistical fallback
    if len(df) < 7:
        avg_qty = df["qty"].mean()
        trend = df["qty"].diff().mean()
        return round(max(avg_qty + (trend if not pd.isna(trend) else 0), 0), 2)

    # Feature engineering
    df["lag_1"] = df["qty"].shift(1)
    df["lag_3"] = df["qty"].shift(3)
    df["lag_6"] = df["qty"].shift(6)
    df["lag_12"] = df["qty"].shift(12)

    df["rolling_mean_3"] = df["qty"].rolling(3).mean()
    df["rolling_mean_6"] = df["qty"].rolling(6).mean()
    df["rolling_std_3"] = df["qty"].rolling(3).std()

    df = df.dropna()
    if df.empty:
        return 0.0

    latest = df.iloc[-1][[
        "lag_1",
        "lag_3",
        "lag_6",
        "lag_12",
        "rolling_mean_3",
        "rolling_mean_6",
        "rolling_std_3",
    ]]

    prediction = model.predict(pd.DataFrame([latest]))[0]
    return round(max(float(prediction), 0), 2)


# ----------------------------
# FASTAPI ENDPOINT (SAVE HERE)
# ----------------------------
@router.get("/drug/{drug_name}")
def forecast_drug(drug_name: str):
    prediction = forecast_drug_logic(drug_name)

    # ✅ Correct KPI-safe save
    save_drug_forecast(drug_name, float(prediction))

    return {
        "drug_name": drug_name,
        "predicted_next_month_qty": prediction,
        "method": "ML / Statistical"
    }

