
import unittest
import numpy as np
from numpy.testing import assert_array_equal 
from data_transformer.transforms import testutils,lags

class TestLags(unittest.TestCase):
    def test_timelag(self):
        data = testutils.test_data(9)
        data[0] = np.random.random(9)
        lagged = lags.tlag(data.copy(),1)
        try:
            assert_array_equal(data.loc[0,0].values,lagged.loc[1,0].values)
        except AssertionError as ae:
            self.fail(str(ae))
