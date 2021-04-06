"""
Recieves .parquet bytes, does a requested transformation, and returns data in the same format.

Each transform takes two arguments:

    rhs, which is the URL to the router resource to be transformed
    The dataset df, which is retrieved from the rhs
"""
import io
import os
import re

import logging

import pydantic
import requests
from requests.exceptions import HTTPError
import fastapi

import pandas as pd
import url_args
from transforms import month_time_lag,Context

from settings import config

try:
    logging.basicConfig(level=getattr(logging,config("LOG_LEVEL")))
except AttributeError:
    pass

logger = logging.getLogger(__name__)

app = fastapi.FastAPI()

TRANSFORMS = {
        "priogrid_month":{
            "identity":lambda df,ctx: df,
            "tlag": month_time_lag
            },
        "country_month":{
            "identity":lambda df,ctx: df,
            "tlag": month_time_lag
            }
        }

@app.get("/{loa}/{transform_name}/{url_args_raw}/{rhs:path}")
def transform(loa:str, transform_name:str, url_args_raw:url_args.url_args, rhs:str):
    rhs_url = os.path.join(config("ROUTER_URL"),loa,rhs)
    rhs_request = requests.get(rhs_url)

    ctx = Context(path=rhs,level_of_analysis=loa)

    if not rhs_request.status_code == 200:
        return fastapi.Response(f"Router returned {rhs_request.status_code} "
                f"{rhs_request.content}",
                status_code=rhs_request.status_code)


    try:
        data = pd.read_parquet(io.BytesIO(rhs_request.content))
    except ValueError:
        logger.error("%s - %s - %s expected a parquet file, but %s was not valid parquet",
                loa,transform_name,url_args_raw,rhs)
        return fastapi.Response(f"RHS {rhs} returned wrong data type "
                f"{str(rhs_request.content)}",
                status_code=500)

    try:
        fn = TRANSFORMS[loa][transform_name]
    except KeyError:
        return fastapi.Response(f"Transform not found: {loa}>{transform_name}", status_code=404)

    if url_args_raw == "_":
        args = []
    else:
        args = url_args.parse(url_args_raw)
        
    try:
        data = fn(data,ctx,*args)
    except TypeError as e:
        # Wrong number of arguments
        return fastapi.Response(content=str(e),status_code=400)
    except HTTPError as httpe:
        return fastapi.Response(content=str(httpe.response.content),status_code=httpe.response.status_code)

    fake_file = io.BytesIO()
    data.to_parquet(fake_file,compression="gzip")

    return fastapi.Response(fake_file.getvalue(),media_type="application/octet-stream")
