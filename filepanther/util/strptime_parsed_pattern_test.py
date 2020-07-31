from unittest import TestCase
from datetime import datetime

from filepanther.util.strptime_parsed_pattern import _parse_multidirective
from filepanther.util.strptime_parsed_pattern import _strptime_safe


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
