from rest_framework import serializers

from quiz.models import Question, Quiz, Choice, Answer, TrialQuestion


# Serialize quizzes as list of links (to show in App)
class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['number', 'num_trials', 'score', 'topic_names']


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
        fields = ['text', 'type', 'image_link', 'choices', 'is_timed']


class TrialQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = TrialQuestion
        fields = ['number', 'question']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['choices']
