import csv
import json
from datetime import datetime

from pathlib import Path

p = Path(__file__).parent / 'files' / 'affiliations.csv'


def get_abbreviation(name):
    abbreviation = ""
    for word in name.split():
        if word[0].isupper():
            abbreviation += word[0]
    return abbreviation

affiliation_json = {"-":["-","*"], "Aluno":["-","*"], "Docente":["-","*"], "Investigador":["-","*"], "Funcionário":["-","*"]}

with p.open(encoding="utf-8") as csvfile:
    groups_reader = csv.reader(csvfile, delimiter=";")
    header = next(groups_reader)

    for row in groups_reader:
        user_type = row[0]
        affiliation = row[1]
        if user_type == "Investigador":
            affiliation = affiliation.split(" - ")[0]
        else:
            affiliation = get_abbreviation(affiliation)

        affiliation_json[user_type].append(affiliation)

    with open("affiliations_abbr.json", "w") as outfile:
        json.dump(affiliation_json, outfile)
