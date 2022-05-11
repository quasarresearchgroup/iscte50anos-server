import random

from django.contrib.auth.models import User

from users.models import Profile, Affiliation

capitalCities = {"Rio", "Washington", "Sydney", "Luanda", "Pequim", "Toronto", "Xangai", "Mumbai", "Goa", "Macau",}

for city in capitalCities:
    User.objects.filter(username=city).delete()


