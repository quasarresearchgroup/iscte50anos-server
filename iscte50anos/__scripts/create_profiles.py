from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import Profile

User = get_user_model()

User.objects.filter(username__contains="test").delete()
for i in range(1, 100):
    user = User.objects.create(username=f"test{i}", first_name="João", last_name=f"Teste{i}")
    profile = Profile.objects.create(user=user, points=i)
