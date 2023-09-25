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


with p_quiz.open(encoding='UTF8') as quizFile:
    quiz_reader = csv.reader(quizFile, delimiter="\t")
    header = next(quiz_reader)
    for index, quizRow in enumerate(quiz_reader):
        topic = Topic.objects.get_or_create(title=quizRow[0])

        question = Question(text=quizRow[1], type="S")
        question.topics.set([topic])

        correct_id = int(quizRow[6])
        for i in range(2, 6):
            question.choices.add(Choice.objects.create(text=quizRow[i], is_correct=(correct_id == i-1)))

        question.save()

# for question in Question.objects.all():
#     print(QuestionSerializer(question).data)