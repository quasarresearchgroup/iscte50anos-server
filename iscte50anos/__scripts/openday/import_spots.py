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

p = Path(__file__).parent / 'files' / 'qrcodes.csv'

QRCode.objects.all().delete()
with p.open(encoding="utf-8") as csvfile:
    groups_reader = csv.reader(csvfile, delimiter=";")
    header = next(groups_reader)
    c = 1
    for row in groups_reader:
        print(row)
        uuid = row[1]
        QRCode.objects.create(id=c, uuid=uuid)
        c += 1

p = Path(__file__).parent / 'files' / 'period.csv'

LayoutPeriod.objects.all().delete()
with p.open(encoding="utf-8") as csvfile:
    groups_reader = csv.reader(csvfile, delimiter=";")
    header = next(groups_reader)
    c = 1
    for row in groups_reader:
        date1 = row[2].split("/")
        date2 = row[3].split("/")
        LayoutPeriod.objects.create(id=c,
                                    description=row[1],
                                    start_date=f"{date1[0]}-{date1[1]}-{date1[2]}",
                                    end_date=f"{date2[0]}-{date2[1]}-{date2[2]}")
        c += 1


p = Path(__file__).parent / 'files' / 'layout.csv'

Layout.objects.all().delete()
with p.open(encoding="utf-8") as csvfile:
    groups_reader = csv.reader(csvfile, delimiter=";")
    header = next(groups_reader)
    c = 1
    for row in groups_reader:

        period_id = row[0]
        qrcode_id = row[1]
        spot_id = row[2]

        period = LayoutPeriod.objects.get(id=period_id)
        qrcode = QRCode.objects.get(id=qrcode_id)
        spot = Spot.objects.get(id=spot_id)

        Layout.objects.create(period=period, qrcode=qrcode, spot=spot)
        c += 1
