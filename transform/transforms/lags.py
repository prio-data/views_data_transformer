
from views_transformation_library import views_2,splag4d
from . import porting

tlag = porting.vectorize_across_dataframe(views_2.tlag)
tlead = porting.vectorize_across_dataframe(views_2.tlead)

get_splag4d = splag4d.get_splag4d
