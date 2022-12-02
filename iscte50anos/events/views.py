from datetime import date
import datetime

from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from events.models import Event
from events.serializers import EventSerializer
from content.serializers import ContentSerializer
from topics.serializers import TopicSerializer

from _controllers.log_controller import save_log


@api_view()
def get_all_events(request):
    save_log(request)
    topics = request.query_params.getlist("topic")
    scopes = request.query_params.getlist("scope")
    if topics and scopes:
        events = Event.objects.filter(topics__id__in=topics, scope__in=scopes)
    elif topics:
        events = Event.objects.filter(topics__id__in=topics)
    elif scopes:
        events = Event.objects.filter(scope__in=scopes)
    else:
        events = Event.objects.all()

    events = events.annotate(num_content=Count("content"))

    serializer = EventSerializer(events, many=True)
    return Response(data=serializer.data)

@api_view()
def get_event(request, event_id: int):
    save_log(request)
    event = Event.objects.filter(id=event_id)
    event = event.annotate(num_content=Count("content"))[0]
    serializer = EventSerializer(event, many=False)
    return Response(data=serializer.data)

@api_view()
def get_event_of_year(request, year: int):
    save_log(request)
    event = Event.objects.filter(date__year=year)
    event = event.annotate(num_content=Count("content"))
    serializer = EventSerializer(event, many=True)
    return Response(data=serializer.data)
    
@api_view()
def get_event_contents(request, event_id):
    save_log(request)
    contents = Event.objects.get(id=event_id).content.all()
    serializer = ContentSerializer(contents, many=True)
    return Response(data=serializer.data)

@api_view()
def get_event_topics(request, event_id):
    save_log(request)
    topics = Event.objects.get(id=event_id).topics.all()
    serializer = TopicSerializer(topics, many=True)
    return Response(data=serializer.data)

@api_view()
def get_years_list(request):
    dates = Event.objects.dates("date", "year")
    return Response(data=dates)
