from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_all_events),
    path('<int:event_id>', views.get_event),
    path('<int:event_id>/contents', views.get_event_contents),
    path('<int:event_id>/topics', views.get_event_topics),
    path('year/<int:year>', views.get_event_of_year),
    path('years', views.get_years_list),
]