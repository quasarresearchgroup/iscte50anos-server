from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('profile', views.get_profile),
    path('leaderboard', views.get_leaderboard),
    path('relative-leaderboard', views.get_relative_leaderboard),
]
