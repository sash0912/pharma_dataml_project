import pandas as pd
import sqlite3
import uuid
from backend.forecast_service.db import DB_PATH
from backend.forecast_service.utils.validators import validate_csv

def process_csv(file_path, filename):
    dataset_id = str(uuid.uuid4())
    df = pd.read_csv(file_path)

    validate_csv(df)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO uploaded_datasets(dataset_id, filename) VALUES (?, ?)",
        (dataset_id, filename)
    )

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO dataset_demand(dataset_id, drug_name, date, qty)
            VALUES (?, ?, ?, ?)
        """, (dataset_id, row["drug_name"], row["date"], int(row["qty"])))

    conn.commit()
    conn.close()

    return dataset_id
