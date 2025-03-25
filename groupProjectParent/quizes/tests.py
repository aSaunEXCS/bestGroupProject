from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Quiz, Question, Answer, Result
from leaderboard.models import LeaderboardEntry
import json

class QuizViewsTest(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')

        # Create a quiz with questions and answers
        self.quiz = Quiz.objects.create(title='Sample Quiz')
        self.question1 = Question.objects.create(quiz=self.quiz, text='What is 2+2?')
        self.answer1 = Answer.objects.create(question=self.question1, text='4', correct=True)
        self.answer2 = Answer.objects.create(question=self.question1, text='3', correct=False)

    def test_quiz_list_view(self):
        response = self.client.get(reverse('quiz_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sample Quiz')

    def test_quiz_data_view(self):
        response = self.client.get(reverse('quiz_data', args=[self.quiz.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['quiz'], 'Sample Quiz')
        self.assertEqual(len(response.json()['questions']), 1)

    def test_quiz_detail_view(self):
        response = self.client.get(reverse('quiz_detail', args=[self.quiz.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sample Quiz')

    def test_submit_quiz_correct_answer(self):
        response = self.client.post(
            reverse('submit_quiz', args=[self.quiz.id]),
            data=json.dumps({'answers': {str(self.question1.id): '4'}, 'time_taken': 30}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['score'], 1)
        self.assertEqual(response.json()['time_taken'], 30)
        result = Result.objects.get(user=self.user, quiz=self.quiz)
        self.assertEqual(result.score, 1)

    def test_submit_quiz_wrong_answer(self):
        response = self.client.post(
            reverse('submit_quiz', args=[self.quiz.id]),
            data=json.dumps({'answers': {str(self.question1.id): '3'}, 'time_taken': 20}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['score'], 0)
        result = Result.objects.get(user=self.user, quiz=self.quiz)
        self.assertEqual(result.score, 0)

    def test_submit_quiz_invalid_method(self):
        response = self.client.get(reverse('submit_quiz', args=[self.quiz.id]))
        self.assertEqual(response.status_code, 405)
