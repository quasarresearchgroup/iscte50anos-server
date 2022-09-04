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

