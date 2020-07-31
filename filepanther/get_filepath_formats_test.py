"""
example unit test for ExampleClass
list of unittest assert methods:
https://docs.python.org/3/library/unittest.html#assert-methods
"""

# std modules:
from unittest import TestCase
from unittest.mock import MagicMock
import pytest

# tested module(s):
from filepanther.get_filepath_formats import get_filepath_formats
from filepanther.get_filepath_formats import _prefill_fmt_str


class Test_get_filepath_formats(TestCase):
    def test_get_filepath_format_zero_result(self):
        """ returns empty dict when no results from DB """
        mock_metadb_handle = MagicMock()
        mock_metadb_handle.connect = MagicMock(
            name="__enter__",
            return_value=MagicMock(
                name="execute",
                return_value=[()]
            )
        )
        result = get_filepath_formats(
            mock_metadb_handle,
            short_name="s3a_ol_1_efr", product_id=36,
            include_test_formats=False
        )
        self.assertEqual(result, {})

    def test_get_filepath_format_one_result(self):
        """ returns empty dict when 1 result from DB """
        FAKE_FORMAT = '1234_filepath_format_%y_{var}.txt'
        # product.short_name,path_format.short_name,params,format_string
        sql_result = [['short_name', 'fmt_name', '{}', FAKE_FORMAT]]
        # meta.connect().__enter__().execute()
        mock_metadb_handle = MagicMock(spec=["connect"])
        mock_metadb_handle.connect = MagicMock()
        mock_metadb_handle.connect.return_value = MagicMock()
        mock_metadb_handle.connect.return_value.__enter__ = MagicMock()
        mock_metadb_handle.connect.return_value.__enter__.return_value = MagicMock()
        mock_metadb_handle.connect.return_value.__enter__.return_value.execute = MagicMock()
        mock_metadb_handle.connect.return_value.__enter__.return_value.execute.return_value = sql_result

        expected = {'short_name.fmt_name': FAKE_FORMAT}
        # MagicMock(
        #         name="execute",
        #         return_value=[FAKE_FORMAT]
        # )
        result = get_filepath_formats(
            mock_metadb_handle,
            short_name="s3a_ol_1_efr", product_id=36,
            include_test_formats=False
        )
        self.assertEqual(result, expected)

    @pytest.mark.real_db
    def test_get_filepath_formats_real(self):
        """filepath formats doesn't raise on actual database usage"""
        from sqlalchemy import create_engine
        from filepanther.SECRETS import META_DB_URI
        get_filepath_formats(
            create_engine(META_DB_URI),
            product_id=6
        )

class Test_prefill_fmt_str(TestCase):
    def test_basic(self):
        result = _prefill_fmt_str("{test}abc.123_%y", '{"test":"Foo"}')
        self.assertEqual(result, 'Fooabc.123_%y')
