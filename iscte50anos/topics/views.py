from django.db import transaction
from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from events.serializers import EventSerializer
from topics.models import Topic, TopicAccess
from quiz.models import Trial

from topics.serializers import TopicSerializer

from _controllers import quiz_controller


@api_view()
@permission_classes([IsAuthenticated])
def get_topic(request, pk):
    topic = Topic.objects.filter(id=pk).first()
    if not topic:
        return Response(status=404, data={"status": "The requested topic does not exist"})
    if topic.title == "Georeferenciação":
        return Response(status=400, data={"status": "The requested topic cannot be accessed"})

    is_first_access = not TopicAccess.objects.filter(user=request.user, topic=topic).exists()
    if is_first_access:
        has_completed_latest_quiz = Trial.objects.filter(is_completed=True,
                                                         quiz__number=request.user.profile.level).exists()
        print(Trial.objects.filter(is_completed=True, quiz__number=request.user.profile.level))
        print(request.user.profile.level)
        if not has_completed_latest_quiz and request.user.profile.level != 0:
            return Response(status=400, data={"status": "The quiz for this level was not completed"})

        with transaction.atomic():
            TopicAccess.objects.create(user=request.user, topic=topic)
            quiz_controller.update_level(request.user)

    serializer = TopicSerializer(topic)
    return Response(serializer.data)


# Read Topic
# Create Topic Access for the authenticated user (if does not exist)
# Create quiz for number of accessed topics
# Make available to user (if previous quizes were answered)

@api_view()
def get_all_topics(request):
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return Response(data=serializer.data)

# @api_view()
# def get_topic_web(request,pk):
#     topic = Topic.objects.get(id=pk)
#     serializer = TopicSerializer(topic, many=False)
#     return Response(data=serializer.data)

# @api_view()
# def get_topic_web_events(request,pk):
#     events = Topic.objects.get(id=pk).events
#     serializer = EventSerializer(events, many=True)
#     return Response(data=serializer.data)
