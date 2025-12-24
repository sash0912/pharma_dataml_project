import pandas as pd
import sqlite3
import uuid
from backend.forecast_service.db import DB_PATH


REQUIRED_CLEAN_COLUMNS = {"drug_name", "date", "qty"}
KAGGLE_COLUMNS = {
    "Drug Name",
    "Sale Date",
    "Units Sold"
}


def process_csv(file_path: str, filename: str) -> str:
    """
    Accepts either:
    1) Clean CSV (drug_name, date, qty)
    2) Kaggle raw pharma sales CSV

    Performs ETL if needed and loads into dataset_demand
    """

    df = pd.read_csv(file_path)

    dataset_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Register dataset
    cur.execute(
        """
        INSERT INTO uploaded_datasets (dataset_id, filename)
        VALUES (?, ?)
        """,
        (dataset_id, filename)
    )

    # ---------- CASE 1: CLEAN CSV ----------
    if REQUIRED_CLEAN_COLUMNS.issubset(df.columns):
        clean_df = df[["drug_name", "date", "qty"]].copy()

    # ---------- CASE 2: KAGGLE RAW CSV ----------
    elif KAGGLE_COLUMNS.issubset(df.columns):
        clean_df = pd.DataFrame({
            "drug_name": df["Drug Name"],
            "date": pd.to_datetime(df["Sale Date"]).dt.strftime("%Y-%m-%d"),
            "qty": df["Units Sold"]
        })

    # ---------- INVALID CSV ----------
    else:
        conn.close()
        raise ValueError(
            "Unsupported CSV format. Please upload a valid pharma sales dataset."
        )

    # Insert into dataset_demand
    for _, row in clean_df.iterrows():
        cur.execute(
            """
            INSERT INTO dataset_demand
            (dataset_id, drug_name, date, qty)
            VALUES (?, ?, ?, ?)
            """,
            (
                dataset_id,
                row["drug_name"],
                row["date"],
                int(row["qty"])
            )
        )

    conn.commit()
    conn.close()

    return dataset_id
