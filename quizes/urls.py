from django.urls import path
from quizes import views



from django.urls import path
from . import views

urlpatterns = [
    path('list', views.quiz_list, name='quiz-list'),  # Show the list of quizzes
    path('quiz/<int:quiz_id>/data/', views.quiz_data, name='quiz-data'),  # API for quiz JSON data
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz-detail'),  # HTML page for quiz
    path('<int:quiz_id>/submit/', views.submit_quiz, name='quiz-submit'),
]
