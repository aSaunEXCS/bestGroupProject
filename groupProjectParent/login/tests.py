from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import CreateUserForm, LoginForm

class AuthViewsTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('my-login')
        self.logout_url = reverse('user-logout')
        self.home_url = reverse('homepage')

        self.user_data = {
            'username': 'testuser',
            'password': 'password123'
        }
        User.objects.create_user(**self.user_data)

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['registerform'], CreateUserForm)

    def test_register_view_post_valid_data(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['loginform'], LoginForm)

    def test_login_view_post_valid_credentials(self):
        response = self.client.post(self.login_url, self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)

    def test_login_view_post_invalid_credentials(self):
        response = self.client.post(self.login_url, {'username': 'wrong', 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('loginform', response.context)
        self.assertIsInstance(response.context['loginform'], LoginForm)

    def test_logout_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

