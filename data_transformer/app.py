"""
Recieves .parquet bytes, does a requested transformation, and returns data in the same format.

Each transform takes two arguments:

    rhs, which is the URL to the router resource to be transformed
    The dataset df, which is retrieved from the rhs
"""
import io
import logging

from fastapi import Response,FastAPI
from requests import HTTPError

from . import url_args, settings, remotes, exceptions, operations, transforms, __version__

try:
    logging.basicConfig(level=getattr(logging,settings.config("LOG_LEVEL")))
except AttributeError:
    pass

logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/")
def handshake():
    return {
        "version": __version__
        }

@app.get("/{loa}/{transform_name}/{url_args_raw}/{rhs:path}")
def transform_data(loa:str, transform_name:str, url_args_raw:url_args.url_args, rhs:str):
    logger.info(f"Doing transform {transform_name}({loa}/{rhs},{url_args_raw})")

    try:
        data = remotes.get_from_router(loa,rhs)

    except HTTPError as httpe:
        resp = httpe.response
        return Response(resp.content,status_code=resp.status_code)

    except ValueError as ve:
        return Response(str(ve))

    arguments = url_args.parse(url_args_raw)

    try:
        namespace, name = transform_name.split(".")
        data = operations.transform_data(data, loa, namespace, name, arguments)

    except exceptions.NotRegistered as nr:
        return Response(f"Transform {transform_name} is not registered for {loa}: {str(nr)}",
                status_code=404)

    except TypeError as type_error:
        return Response("Wrong number of arguments for function "
                f"{transform_name}: {arguments}. Raised {type_error}", status_code = 400)

    fake_file = io.BytesIO()
    data.to_parquet(fake_file,compression="gzip")
    return Response(fake_file.getvalue(),media_type="application/octet-stream")

@app.get("/transforms/")
def list_transforms():
    return {
            "transforms": transforms.registry.list_transforms()
        }

