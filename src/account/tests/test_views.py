from django.test import TestCase, Client
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.urls import reverse
from account.forms import RegisterForm

class AccountViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
    
    def test_login_view_get(self):
        response = self.client.get(reverse('account:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('account:login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertRedirects(response, '/')

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('account:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Please enter a correct username and password')

    def test_logout_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('account:logout'))
        self.assertRedirects(response, reverse('account:login'))

    def test_register_view_get(self):
        response = self.client.get(reverse('account:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertIsInstance(response.context['form'], RegisterForm)

    def test_register_view_post_valid(self):
        response = self.client.post(reverse('account:register'), {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        })
        self.assertRedirects(response, '/')
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_view_post_invalid(self):
        response = self.client.post(reverse('account:register'), {
            'username': '',
            'password1': 'password',
            'password2': 'differentpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, 'This field is required')

    def test_change_password_view_get(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('account:change_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/change_password.html')
        self.assertIsInstance(response.context['form'], PasswordChangeForm)

    def test_change_password_view_post_valid(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('account:change_password'), {
            'old_password': 'password123',
            'new_password1': 'NewComplexPass123!',
            'new_password2': 'NewComplexPass123!'
        })
        self.assertRedirects(response, '/')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewComplexPass123!'))

    def test_change_password_view_post_invalid(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('account:change_password'), {
            'old_password': 'wrongpassword',
            'new_password1': 'NewComplexPass123!',
            'new_password2': 'NewComplexPass123!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/change_password.html')
        self.assertContains(response, 'Your old password was entered incorrectly.')

    def test_forgot_password_view_get(self):
        response = self.client.get(reverse('account:forgot_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/forgot_password.html')

    def test_forgot_password_view_redirect_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('account:forgot_password'))
        self.assertRedirects(response, '/')
