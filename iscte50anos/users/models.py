from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Affiliation(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(
        max_length=10,
        choices=(("student", "Student"), ("professor", "Professor"), ("researcher", "Researcher"), ("staff", "Staff")),
        default="student"
    )
    cycle = models.CharField(
        max_length=3,
        choices=(("bsc", "Bachelor's"), ("msc", "Master's"), ("phd", "Doctorate"))
    )
    abbreviation = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f'{self.type} - {self.abbreviation}'


class Profile(models.Model):
    # name, surname, email, username in django User model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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


