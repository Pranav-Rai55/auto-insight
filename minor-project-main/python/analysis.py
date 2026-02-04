# analysis.py

import pandas as pd

# --------------------------
# Summary Statistics
# --------------------------
def basic_stats(df, columns=None):
    if columns:
        return df[columns].describe()
    return df.describe()

# --------------------------
# Correlation matrix
# --------------------------
def correlation(df, method='pearson'):
    return df.corr(method=method)

# --------------------------
# Value counts for categorical columns
# --------------------------
def value_counts(df, column):
    return df[column].value_counts()

# --------------------------
# Grouped statistics
# --------------------------
def grouped_stats(df, group_col, agg_col, agg_func='mean'):
    return df.groupby(group_col)[agg_col].agg(agg_func).reset_index()

# --------------------------
# Detect outliers using IQR
# --------------------------
def detect_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(df[column] < lower) | (df[column] > upper)]
