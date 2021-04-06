from views_transformation_library.views_2 import tlag

class Context:
    def __init__(self,path,level_of_analysis):
        self.path = path
        self.level_of_analysis = level_of_analysis

def apply_to_first_column(fn):
    def inner(dataframe,*args,**kwargs):
        dataframe[dataframe.columns[0]] = fn(dataframe[dataframe.columns[0]],*args,**kwargs)
        return dataframe
    return inner

def sort_first(fn):
    def inner(dataframe,*args,**kwargs):
        return fn(dataframe.sort_index(level=0),*args,**kwargs)
    return inner


def identity(*args,**kwargs):
    return args[0]

def transform_pipeline(pre,trf,post):
    def inner(dataframe,context,*args,**kwargs):
        prepared = pre(dataframe,context,*args,**kwargs)
        transformed = trf(prepared,*args,**kwargs)
        return post(transformed,context,*args,**kwargs)
    return inner

month_time_lag = transform_pipeline(
        identity,
        apply_to_first_column(sort_first(tlag)),
        identity 
    )
