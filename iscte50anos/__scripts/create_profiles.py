from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import Profile

User = get_user_model()

User.objects.filter(username__contains="test").delete()
users = []
profiles = []
for i in range(1, 100):
    user = User(username=f"test{i}", first_name="João", last_name=f"Teste{i}")
    users.append(user)
    profiles.append(Profile(user=user, points=i))

User.objects.bulk_create(users)
Profile.objects.bulk_create(profiles)