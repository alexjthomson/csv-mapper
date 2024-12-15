import json
from django.test import TestCase, RequestFactory
from api.views.source import *
from api.models import Source
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

class SourceViewTests(TestCase):
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

    def test_source_list_get_no_perms(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get("/api/source/")
        self.assertEqual(response.status_code, 403)  # Expecting 403 for unauthorized access

    def test_source_list_get_with_perms(self):
        self.client.login(username='permuser', password='password')  # Log in the user with permissions
        Source.objects.create(name="Source1", location="http://example.com", has_header=True)
        response = self.client.get('/api/source/')  # Use the actual URL of the endpoint
        self.assertEqual(response.status_code, 200)

    def test_source_detail_get(self):
        source = Source.objects.create(name="Source1", location="http://example.com", has_header=True)
        request = self.factory.get(f'/api/source/{source.id}/')
        request.user = self.user_with_perms
        response = source_detail(request, source.id)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode('utf-8'))["data"]
        self.assertEqual(response_data["name"], "Source1")

    def test_source_detail_delete(self):
        source = Source.objects.create(name="Source1", location="http://example.com", has_header=True)
        request = self.factory.delete(f'/api/source/{source.id}/')
        request.user = self.user_with_perms
        response = source_detail(request, source.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8'))["message"], f"Deleted source `{source.id}`.")
        self.assertEqual(Source.objects.count(), 0)