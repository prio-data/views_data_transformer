from views_transformation_library import splag4d,spatial_tree,temporal_tree

def spatial_lag(df, kernel_inner, kernel_width, kernel_power, norm_kernel):
    '''

    Performs spatial lags on a dataframe by transforming from flat format to 4d tensor
    with dimensions longitude x latitude x time x features.

    Spatial lagging can then be done as a 2d convolution on long-lat slices using
    scipy convolution algorithms.

    Arguments:

    df:                a dataframe of series to be splagged

    use_stride_tricks: boolean, decide to use stride_tricks or not (optional,
                       defaults to True)

    kernel_inner:      inner border of convolution region (set to 1 to exclude central
                       cell)

    kernel_width:      width in cells of kernel, so outer radius of kernel =
                       kernel_inner + kernel_width

    kernel_power:      weight values of cells by (distance from centre of kernel)**
                       (-kernel_power) - set to zero for no distance weighting

    norm_kernel:       set to 1 to normalise kernel weights

    '''

    # Just a wrapper to make arguments positional (expected by the service)
    return splag4d.get_splag4d(
            df,
            kernel_inner = kernel_inner,
            kernel_width = kernel_width,
            kernel_power = kernel_power,
            norm_kernel = norm_kernel
            )

def spatial_tree_lag(df,thetacrit,dfunction_option):

    '''
    get_tree_lag

    Driver function for computing tree-lagged features

    Arguments:

    df: dataframe containing one or more features to be lagged

    thetacrit: opening angle used to decide whether to open nodes - large values cause more
    aggressive aggregation of nodes

    dfunction_option: an integer selecting which distance weighting to use:

                     - 0: ln(1+d) weighting

                     - 1: 1/d weighting

                     - 2: 1/d^2 weighting

    '''

    # Just a wrapper to make arguments positional (expected by the service)
    return spatial_tree.get_tree_lag(
            df,
            thetacrit = thetacrit,
            dfunction_option = dfunction_option
            )

def temporal_tree_lag(df,thetacrit,weight_function,sigma,use_stride_tricks):

    '''
    get_tree_lag

    Driver function for computing temporal-tree-lagged features

    Arguments:

    df:                  dataframe containing feature to be lagged

    thetacrit:           parameter controlling how aggressively nodes in the past are
                         aggregated

    weight_function:    choice of weighting function. Allowed choices:

                        - 'uniform': weights for all nodes are unity. Unlikely to be
                          meaningful but provided for completeness

                        - 'oneovert': weights for nodes are 1/(tnow-tnode)

                        - 'expon': weights for nodes are exp(-(tnow-tnode)/sigma)

                        - 'ramp': weights for nodes are 1-(tnow-tnode)/sigma for
                          (tnow-tnode)<sigma, 0 otherwise

                        - 'sigmoid': weights are 1./(1+np.exp(-lag)) where
                          lag=(mid-tnow+5*sigma5)/sigma5 and sigma5=sigma/5

    tau:              parameter in time units used by df controlling width of expon,
                        ramp and sigmoid functions

    use_stride_tricks:  flag to use numpy stride tricks

    '''

    # Just a wrapper to make arguments positional (expected by the service)
    return temporal_tree.get_tree_lag(
            df,
            thetacrit=thetacrit,
            weight_functions=weight_function,
            sigma=sigma,
            use_stride_tricks=use_stride_tricks
            )

