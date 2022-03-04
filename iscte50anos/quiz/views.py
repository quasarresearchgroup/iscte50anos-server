from django.shortcuts import render

# Get list of available quizzes for the user
from quiz.models import Quiz
from quiz.serializers import QuizListSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view()
@permission_classes([IsAuthenticated])
def get_user_quiz_list(request):
    quizzes = Quiz.objects.filter(user=request.user)
    return Response(data=QuizListSerializer(quizzes, many=True).data)

# Get and start quiz
def start_quiz(request, quiz_id):
    pass
    # Check if more trials are available (or if score is max)
    # if trials are available, create next trial (check level) (or max 3)
    # Create next available trial
    # Send questions

# Questions?
def get_next_question(request, quiz, trial):
    pass
    # Store current question in trial?
    # Send question one by one?

def answer_current_question(request, trial, question_id):
    pass
    # Get user input and validate
    # Answer current question (that is in the current trial)
    # Create answer (if not answered)

def answer_question(request, trial, question_id):
    pass
    # Get user input and validate
    # Check if question for trial was already answered
    # Create answer (if not answered)

