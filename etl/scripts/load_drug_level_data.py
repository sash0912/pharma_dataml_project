import pandas as pd
import sqlite3

CSV_PATH = "data/raw/kaggle_sample_pharma_sales.csv"
DB_PATH = "backend/data/forecasts.db"

df = pd.read_csv(CSV_PATH)


df["Sale Date"] = pd.to_datetime(df["Sale Date"])
df["Units Sold"] = df["Units Sold"].astype(int)

final_df = df[["Sale Date", "Drug Name", "Units Sold"]].rename(
    columns={
        "Sale Date": "date",
        "Drug Name": "drug_name",
        "Units Sold": "qty"
    }
)

conn = sqlite3.connect(DB_PATH)
final_df.to_sql("historical_demand", conn, if_exists="append", index=False)
conn.close()

print(f"Inserted {len(final_df)} rows into historical_demand")
