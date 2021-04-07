"""
Transform registry
Here each transform function is registered to a particular LOA
"""
from . import registry

def transform(data,loa,transform_name,arguments):
    fn = registry.get_transform(loa,transform_name)
    return fn(data,*arguments)

