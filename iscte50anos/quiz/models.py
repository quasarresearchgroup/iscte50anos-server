import random
from enum import Enum

from django.conf import settings
from django.db import models

from topics.models import Topic, TopicAccess
from users.models import Level

class QuizImage(models.Model):
    description = models.CharField(max_length=200, blank=True)
    image = models.ImageField(null=True, blank=True)

class Question(models.Model):
    text = models.CharField(max_length=200, null=False)
    type = models.CharField(
        max_length=1,
        choices=(("S", "Single"), ("M", "Multiple"))
    )
    topics = models.ManyToManyField(Topic, related_name="questions")
    image = models.ForeignKey(QuizImage, on_delete=models.CASCADE, related_name="questions", null=True, blank=True)


    def __str__(self):
        return self.text


# TODO Change to Choice
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=200, null=False)
    is_correct = models.BooleanField(null=False)

    def __str__(self):
        return self.text


class Quiz(models.Model):
    number = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)
    questions = models.ManyToManyField(Question, through='QuizQuestion')

    def __str__(self):
        return f"Quiz {self.level.level} - {self.user}"

    def is_completed(self):
        return


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


# TODO migrate
class Trial(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    number = models.IntegerField()
    current_question = models.IntegerField(default=0)