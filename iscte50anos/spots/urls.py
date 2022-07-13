from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('<uuid:uuid>', views.access_qrcode),
    path('', views.get_spot_list),
]
