from rest_framework import serializers

from quiz.models import Question, Quiz

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


# Serializer for possible answers of a question
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text']


# Serializer for a question of a quiz
class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(read_only=True, many=True)
    class Meta:
        model = Question
        fields = ['text', 'answers']



