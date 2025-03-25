from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from leaderboard.models import LeaderboardEntry
from leaderboard.views import calculate_percentile, calculate_best_score_for_game, calculate_overall_score

class LeaderboardTests(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        # Create leaderboard entries
        self.games = ["Energy Conservation", "Cycling", "Recycling", "Quiz"]
        LeaderboardEntry.objects.create(user=self.user1, game="Energy Conservation", score=50)
        LeaderboardEntry.objects.create(user=self.user2, game="Energy Conservation", score=80)
        LeaderboardEntry.objects.create(user=self.user1, game="Cycling", score=40)
        LeaderboardEntry.objects.create(user=self.user2, game="Cycling", score=60)

    def test_calculate_percentile(self):
        scores = [50, 80, 40, 60]
        self.assertEqual(calculate_percentile(80, scores), 100.0)
        self.assertEqual(calculate_percentile(40, scores), 25.0)
        self.assertEqual(calculate_percentile(30, scores), 0)

    def test_calculate_best_score_for_game(self):
        self.assertEqual(calculate_best_score_for_game(self.user1, "Energy Conservation"), 50)
        self.assertEqual(calculate_best_score_for_game(self.user1, "Quiz"), 0)

    def test_calculate_overall_score(self):
        self.assertEqual(calculate_overall_score(self.user1, self.games), 90)
        self.assertEqual(calculate_overall_score(self.user2, self.games), 140)

    def test_homepage_view_authenticated(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('energy_percentile', response.context)
        self.assertIn('cycling_percentile', response.context)
        self.assertIn('recycling_percentile', response.context)
        self.assertIn('quiz_percentile', response.context)
        self.assertIn('overall_percentile', response.context)

    def test_homepage_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('homepage'))
        self.assertRedirects(response, '/my-login/?next=/homepage')

