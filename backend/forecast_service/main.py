from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

MODEL_PATH = "ml/models/xgboost_model.pkl"


model = joblib.load(MODEL_PATH)

app = FastAPI(
    title="Pharmaceutical Demand Forecast API",
    version="1.0"
)


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
    data = pd.DataFrame([request.dict()])
    prediction = model.predict(data)[0]
    return {"predicted_qty": round(float(prediction), 2)}
