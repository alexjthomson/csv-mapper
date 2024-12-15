from django.test import TestCase
from django.contrib.auth.models import User, Group

class TestCreateUserProfileSignal(TestCase):
    def setUp(self):
        # Create the default group required by the signal:
        self.default_group = Group.objects.create(name='default')

    def test_user_added_to_default_group_on_creation(self):
        # Create a user
        user = User.objects.create_user(username='testuser', password='password')

        # Refresh the user instance to fetch related group data:
        user.refresh_from_db()

        # Assert the user is added to the default group:
        self.assertIn(self.default_group, user.groups.all())

    def test_signal_does_not_fail_if_default_group_does_not_exist(self):
        # Delete the default group:
        self.default_group.delete()

        # Create a user
        user = User.objects.create_user(username='testuser', password='password')

        # Refresh the user instance to fetch related group data:
        user.refresh_from_db()

        # Assert the user is not added to any groups:
        self.assertEqual(user.groups.count(), 0)
