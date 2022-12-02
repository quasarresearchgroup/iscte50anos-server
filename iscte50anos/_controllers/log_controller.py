import random
from quiz.models import Quiz, Question, TrialQuestion
from topics.models import TopicAccess, Topic

from users.models import Profile, Level

from log.models import AccessLog


def save_log(request):
    origin_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    link = request.build_absolute_uri()
    AccessLog.objects.create(origin_ip=origin_ip, link=link)
