
import os
import io
import logging
import requests
from requests.exceptions import HTTPError
import pandas as pd
import settings

def get_data(loa,path):
    """
    Retrieves corresponding data from Router
    """
    url = os.path.join(settings.ROUTER_URL,loa,path)
    response = requests.get(url)
    if not response.status_code == 200:
        raise HTTPError(response=response)
    """
    if not response.headers["Content-Type"] == "application/octet-stream":
        raise ValueError(f"Request to {url} returned wrong Content-Type:"
        f"{response.headers['Content-Type']}"
        )
    """
    try:
        dataframe = pd.read_parquet(io.BytesIO(response.content))
    except OSError as ose:
        raise ValueError(
                f"Response from {url} was not parquet: {response.content}"
                ) from ose

    return dataframe

def get_nav(path):
    """
    Retrieves temporal navigation information for a given path
    """
    url = os.path.join(settings.ROUTER_URL,"nav",path)
    response = requests.get(url)
    if not response.status_code == 200:
        raise HTTPError(response=response)
    return response.json()

def merge_with_previous(loa,path,dataframe,until):
    """
    Merges data with previous until path year >= until 
    or path == lower path bound
    """
    logging.warning("merging with prev")
    nav = get_nav(path)
    current_year = nav["current"]["year"] 
    data = pd.concat([dataframe,get_data(loa,nav["previous"]["path"])])
    if current_year == until or nav["current"]["path"] == nav["bounds"]["start"]["path"]:
        return data
    else:
        return merge_with_previous(loa,nav["previous"]["path"],data,until)
