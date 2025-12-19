import sqlite3
import random

conn = sqlite3.connect("backend/data/forecasts.db")
cursor = conn.cursor()

drugs = {
    "Drug A": 35,
    "Drug B": 50,
    "Drug C": 42,
    "Drug D": 60,
    "Drug E": 28
}

start_year = 2005
end_year = 2025

rows = []

for drug, base in drugs.items():
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            date = f"{year}-{month:02d}-01"

            # Seasonality (higher in winter)
            seasonal_factor = 1.15 if month in [11, 12, 1, 2] else 1.0

            qty = int(
                base * seasonal_factor +
                random.randint(-5, 8)
            )

            qty = max(qty, 5)
            rows.append((date, drug, qty))


cursor.executemany("""
INSERT INTO historical_demand (date, drug_name, qty)
VALUES (?, ?, ?)
""", rows)

conn.commit()
conn.close()

print(f"Inserted {len(rows)} rows successfully!")
