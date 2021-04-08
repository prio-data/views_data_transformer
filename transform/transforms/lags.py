
from views_transformation_library import views_2
from . import porting

tlag = porting.vectorize_across_dataframe(views_2.tlag)
tlead = porting.vectorize_across_dataframe(views_2.tlead)
