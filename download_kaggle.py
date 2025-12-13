# download_kaggle.py
import sys
import os
from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset(dataset_ref, out_dir="data"):
    os.makedirs(out_dir, exist_ok=True)
    api = KaggleApi()
    api.authenticate()
    print(f"Downloading {dataset_ref} into {out_dir} ...")
    api.dataset_download_files(dataset_ref, path=out_dir, unzip=True, quiet=False)
    print("Done.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_kaggle.py <dataset-ref> [out_dir]")
        print("Example: python download_kaggle.py milanzdravkovic/pharma-sales-data data")
        sys.exit(1)
    dataset_ref = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "data"
    download_dataset(dataset_ref, out_dir)
