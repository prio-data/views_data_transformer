from collections import defaultdict
from views_transformation_library.views_2 import tlag
from fetch import merge_with_previous,get_nav
from calls import get_year_month_id_bounds
import logging

class Context:
    def __init__(self,path,level_of_analysis):
        self.path = path
        self.level_of_analysis = level_of_analysis
        self.nav = None

    @property
    def year(self):
        if self.nav is None:
            self.get_nav()
        return self.nav["current"]["year"]
    
    def get_nav(self):
        self.nav = get_nav(self.path)

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

def get_previous_months(dataframe,context,*args,**_):
    n_months = args[0]
    n_years = (n_months // 12) + 1 
    until = context.year - n_years
    dataframe = merge_with_previous(
            context.level_of_analysis,
            context.path,dataframe,until
        )
    return dataframe

def trim_to_year(dataframe,context,*_,**__):
    start,end = get_year_month_id_bounds(context.year)
    subset = dataframe.sort_index(level=0).loc[start:end,:]
    return subset

month_time_lag = transform_pipeline(
        get_previous_months,
        apply_to_first_column(sort_first(tlag)),
        identity 
    )
