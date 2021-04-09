import os
import io
import logging

import fastapi
import requests
import pandas as pd
from . import settings

logger = logging.getLogger(__name__)

def router_url(loa,path):
    ROUTER_URL = settings.config("ROUTER_URL")
    return os.path.join(ROUTER_URL,loa,path)

def get_from_router(loa,path)->pd.DataFrame:
    response = requests.get(router_url(loa,path))

    if not response.status_code == 200:
        raise requests.HTTPError(response=response)

    try:
        data = pd.read_parquet(io.BytesIO(response.content))
    except ValueError as ve:
        raise ValueError(f"{path} was not parquet: {str(response.content)}") from ve

    return data
