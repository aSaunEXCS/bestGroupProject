from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import time
#Test set up
class GameIndexViewTestCase(TestCase):
    def setUp(self):
        # Create a test user and client
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.index_url = reverse('index')

    def test_index_redirect_if_not_logged_in(self):
        response = self.client.get(self.index_url)
        self.assertRedirects(response, f'/my-login/?next={self.index_url}')

    def test_index_initial_game_state(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.index_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('game_state', self.client.session)

        game_state = self.client.session['game_state']
        self.assertIn('devices', game_state)
        self.assertEqual(game_state['score'], 25)
        self.assertTrue(game_state['status'])
        self.assertIsInstance(game_state['start_time'], float)

    def test_index_restore_existing_game_state(self):
        self.client.login(username='testuser', password='password')
        self.client.session['game_state'] = {
            'devices': {'lamp': True, 'laptop': False},
            'score': 15,
            'start_time': time.time() - 100,
            'status': True,
        }
        self.client.session.save()

        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        game_state = self.client.session['game_state']
        self.assertEqual(game_state['score'], 15)

    def test_index_clear_completed_game_state(self):
        self.client.login(username='testuser', password='password')
        self.client.session['game_state'] = {'status': False}
        self.client.session.save()

        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        game_state = self.client.session['game_state']
        self.assertEqual(game_state['score'], 25)
        self.assertTrue(game_state['status'])
