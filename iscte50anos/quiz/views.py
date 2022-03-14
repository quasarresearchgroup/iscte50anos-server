import random

from django.shortcuts import render, get_object_or_404

# Get list of available quizzes for the user
from quiz.models import Quiz
from quiz.serializers import QuizListSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from quiz.models import Trial, TrialQuestion, Question

from quiz.serializers import QuestionSerializer, AnswerSerializer


@api_view()
@permission_classes([IsAuthenticated])
def get_user_quiz_list(request):
    quizzes = Quiz.objects.filter(user=request.user)
    return Response(data=QuizListSerializer(quizzes, many=True).data)

# Get and start quiz
@api_view()
@permission_classes([IsAuthenticated])
def start_quiz_trial(request, quiz_num):

    quiz = get_object_or_404(Quiz, user=request.user, number=quiz_num)

    # Count trials for quiz
    trial_count = Trial.objects.filter(quiz=quiz).count()

    # Cannot create more trials
    # TODO already max score
    if trial_count >= 3:
        return Response(status=400) # Bad request

    new_trial = Trial.objects.create(quiz=quiz, number=trial_count+1)
    return Response(status=200)


# Questions?
@api_view()
@permission_classes([IsAuthenticated])
def get_next_question(request, quiz_num, num_trial):
    trial = get_object_or_404(Trial, quiz__number=quiz_num, quiz__user=request.user, number=num_trial)

    id_answered_questions_id = [tq.question.id for tq in list(trial.questions.all())]

    available_questions = list(trial.quiz.questions.exclude(id__in=id_answered_questions_id))

    if len(available_questions) == 0:
        return Response(status=400)

    next_question = random.choice(available_questions)

    trial_question = TrialQuestion.objects.create(trial=trial, question=next_question)

    return Response(data=QuestionSerializer(next_question).data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def answer_current_question(request, quiz, trial):
    trial_question = TrialQuestion.objects.get()
    answer_serializer = AnswerSerializer(data=request.data)
    if answer_serializer.is_valid():

        return Response(status=200)
    else:
        return Response(status=400)
    # Get user input and validate
    # Answer current question (that is in the current trial)
    # Create answer (if not answered)


'''
def answer_question(request, quiz, trial, question_id):
    pass
    # Get user input and validate
    # Check if question for trial was already answered
    # Create answer (if not answered)
'''
