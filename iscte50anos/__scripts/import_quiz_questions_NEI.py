import os
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

quiz_dir = Path(__file__).parent / 'files' / 'NEI_quiz'

Question.objects.all().delete()


def import_1():
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
                choices.append(Choice(text=quizRow[i], is_correct=(correct_id == i - 1), question=question))
            Choice.objects.bulk_create(choices)


def import_2():
    for filename in os.listdir(quiz_dir):
        with open(os.path.join(quiz_dir, filename)) as quizFile:
            quiz_reader = csv.reader(quizFile, delimiter="\t")
            header = next(quiz_reader)

            topic = Topic.objects.get_or_create(title=filename.split('.')[0])[0]
            for index, quizRow in enumerate(quiz_reader):

                question = Question.objects.create(text=quizRow[0], type="S")
                print(quizRow[0])
                question.topics.set([topic])

                correct_id = int(quizRow[5])

                choices = []
                for i in range(1, 5):
                    choices.append(Choice(text=quizRow[i], is_correct=(correct_id == i - 1), question=question))
                Choice.objects.bulk_create(choices)


import_2()
