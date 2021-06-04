import pandas as pd

def identity(x):
    return x

def rename(df: pd.DataFrame, new_name: str):
    """
    Rename the first column in a data-frame to the provided string
    """
    return df.rename(columns = {df.columns[0]: new_name})
