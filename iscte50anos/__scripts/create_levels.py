from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import Level
from topics.models import Topic

# TODO create score progression for each level
Level.objects.all().delete()

topics = Topic.objects.all()
levels = []
c = 0
for topic in topics:
    levels.append(Level(number=c, num_topics=c, question_score=10))
    c += 1
print(levels)
Topic.objects.bulk_create(levels)
