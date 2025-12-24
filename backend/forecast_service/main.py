from backend.forecast_service.routes.llm_qa import router as llm_router
from backend.forecast_service.routes.question_answer import router as qa_router
from backend.forecast_service.routes.drug_forecast import router as drug_forecast_router
from backend.forecast_service.routes.drug_analytics import router as drug_analytics_router
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
from fastapi import FastAPI
from backend.forecast_service.schemas import ForecastRequest, ForecastResponse
from backend.forecast_service.analytics import get_basic_analytics, get_recent_trend
from backend.forecast_service.db import init_db, save_forecast, DB_PATH
from backend.forecast_service.cache import get_cached_prediction, set_cached_prediction
from backend.forecast_service.routes.upload import router as upload_router
from backend.forecast_service.routes.dashboard import router as dashboard_router



import sqlite3

MODEL_PATH = "ml/models/xgboost_model.pkl"
model = joblib.load(MODEL_PATH)

app = FastAPI(
    title="Pharmaceutical Demand Forecast API",
    version="1.0"
)

app.include_router(drug_analytics_router)
app.include_router(drug_forecast_router)
app.include_router(qa_router) 
app.include_router(llm_router)
app.include_router(upload_router)
app.include_router(dashboard_router)




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


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
    prediction = round(prediction * 1.05, 2)

    save_forecast(input_data, float(prediction))
    set_cached_prediction(input_data, float(prediction))

    return {"predicted_qty": prediction}


@app.get("/history")
def get_forecast_history(limit: int = 10):
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

    return [{"created_at": r[0], "predicted_qty": r[1]} for r in rows]


@app.get("/analytics/summary")
def analytics_summary():
    return get_basic_analytics()


@app.get("/analytics/trend")
def analytics_trend(days: int = 7):
    return get_recent_trend(days)
