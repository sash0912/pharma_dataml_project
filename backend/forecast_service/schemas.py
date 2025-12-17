from pydantic import BaseModel, Field

class ForecastRequest(BaseModel):
    lag_1: float = Field(..., ge=0, description="Last month demand")
    lag_3: float = Field(..., ge=0, description="3 months ago demand")
    lag_6: float = Field(..., ge=0, description="6 months ago demand")
    lag_12: float = Field(..., ge=0, description="12 months ago demand")

    rolling_mean_3: float = Field(..., ge=0)
    rolling_mean_6: float = Field(..., ge=0)
    rolling_std_3: float = Field(..., ge=0)

class ForecastResponse(BaseModel):
    predicted_qty: float
