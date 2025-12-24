# routes/upload.py

from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import uuid

from backend.forecast_service.services.csv_service import process_csv
from backend.forecast_service.services.dataset_forecast import run_forecast

router = APIRouter(
    prefix="/upload",
    tags=["CSV Upload"]
)


@router.post("/")
def upload_csv(file: UploadFile = File(...)):
    # 1️⃣ Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed"
        )

    # 2️⃣ Save file temporarily
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)

    temp_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 3️⃣ Process CSV → DB
    dataset_id = process_csv(temp_path, file.filename)

    # 4️⃣ Run forecast
    run_forecast(dataset_id)

    # 5️⃣ Cleanup temp file
    os.remove(temp_path)

    # 6️⃣ Return dataset_id for dashboard redirect
    return {
        "dataset_id": dataset_id,
        "message": "CSV uploaded and forecast generated successfully"
    }
