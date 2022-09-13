from datetime import date
import datetime
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from events.models import Event
from events.serializers import EventSerializer
from content.serializers import ContentSerializer
from topics.serializers import TopicSerializer


@api_view()
def get_all_events(request):

    topics = request.query_params.getlist("topic",None)
    if topics : 
        events  = Event.objects.filter( topics__id__in= topics)
    else:
        events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(data=serializer.data)

@api_view()
def get_event(request,event_id:int):
    event = Event.objects.get(id=event_id)
    serializer = EventSerializer(event , many=False)
    return Response(data=serializer.data)

@api_view()
def get_event_of_year(request,year:int,multiplier:int):
    event = Event.objects.filter(date__gte=datetime.date(year,1,1),date__lte = datetime.date(year+multiplier,12,31))
    serializer = EventSerializer(event , many=True)
    return Response(data=serializer.data)
    
@api_view()
def get_event_contents(request,event_id):
    contents = Event.objects.get(id=event_id).content.all()
    serializer = ContentSerializer(contents , many=True)
    return Response(data=serializer.data)

@api_view()
def get_event_topics(request,event_id):
    topics = Event.objects.get(id=event_id).topics.all()
    serializer = TopicSerializer(topics , many=True)
    return Response(data=serializer.data)
