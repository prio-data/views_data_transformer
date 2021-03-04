import os
import io
import math
import fastapi
import requests
import pandas as pd
import numpy as np

def lag_by_index(df,lag_size,index_no=0):
    """
    "lags" the specified index 
    """
    idx_names = df.index.names
    if idx_names[0] is None:
        idx_names = ["index"]

    df = df.reset_index()
    df[idx_names[index_no]]+=lag_size
    df = df.set_index(idx_names)
    return df


def timelag(rhs_url: str, df:pd.DataFrame, lag_size:int):
    """
    This function exposes lag_by_index, handling the retrieval of data for 
    the previous year(s) to carry over.
    """

    tindices = np.array([i[0] for i in df.index.values])
    start,end = tindices.min(),tindices.max()
    year_unit_size = (end-start)+1
    tlag_year_size = (lag_size / year_unit_size) 

    for i in range(math.ceil(tlag_year_size)):
        prev_url,yr = os.path.split(rhs_url)
        prev_url = os.path.join(prev_url,str(int(yr)-(i+1)))

        prev_request = requests.get(prev_url)

        if prev_request.status_code != 200:
            raise requests.HTTPError(response = prev_request)

        prev_data = pd.read_parquet(io.BytesIO(prev_request.content))
        df = pd.concat([prev_data,df])

    df = lag_by_index(df,lag_size)
    df.columns = [c+"_tlag_"+str(lag_size) for c in df.columns]
    return df.sort_index(level=0).loc[start:end,:]
