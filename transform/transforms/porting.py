"""
Wrappers useful for porting transforms from ViEWS 2
"""
import functools

def vectorize_across_dataframe(fn):
    """
    Wraps series-applied function so that it can be applied to a
    data-frame. It is then applied to each column in the data-frame. 

    The transform service only ever handles single-column data-frames (excepting indices).
    """
    @functools.wraps(fn)
    def inner(data,*args,**kwargs):
        for name in data.columns:
            data[name] = fn(data[name],*args,**kwargs)
        return data
    return inner
