"""
Guards
======

Some operations rely on certain assumptions about the data being true. These
decorators ensure that assumptions hold true.
"""
from typing import Callable, Any
import functools
import pandas as pd
import numpy as np

def preprocess(with_function: Callable[[pd.DataFrame], pd.DataFrame]):
    def wrapper(fn: Callable[[Any], pd.DataFrame]) -> Callable[[Any], pd.DataFrame]:
        @functools.wraps(fn)
        def inner(df: pd.DataFrame, *args, **kwargs):
            df = with_function(df)
            return fn(df, *args, **kwargs)
        return inner
    return wrapper

def floats_only(df: pd.DataFrame)-> pd.DataFrame:
    """
    floats_only
    ===========

    parameters:
        df (pandas.DataFrame): A dataframe with any kind of data types
    returns:
        pandas.DataFrame: A dataframe with only floats

    Converts any dataframe to a dataframe with only floats, replacing datatypes
    that cannot be converted with missing values (numpy.NaN).
    """
    for column in df.columns:
        try:
            df[column] = df[column].astype(float)
        except ValueError:
            df[column] = np.NaN

    return df
