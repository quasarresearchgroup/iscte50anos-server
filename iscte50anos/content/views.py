from importlib.resources import contents
from rest_framework.response import Response
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view

from content.models import Content
from content.serializers import ContentSerializer


@api_view()
def get_content(request):
    contents = Content.objects.all()
    serializer = ContentSerializer(contents , many=True)
    return Response(data=serializer.data)

@api_view()
def get_content_within_id_limits(request,content_lower_id:int,content_upper_id:int):
    contents = Content.objects.filter(id__gte=content_lower_id,id__lte =content_upper_id )
    serializer = ContentSerializer(contents , many=True)
    return Response(data=serializer.data)

@api_view()
def get_content_id(request,content_id:int):
    contents = Content.objects.filter(id=content_id )
    serializer = ContentSerializer(contents , many=False)
    return Response(data=serializer.data)



