from django.contrib import admin

# Register your models here.
from .models import *


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'question_text')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer_text', 'is_correct')


class TestAdmin(admin.ModelAdmin):
    list_display = ('exam', 'start_time', 'completed', 'wrong_anwers')


admin.site.register(Exam)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(TestAnswer)

