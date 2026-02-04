# data_processor.py
"""
Data processing utilities:
- parse uploaded files (csv, xlsx, json)
- infer column types
- basic cleaning (drop duplicates, simple imputation options)
- produce summary metadata for frontend
"""

from typing import Dict, Any, Tuple, Optional
import pandas as pd
import numpy as np
import io

SUPPORTED_FILE_TYPES = (".csv", ".xlsx", ".xls", ".json")


def read_file_bytes(file_bytes: bytes, filename: str) -> pd.DataFrame:
    """Read bytes upload into a pandas DataFrame based on filename extension."""
    lower = filename.lower()
    if lower.endswith(".csv"):
        return pd.read_csv(io.BytesIO(file_bytes))
    if lower.endswith((".xlsx", ".xls")):
        return pd.read_excel(io.BytesIO(file_bytes))
    if lower.endswith(".json"):
        return pd.read_json(io.BytesIO(file_bytes), orient="records")
    raise ValueError(f"Unsupported file type for {filename}")


def infer_column_types(df: pd.DataFrame) -> Dict[str, str]:
    """Return a map column -> inferred type (numeric/categorical/datetime/text)."""
    types = {}
    for col in df.columns:
        series = df[col]
        if pd.api.types.is_datetime64_any_dtype(series):
            types[col] = "datetime"
            continue
        # Try to parse to datetime if many values parse
        if series.dropna().shape[0] > 0:
            sample = series.dropna().iloc[:min(50, series.dropna().shape[0])]
            try_parsed = pd.to_datetime(sample, errors="coerce")
            if try_parsed.notna().sum() / len(sample) > 0.8:
                types[col] = "datetime"
                continue
        if pd.api.types.is_numeric_dtype(series):
            types[col] = "numeric"
        else:
            # If low unique values relative to rows => categorical
            nunique = series.nunique(dropna=True)
            if nunique <= 20 or (nunique / max(1, len(series)) < 0.05):
                types[col] = "categorical"
            else:
                types[col] = "text"
    return types


def basic_clean(
    df: pd.DataFrame,
    drop_duplicates: bool = True,
    fill_na_method: Optional[str] = None,
) -> pd.DataFrame:
    """
    Basic cleaning:
    - drop duplicates by default
    - fill_na_method can be 'mean', 'median', 'mode' or None
    """
    df = df.copy()
    if drop_duplicates:
        df = df.drop_duplicates()

    if fill_na_method is not None:
        for col in df.columns:
            if df[col].isna().sum() == 0:
                continue
            if fill_na_method == "mean" and pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
            elif fill_na_method == "median" and pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
            elif fill_na_method == "mode":
                mode = df[col].mode()
                if len(mode) > 0:
                    df[col] = df[col].fillna(mode.iloc[0])
                else:
                    df[col] = df[col].fillna("")
            else:
                # fallback: forward fill then backfill
                df[col] = df[col].fillna(method="ffill").fillna(method="bfill")
    return df


def compute_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """Return summary statistics & metadata for each column and dataset-level info."""
    col_types = infer_column_types(df)
    summary = {}
    for col in df.columns:
        ser = df[col]
        info = {
            "dtype": str(ser.dtype),
            "inferred_type": col_types.get(col, "unknown"),
            "n_missing": int(ser.isna().sum()),
            "n_unique": int(ser.nunique(dropna=True)),
            "sample_values": ser.dropna().astype(str).unique()[:5].tolist(),
        }
        if pd.api.types.is_numeric_dtype(ser):
            info.update(
                {
                    "mean": None if ser.dropna().empty else float(ser.mean()),
                    "median": None if ser.dropna().empty else float(ser.median()),
                    "min": None if ser.dropna().empty else float(ser.min()),
                    "max": None if ser.dropna().empty else float(ser.max()),
                    "std": None if ser.dropna().empty else float(ser.std()),
                }
            )
        summary[col] = info

    dataset_info = {
        "n_rows": int(df.shape[0]),
        "n_columns": int(df.shape[1]),
        "columns": list(df.columns),
    }

    return {"dataset_info": dataset_info, "columns": summary}


# Convenience end-to-end function
def process_uploaded_file(
    file_bytes: bytes,
    filename: str,
    fill_na_method: Optional[str] = None,
    drop_duplicates: bool = True,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Read file bytes, clean, and return (clean_df, summary_metadata).
    Raises ValueError on unsupported type.
    """
    df = read_file_bytes(file_bytes, filename)
    df_clean = basic_clean(df, drop_duplicates=drop_duplicates, fill_na_method=fill_na_method)
    metadata = compute_summary(df_clean)
    return df_clean, metadata


if __name__ == "__main__":
    # quick local test
    csv = b"country,sales,month\nA,100,2020-01\nB,150,2020-01\nA,120,2020-02\n"
    df, meta = process_uploaded_file(csv, "test.csv")
    print(meta)
