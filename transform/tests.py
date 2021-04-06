import io
import unittest
from unittest import mock
from pydantic.errors import StrRegexError
import pandas as pd
import numpy as np
import requests

from app import transform
from url_args import type_infer,parse

from transforms import lag_by_index

mock_data = pd.DataFrame({"value":np.linspace(1,9,9)})
mock_data.index = pd.MultiIndex.from_product([[1,2,3],[1,2,3]])
mock_data.index.names = ["time","unit"]
mock_data_buffer = io.BytesIO()
mock_data.to_parquet(mock_data_buffer,compression="gzip")
mock_data_bytes = mock_data_buffer.getvalue()

class Tests(unittest.TestCase):
    def test_identity(self):
        """
        Just checks the identity function, which returns
        the data as-is
        """
        with mock.patch("app.requests") as mock_requests:
            rsp = requests.Response()
            rsp.status_code=200
            rsp._content=mock_data_bytes
            rsp.headers["Content-Type"]="application/octet-stream"
            mock_requests.get.return_value = rsp
            resp = transform("priogrid_month","identity","_","")
            data = pd.read_parquet(io.BytesIO(resp.body))
            try:
                pd.testing.assert_frame_equal(data,mock_data)
            except AssertionError:
                self.fail()

    def test_params(self):
        """
        Tests asking for a transform with a variety of parameters,
        including erroneous ones.
        """

        with mock.patch("app.requests") as mock_requests:
            rsp = requests.Response()
            rsp.status_code=200
            rsp._content=mock_data_bytes
            rsp.headers["Content-Type"]="application/octet-stream"
            mock_requests.get.return_value = rsp

            resp = transform("priogrid_month","identity","yee_haw","")
            self.assertEqual(resp.status_code,400)

            resp = transform("priogrid_month","identity","_","")
            self.assertEqual(resp.status_code,200)

    def test_url_args_parse(self):
        """
        Tests the argument-parsing scheme employed here, where
        a1_a2_...an are passed as a tuple of arguments to the
        invoked transform function.
        """

        def fails():
            parse("yee_")
        for bad_pattern in ["yee_","_a_","<z>"]:
            fails = lambda: parse(bad_pattern)
            self.assertRaises(StrRegexError,fails)

        parsed = parse("1_2_3")
        self.assertEqual(sum(parsed),6)
        self.assertEqual(len(parsed),3)

        parsed = parse("1_1.2")
        self.assertEqual(sum(parsed),2.2)
        self.assertEqual(len(parsed),2)

    def test_type_infer(self):
        """
        Tests type inference, used for arg parsing
        """
        self.assertEqual(type_infer("1"),1)
        self.assertEqual(type_infer("1.2"),1.2)
        self.assertEqual(type_infer("1.2a"),"1.2a")
        self.assertEqual(type_infer("+?fa<z>_12"),"+?fa<z>_12")
        self.assertEqual(type_infer("_"),"_")

    def test_lag_by_idx(self):
        orig = mock_data.copy()
        lagged = lag_by_index(mock_data.copy(),1)
        lagged.columns = ["lagged"]
        both = orig.join(lagged)
        np.testing.assert_array_equal(
                both.lagged.values[3:6],
                orig.value.values[0:3]
                )