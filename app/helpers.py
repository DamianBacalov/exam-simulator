import re
from datetime import datetime
from app.models import Exam, Question, Answer


def is_correct_answer(options, answer):
    correct_ids = [a.id for a in options if a.is_correct == True]
    is_correct = sorted(correct_ids)==sorted(answer)
    return is_correct


def import_exam_text(exam_name, exam_text):
    exam = Exam()
    exam.name = exam_name
    exam.pub_date = datetime.now()
    exam.save()

    # with open(exam_file, 'r', encoding='utf-8') as infile:
    #     questions = infile.read()
    questions = exam_text
    # print(questions)

    # 1st regex: questions
    questions_regex = 'Question.*?[\r\n]([\s\S]*?)[\r\n]{3}'
    questions_match = re.compile(questions_regex, re.DOTALL).findall(questions)
    # print(len(questions_match))

    # 2nd regex: question
    for q in questions_match:
        question_regex = '([\s\S]*?)[\r\n]A[\*|\.]'
        question_match = re.compile(question_regex, re.DOTALL).findall(q)
        question_text = question_match[0]
        # print(question_text)
        question = Question()
        question.exam = exam
        question.question_text = question_text
        question.save()

        # 3rd regex: options
        options_regex = '^\w(\*)?\. ([^\n]+)'
        options_match = re.compile(options_regex, re.MULTILINE).findall(q)
        for correct, option in options_match:
            is_correct = correct == '*'
            option_text = option
            # print(is_correct)
            answer = Answer()
            answer.question = question
            answer.answer_text = option_text
            answer.is_correct = is_correct
            answer.save()
