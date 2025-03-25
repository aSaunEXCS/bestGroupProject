from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from leaderboard.models import LeaderboardEntry

class WasteGameViewTest(TestCase):
    def setUp(self):
        # Set up a user and client for testing
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.url = reverse('waste_game')

    def test_redirect_if_not_logged_in(self):
        # Ensure the view redirects unauthenticated users
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_game_initial_load(self):
        # Test initial game state for logged-in user
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('image', response.context)
        self.assertEqual(response.context['score'], 0)

    def test_correct_answer_increases_score(self):
        # Test that a correct answer increases the score
        self.client.login(username='testuser', password='password')
        self.client.get(self.url)  # Start the game
        response = self.client.post(self.url, {'answer': 'non-recyclable'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session['waste_score'], 100)

    def test_wrong_answer_does_not_increase_score(self):
        # Test that a wrong answer doesn't change the score
        self.client.login(username='testuser', password='password')
        self.client.get(self.url)  # Start the game
        response = self.client.post(self.url, {'answer': 'recyclable'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session['waste_score'], 0)

    def test_game_completion_and_leaderboard_entry(self):
        # Simulate a full game and check leaderboard entry
        self.client.login(username='testuser', password='password')
        for _ in range(10):
            current_image = self.client.session['waste_index']
            answer = 'recyclable' if current_image in [2, 3, 4, 6, 7, 8] else 'non-recyclable'
            self.client.post(self.url, {'answer': answer})

        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'Recycle/win.html')
        self.assertTrue(LeaderboardEntry.objects.filter(user=self.user, game="Recycling").exists())

    def test_session_resets_after_game(self):
        # Ensure session resets after game completion
        self.client.login(username='testuser', password='password')
        for _ in range(10):
            answer = 'recyclable'  # Assuming repetitive answers for simplicity
            self.client.post(self.url, {'answer': answer})

        self.assertNotIn('waste_index', self.client.session)
        self.assertNotIn('waste_score', self.client.session)
