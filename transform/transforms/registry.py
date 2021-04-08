"""
Returns functions from a
"""
import os
import importlib
from . import exceptions 

_LOA_DISALLOW = {
        "priogrid_month":[],
        "country_month":[
                "grid",
            ]
    }

def get_transform(loa,name):
    try:
        module,function_name = name.split(".")
        assert module not in _LOA_DISALLOW[loa]
        from_mod,_ = os.path.splitext(__name__)
        module = importlib.import_module("."+module,package=from_mod)
        fn = getattr(module,function_name)
    except (ModuleNotFoundError,AttributeError,AssertionError) as e:
        raise exceptions.NotRegistered(e) from e
    return fn
