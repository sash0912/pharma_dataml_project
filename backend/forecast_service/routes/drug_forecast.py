from fastapi import APIRouter
import sqlite3
import pandas as pd
import joblib

from backend.forecast_service.db import DB_PATH, save_drug_forecast

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

    
    if df.empty:
        return {
            "drug_name": drug_name,
            "predicted_next_month_qty": 0,
            "method": "no_data",
            "note": "No historical data available"
        }

    
    df["date"] = pd.to_datetime(df["date"])

    
    if len(df) < 7:
        avg_qty = df["qty"].mean()
        trend = df["qty"].diff().mean()

        prediction = avg_qty + (trend if not pd.isna(trend) else 0)
        prediction = max(round(float(prediction), 2), 0)

        
        save_drug_forecast(
            drug_name=drug_name,
            predicted_qty=prediction,
            method="statistical_fallback"
        )

        return {
            "drug_name": drug_name,
            "predicted_next_month_qty": prediction,
            "method": "statistical_fallback",
            "note": "Used average + trend due to limited data"
        }

    
    df["lag_1"] = df["qty"].shift(1)
    df["lag_3"] = df["qty"].shift(3)
    df["lag_6"] = df["qty"].shift(6)
    df["lag_12"] = df["qty"].shift(12)

    df["rolling_mean_3"] = df["qty"].rolling(3).mean()
    df["rolling_mean_6"] = df["qty"].rolling(6).mean()
    df["rolling_std_3"] = df["qty"].rolling(3).std()

    df = df.dropna()

    
    if df.empty:
        avg_qty = df["qty"].mean()
        prediction = max(round(float(avg_qty), 2), 0)

        save_drug_forecast(
            drug_name=drug_name,
            predicted_qty=prediction,
            method="fallback_after_feature_drop"
        )

        return {
            "drug_name": drug_name,
            "predicted_next_month_qty": prediction,
            "method": "fallback_after_feature_drop",
            "note": "Feature engineering reduced data too much"
        }

    
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

    
    save_drug_forecast(
        drug_name=drug_name,
        predicted_qty=prediction,
        method="ML"
    )

    return {
        "drug_name": drug_name,
        "predicted_next_month_qty": prediction,
        "method": "ML"
    }
