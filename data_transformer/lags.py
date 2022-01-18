from views_transformation_library import splag4d,splag_country,spatial_tree,temporal_tree,spacetime_distance
from . import guards

@guards.preprocess(guards.floats_only)
def spatial_lag(df, kernel_inner, kernel_width, kernel_power, norm_kernel):
    '''

    spatial_lag

    Performs convolutional spatial lags on a pg dataframe by transforming from flat 
    format to 4d tensor with dimensions longitude x latitude x time x features.

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

@guards.preprocess(guards.floats_only)
def spatial_lag_country(df,kernel_inner,kernel_width,kernel_power,norm_kernel):
    '''
    
    spatial_lag_country
    
    Performs convolutional spatial lags on a country dataframe. 
    
    Country neighbours are obtained from the country_country_month_expanded table
    in the database.
    
    Arguments:

    df:             a dataframe of series to be splagged
    
    kernel_inner:   'radius' in countries where you wish to start collecting neighbours 
                    - 0 indicates that you include the target country, 1 indicates that 
                    you leave out the target country, 2 indicates that you leave out the 
                    target country and its neighbours, and so on.
    
    kernel_width:   how far out in countries from the inner radius you wish to go. For 
                    example, to get just the immediate neighbours but not the target 
                    country, set kernel_inner to 1, kernel_width to 1. To get neighbours 
                    of neighbours as well, set kernel_inner to 1, kernel_width to 2.   
    
    kernel_power:   controls distance weighting. Distances are obtained from country
                    centroids, and the contribution of a country to the spatial lag
                    is feature(country)*distance**(kernel_power). Setting kernel_power
                    to 0 produces unweighted results.
                   
    norm_kernel:    set to 1 to normalise kernel weights         
    
    '''
    
    # Just a wrapper to make arguments positional (expected by the service)
    return splag_country.get_splag_country(
            df,
            kernel_inner = kernel_inner,
            kernel_width = kernel_width,
            kernel_power = kernel_power,
            norm_kernel = norm_kernel
            )

@guards.preprocess(guards.floats_only)
def spatial_tree_lag(df,thetacrit,dfunction_option):

    '''
    
    spatial_tree_lag
    
    Performs spatial lags on a pg dataframe using a two-dimensional tree 

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

@guards.preprocess(guards.floats_only)
def spacetime_dist(df,thetacrit,dfunction_option):

    '''
    
    spacetime_dist
    
    For every point in the supplied df, uses scipy.spatial cKDTree to find the nearest k
    past events (where an event is any non-zero value in the input df) and returns either 
    the mean spacetime distance to the k events, or the mean of 
    (size of event)/(spacetime distance)**power.
    
    Arguments:

    df:            input df

    return_values: choice of what to return. Allowed values:

                   distances - return mean spacetime distance to nearest k events     

                   weights   - return mean of (size of event)/(spacetime distance)**power

    k:             number of nearest events to be averaged over

    nu:            weighting to be applied to time-component of distances, so that 
                   spacetime distance = sqrt(delta_latitude^2 + delta_longitude^2 +
                   nu^2*delta_t^2)

    power:         power to which distance is raised when computing weights. Negative
                   values are automatically converted to positive values.

    '''


    # Just a wrapper to make arguments positional (expected by the service)
    return spacetime_distance.get_spacetime_distances(
            df,
            return_values=return_values,
            k=k,
            nu=nu,
            power=power
            )

@guards.preprocess(guards.floats_only)
def temporal_tree_lag(df,thetacrit,weight_function,sigma,use_stride_tricks):

    '''
    
    temporal_tree_lag
    
    Performs flexible time-lagging on df features which may be real or dummy,
    using a one-dimensional tree

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

    sigma:              parameter in time units used by df controlling width of expon,
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

