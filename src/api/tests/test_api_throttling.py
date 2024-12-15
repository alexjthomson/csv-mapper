from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from django.core.cache import cache
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory
from rest_framework.test import APIClient, APITestCase
from api.views.source import *

class ThrottlingTestCase(APITestCase):
    databases = {'default', 'graph'}
    
    def setUp(self):
        cache.clear()
        
        self.url = '/api/source/'
        self.factory = RequestFactory()

        # Create the required 'default' group
        self.default_group = Group.objects.create(name='default')

        # Create test users
        self.user = User.objects.create_user(username='testuser', password='password')

        # Assign permissions to the user with permissions
        permissions = [
            'view_source',
            'add_source',
        ]
        content_type = ContentType.objects.get(app_label='api', model='source')
        for codename in permissions:
            permission = Permission.objects.get(codename=codename, content_type=content_type)
            self.user.user_permissions.add(permission)

        # APIClient setup
        self.client = APIClient()

    # NOTE: Anonymous throttling cannot be tested since you must be
    # authenticated to access any of the API endpoints.
    # def test_anonymous_throttling(self):
    #     throttle_limit = 500 # Anonymous rate limit

    #     # Make requests as an anonymous user
    #     for _ in range(throttle_limit):
    #         response = self.client.get(self.url)
    #         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #     # Exceed the throttle limit
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
    #     self.assertIn('throttled', response.data['detail'].lower())

    def test_registered_user_throttling(self):
        throttle_limit = 4000 # Registered user rate limit

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Make requests as an authenticated user
        for _ in range(throttle_limit):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Exceed the throttle limit
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertIn('throttled', response.data['detail'].lower())