"""
In this module is functionality related to the task of parsing a tuple of
arguments, complete with proper type inference, from a string.

Ideally, we'd use paths for this (e.g /add/1/1>2), but since there's already a
lot of dynamic pathing going on, I've opted to do /add2/1_1/base/1>3 instead
(the 1_1 is a tuple of arguments).

Args can be ints, floats or strings. Keyword arguments are not supported.
"""
from pydantic import constr

valid_characters=r"A-Za-z0-9\."
url_args_regexp = (r"^((?:"
    f"[{valid_characters}]|"
    f"(?:(?<=[{valid_characters}])_(?=[{valid_characters}])"
    r"))+|_)$"
    )

url_args = constr(regex=url_args_regexp)

def type_infer(p):
    if p == "_":
        return None
    try:
        return int(p)
    except ValueError:
        try:
            return float(p)
        except ValueError:
            return str(p)

def parse_url_args(raw:str):
    url_args.validate(raw)
    args = [type_infer(a) for a in raw.split("_")]
    args = [a for a in args if a is not None and a != '']
    return args

transform_namespace_name = constr(regex=r"[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+")

def parse_transform_namespace_name(namespace_name):
    return namespace_name.split(".")
