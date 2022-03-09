from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response

from events.models import Event
from events.serializers import EventSerializer


def get_all_events(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(data=serializer.data)
