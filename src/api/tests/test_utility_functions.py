from django.test import TestCase
from django.http import JsonResponse
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
        # Test cleaning a CSV value with allowed and disallowed characters
        result = clean_csv_value("hello123!@#$%^&*(){}<>[]|~`")
        self.assertEqual(result, "hello123!@#$%^&*{}<>[]")

    def test_success_response(self):
        # Test constructing a success response
        response = success_response({"key": "value"}, 200, "Success!")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "result": "success",
            "message": "Success!",
            "data": {"key": "value"},
        })

    def test_error_response(self):
        # Test constructing an error response
        response = error_response("An error occurred.", 400)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "result": "error",
            "message": "An error occurred.",
        })

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
