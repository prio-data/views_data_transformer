import unittest
from pydantic.errors import StrRegexError

from . import url_args

class TestUtilityFunctions(unittest.TestCase):
    def test_url_parse(self):
        """
        Tests the argument-parsing scheme employed here, where
        a1_a2_...an are passed as a tuple of arguments to the
        invoked transform function.
        """

        def fails():
            url_args.parse("yee_")
        for bad_pattern in ["yee_","_a_","<z>"]:
            fails = lambda: url_args.parse(bad_pattern)
            self.assertRaises(StrRegexError,fails)

        parsed = url_args.parse("1_2_3")
        self.assertEqual(sum(parsed),6)
        self.assertEqual(len(parsed),3)

        parsed = url_args.parse("1_1.2")
        self.assertEqual(sum(parsed),2.2)
        self.assertEqual(len(parsed),2)

    def test_type_infer(self):
        """
        Tests type inference, used for arg parsing
        """
        cases = [
                ("1",1),
                ("1.2",1.2),
                ("1.2a","1.2a"),
                ("+?fa<z>_12","+?fa<z>_12"),
                ("_","_"),
            ]

        for arg,out in cases:
            self.assertEqual(url_args.type_infer(arg),out)
