from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from quizes.models import Quiz, Question, Result
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
    return render(request, 'quiz_detail.html', {'quiz': quiz})


@csrf_exempt
def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        data = json.loads(request.body)
        score = 0
        start_time = now()
        for question_id, selected_answer in data.get("answers", {}).items():
            question = get_object_or_404(Question, id=question_id, quiz=quiz)
            correct_answer = question.get_answers().filter(correct=True).first()
            if correct_answer and correct_answer.text == selected_answer:
                score += 1
        time_taken = (now() - start_time).seconds
        result = Result.objects.create(user=request.user, quiz=quiz, score=score, time_taken=time_taken)
        return JsonResponse({'score': score, 'time_taken': time_taken})
