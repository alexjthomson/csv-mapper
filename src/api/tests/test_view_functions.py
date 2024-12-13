import json
from django.test import TestCase, RequestFactory
from unittest.mock import patch, mock_open, MagicMock
from api.views import (
    error_response_no_perms,
    error_response_invalid_json_body,
    error_response_expected_field,
    error_response_invalid_field,
    error_response_http_method_unsupported,
    error_response_source_not_found,
    error_response_graph_not_found,
    error_response_graph_dataset_not_found,
    read_source_at,
    source_list,
    source_detail,
)
from api.models import Source
from django.contrib.auth.models import AnonymousUser, Group, Permission, User
from django.contrib.contenttypes.models import ContentType

class ViewFunctionTests(TestCase):
    databases = {'default', 'graph'}
    
    def setUp(self):
        self.factory = RequestFactory()

        # Create the required 'default' group
        self.default_group = Group.objects.create(name='default')

        # Create test users
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user_with_perms = User.objects.create_user(username='permuser', password='password')

        # Assign permissions to the user with permissions
        permissions = [
            'view_source',
            'add_source',
            'delete_source',
        ]
        content_type = ContentType.objects.get(app_label='api', model='source')
        for codename in permissions:
            permission = Permission.objects.get(codename=codename, content_type=content_type)
            self.user_with_perms.user_permissions.add(permission)

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

    def test_error_response_http_method_unsupported(self):
        response = error_response_http_method_unsupported("PATCH")
        self.assertEqual(response.status_code, 405)
        self.assertEqual(json.loads(response.content.decode('utf-8'))["message"], "Unsupported HTTP method: `PATCH`.")

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

    @patch("api.views.urlopen")
    def test_read_source_at_http(self, mock_urlopen):
        mock_urlopen.return_value.__enter__.return_value.read.return_value = b"col1,col2\nval1,val2"
        success, csv_file = read_source_at("http://example.com/source.csv")
        self.assertTrue(success)
        self.assertEqual(csv_file.read(), "col1,col2\nval1,val2")

    def test_read_source_at_invalid_url(self):
        success, response = read_source_at("invalid-url")
        self.assertFalse(success)
        self.assertEqual(response.status_code, 400)

    @patch("builtins.open", mock_open(read_data="col1,col2\nval1,val2"))
    def test_read_source_at_file(self):
        success, csv_file = read_source_at("file:///path/to/source.csv")
        self.assertTrue(success)
        self.assertEqual(csv_file.read(), "col1,col2\nval1,val2")

    def test_source_list_get_no_perms(self):
        response = self.client.get("/api/source-list/")
        self.assertEqual(response.status_code, 403)  # Expecting 403 for unauthorized access

    def test_source_list_get_with_perms(self):
        self.client.login(username='permuser', password='password')  # Log in the user with permissions
        Source.objects.create(name="Source1", location="http://example.com", has_header=True)
        response = self.client.get('/api/source-list/')  # Use the actual URL of the endpoint
        self.assertEqual(response.status_code, 200)

    def test_source_detail_get(self):
        source = Source.objects.create(name="Source1", location="http://example.com", has_header=True)
        request = self.factory.get(f'/api/sources/{source.id}/')
        request.user = self.user_with_perms
        response = source_detail(request, source.id)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode('utf-8'))["data"]
        self.assertEqual(response_data["name"], "Source1")

    def test_source_detail_delete(self):
        source = Source.objects.create(name="Source1", location="http://example.com", has_header=True)
        request = self.factory.delete(f'/api/sources/{source.id}/')
        request.user = self.user_with_perms
        response = source_detail(request, source.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8'))["message"], f"Deleted source `{source.id}`.")
        self.assertEqual(Source.objects.count(), 0)