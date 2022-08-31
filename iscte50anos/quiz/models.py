import random
from enum import Enum

from django.conf import settings
from django.db import models

from topics.models import Topic, TopicAccess
from users.models import Level

QUIZ_SIZE = 8
QUESTION_POINTS = 10


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
    # choices

    def image_link(self):
        if self.image:
            return self.image.link
        return ""

    def is_timed(self):
        return not self.topics.filter(title="Georeferenciação").exists()

    def __str__(self):
        return f"{self.text}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=200, null=False)
    is_correct = models.BooleanField(null=False)

    def __str__(self):
        return f"{self.text} - {self.question} (ID: {self.id})"


class Quiz(models.Model):
    number = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quizzes")
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)

    # trials
    topics = models.ManyToManyField(Topic)

    def __str__(self):
        return f"Quiz {self.number} - {self.user}"

    def num_trials(self):
        return self.trials.all().count()

    def topic_names(self):
        return "; ".join([topic.title for topic in self.topics.all()])

    def is_completed(self):
        return self.trials.filter(is_completed=True).count() == 3

    def score(self):
        quiz_score = 0
        for trial in self.trials.all():
            trial_score = trial.score()
            if trial_score > quiz_score:
                quiz_score = trial_score
        return quiz_score


class Trial(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="trials")
    number = models.IntegerField()
    # TODO make as field for performance
    is_completed = models.BooleanField(default=False)

    '''def is_completed(self):
        return not self.questions.filter(accessed=False).exists() and \
               self.questions.filter(number=QUIZ_SIZE).select_related("answer").first().is_answered()'''

    def progress(self):
        if self.is_completed():
            return QUIZ_SIZE
        progress = self.questions.filter(accessed=True).count()
        if progress == QUIZ_SIZE and not self.is_completed():
            progress -= 1
        return progress

    def quiz_size(self):
        return QUIZ_SIZE

    def score(self):
        trial_score = 0
        # prevent players to know score before completing trial (to know answers)
        if not self.is_completed():
            return 0

        for trial_question in self.questions.all().select_related("question", "answer"):
            question_score = 0
            question = trial_question.question
            answer = trial_question.answer
            if answer is None:
                continue

            if question.type == "S":
                choice = answer.choices.first()
                if choice is not None and choice.is_correct:
                    # TODO add score according to level (for now each question scores 10 points)
                    question_score = QUESTION_POINTS
            elif question.type == "M":
                for choice in answer.choices.all():
                    if choice is not None and choice.is_correct:
                        # answer_score = answer_value/(num_total_correct_answers)
                        answer_score = 5
                        question_score += answer_score
                    else:
                        # wrong_answer_deduction = wrong_answer_value/(num_total_correct_answers)
                        wrong_answer_deduction = 1
                        question_score -= wrong_answer_deduction

                if question_score < 0:
                    question_score = 0

            trial_score = trial_score + question_score

        max_score = (QUIZ_SIZE * QUESTION_POINTS) - ((self.number - 1) * QUESTION_POINTS)
        return trial_score if trial_score <= max_score else max_score

    def __str__(self):
        return f"{self.quiz} || Trial {self.number}"


class Answer(models.Model):
    answer_time = models.DateTimeField(auto_now_add=True)
    choices = models.ManyToManyField(Choice)


class TrialQuestion(models.Model):
    trial = models.ForeignKey(Trial, on_delete=models.CASCADE, related_name="questions")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="trial_questions")
    number = models.IntegerField(default=1)

    #TODO mark trial question as timed for performance

    # is_timed = models.BooleanField(default=False)

    accessed = models.BooleanField(default=False)
    access_time = models.DateTimeField(auto_now=True)

    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, related_name="trial_question")

    def is_answered(self):
        return self.accessed and self.answer is not None

    def __str__(self):
        return f"{self.trial} || Question {self.number}: {self.question} || ACCESS: {self.access_time}"




