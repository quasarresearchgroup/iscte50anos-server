from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('<uuid:uuid>', views.get_topic),
]
