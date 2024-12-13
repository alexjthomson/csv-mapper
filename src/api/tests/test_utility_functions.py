import json
from django.test import TestCase
from unittest.mock import patch, mock_open
from io import StringIO
from api.views import (
    clean_csv_value,
    success_response,
    error_response,
    read_source_at,
)

class UtilityFunctionTests(TestCase):

    def test_clean_csv_value(self):
        # Test cleaning a CSV value with allowed and disallowed characters:
        self.assertEqual(
            clean_csv_value("hello123_-./\\({)}[]+<>,!?£$%^&*"),
            "hello123_-./\\({)}[]+<>,!?£$%^&*"
        )
        self.assertEqual(
            clean_csv_value("This contains no disallowed characters`:;\"'@#~=¬|"),
            "This contains no disallowed characters"
        )
        self.assertEqual(
            clean_csv_value("     Leading and trailing white-space has been stripped    "),
            "Leading and trailing white-space has been stripped"
        )

    def test_success_response(self):
        response = success_response({"key": "value"}, 200, "Success message")
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),  # Decode JSON response content
            {
                "result": "success",
                "message": "Success message",
                "data": {"key": "value"}
            }
        )

    def test_error_response(self):
        response = error_response("Error message", 400)
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),  # Decode JSON response content
            {
                "result": "error",
                "message": "Error message"
            }
        )

    @patch("api.views.urlopen")
    def test_read_source_at_http(self, mock_urlopen):
        # Mock a successful HTTP source read
        mock_urlopen.return_value.__enter__.return_value.read.return_value = b"col1,col2\nval1,val2"
        success, csv_file = read_source_at("http://example.com/source.csv")
        self.assertTrue(success)
        self.assertIsInstance(csv_file, StringIO)
        self.assertEqual(csv_file.read(), "col1,col2\nval1,val2")

    def test_read_source_at_file(self):
        # Mock a local file read
        with patch("builtins.open", mock_open(read_data="col1,col2\nval1,val2")):
            success, csv_file = read_source_at("file:///path/to/source.csv")
            self.assertTrue(success)
            self.assertIsInstance(csv_file, StringIO)
            self.assertEqual(csv_file.read(), "col1,col2\nval1,val2")
