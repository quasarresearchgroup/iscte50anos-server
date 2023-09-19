from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.exchange_access_token),
    path('signup', views.nei_signup),
    path('login', views.openday_login),
    path('logout', views.openday_logout),
]