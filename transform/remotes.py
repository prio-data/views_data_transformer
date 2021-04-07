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
        return fastapi.Response(f"Router returned {response.status_code} "
                f"{response.content}",
                status_code=response.status_code)


    try:
        data = pd.read_parquet(io.BytesIO(response.content))
    except ValueError:
        return fastapi.Response(f"{path} was not parquet: {str(response.content)}",status_code=500)

    return data
