from abc import ABC

from rest_framework import serializers

from quiz.models import Question, Quiz, Choice, Answer, TrialQuestion, Trial
from topics.serializers import TopicSerializer


class TrialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trial
        fields = ['number', 'progress', 'quiz_size', 'is_completed', 'score']


# Serialize quizzes as list of links (to show in App)
class QuizListSerializer(serializers.ModelSerializer):
    trials = TrialSerializer(read_only=True, many=True)
    topics = TopicSerializer(read_only=True, many=True)

    class Meta:
        model = Quiz
        fields = ['number', 'max_num_trials', 'num_trials', 'score', 'topics', 'trials']


# Serializer for possible choices of a question
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['text', 'id']


# Show question (single fed questions)
class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ['id','text', 'type', 'image_link', 'category', 'choices', 'is_timed', 'time', 'id']


class TrialQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = TrialQuestion
        fields = ['number', 'question']


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['choices', 'question_id']


class TrialAnswerSerializer(serializers.Serializer):
    answers = AnswerSerializer(many=True)

