from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Exam, Question, Test, Answer, TestAnswer
from .forms import StartTestForm
from .helpers import is_correct_answer, import_exam_text
from datetime import datetime
import random, json
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.
def home(request):
    exams = Exam.objects.all().order_by('name')
    tests = Test.objects.all().order_by('-start_time')
    return render(request, 'index.html', {'exam_list': exams, 'test_list': tests})


@login_required(login_url='/admin/')
def import_exam(request):
    if request.method == "POST":
        exam_name = request.POST['exam_name']
        exam_text = request.FILES['exam_file'].read().decode('utf-8')
        import_exam_text(exam_name, exam_text)
        return redirect('exams:index')

    return render(request, 'import_exam.html')


def new_test(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    errors = ""
    if request.method == "POST":
        form = StartTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.exam = exam
            # Defino questions_order
            questions_id = Question.objects.filter(exam=exam.id).values_list('pk', flat=True)
            questions_list = list(questions_id)
            random.shuffle(questions_list)
            # end questions_order
            test.questions_order = json.dumps(questions_list)
            test.save()
            return redirect('exams:test', pk=test.uid)
        else:
            errors = ["Error en los datos, intente nuevamente."]

    questions_count = Question.objects.filter(exam=exam).count()
    form = StartTestForm()
    return render(request, 'start_test.html', {'form': form, 'exam': exam.name
                                            , 'count': questions_count, 'errors': errors})


def test(request, pk):
    if request.method == "POST":
        return redirect('exams:questions', pk=pk, qid=1)

    test = get_object_or_404(Test, uid=pk)
    exam = Exam.objects.get(pk=test.exam.id)
    questions_order = json.loads(test.questions_order)
    questions_count = len(questions_order)
    questions = Question.objects.filter(exam=exam.id)
    answers = TestAnswer.objects.filter(test=test.id)
    # Sort answers to match the test order
    answers_sorted = []
    can_review = settings.EXAM_CAN_REVIEW
    if test.completed:
        for i in questions_order:
            answers_sorted.append([a for a in answers if a.question.id==i][0])
    return render(request, 'test.html', {'exam': exam.name
                                            , 'test': test
                                            , 'count': questions_count
                                            , 'answers': answers_sorted
                                            , 'can_review': can_review})
    

def test_questions(request, pk, qid):
    test = get_object_or_404(Test, uid=pk)
    exam = Exam.objects.get(pk=test.exam.id)

    # Selecciono la pregunta según el orden definido para este test
    questions_order = json.loads(test.questions_order)
    questions_count = len(questions_order)
    question_id = questions_order[qid -1]
    question = Question.objects.get(id=question_id)

    answers = Answer.objects.filter(question=question)
    # single or multple correct answers
    multiple = len([a for a in answers if a.is_correct == True]) > 1

    # Verifico si ya existe un registro para esta respuesta
    test_answer = TestAnswer.objects.filter(test=test.pk, question=question_id)
    if len(test_answer)==0:
        # defino el orden de las respuestas
        answers_order = [i for i in range(len(answers))]
        random.shuffle(answers_order)

        test_answer = TestAnswer()
        test_answer.test = test
        test_answer.question = question
        test_answer.answers_order = json.dumps(answers_order)
        test_answer.save()
    else:
        test_answer = test_answer[0]
        if request.method == "POST":
            if multiple:
                post_answer = request.POST.getlist('choice []')
            else:
                post_answer = [request.POST.get('choice')]
            if post_answer == [None]:
                return redirect('exams:questions', pk=test.uid, qid=qid)
            user_answer = [int(a) for a in post_answer]
            test_answer.selected_answers = json.dumps(user_answer)
            test_answer.is_correct = is_correct_answer(answers, user_answer)
            test_answer.end_time = datetime.now()
            test_answer.save()
            if qid < questions_count:
                return redirect('exams:questions', pk=test.uid, qid=qid+1)
            else:
                # TODO: verify ALL questions have answer
                wrong_anwers = TestAnswer.objects.filter(test=test.id, is_correct=False)
                test.completed = True
                test.wrong_anwers = len(wrong_anwers)
                test.save()
                return redirect('exams:test', pk=test.uid)
        else:
            answers_order = json.loads(test_answer.answers_order)

        
    selected_answers = [] if test_answer.selected_answers is None else json.loads(test_answer.selected_answers)
    options = [answers[i] for i in answers_order]
    # return HttpResponse("test_questions")
    return render(request, 'test_question.html', {'exam': exam.name
                                            , 'question_index': qid
                                            , 'questions_count': questions_count
                                            , 'test': test
                                            , 'question': question
                                            , 'options': options
                                            , 'selected_answers': selected_answers
                                            , 'multiple': multiple})