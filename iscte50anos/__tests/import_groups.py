import csv
from datetime import datetime

from pathlib import Path

from users.models import Affiliation

p = Path(__file__).parent / 'files' / 'timeline.csv'


def get_type(user_type):
    if user_type == "Aluno":
        return "student"
    if user_type == "Funcionário":
        return "staff"
    if user_type == "Docente":
        return "professor"
    else:
        return "researcher"


def get_abbreviation(name):
    abbreviation = ""
    for word in name.split():
        if len(word) > 3:
            abbreviation += word[0]
    return abbreviation


Affiliation.objects.all().delete()
with p.open(encoding="utf-16") as csvfile:
    groups_reader = csv.reader(csvfile, delimiter="\t")
    header = next(groups_reader)

    for row in groups_reader:
        user_type = row[0]
        affiliation = row[1]
        if affiliation.contains(""):
            Affiliation.objects.create(name=affiliation, )