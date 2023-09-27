from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from . import views

# Quizzes endpoint

urlpatterns = [
    path('<int:spot_id>', views.submit_puzzle),
]