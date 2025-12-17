import pandas as pd
import joblib
from fastapi import FastAPI
from pydantic import BaseModel
from backend.forecast_service.schemas import ForecastRequest, ForecastResponse
from backend.forecast_service.analytics import get_basic_analytics, get_recent_trend
from backend.forecast_service.db import init_db, save_forecast
from backend.forecast_service.cache import get_cached_prediction, set_cached_prediction

MODEL_PATH = "ml/models/xgboost_model.pkl"


model = joblib.load(MODEL_PATH)

app = FastAPI(
    title="Pharmaceutical Demand Forecast API",
    version="1.0"
)
init_db()
class ForecastRequest(BaseModel):
    lag_1: float
    lag_3: float
    lag_6: float
    lag_12: float
    rolling_mean_3: float
    rolling_mean_6: float
    rolling_std_3: float

class ForecastResponse(BaseModel):
    predicted_qty: float

@app.get("/")
def health_check():
    return {"status": "Forecast service is running"}

@app.post("/predict", response_model=ForecastResponse)
def predict_demand(request: ForecastRequest):
    input_data = request.dict()
    data = pd.DataFrame([input_data])

    cached = get_cached_prediction(input_data)
    if cached is not None:
        return {"predicted_qty": cached}

    prediction = model.predict(data)[0]

    prediction = max(prediction, 0)
    prediction = round(prediction, 2)
    prediction = prediction * 1.05

    save_forecast(input_data, float(prediction))
    set_cached_prediction(input_data, float(prediction))

    return {"predicted_qty": round(float(prediction), 2)}

@app.get("/history")
def get_forecast_history(limit: int = 10):
    import sqlite3

    conn = sqlite3.connect("backend/data/forecasts.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT created_at, predicted_qty
        FROM forecasts
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {"created_at": r[0], "predicted_qty": r[1]}
        for r in rows
    ]
@app.get("/analytics/summary")
def analytics_summary():
    return get_basic_analytics()


@app.get("/analytics/trend")
def analytics_trend(days: int = 7):
    return get_recent_trend(days)

