from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from topics.models import Topic, TopicAccess

from topics.serializers import TopicSerializer

from _controllers import quiz_controller

from qrcode.models import QRCode, QRCodeAccess

from qrcode.serializers import QRCodeSerializer


@api_view()
@permission_classes([IsAuthenticated])
def get_qrcode_link(request, uuid):
    qrcode = QRCode.objects.get(uuid=uuid),
    is_first_access = not QRCodeAccess.objects.filter(user=request.user, qrcode__uuid=uuid).exists()
    if is_first_access:
        # TODO Validate answered quizzes from previous level
        TopicAccess.objects.create(user=request.user, qrcode=qrcode)

    serializer = QRCodeSerializer(qrcode)
    return Response(serializer.data)


# Read Topic
# Create Topic Access for the authenticated user (if does not exist)
# Create quiz for number of accessed topics
# Make available to user (if previous quizes were answered)