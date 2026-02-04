# cleaning.py

import pandas as pd

# --------------------------
# Load Data
# --------------------------
def load_data(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type. Use CSV or Excel.")
    return df

# --------------------------
# Remove duplicates
# --------------------------
def remove_duplicates(df):
    return df.drop_duplicates()

# --------------------------
# Handle missing values
# method: 'drop' or 'fill'
# fill_value: value to fill if method='fill'
# --------------------------
def handle_missing(df, method='drop', fill_value=None):
    if method == 'drop':
        return df.dropna()
    elif method == 'fill':
        if fill_value is not None:
            return df.fillna(fill_value)
        else:
            raise ValueError("fill_value must be provided when method='fill'")
    else:
        raise ValueError("Method must be 'drop' or 'fill'")

# --------------------------
# Convert data types
# --------------------------
def convert_dtype(df, column, dtype):
    df[column] = df[column].astype(dtype)
    return df

# --------------------------
# Basic summary
# --------------------------
def summary(df):
    return df.describe(include='all')
