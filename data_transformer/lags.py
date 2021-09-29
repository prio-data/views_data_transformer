from views_transformation_library import splag4d,spatial_tree

def spatial_lag(df, kernel_inner, kernel_width, kernel_power, norm_kernel):
    # Just a wrapper to make arguments positional (expected by the service)
    return splag4d.get_splag4d(
            df,
            kernel_inner = kernel_inner,
            kernel_width = kernel_width,
            kernel_power = kernel_power,
            norm_kernel = norm_kernel
            )

def spatial_tree_lag(df,thetacrit,dfunction_option):
    # Just a wrapper to make arguments positional (expected by the service)
    return spatial_tree.get_tree_lag(
            df,
            thetacrit = thetacrit,
            dfunction_option = dfunction_option
            )