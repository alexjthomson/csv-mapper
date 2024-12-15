from django.core.cache import cache
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory
from rest_framework.test import APIClient, APITestCase
from unittest.mock import patch, MagicMock
from api.models import Source
from api.views.source import *
from io import StringIO

class SourceListViewTests(APITestCase):
    databases = {'default', 'graph'}
    
    def setUp(self):
        cache.clear()
        
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
        ]
        content_type = ContentType.objects.get(app_label='api', model='source')
        for codename in permissions:
            permission = Permission.objects.get(codename=codename, content_type=content_type)
            self.user_with_perms.user_permissions.add(permission)

        # APIClient setup
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_with_perms)
    
    def test_get_sources_success(self):
        Source.objects.create(name="Source 1", location="path/to/source1.csv", has_header=True)
        Source.objects.create(name="Source 2", location="path/to/source2.csv", has_header=False)

        response = self.client.get('/api/source/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 2)

    def test_get_sources_no_permission(self):
        """
        Ensure that a user without the 'view_source' permission cannot access the get method.
        """
        
        # Authenticate as a user without permissions
        self.client.force_authenticate(user=self.user)

        # Make the GET request
        response = self.client.get('/api/source/')

        # Assert that the response is a 403 Forbidden:
        self.assertEqual(response.status_code, 403)

    def test_post_source_success(self):
        response = self.client.post('/api/source/', {
            "name": "Test Source",
            "location": "path/to/test.csv",
            "has_header": True
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Source.objects.count(), 1)

    def test_post_source_invalid_data(self):
        response = self.client.post('/api/source/', {
            "name": "Test Source",
            "location": None,  # Invalid field
            "has_header": True
        }, format='json')
        self.assertEqual(response.status_code, 400)

class SourceDetailViewTests(APITestCase):
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
            'change_source',
            'delete_source',
        ]
        content_type = ContentType.objects.get(app_label='api', model='source')
        for codename in permissions:
            permission = Permission.objects.get(codename=codename, content_type=content_type)
            self.user_with_perms.user_permissions.add(permission)

        # APIClient setup
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_with_perms)

        # Create a source for testing
        self.source = Source.objects.create(name="Source 1", location="path/to/source.csv", has_header=True)
    
    def test_get_source_success(self):
        response = self.client.get(f'/api/source/{self.source.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['name'], self.source.name)

    def test_get_source_not_found(self):
        response = self.client.get('/api/source/999/')
        self.assertEqual(response.status_code, 404)

    def test_delete_source_success(self):
        response = self.client.delete(f'/api/source/{self.source.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Source.objects.count(), 0)

    def test_delete_source_not_found(self):
        response = self.client.delete('/api/source/999/')
        self.assertEqual(response.status_code, 404)

    def test_put_source_success(self):
        response = self.client.put(f'/api/source/{self.source.id}/', {
            "name": "Updated Source",
            "location": "path/to/updated.csv",
            "has_header": False
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.source.refresh_from_db()
        self.assertEqual(self.source.name, "Updated Source")
        self.assertEqual(self.source.has_header, False)

    def test_put_source_invalid_data(self):
        response = self.client.put(f'/api/source/{self.source.id}/', {
            "name": None,  # Invalid field
            "location": "path/to/updated.csv",
            "has_header": False
        }, format='json')
        self.assertEqual(response.status_code, 400)

class SourceDataViewTests(APITestCase):
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
        ]
        content_type = ContentType.objects.get(app_label='api', model='source')
        for codename in permissions:
            permission = Permission.objects.get(codename=codename, content_type=content_type)
            self.user_with_perms.user_permissions.add(permission)

        # APIClient setup
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_with_perms)

        # Create a source for testing
        self.source = Source.objects.create(name="Source 1", location="path/to/source.csv", has_header=True)
    
    @patch('api.views.source.read_source_at')
    def test_get_source_data_success(self, mock_read_source_at):
        # Mock the CSV file content as a string, like a real CSV file
        mock_csv_content = "Header1,Header2\nRow1Col1,Row1Col2\n"
        mock_csv_file = StringIO(mock_csv_content)

        # Mock the read_source_at function to return success with the mock file:
        mock_read_source_at.return_value = (True, mock_csv_file)

        # Set the source location and headers
        self.source.location = 'http://example.com/test.csv'
        self.source.has_header = True
        self.source.save()

        # Perform the GET request:
        response = self.client.get(f'/api/source/{self.source.id}/data/')
        self.assertEqual(response.status_code, 200)
        
        # Validate the data structure:
        response_data = response.json()  # Extract the response JSON
        self.assertIsInstance(response_data, dict)  # Validate the root is a dict
        self.assertIn('data', response_data)  # Ensure the 'data' key is present
        self.assertIsInstance(response_data['data'], list)  # Validate the 'data' value is a list

        # Validate the content of the list
        data = response_data['data']
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Header1')
        self.assertEqual(data[1]['name'], 'Header2')

    @patch('api.views.source.read_source_at')
    def test_get_source_data_read_failure(self, mock_read_source_at):
        mock_read_source_at.return_value = (False, error_response('Failed to read source.', 400))

        response = self.client.get(f'/api/source/{self.source.id}/data/')
        self.assertEqual(response.status_code, 400)

    def test_get_source_data_not_found(self):
        response = self.client.get('/api/source/999/data/')
        self.assertEqual(response.status_code, 404)