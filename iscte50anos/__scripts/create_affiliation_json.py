import csv
import json
from datetime import datetime

from pathlib import Path

from users.models import Affiliation

p = Path(__file__).parent / 'files' / 'affiliations.csv'


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
        if word[0].isupper():
            abbreviation += word[0]
    return abbreviation


affiliation_json = {"-": ["-", "*"], "Aluno": ["-", "*"], "Docente": ["-", "*"],
                    "Investigador": ["-", "*"], "Funcionário": ["-", "*"]}

Affiliation.objects.all().delete()
with p.open(encoding="utf-8") as csvfile:
    groups_reader = csv.reader(csvfile, delimiter=";")
    header = next(groups_reader)
    i = 0
    for row in groups_reader:
        user_type = row[0]
        affiliation = row[1]
        if user_type == "Investigador":
            affiliation = affiliation.split(" - ")[0]
            abbr = affiliation
        else:
            abbr = get_abbreviation(affiliation)

        affiliation_json[user_type].append(abbr)

        Affiliation.objects.create(id=i,
                                   name=affiliation,
                                   type=get_type(user_type),
                                   abbreviation=abbr,
                                   full_description=f"{user_type} de {affiliation}")
        i+=1

    with open("affiliations_abbr.json", "w") as outfile:
        json.dump(affiliation_json, outfile)
