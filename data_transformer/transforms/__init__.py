"""
Transform registry
Here each transform function is registered to a particular LOA
"""
import os
import logging
from . import registry

logger = logging.getLogger(__name__)

def annotate_with(data,fn,arguments):
    to_transform = data.columns[0]
    function_name = os.path.splitext(fn.__module__)[-1].replace(".","_") + "_" + fn.__name__
    annotated = to_transform + function_name
    if arguments:
        annotated = annotated + "_" + "_".join([str(a) for a in arguments])
    data.rename(columns={to_transform:annotated},inplace=True)

def transform(data,loa,transform_name,arguments):
    fn = registry.get_transform(loa,transform_name)
    annotate_with(data,fn,arguments)
    logger.debug("Applying %s with arguments %s",fn.__name__,str(arguments))
    return fn(data,*arguments)
