import os
from kaggle.api.kaggle_api_extended import KaggleApi

RAW_DATA_DIR = "data/raw"

DATASETS = [
    "harshal19/pharmaceutical-drug-sales",
    "radheshyamkollipara/pharmaceutical-sales"
]

os.makedirs(RAW_DATA_DIR, exist_ok=True)

api = KaggleApi()
api.authenticate()

for dataset in DATASETS:
    print(f"Downloading dataset: {dataset}")
    api.dataset_download_files(
        dataset,
        path=RAW_DATA_DIR,
        unzip=True
    )

print("All datasets downloaded successfully.")
