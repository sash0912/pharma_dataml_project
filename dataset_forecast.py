# backend/forecast_service/services/dataset_forecast.py

import sqlite3
import pandas as pd
import joblib
from datetime import datetime, timedelta

from backend.forecast_service.db import DB_PATH

MODEL_PATH = "ml/models/xgboost_model.pkl"
model = joblib.load(MODEL_PATH)


def run_forecast(dataset_id: str):
    """
    Generate forecast for a given dataset_id
    """

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT drug_name, date, qty
        FROM dataset_demand
        WHERE dataset_id = ?
        ORDER BY date
        """,
        conn,
        params=(dataset_id,)
    )

    if df.empty:
        conn.close()
        return

    for drug in df["drug_name"].unique():
        drug_df = df[df["drug_name"] == drug]

        if len(drug_df) < 1:
            continue

        last_qty = drug_df["qty"].iloc[-1]

        prediction = float(model.predict([[last_qty]])[0])

        forecast_date = (
            datetime.now() + timedelta(days=30)
        ).strftime("%Y-%m-%d")

        conn.execute(
            """
            INSERT INTO dataset_forecasts
            (dataset_id, drug_name, forecast_date, predicted_qty)
            VALUES (?, ?, ?, ?)
            """,
            (dataset_id, drug, forecast_date, prediction)
        )

    conn.commit()
    conn.close()
