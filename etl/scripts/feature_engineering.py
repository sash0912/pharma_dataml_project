import os
import pandas as pd

PROCESSED_FILE = "data/processed/standardized_sales.csv"
FEATURE_DIR = "data/features"

os.makedirs(FEATURE_DIR, exist_ok=True)

df = pd.read_csv(PROCESSED_FILE)

df["date"] = pd.to_datetime(df["date"], errors="coerce", format="mixed")

df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

monthly_df = (
    df.groupby(["month", "product"])["qty"]
    .sum()
    .reset_index()
    .sort_values(["product", "month"])
)

for lag in [1, 3, 6, 12]:
    monthly_df[f"lag_{lag}"] = (
        monthly_df.groupby("product")["qty"]
        .shift(lag)
    )

monthly_df["rolling_mean_3"] = (
    monthly_df.groupby("product")["qty"]
    .rolling(3)
    .mean()
    .reset_index(level=0, drop=True)
)

monthly_df["rolling_mean_6"] = (
    monthly_df.groupby("product")["qty"]
    .rolling(6)
    .mean()
    .reset_index(level=0, drop=True)
)

monthly_df["rolling_std_3"] = (
    monthly_df.groupby("product")["qty"]
    .rolling(3)
    .std()
    .reset_index(level=0, drop=True)
)

monthly_df = monthly_df.dropna()

output_path = os.path.join(FEATURE_DIR, "sales_features_monthly.csv")
monthly_df.to_csv(output_path, index=False)

print(f"Feature dataset saved to {output_path}")
print(f"Total rows: {len(monthly_df)}")
