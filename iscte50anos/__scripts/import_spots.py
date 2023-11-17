import csv
from datetime import datetime

from pathlib import Path

from users.models import Affiliation

from spots.models import Spot, QRCode, Layout, LayoutPeriod

p = Path(__file__).parent / 'files' / 'spots.csv'


Spot.objects.all().delete()
with p.open(encoding="utf-8") as csvfile:
    groups_reader = csv.reader(csvfile, delimiter=";")
    header = next(groups_reader)
    c = 1
    for row in groups_reader:
        link = row[1]
        description = row[2]
        Spot.objects.create(id=c, location_photo_link=link, description=description)
        c += 1




