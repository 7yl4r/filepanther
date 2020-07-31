# std modules:
from unittest import TestCase

# tested module(s):
from filepanther.filepath_to_metadata import filepath_to_metadata


class Test_filepath_to_metadata(TestCase):
    def test_path_with_nothing_returns_nothing(self):
        """ returns empty dict when fmt string has no vars in it"""

        result = filepath_to_metadata(
            format_string="nothing_in_here.txt",
            filepath="nothing_in_here.txt"
        )
        self.assertEqual(result, {})

    def test_single_var(self):
        """can parse one variable from str"""

        result = filepath_to_metadata(
            format_string="one_thing_{this}.txt",
            filepath="one_thing_abc.txt"
        )
        self.assertEqual(result, {"this": "abc"})

    def test_str_with_strptime_directives(self):
        """can parse one named variable and one strftime directive"""

        result = filepath_to_metadata(
            format_string="one_thing_{this}_%Y.txt",
            filepath="one_thing_abc_2020.txt"
        )
        self.assertEqual(result, {
            "this": "abc",
            "dt_Y": 2020
        })

    # # TODO:
    # def test_duplicate_named_var(self):
    #     """can parse string with duplicate named variable"""
    #     result = filepath_to_metadata(
    #         format_string="{this}_duplicate_thing_{this}.txt",
    #         filepath="abc_one_thing_abc.txt"
    #     )
    #     self.assertEqual(result, {
    #         "this": "abc"
    #     })
    #
    # def test_duplicate_strftime_directive(self):
    #     """can parse string with duplicate strftime directive"""
    #     result = filepath_to_metadata(
    #         format_string="%Y_duplicate_thing_%Y.txt",
    #         filepath="2020_one_thing_2020.txt"
    #     )
    #     self.assertEqual(result, {
    #         "this": "abc"
    #     })
