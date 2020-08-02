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

    def test_worldview_filepath(self):
        """can parse worldview filepath"""
        result = filepath_to_metadata(
            format_string=(
                "WV{sat_n:2}_%Y%m%d%H%M%S_{unknown_stuff:16}_"
                "%y%b%d%H%M%S-M1BS-{idNumber:12}_{unknown_int:2}_"
                "P{passNumber:3}_{region_short_name}_SOALCHI_"
                "filt_{filter_width:1d}.tif"
            ),
            filepath=(
                "WV03_20150801165729_104001000E057100_"
                "15AUG01165729-M1BS-501124619070_01_P002_WELA_SOALCHI_"
                "filt_3.tif"
            )
        )
        self.assertEqual(result, {
            "sat_n": "03",
            "dt_Y": 2015,
            "dt_m": 8,
            "dt_d": 1,
            "dt_H": 16,
            "dt_M": 57,
            "dt_S": 29,
            "unknown_stuff": "104001000E057100",
            "dt_y": 15,
            "dt_b": "AUG",
            "idNumber": "501124619070",
            "unknown_int": "01",
            "passNumber": "002",
            "region_short_name": "WELA",
            "filter_width": 3,
            "_datetime": datetime(2015, 8, 1, 16, 57, 29)
        })

    def test_strptime_smush(self):
        """parses a bunch of strptime directives squished together"""
        result = filepath_to_metadata(
            format_string="%Y%m%d%H%M%S_{unknown_stuff:16}_%y%b%d%H%M%S",
            filepath="20150801165729_104001000E057100_15AUG01165729"
        )
        self.assertEqual(result, {
            "dt_Y": 2015,
            "dt_m": 8,
            "dt_d": 1,
            "dt_H": 16,
            "dt_M": 57,
            "dt_S": 29,
            "dt_y": 15,
            "dt_b": "AUG",
            "unknown_stuff": "104001000E057100",
            "_datetime": datetime(2015, 8, 1, 16, 57, 29)
        })

    def test_strptime_cross_directive_constraints(self):
        """
        Can parse non-conflicting cross-directive constraints.
        Eg: year = 2015 and 2-digit year 15
        """
        result = filepath_to_metadata(
            format_string="%Y_apple_%y",
            filepath="2015_apple_15"
        )
        self.assertEqual(result, {
            "dt_Y": 2015,
            "dt_y": 15,
            "_datetime": datetime(2015, 1, 1)
        })
