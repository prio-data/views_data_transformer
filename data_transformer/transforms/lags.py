
from views_transformation_library import views_2,splag4d
from . import porting

tlag = porting.vectorize_across_dataframe(views_2.tlag)
tlag.__name__ = "tlag"

tlead = porting.vectorize_across_dataframe(views_2.tlead)
tlead.__name__ = "tlead"

splag = lambda df,a,b,c,d: splag4d.get_splag4d(
        df,
        kernel_inner = a,
        kernel_width=b,
        kernel_power=c,
        norm_kernel=d
    )
splag.__name__ = "splag"
