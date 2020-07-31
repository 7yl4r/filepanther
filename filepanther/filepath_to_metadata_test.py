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
