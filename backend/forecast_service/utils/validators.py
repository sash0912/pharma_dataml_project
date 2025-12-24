# utils/validators.py

REQUIRED_COLUMNS = {"drug_name", "date", "qty"}

def validate_csv(df):
    """
    Validates uploaded CSV structure
    """
    if df.empty:
        raise ValueError("CSV file is empty")

    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {missing}")
