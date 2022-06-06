import csv
from datetime import datetime

from events.models import Event
from pathlib import Path

p = Path(__file__).parent / 'files' / 'timeline.csv'


def translate_scope(scope):
    if scope == "Iscte":
        return "iscte"
    if scope == "Portugal" or scope == "Nacional":
        return "portugal"
    else:
        return "world"


Event.objects.all().delete()
i = 1
with p.open(encoding="utf-16") as csvfile:
    timeline_reader = csv.reader(csvfile, delimiter="\t")
    header = next(timeline_reader)
    for row in timeline_reader:
        date = datetime.strptime(row[0], '%d/%m/%Y')
        if row[3] == "":
            Event.objects.create(id=i, date=date, title=row[2])
        else:
            Event.objects.create(id=i, date=date, title=row[2], scope=translate_scope(row[3]))
        i += 1
