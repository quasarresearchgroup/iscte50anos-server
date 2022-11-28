from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view

from feedback.serializers import TimelinePollSerializer
from rest_framework.response import Response


@api_view(['POST'])
def submit_timeline_poll(request):
    timeline_poll_serializer = TimelinePollSerializer(data=request.data)
    if timeline_poll_serializer.is_valid():
        created_poll = timeline_poll_serializer.save()
        return Response(data={"message": "Sugestão submetida com sucesso"}, status=201)
    else:
        return Response(data={"message": "Input inválido", "code": 1}, status=400) # Bad request (invalid serializer)