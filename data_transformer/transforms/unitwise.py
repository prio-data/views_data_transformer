
from views_transformation_library import views_2
from . import porting

unit_mean = porting.vectorize_across_dataframe(views_2.mean)
unit_demean = porting.vectorize_across_dataframe(views_2.demean)
