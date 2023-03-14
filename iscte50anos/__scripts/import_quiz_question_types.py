from collections import defaultdict
import csv
from datetime import datetime
import json
from typing import Optional

from events.models import Event
from pathlib import Path

from quiz.models import Question
from quiz.serializers import QuestionSerializer

p_quiz= Path(__file__).parent / 'files' / 'Cronologia Cinquentenário - Quiz.tsv'


def translate_question_category(category:str)->Optional[str]:
# AutoExplicativa
    if category == "AutoExplicativa":
        return "self_explanatory"
# Quotidiano
    if category == "Quotidiano":
        return "daily_life"
# Georeferenciação
    if category == "Georeferenciação":
        return "georeferencing"
# Cronologia
    if category == "Cronologia":
        return "chronology"
# Dimensões
    if category == "Dimensões":
        return "dimensions"
    else:
        return None


with p_quiz.open(encoding='UTF8') as quizFile:
    quiz_reader = csv.reader(quizFile, delimiter="\t")
    header = next(quiz_reader)
    for index,quizRow in enumerate(quiz_reader):
        # print(quizRow)
        question_id:int = int(quizRow[0])
        question_string:str = quizRow[1]
        question_image_link:str = quizRow[2]
        question_category:str = translate_question_category(quizRow[5])

        print(f"id:{question_id};question:{question_string}; question_image_link:{question_image_link}; question_category:{question_category};")
        Question.objects.filter(pk=question_id).update(category = question_category)

# for question in Question.objects.all():
#     print(QuestionSerializer(question).data)