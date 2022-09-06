from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import Level
from topics.models import Topic

# TODO create score progression for each level

topics = Topic.objects.all()
levels = []
c = 0
for topic in topics:
    levels.append(Level(number=c, ))
    c += 1
Topic.objects.bulk_create(levels)
