from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from . import views

# Quizzes endpoint

urlpatterns = [
    path('', views.get_user_quiz_list),
    # TODO register quiz start and answer
]