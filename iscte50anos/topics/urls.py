from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_all_topics),
    path('<int:pk>', views.get_topic),
    # path('web/<int:pk>', views.get_topic_web),
    # path('web/<int:pk>/events', views.get_topic_web_events),
]
