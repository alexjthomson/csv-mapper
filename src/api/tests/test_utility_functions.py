import json
from django.test import TestCase
from unittest.mock import patch, Mock
from api.views import (
    clean_csv_value,
    success_response,
    error_response,
    read_source_at,
)
from io import StringIO

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
        self.assertEqual(
            clean_csv_value("`:;\"'@#~=¬|"),
            ""
        )
        self.assertEqual(
            clean_csv_value(None),
            ""
        )
        self.assertEqual(
            clean_csv_value(""),
            ""
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
            
    @patch("api.views.utility.requests.get")
    def test_read_source_at_http(self, mock_get):
        # Mock response from `requests.get`:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'text/csv'}
        mock_response.text = "col1,col2\nval1,val2"
        mock_get.return_value = mock_response

        # Call the function:
        success, csv_file = read_source_at("http://example.com/source.csv")

        # Assertions:
        self.assertTrue(success)
        self.assertIsInstance(csv_file, StringIO)
        self.assertEqual(csv_file.read(), "col1,col2\nval1,val2")

    def test_read_source_at_invalid_url(self):
        success, response = read_source_at("invalid-url")
        self.assertFalse(success)
        self.assertEqual(response.status_code, 400)
