"""
Recieves .parquet bytes, does a requested transformation, and returns data in the same format.

Each transform takes two arguments:

    rhs, which is the URL to the router resource to be transformed
    The dataset df, which is retrieved from the rhs
"""
from typing import List
import io
import logging

from fastapi import Response,FastAPI
from requests import HTTPError

from . import parsing, settings, remotes, exceptions, operations, transforms, __version__, models

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

@app.get("/apply/{loa}/{transform_namespace_name}/{url_args_raw}/{rhs:path}")
def transform_data(
        loa:str,
        transform_namespace_name: parsing.transform_namespace_name,
        url_args_raw: parsing.url_args,
        rhs:str):

    try:
        data = remotes.get_from_router(loa,rhs)

    except HTTPError as httpe:
        resp = httpe.response
        return Response(resp.content,status_code=resp.status_code)

    except ValueError as ve:
        return Response(str(ve))

    namespace, name = parsing.parse_transform_namespace_name(transform_namespace_name)
    arguments = parsing.parse_url_args(url_args_raw)

    logger.info(f"Doing transform {namespace}.{name} ({arguments})")

    try:
        data = operations.transform_data(data, loa, namespace, name, arguments)

    except exceptions.NotRegistered as nr:
        return Response(f"Transform {namespace}.{name} is not registered for {loa}: {str(nr)}",
                status_code=404)

    except TypeError as type_error:
        return Response("Wrong number of arguments for function "
                f"{namespace}.{name}: {arguments}. Raised {type_error}", status_code = 400)

    fake_file = io.BytesIO()
    data.to_parquet(fake_file,compression="gzip")
    return Response(fake_file.getvalue(),media_type="application/octet-stream")

@app.get("/transforms/")
def transform_list()-> List[models.Transform]:
    return {
            "transforms": transforms.registry.list_transforms()
        }


@app.get("/transforms/{loa}/{transform_namespace_name}/")
def transform_detail(
        loa: str,
        transform_namespace_name: parsing.transform_namespace_name,
        )-> List[models.Transform]:
    namespace, name = parsing.parse_transform_namespace_name(transform_namespace_name)
    try:
        return transforms.registry.get_transform_function_detail(loa, namespace, name)
    except exceptions.NotRegistered:
        return Response(status_code = 404)

