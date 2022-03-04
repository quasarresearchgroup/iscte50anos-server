from django.conf import settings
from django.db import models


class Topic(models.Model):
    title = models.CharField(max_length=50)
    link = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

    # Serve API in order of content type


class TopicAccess(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    when = models.DateTimeField(auto_now_add=True)
    #is_scan = models.BooleanField()

    def __str__(self):
        return f'{self.topic} - {self.user}'
