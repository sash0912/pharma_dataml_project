import pandas as pd
import sqlite3

DB_PATH = "backend/data/forecasts.db"
CSV_PATH = "data/raw/kaggle_sample_pharma_sales.csv"

# Load CSV
df = pd.read_csv(CSV_PATH)

# Rename required columns
df = df.rename(columns={
    "Sale Date": "date",
    "Drug Name": "drug_name",
    "Units Sold": "qty"
})

# Keep only required columns
df = df[["date", "drug_name", "qty"]]

# Parse date
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Drop bad rows
df = df.dropna()

# Save to SQLite
conn = sqlite3.connect(DB_PATH)
df.to_sql("historical_demand", conn, if_exists="replace", index=False)
conn.close()

print("✅ Historical demand successfully loaded")
print(df.head())
