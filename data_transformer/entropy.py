from views_transformation_library import temporal_entropy as te
from . import guards

@guards.preprocess(guards.floats_only)

def temporal_entropy(df,window,offset):
    """"
    get_temporal_entropy created 04/03/2022 by Jim Dale

    Computed entropy along the time axis within a window of length specified by 'window'.

    The entropy of a feature x over a window of length w is

    sum_(i=1,w) (x_i/X)log_2(x_i/X) where X = sum_(i=1,w) (x_i)

    Arguments:

    df:                a dataframe for which entropy is to be computed

    window:            integer size of window

    offset:            datasets containing mostly zeros will return
                       NaNs or Infs for entropy most or all of the time.
                       Since this is unlikely to be desirable, an
                       offset can be added to all feature values. so
                       that sensible values for entropy are returned.

    Returns:

    A df containing the entropy computed for all times for all columns

    """

    # Just a wrapper to make arguments positional (expected by the service)
    return te.get_temporal_entropy(df,window=window,offset=offset)
