from django.db import models
from django.contrib.auth.models import User
# Model representing a Quiz
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_questions(self):
        return self.question_set.all()


# Model representing a Question in a Quiz
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

    def get_answers(self):
        return self.answer_set.all()


# Model representing an Answer to a Question
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Q: {self.question.text} | A: {self.text} | Correct: {self.correct}"
# Model representing the result of a user taking a quiz
class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    time_taken = models.FloatField()

    def __str__(self):
        return f"{self.user} - {self.quiz.title} - Score: {self.score}"