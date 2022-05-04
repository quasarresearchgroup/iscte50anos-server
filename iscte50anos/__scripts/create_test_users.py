import random

from django.contrib.auth.models import User

from users.models import Profile, Affiliation

capitalCities = {"Rio", "Washington", "Sydney", "Luanda", "Pequim", "Toronto", "Xangai", "Mumbai", "Goa", "Macau",}

for city in capitalCities:
    password = f"{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}" \
               f"{random.randint(0,9)}{random.randint(0,9)}"

    print(f'{city} {password}')

    user = User(username=city, first_name=city)

    user.set_password(password)
    user.save()

    affiliation = Affiliation.objects.get_or_create(subtype="Teste",
                                          name="Open Day")[0]

    Profile.objects.create(user=user)

