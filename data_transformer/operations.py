"""
Stateful operations
"""

from . import transforms

def transform_data(data, data_type, namespace, name, arguments):
    fn = transforms.registry.get_transform(data_type, namespace, name)
    return fn(data, *arguments)
