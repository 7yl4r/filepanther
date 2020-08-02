# std modules:
from datetime import datetime
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
            "dt_Y": 2020,
            "_datetime": datetime(2020, 1, 1)
        })

    def test_fname_str_without_path_info(self):
        """can parse fname instead of fpath"""

        result = filepath_to_metadata(
            format_string="/mismatch/one_thing_{this}_%Y.txt",
            filepath="/_mismatch_/one_thing_abc_2020.txt",
            basename_only=True
        )
        self.assertEqual(result, {
            "this": "abc",
            "dt_Y": 2020,
            "_datetime": datetime(2020, 1, 1)
        })

    def test_datetime_parsing(self):
        """can parse full datetime"""
        result = filepath_to_metadata(
            format_string="WV02_%Y-%m-%dT%H:%M:%S.file",
            filepath="WV02_2001-02-03T04:05:06.file"
        )
        self.assertEqual(
            result["_datetime"],
            datetime(2001, 2, 3, 4, 5, 6)
        )

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

    def test_duplicate_strftime_directive(self):
        """can parse string with duplicate strftime directive"""
        result = filepath_to_metadata(
            format_string="%Y_duplicate_thing_%Y.txt",
            filepath="2020_duplicate_thing_2020.txt"
        )
        self.assertEqual(result, {
            "dt_Y": 2020,
            "_datetime": datetime(2020, 1, 1)
        })

    def test_duplicate_strftime_directive_different(self):
        """raises on parse of duplicate different-valued strftime directive"""
        with self.assertRaises(ValueError):
            filepath_to_metadata(
                format_string="%Y_duplicate_thing_%Y.txt",
                filepath="2020_duplicate_thing_2010.txt"
            )
