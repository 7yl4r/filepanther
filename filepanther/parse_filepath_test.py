"""
"""

# std modules:
from unittest import TestCase
from unittest.mock import patch
from datetime import datetime

# dependencies:
from filepanther.parse_filepath import parse_filepath
from filepanther.util.strptime_parsed_pattern import strptime_parsed_pattern


class Test_parse_filepath(TestCase):
    @patch('filepanther.parse_filepath.get_filepath_formats')
    def test_parse_wv_filepath_from_db(self, mock_get_filepath_formats):
        """filepath parses w/ result from meta db"""
        mock_get_filepath_formats.return_value = {
            'fpath_pattern':
                'WV{sat_n}_%Y%m%d%H%M%S_{junk}_%y%b%d%H%M%S-' +
                '{m_or_p}1BS-{idNumber}_P{passNumber}{ext}'
        }
        filename = (
            'WV02_20091220161049_103001000366EE00_09DEC20161049-M1BS-' +
            '502573785040_01_P001.ntf'
        )
        result = parse_filepath(
            {}, filepath=filename
        )
        self.assertEqual(result['sat_n'], '02')
        self.assertEqual(result['junk'], '103001000366EE00')
        self.assertEqual(result['idNumber'], '502573785040_01')

    def test_parse_wv_filepath(self):
        """filepath parses w/ hard-coded load_format"""
        filename = (
            'WV02_20091220161049_103001000366EE00_09DEC20161049-M1BS-' +
            '502573785040_01_P001.ntf'
        )
        result = parse_filepath(
            {}, filepath=filename,
            load_format=(
                'WV{sat_n}_%Y%m%d%H%M%S_{junk}_%y%b%d%H%M%S-' +
                '{m_or_p}1BS-{idNumber}_P{passNumber}{ext}'
            )
        )
        self.assertEqual(result['sat_n'], '02')
        self.assertEqual(result['junk'], '103001000366EE00')
        self.assertEqual(result['idNumber'], '502573785040_01')


class Test__strptime_parsed_pattern(TestCase):
    def test_strptime_with_param_with_leading_zeros(self):
        """strptime works when a named param has leading zeros"""
        strptime_parsed_pattern(
            input_str="w2_2018_09_17T012529_fl_ne_058438305_.z",
            format_str="w2_%Y_%m_%dT%H%M%S_{area_name}_{order_id:09d}_.z",
            params=dict(
                area_name="fl_ne",
                order_id=int("058438305")
            )
        )

    def test_strptime_with_duplicate_directive(self):
        """strptime wrapper handles duplicate datetime directive"""
        dt = strptime_parsed_pattern(
            input_str="test_11_test2_11",
            format_str="test_%d_test2_%d",
            params={}
        )
        self.assertEqual(dt, datetime.strptime('11', '%d'))

    def test_strptime_with_duplicate_directive_conflict(self):
        """strptime wrapper raises on conflicting duplicate directives"""
        with self.assertRaises(ValueError):
            strptime_parsed_pattern(
                input_str="test_11_test2_22",
                format_str="test_%d_test2_%d",
                params={}
            )
