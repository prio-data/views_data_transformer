
import math
import pandas as pd
import numpy as np

def test_multi_index(n):
    return pd.MultiIndex.from_product([range(n),range(n)])

def test_data(n):
    try:
        assert math.sqrt(n) % 1 == 0
    except AssertionError as ae:
        raise ValueError("n must have a whole square root") from ae

    data = pd.DataFrame(np.zeros(n))
    data.index = test_multi_index(int(math.sqrt(n)))
    return data
