from django.contrib import admin

# Register your models here.
from topics.models import Topic

from topics.models import TopicAccess

admin.site.register(Topic)
admin.site.register(TopicAccess)