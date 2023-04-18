from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from . import views

# Quizzes endpoint

urlpatterns = [
    path('', views.get_user_quiz_list),
    path('<int:quiz_num>/trials', views.start_quiz_trial), # Create new trial
    path('<int:quiz_num>/trials/<int:num_trial>/next_question', views.get_next_question), # Get next question
    path('<int:quiz_num>/trials/<int:num_trial>/', views.get_trial), # Get next question
    path('<int:quiz_num>/trials/<int:num_trial>/questions/<int:question_num>/answer', views.answer_question),
]