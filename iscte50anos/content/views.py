from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view


@api_view()
def get_content(request):
    pass