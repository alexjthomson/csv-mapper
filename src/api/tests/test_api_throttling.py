from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class ThrottlingTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/source/'

        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_anonymous_throttling(self):
        throttle_limit = 500 # Anonymous rate limit

        # Make requests as an anonymous user
        for _ in range(throttle_limit):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Exceed the throttle limit
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertIn('throttled', response.data['detail'].lower())

    def test_registered_user_throttling(self):
        throttle_limit = 4000 # Registered user rate limit

        # Authenticate the user
        self.client.login(username='testuser', password='password')

        # Make requests as an authenticated user
        for _ in range(throttle_limit):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Exceed the throttle limit
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertIn('throttled', response.data['detail'].lower())