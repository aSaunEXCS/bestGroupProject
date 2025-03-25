from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm
from unittest.mock import patch

class ProfileViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.profile_url = reverse('profile')

    def test_profile_view_redirect_if_not_logged_in(self):
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, f'/accounts/login/?next={self.profile_url}')

    def test_profile_view_get_request_logged_in(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'UserProfile/UserProfile.html')
        self.assertIsInstance(response.context['form'], ProfileForm)
        self.assertIsInstance(response.context['profile'], Profile)

    @patch('leaderboard.utils.update_badges')
    def test_profile_view_post_valid_form(self, mock_update_badges):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.profile_url, {'bio': 'Test Bio'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.bio, 'Test Bio')
        mock_update_badges.assert_called_once()

    @patch('leaderboard.utils.update_badges')
    def test_profile_view_post_invalid_form(self, mock_update_badges):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.profile_url, {'bio': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'UserProfile/UserProfile.html')
        self.assertFormError(response, 'form', 'bio', 'This field is required.')
        mock_update_badges.assert_called_once()
