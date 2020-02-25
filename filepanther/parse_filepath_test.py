"""
"""

# std modules:
from unittest import TestCase
from unittest.mock import patch
from datetime import datetime

# dependencies:
from filepanther.parse_filepath import parse_filepath
from filepanther.parse_filepath import _strptime_parsed_pattern
from filepanther.parse_filepath import _parse_multidirective
from filepanther.parse_filepath import _strptime_safe


class Test_parse_filepath(TestCase):
    @patch('filepanther.parse_filepath.get_filepath_formats')
    def test_parse_wv_filepath(self, mock_get_filepath_formats):
        mock_get_filepath_formats.return_value = {
            'fpath_pattern':
                '%y%b%d%H%M%S-{m_or_p}1BS-{idNumber}_P{passNumber}{ext}'
        }
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
        print(result)
        self.assertEqual(result['sat_n'], '02')
        self.assertEqual(result['junk'], '103001000366EE00')
        self.assertEqual(result['idNumber'], '502573785040_01')


class Test_parse_multidirective(TestCase):
    def test_multidirective_wv2(self):
        fmtstr = (
            "/srv/imars-objects/extra_data/WV02/2013.01/"
            "WV02_%Y%m%d%H%M%S_0000000000000000_%y%b%d%H%M%S"
            "-M1BS-059048321010_01_P001.xml"
        )
        inpstr = (
            "/srv/imars-objects/extra_data/WV02/2013.01/"
            "WV02_20130123163628_0000000000000000_13Jan23163628-"
            "M1BS-059048321010_01_P001.xml"
        )
        read_value, new_str = _parse_multidirective(inpstr, fmtstr, "%M")
        self.assertEqual(read_value, 36)


class Test_strptime_safe(TestCase):
    def test_multidirective_zfill(self):
        fmtstr = (
            "/%Y.%m/WV02_%Y%m_000_%y%d%H%M%S.xml"
        )
        inpstr = (
            "/2013.01/WV02_201301_000_1323163628.xml"
        )

        self.assertEqual(
            _strptime_safe(inpstr, fmtstr),
            datetime(2013, 1, 23, 16, 36, 28)
        )


class Test__strptime_parsed_pattern(TestCase):
    def test_strptime_with_param_with_leading_zeros(self):
        """strptime works when a named param has leading zeros"""
        _strptime_parsed_pattern(
            input_str="w2_2018_09_17T012529_fl_ne_058438305_.z",
            format_str="w2_%Y_%m_%dT%H%M%S_{area_name}_{order_id:09d}_.z",
            params=dict(
                area_name="fl_ne",
                order_id=int("058438305")
            )
        )

    def test_strptime_with_duplicate_directive(self):
        """strptime wrapper handles duplicate datetime directive"""
        dt = _strptime_parsed_pattern(
            input_str="test_11_test2_11",
            format_str="test_%d_test2_%d",
            params={}
        )
        self.assertEqual(dt, datetime.strptime('11', '%d'))

    def test_strptime_with_duplicate_directive_conflict(self):
        """strptime wrapper raises on conflicting duplicate directives"""
        with self.assertRaises(ValueError):
            _strptime_parsed_pattern(
                input_str="test_11_test2_22",
                format_str="test_%d_test2_%d",
                params={}
            )
