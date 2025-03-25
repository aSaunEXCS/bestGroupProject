from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import LeaderboardEntry

class LeaderboardViewTest(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        
        # Create leaderboard entries
        LeaderboardEntry.objects.create(user=self.user1, game='Energy Conservation', score=100)
        LeaderboardEntry.objects.create(user=self.user1, game='Recycling', score=200)
        LeaderboardEntry.objects.create(user=self.user2, game='Cycling', score=150)
        LeaderboardEntry.objects.create(user=self.user2, game='Quiz', score=50)

        self.client = Client()

    def test_leaderboard_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('leaderboard_view'))
        self.assertRedirects(response, '/my-login/?next=/leaderboard_view/')

    def test_leaderboard_view_logged_in(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('leaderboard_view'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leaderboards.html')
        
        # Check if games are in context
        self.assertIn('games', response.context)
        self.assertEqual(response.context['games'], ["Energy Conservation", "Recycling", "Cycling", "Quiz"])

        # Check leaderboard data
        self.assertIn('leaderboard_data', response.context)
        leaderboard_data = response.context['leaderboard_data']
        
        # Ensure user1 and user2 appear in leaderboard
        self.assertEqual(len(leaderboard_data), 2)
        self.assertEqual(leaderboard_data[0]['display_name'], 'user1')
        self.assertEqual(leaderboard_data[0]['overall'], 300)  # user1: 100+200
        self.assertEqual(leaderboard_data[1]['display_name'], 'user2')
        self.assertEqual(leaderboard_data[1]['overall'], 200)  # user2: 150+50
