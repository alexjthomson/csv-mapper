import json
from django.test import TestCase
from api.views import (
    error_response_no_perms,
    error_response_invalid_json_body,
    error_response_expected_field,
    error_response_invalid_field,
    error_response_source_not_found,
    error_response_graph_not_found,
    error_response_graph_dataset_not_found
)

class ResponseFunctionsTests(TestCase):
    def test_error_response_no_perms(self):
        response = error_response_no_perms()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content.decode('utf-8'))["message"], "User does not have permission to perform this action.")

    def test_error_response_invalid_json_body(self):
        response = error_response_invalid_json_body()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content.decode('utf-8'))["message"], "Invalid JSON request body.")

    def test_error_response_expected_field(self):
        response = error_response_expected_field("field_name")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content.decode('utf-8'))["message"], "Expected `field_name` field was not found.")

    def test_error_response_invalid_field(self):
        response = error_response_invalid_field("field_name")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content.decode('utf-8'))["message"], "Expected `field_name` field has an invalid value.")

    def test_error_response_source_not_found(self):
        response = error_response_source_not_found(1)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content.decode('utf-8'))["message"], "Source `1` does not exist.")

    def test_error_response_graph_not_found(self):
        response = error_response_graph_not_found(1)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content.decode('utf-8'))["message"], "Graph `1` does not exist.")

    def test_error_response_graph_dataset_not_found(self):
        response = error_response_graph_dataset_not_found(1)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content.decode('utf-8'))["message"], "Graph dataset `1` does not exist.")