import pandas as pd
import sqlite3

DB_PATH = "backend/data/forecasts.db"
DATA_PATH = "data/raw/kaggle_sample_pharma_sales.csv"

def load_data():
    df = pd.read_csv(DATA_PATH)

    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    df["sale_date"] = pd.to_datetime(df["sale_date"])

    df["month"] = df["sale_date"].dt.to_period("M").astype(str)

    monthly = (
        df.groupby(["month", "drug_name"])["units_sold"]
        .sum()
        .reset_index()
    )

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historical_demand (
            date TEXT,
            drug_name TEXT,
            qty INTEGER
        )
    """)


    cursor.execute("DELETE FROM historical_demand")

    for _, row in monthly.iterrows():
        cursor.execute(
            """
            INSERT INTO historical_demand (date, drug_name, qty)
            VALUES (?, ?, ?)
            """,
            (row["month"], row["drug_name"], int(row["units_sold"]))
        )

    conn.commit()
    conn.close()

    print("Historical drug-level demand loaded successfully")

if __name__ == "__main__":
    load_data()
