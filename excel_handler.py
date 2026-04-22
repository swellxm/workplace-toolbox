import pandas as pd
import openpyxl
from io import BytesIO
from typing import Optional, Tuple

def read_excel_file(file) -> pd.DataFrame:
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    return pd.read_excel(file)

def deduplicate_data(df: pd.DataFrame, keep: str = 'first') -> pd.DataFrame:
    return df.drop_duplicates(keep=keep)

def summarize_data(df: pd.DataFrame, group_col: str, value_col: str, agg_func: str) -> pd.DataFrame:
    result = df.groupby(group_col)[value_col].agg(agg_func).reset_index()
    result.columns = [group_col, f"{value_col}_{agg_func}"]
    return result

def split_by_value(df: pd.DataFrame, split_col: str) -> dict:
    unique_values = df[split_col].unique()
    return {str(value): df[df[split_col] == value] for value in unique_values}

def split_by_count(df: pd.DataFrame, rows_per_file: int) -> list:
    n_splits = len(df) // rows_per_file + (1 if len(df) % rows_per_file else 0)
    return [df.iloc[i * rows_per_file:min((i + 1) * rows_per_file, len(df))] for i in range(n_splits)]

def merge_dataframes(dfs: list) -> pd.DataFrame:
    return pd.concat(dfs, ignore_index=True)

def convert_format(df: pd.DataFrame, target_format: str) -> BytesIO:
    output = BytesIO()
    if target_format == 'csv':
        df.to_csv(output, index=False, encoding='utf-8-sig')
    else:
        df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    return output

def get_column_types(df: pd.DataFrame) -> dict:
    return {
        'numeric': df.select_dtypes(include=['number']).columns.tolist(),
        'categorical': df.select_dtypes(include=['object']).columns.tolist(),
        'datetime': df.select_dtypes(include=['datetime']).columns.tolist()
    }
