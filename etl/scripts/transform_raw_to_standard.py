import os
import pandas as pd

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)

def standardize_sales_dataset(
    file_name: str,
    date_col: str,
    source_name: str
):
    print(f"Processing {file_name}")

    df = pd.read_csv(os.path.join(RAW_DIR, file_name))

  
    df["date"] = pd.to_datetime(df[date_col], errors="coerce")

  
    drug_cols = [
        col for col in df.columns
        if col.startswith(("M01", "N02", "N05", "R03", "R06"))
    ]

 
    long_df = df.melt(
        id_vars=["date"],
        value_vars=drug_cols,
        var_name="product",
        value_name="qty"
    )


    long_df["price"] = None
    long_df["region"] = None
    long_df["source"] = source_name


    long_df = long_df.dropna(subset=["date", "qty"])

    return long_df


all_dfs = []

all_dfs.append(
    standardize_sales_dataset(
        "kaggle_sales_hourly.csv",
        "datum",
        "kaggle_sales_hourly"
    )
)

all_dfs.append(
    standardize_sales_dataset(
        "kaggle_sales_daily.csv",
        "datum",
        "kaggle_sales_daily"
    )
)

all_dfs.append(
    standardize_sales_dataset(
        "kaggle_sales_monthly.csv",
        "datum",
        "kaggle_sales_monthly"
    )
)

final_df = pd.concat(all_dfs, ignore_index=True)

output_path = os.path.join(PROCESSED_DIR, "standardized_sales.csv")
final_df.to_csv(output_path, index=False)

print(f"Standardized dataset saved to {output_path}")
print(f"Total rows: {len(final_df)}")
