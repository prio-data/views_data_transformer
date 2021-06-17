import pandas as pd

def rename(df: pd.DataFrame, *args):
    """
    Rename the first column in a data-frame to the provided string
    """
    new_name = "_".join([str(a) for a in args])
    return df.rename(columns = {df.columns[0]: new_name})
