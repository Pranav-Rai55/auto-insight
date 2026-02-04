import pandas as pd
import os

def load_data_from_path(file_path):
    """
    Load a dataset from the given path with safe encoding fallback.
    - Tries UTF-8 first.
    - If decoding fails, retries with Latin-1.
    - Supports .csv, .xlsx, and .xls formats.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")

    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path, encoding="utf-8")
        elif file_path.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
    except UnicodeDecodeError:
        print("⚠️ UTF-8 decode failed — retrying with Latin-1 encoding...")
        df = pd.read_csv(file_path, encoding="latin1")

    print(f"✅ File loaded successfully: {os.path.basename(file_path)}  →  {df.shape[0]} rows, {df.shape[1]} columns")
    return df
