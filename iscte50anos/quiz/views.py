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

ANSWER_TIME = 45  # segundos
# QUIZ_SIZE = 5 # TODO change for experiences (8)


@api_view()
@permission_classes([IsAuthenticated])
def get_user_quiz_list(request):
    quizzes = Quiz.objects.filter(user=request.user).order_by("-number")
    return Response(data=QuizListSerializer(quizzes, many=True).data)


# Get and start quiz
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def start_quiz_trial(request, quiz_num):
    quiz = Quiz.objects.filter(user=request.user, number=quiz_num).select_for_update().first()
    if quiz is None:
        return Response(status=404, data={"status": "Quiz does not exist"})

    # Count trials for quiz
    trial_count = Trial.objects.filter(quiz=quiz).count()

    # Cannot create more trials
    # TODO already max score
    if trial_count >= 3:
        return Response(status=400, data={"status": "All available trials created"})  # Bad request

    new_trial = Trial.objects.create(quiz=quiz, number=trial_count + 1)

    quiz_controller.assign_trial_questions(request.user, new_trial, quiz.topics.all())

    # return Response(status=201, data={"trial_number": trial_count + 1, "quiz_size": QUIZ_SIZE})
    return Response(status=201, data={"trial_number": trial_count + 1, "quiz_size": new_trial.quiz_size()})


@api_view()
@permission_classes([IsAuthenticated])
def get_current_question_old(request, quiz_num, num_trial):
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
                                                  number=len(id_answered_questions_id) + 1)

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
                                                  number=len(id_answered_questions_id) + 1)

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

    if trial.is_completed:
        return Response(status=400, data={"status": "Trial is complete"})

    next_question = trial.questions.filter(accessed=False).select_related("question").first()

    if next_question is None:
        last_question = trial.questions.filter(number=QUIZ_SIZE).select_related("question").first()
        if not last_question.is_answered():
            return Response(status=201, data=TrialQuestionSerializer(last_question).data)

        trial.is_completed = True
        trial.save()

        user_updated_score = quiz_controller.calculate_user_score(request.user)
        profile = request.user.profile
        profile.points = user_updated_score
        profile.save()

        # Profile.objects.filter(user=request.user).update(points=user_updated_score)
        return Response(status=201, data={"trial_score": trial.score()})

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
                                                                      number=question_num).select_related(
        "question").first()
    if trial_question is None:
        return Response(status=404, data={"status": "Trial or Quiz do not exist"})

    if trial_question.answer:
        return Response(status=400, data={"status": "Question already answered"})

    if not trial_question.accessed:
        return Response(status=400, data={"status": "Question was not accessed"})

    is_timed = trial_question.question.is_timed()
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
        answer = answer_serializer.save(choices=answer_choices, trial_question=[trial_question])

        return Response(status=201)
    else:
        return Response(status=400, data={"status": "Invalid body"})
