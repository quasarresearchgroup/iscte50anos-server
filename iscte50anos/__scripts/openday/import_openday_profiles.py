import csv

from pathlib import Path
import random

from django.contrib.auth.models import User
from users.models import Profile, Affiliation

p = Path(__file__).parent / 'files' / 'openday_profiles.csv'


User.objects.exclude(username="admin").delete()
with p.open(encoding="utf-8") as csvfile:
    groups_reader = csv.reader(csvfile, delimiter=";")
    header = next(groups_reader)

    for row in groups_reader:
        first_name = row[0]
        last_name = row[1]
        email = row[2]
        concelho = row[3]
        school = row[4]

        user = User(username=f"{first_name}{last_name}{random.randint(1,10)}",
                            first_name=first_name,
                            last_name=last_name,
                            email=email)

        user.set_password(f"{first_name.lower()}{last_name.lower()}")
        user.save()

        affiliation = Affiliation.objects.get(subtype=concelho,
                                              name=school)

        Profile.objects.create(user=user, affiliation=affiliation)

