import random
from enum import Enum

from django.conf import settings
from django.db import models

from topics.models import Topic, TopicAccess
from users.models import Level


class QuizImage(models.Model):
    description = models.CharField(max_length=200, blank=True)
    link = models.CharField(max_length=200, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.description


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
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=200, null=False)
    is_correct = models.BooleanField(null=False)

    def __str__(self):
        return f"{self.text} - {self.question}"


class Quiz(models.Model):
    number = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quizzes")
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)
    questions = models.ManyToManyField(Question, through='QuizQuestion')

    def __str__(self):
        return f"Quiz {self.level.level} - {self.user}"

    def is_completed(self):
        return


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Trial(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    number = models.IntegerField()

    def __str__(self):
        return f"Quiz {self.quiz}: Trial {self.number}"


class TrialQuestion(models.Model):
    trial = models.ForeignKey(Trial, on_delete=models.CASCADE, related_name="questions")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    access_time = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    trial_question = models.ForeignKey(TrialQuestion, on_delete=models.CASCADE, related_name="answers")
    answer_date = models.DateTimeField(auto_now_add=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

