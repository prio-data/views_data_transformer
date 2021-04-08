
from views_transformation_library import views_2
from . import porting

delta = porting.vectorize_across_dataframe(views_2.delta)

moving_average = porting.vectorize_across_dataframe(views_2.moving_average)
moving_sum = porting.vectorize_across_dataframe(views_2.moving_sum)

cweq = porting.vectorize_across_dataframe(views_2.cweq)
time_since = porting.vectorize_across_dataframe(views_2.time_since)

decay = porting.vectorize_across_dataframe(views_2.decay)

rollmax = porting.vectorize_across_dataframe(views_2.rollmax)


onset_possible = porting.vectorize_across_dataframe(views_2.onset_possible)
onset = porting.vectorize_across_dataframe(views_2.onset)
