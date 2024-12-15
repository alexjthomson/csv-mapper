from django.test import TestCase
from unittest.mock import Mock
from api.dbrouters import ApiRouter

class TestApiRouter(TestCase):
    def setUp(self):
        self.router = ApiRouter()
        self.mock_model = Mock()
        self.mock_model._meta.app_label = 'api'
        self.non_api_model = Mock()
        self.non_api_model._meta.app_label = 'non_api'

    def test_db_for_read(self):
        # Test routing read for `api` app:
        result = self.router.db_for_read(self.mock_model)
        self.assertEqual(result, 'graph')

        # Test routing read for non-`api` app:
        result = self.router.db_for_read(self.non_api_model)
        self.assertIsNone(result)

    def test_db_for_write(self):
        # Test routing write for `api` app:
        result = self.router.db_for_write(self.mock_model)
        self.assertEqual(result, 'graph')

        # Test routing write for non-`api` app:
        result = self.router.db_for_write(self.non_api_model)
        self.assertIsNone(result)

    def test_allow_relation(self):
        # Test allowing relation when one object is from the `api` app:
        result = self.router.allow_relation(self.mock_model, self.non_api_model)
        self.assertTrue(result)

        # Test allowing relation when both objects are from the `api` app:
        result = self.router.allow_relation(self.mock_model, self.mock_model)
        self.assertTrue(result)

        # Test disallowing relation when neither object is from the `api` app:
        result = self.router.allow_relation(self.non_api_model, self.non_api_model)
        self.assertIsNone(result)

    def test_allow_migrate(self):
        # Test migration allowed for `api` app on 'graph' database:
        result = self.router.allow_migrate('graph', 'api')
        self.assertTrue(result)

        # Test migration disallowed for `api` app on a non-'graph' database:
        result = self.router.allow_migrate('default', 'api')
        self.assertFalse(result)

        # Test migration allowed for non-`api` app on 'default' database:
        result = self.router.allow_migrate('default', 'non_api')
        self.assertIsNone(result)