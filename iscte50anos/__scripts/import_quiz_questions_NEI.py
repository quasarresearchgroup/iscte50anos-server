from collections import defaultdict
import csv
from datetime import datetime
import json
from typing import Optional

from events.models import Event
from pathlib import Path

from quiz.models import Question, Choice
from topics.models import Topic
from quiz.serializers import QuestionSerializer

p_quiz = Path(__file__).parent / 'files' / 'quiz.tsv'

Question.objects.all().delete()

# TODO coluna muito longa
with p_quiz.open(encoding='UTF8') as quizFile:
    quiz_reader = csv.reader(quizFile, delimiter="\t")
    header = next(quiz_reader)
    for index, quizRow in enumerate(quiz_reader):
        topic = Topic.objects.get_or_create(title=quizRow[0])[0]

        question = Question.objects.create(text=quizRow[1], type="S")
        print(quizRow[1])
        question.topics.set([topic])

        correct_id = int(quizRow[6])

        choices = []
        for i in range(2, 6):
            choices.append(Choice(text=quizRow[i], is_correct=(correct_id == i-1), question=question))
        Choice.objects.bulk_create(choices)


# for question in Question.objects.all():
#     print(QuestionSerializer(question).da