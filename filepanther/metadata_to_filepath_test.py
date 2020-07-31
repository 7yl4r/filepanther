# std modules:
from unittest import TestCase

# tested module(s):
from filepanther.metadata_to_filepath import metadata_to_filepath


class Test_metadata_to_filepath(TestCase):
    def test_path_with_one_var(self):
        """can fill one var"""

        result = metadata_to_filepath(
            format_string="var_goes_{here}.txt",
            metadata_dict={"here": "abc"}
        )
        self.assertEqual(result, "var_goes_abc.txt")

    def test_path_w_one_var_one_strftime_name(self):
        """can fill one var and one strftime directive"""
        result = metadata_to_filepath(
            format_string="var_goes_{here}_%Y.txt",
            metadata_dict={
                "here": "abc",
                "dt_Y": 2020
            }
        )
        self.assertEqual(result, "var_goes_abc_2020.txt")
