"""
Recieves .parquet bytes, does a requested transformation, and returns data in the same format.
"""
import io
import os
import requests
import fastapi
import pandas as pd

ROUTER_URL = "http://0.0.0.0:8000"

app = fastapi.FastAPI()

TRANSFORMS = {
        "priogrid_month":{
            "identity":lambda x: x
            },
        "country_month":{
            "identity":lambda x: x
            }
        }

def type_infer(p):
    try:
        return int(p)
    except ValueError:
        return str(p)

@app.get("/{loa}/{transform_name}/{params}/{rhs:path}")
def transform(loa:str,transform_name:str,params:str,rhs:str):
    rhs_request = requests.get(os.path.join(ROUTER_URL,loa,rhs))

    if not rhs_request.status_code == 200:
        return fastapi.Response(f"Router returned {rhs_request.status_code} "
                f"{rhs_request.content}",
                status_code=rhs_request.status_code)


    try:
        data = pd.read_parquet(io.BytesIO(rhs_request.content))
    except ValueError:
        return fastapi.Response(f"RHS {rhs} returned wrong data type "
                f"{str(rhs_request.content)}",
                status_code=500)

    try:
        fn = TRANSFORMS[loa][transform_name]
    except KeyError:
        return fastapi.Response(f"Transform not found: {loa}>{transform_name}", status_code=404)

    """
    if params != "_":
        args = [type_infer(p) for p in params.split("_")] + [data]
    else:
        args = [data]
    data = fn(*params)
    """

    fake_file = io.BytesIO()
    data.to_parquet(fake_file,compression="gzip")
    return fastapi.Response(fake_file.getvalue(),media_type="application/octet-stream")
