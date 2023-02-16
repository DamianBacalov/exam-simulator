from django.db import models
from datetime import datetime
from django.core.validators import int_list_validator
import uuid

'''
Test Models:
. ./manage.py shell
. from app import models
. exams = models.Exam.objects.all()

To get all de PKs:
. pks = models.Question.objects.all().values_list('pk', flat=True)
. pks_list = list(pks)

To shuffle ids
. import random
. random.shuffle(pks_list)
'''
class Exam(models.Model):
    name = models.CharField(max_length=64)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.name


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    question_image = models.ImageField(upload_to='./', null=True, blank=True)

    def __str__(self):
        return self.question_text[:40]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text[:20]


class Test(models.Model):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, null=True, blank=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=datetime.now)
    user = models.CharField(max_length=64)
    questions_order = models.CharField(validators=[int_list_validator], max_length=300)
    questions_answered = models.IntegerField(default=0)
    wrong_anwers = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)


class TestAnswer(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)
    answers_order = models.CharField(validators=[int_list_validator], max_length=16)
    selected_answers = models.CharField(validators=[int_list_validator], max_length=8, null=True, blank=True)
    is_correct = models.BooleanField(default=False)

