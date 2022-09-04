from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_content),
    path('content_id', views.get_content_id),
    path('<content_lower_id>-<content_upper_id>', views.get_content_within_id_limits),
]
