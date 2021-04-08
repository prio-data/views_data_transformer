
from views_transformation_library import views_2
from . import porting

gte = porting.vectorize_across_dataframe(views_2.greater_or_equal)

lte = porting.vectorize_across_dataframe(views_2.smaller_or_equal)

in_range = porting.vectorize_across_dataframe(views_2.in_range)

ln = porting.vectorize_across_dataframe(views_2.ln)
