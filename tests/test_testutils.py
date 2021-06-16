
import math
import unittest 
from data_transformer import testutils

class TestTestutils(unittest.TestCase):
    def test_testutils(self):
        for n in range(1,100):
            if math.sqrt(n) % 1 == 0:
                data = testutils.test_data(n)
                self.assertEqual(data.shape[0],n)

