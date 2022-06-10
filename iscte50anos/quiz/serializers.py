from rest_framework import serializers

from quiz.models import Question, Quiz, Choice, Answer, TrialQuestion

# Serializer for full quiz (with questions and respective answer choices)
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["questions", "level"]


# Serialize quizzes as list of links (to show in App)
class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['level']


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
        fields = ['text', 'type', 'choices']


class TrialQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = TrialQuestion
        fields = ['number', 'question']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['choices']

