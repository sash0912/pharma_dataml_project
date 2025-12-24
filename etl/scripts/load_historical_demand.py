import pandas as pd
import sqlite3
from pathlib import Path

DB_PATH = "backend/data/forecasts.db"
CSV_PATH = "data/raw/kaggle_sample_pharma_sales.csv"

# Load CSV
df = pd.read_csv(CSV_PATH)

# Rename columns to match DB schema
df = df.rename(columns={
    "Drug Name": "drug_name",
    "Sale Date": "date",
    "Units Sold": "qty"
})

# Keep only required columns
df = df[["date", "drug_name", "qty"]]

# Convert date
df["date"] = pd.to_datetime(df["date"])

# Aggregate (important)
df = df.groupby(
    ["drug_name", pd.Grouper(key="date", freq="M")]
)["qty"].sum().reset_index()

# Insert into DB
conn = sqlite3.connect(DB_PATH)
df.to_sql("historical_demand", conn, if_exists="replace", index=False)
conn.close()

print("✅ historical_demand restored successfully")
