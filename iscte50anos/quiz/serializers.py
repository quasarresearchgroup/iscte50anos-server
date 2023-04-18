from rest_framework import serializers

from quiz.models import Question, Quiz, Choice, Answer, TrialQuestion, Trial


class TrialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trial
        fields = ['number', 'progress', 'quiz_size', 'is_completed', 'score']


# Serialize quizzes as list of links (to show in App)
class QuizListSerializer(serializers.ModelSerializer):
    trials = TrialSerializer(read_only=True, many=True)

    class Meta:
        model = Quiz
        fields = ['number', 'num_trials', 'score', 'topic_names', 'trials']


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
        fields = ['text', 'type', 'image_link', 'category', 'choices', 'is_timed', 'time', 'id']


class TrialQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True, many=True)

    class Meta:
        model = TrialQuestion
        fields = ['number', 'question']


class AnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField()

    class Meta:
        model = Answer
        fields = ['choices']


class TrialAnswerSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        fields = ['number']
