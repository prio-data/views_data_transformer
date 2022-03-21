from views_transformation_library import temporal_entropy
from . import guards

@guards.preprocess(guards.floats_only)
def temp_entropy(df,window):
    """"
    get_temporal_entropy created 04/03/2022 by Jim Dale

    Computed entropy along the time axis within a window of length specified by 'window'.

    The entropy of a feature x over a window of length w is

    sum_(i=1,w) (x_i/X)log_2(x_i/X) where X = sum_(i=1,w) (x_i)

    Arguments:

    df:                a dataframe for which entropy is to be computed

    window:            intger size of window

    Returns:

    A df containing the entropy computed for all times for all columns

    """

    # Just a wrapper to make arguments positional (expected by the service)
    return temporal_entropy.get_temporal_entropy(df,window=window)
