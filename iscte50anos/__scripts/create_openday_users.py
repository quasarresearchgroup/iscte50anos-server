import random

from django.contrib.auth.models import User

from users.models import Profile

capitalCities = {"Lisboa", "Paris", "Madrid", "Berna", "Kiev", "Berlim", "Atenas", "Bruxelas", "Roma", "Praga",
                 "Dublin", "Oslo", "Amsterdão", "Varsóvia", "Estocolmo", "Zagreb", "Copenhaga", "Sofia", "Viena",
                 "Bratislava", "Londres", "Bucareste", "Belgrado", "Riga", "Liubliana", "Tallinn", "Vilnius",
                 "Andorra", "Mónaco", "Luxemburgo"}

for city in capitalCities:
    password = f"{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}" \
               f"{random.randint(0,9)}{random.randint(0,9)}"

    print(f'{city} {password}')

    user = User(username=city, first_name=city)

    user.set_password(password)
    user.save()

    Profile.objects.create(user=user)

