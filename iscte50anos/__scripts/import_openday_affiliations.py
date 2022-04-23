import csv
import json
from datetime import datetime

from pathlib import Path

from users.models import Affiliation

p = Path(__file__).parent / 'files' / 'openday_affiliations.csv'


def get_abbreviation(name):
    abbreviation = ""
    for word in name.split():
        if word[0].isupper():
            abbreviation += word[0]
    return abbreviation


affiliation_json = {"-": ["-", "*"]}

Affiliation.objects.all().delete()
with p.open(encoding="utf-8") as csvfile:
    groups_reader = csv.reader(csvfile, delimiter=";")
    header = next(groups_reader)
    i = 1
    for row in groups_reader:
        school = row[0]
        zone = row[1]
        if "-" in school:
            affiliation = school.split(" - ")[0]
            if len(affiliation) > 30:
                abbr = get_abbreviation(affiliation)
            else:
                abbr = affiliation
        else:
            abbr = get_abbreviation(school)

        if zone not in affiliation_json:
            affiliation_json[zone] = ["-", "*"]
        affiliation_json[zone].append(school)

        Affiliation.objects.create(id=i,
                                   name=school,
                                   type="student",
                                   subtype=zone,
                                   abbreviation=abbr,
                                   full_description=f"{school}")
        i+=1

    with open("openday_affiliations.json", "w") as outfile:
        print(affiliation_json)
        json.dump(affiliation_json, outfile)
