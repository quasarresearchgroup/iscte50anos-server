from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from topics.models import TopicAccess

import random

class Affiliation(models.Model):
    name = models.CharField(max_length=30)
    cycle = models.CharField(
        max_length=3,
        choices=(("bsc", "Bachelor's"), ("msc","Master's"), ("phd", "Doctorate"))
    )

    def __str__(self):
        return f'{self.name} - {self.cycle}'


class Profile(models.Model):
    # name, surname, email in django User model

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=10,
        choices=(("student", "Student"), ("prof", "Professor"), ("researcher", "Researcher"), ("staff", "Staff"))
    )
    affiliation = models.ForeignKey(Affiliation, on_delete=models.SET_NULL, null=True)
    level = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}'


class Level(models.Model):
    level = models.IntegerField()

    percent_correct = models.DecimalField(decimal_places=2, max_digits=3)

    # Total topics accessed to unlock this level
    min_topics = models.IntegerField()

    # Maximum topics to stay in this level
    max_topics = models.IntegerField()

    trials_allowed = models.IntegerField()

    max_points_quiz = models.IntegerField()

    # Seconds
    max_time_per_question = models.IntegerField()

    num_single_questions = models.IntegerField()

    num_multiple_questions = models.IntegerField()

    def __str__(self):
        return "Level " + str(self.level)


