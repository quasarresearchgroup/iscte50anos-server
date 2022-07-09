import random
from datetime import timezone

from django.db import transaction
from django.shortcuts import render, get_object_or_404

# Get list of available quizzes for the user
from django.utils.datetime_safe import datetime
from quiz.models import Quiz
from quiz.serializers import QuizListSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from quiz.models import Trial, TrialQuestion, Question

from quiz.serializers import QuestionSerializer, AnswerSerializer, TrialQuestionSerializer

from _controllers import quiz_controller

ANSWER_TIME = 45 # segundos

@api_view()
@permission_classes([IsAuthenticated])
def get_user_quiz_list(request):
    quizzes = Quiz.objects.filter(user=request.user)
    return Response(data=QuizListSerializer(quizzes, many=True).data)


# Get and start quiz
@api_view(["POST"])
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

    quiz_controller.assign_trial_questions(request.user, new_trial, quiz.topics.all())

    return Response(status=201, data={"trial_number": trial_count+1})

@api_view()
@permission_classes([IsAuthenticated])
def get_current_question(request, quiz_num, num_trial):
    # trial = get_object_or_404(Trial, quiz__number=quiz_num, quiz__user=request.user, number=num_trial)
    trial = Trial.objects.filter(quiz__number=quiz_num,
                                                     quiz__user=request.user,
                                                     number=num_trial).first()

    if trial is None:
        return Response(status=404, data={"status": "Trial or Quiz do not exist"})

    id_answered_questions_id = [tq.question.id for tq in list(trial.questions.all())]

    available_questions = list(trial.quiz.questions.exclude(id__in=id_answered_questions_id))

    if len(available_questions) == 0:
        return Response(status=201, data={"trial_score": trial.calculate_score()})

    next_question = random.choice(available_questions)

    trial_question = TrialQuestion.objects.create(trial=trial,
                                                  question=next_question,
                                                  number=len(id_answered_questions_id)+1)

    return Response(status=201, data=TrialQuestionSerializer(trial_question).data)

# Questions?
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def get_next_question_old(request, quiz_num, num_trial):
    # trial = get_object_or_404(Trial, quiz__number=quiz_num, quiz__user=request.user, number=num_trial)
    trial = Trial.objects.select_for_update().filter(quiz__number=quiz_num,
                                                     quiz__user=request.user,
                                                     number=num_trial).first()

    if trial is None:
        return Response(status=404, data={"status": "Trial or Quiz do not exist"})

    id_answered_questions_id = [tq.question.id for tq in list(trial.questions.all())]

    available_questions = list(trial.quiz.questions.exclude(id__in=id_answered_questions_id))

    if len(available_questions) == 0:
        user_updated_score = quiz_controller.calculate_user_score(request.user)
        profile = request.user.profile
        profile.points = user_updated_score
        profile.save()
        return Response(status=201, data={"trial_score": trial.calculate_score()})

    next_question = random.choice(available_questions)

    trial_question = TrialQuestion.objects.create(trial=trial,
                                                  question=next_question,
                                                  number=len(id_answered_questions_id)+1)

    return Response(status=201, data=TrialQuestionSerializer(trial_question).data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def get_next_question(request, quiz_num, num_trial):
    # trial = get_object_or_404(Trial, quiz__number=quiz_num, quiz__user=request.user, number=num_trial)
    trial = Trial.objects.select_for_update().filter(quiz__number=quiz_num,
                                                     quiz__user=request.user,
                                                     number=num_trial).first()

    if trial is None:
        return Response(status=404, data={"status": "Trial or Quiz do not exist"})

    next_question = trial.questions.select_for_update().filter(accessed=False).first()

    if next_question is None:
        user_updated_score = quiz_controller.calculate_user_score(request.user)
        profile = request.user.profile
        profile.points = user_updated_score
        profile.save()
        return Response(status=201, data={"trial_score": trial.calculate_score()})

    next_question.accessed = True
    next_question.save()

    return Response(status=201, data=TrialQuestionSerializer(next_question).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def answer_question(request, quiz_num, num_trial, question_num):
    # Acquire lock
    trial_question = TrialQuestion.objects.select_for_update().filter(trial__quiz__number=quiz_num,
                                                                      trial__quiz__user=request.user,
                                               trial__number=num_trial,
                                               number=question_num).first()
    if trial_question is None:
        return Response(status=404, data={"status": "Trial does not exist"})

    if trial_question.answer:
        return Response(status=400, data={"status": "Question already answered"})

    if not trial_question.accessed:
        return Response(status=400, data={"status": "Question has not accessed"})

    # TODO check if timed from question
    is_timed = True
    if is_timed:
        today = datetime.now(timezone.utc)
        time_delta = today - trial_question.access_time
        if time_delta.total_seconds() > ANSWER_TIME:
            return Response(status=400, data={"status": "Answer time has expired"})

    answer_serializer = AnswerSerializer(data=request.data)
    if answer_serializer.is_valid():
        # TODO optimize
        question_choices = trial_question.question.choices.all()
        answer_choices = answer_serializer.validated_data["choices"]
        for choice in answer_choices:
            if choice not in question_choices:
                return Response(status=400, data={"status": "Invalid answer"})
        answer = answer_serializer.save(choices=answer_choices)
        trial_question.answer = answer
        trial_question.save()
        return Response(status=201)
    else:
        return Response(status=400, data={"status": "Invalid body"})
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
