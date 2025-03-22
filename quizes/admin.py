from django.contrib import admin
from .models import Quiz, Question, Answer, Result

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('text', 'quiz')

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title',)

class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'time_taken')

# Registering models
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Result, ResultAdmin)
