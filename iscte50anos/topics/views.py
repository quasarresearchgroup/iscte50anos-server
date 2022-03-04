from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from topics.models import Topic, TopicAccess

from topics.serializers import TopicSerializer

from __utils import quiz_utils


@api_view()
@permission_classes([IsAuthenticated])
def get_topic(request, pk):
    topic = Topic.objects.get(id=pk)
    is_first_access = not TopicAccess.objects.filter(user=request.user, topic=topic).exists()
    if is_first_access:
        # TODO Validate answered quizzes from previous level
        TopicAccess.objects.create(user=request.user, topic=topic)
        quiz_utils.update_level(request.user)

    serializer = TopicSerializer(topic)
    return Response(serializer.data)


# Read Topic
# Create Topic Access for the authenticated user (if does not exist)
# Create quiz for number of accessed topics
# Make available to user (if previous quizes were answered)