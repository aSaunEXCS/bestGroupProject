from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from quizes.models import Quiz, Question, Result
from django.db.models import F
from leaderboard.models import leaderboard
import json

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

def quiz_data(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = []
    for q in quiz.get_questions():
        answers = [a.text for a in q.get_answers()]
        questions.append({"question": q.text, "answers": answers})
    return JsonResponse({'quiz': quiz.title, 'questions': questions})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.get_questions()
    return render(request, 'quiz_detail.html', {'quiz': quiz})


@csrf_exempt
def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        data = json.loads(request.body)
        score = 0
        time_taken = data.get("time_taken", 0)  # Get time from frontend

        for question_id, selected_answer in data.get("answers", {}).items():
            question = get_object_or_404(Question, id=question_id, quiz=quiz)
            correct_answer = question.get_answers().filter(correct=True).first()
            if correct_answer and correct_answer.text == selected_answer:
                score += 1

        result = Result.objects.create(user=request.user, quiz=quiz, score=score, time_taken=time_taken)
        leaderboard.objects.filter(username=request.user).update(points=F('points') + Result.objects.values('score'))

        return JsonResponse({'score': score, 'time_taken': time_taken})  # Return time_taken
    return HttpResponse(status=405)
