import os, sys
import pandas as pd

DATA_FILE = "master_csv.csv"   
def load_data():
    """
    Load and preprocess the master stock dataset.
    - Validates file existence
    - Converts Date column to datetime
    - Sorts by Symbol and Date
    Returns: Pandas DataFrame
    """
    if not os.path.exists(DATA_FILE):
        sys.exit("Error: master_csv.csv not found. Run yaml_to_csv.py first.")

    df = pd.read_csv(DATA_FILE)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    if "ticker" in df.columns and "date" in df.columns:
        df.sort_values(by=["ticker", "date"], inplace=True)

    return df
