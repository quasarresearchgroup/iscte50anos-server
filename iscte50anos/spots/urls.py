from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('<uuid:uuid>', views.access_qrcode),
    # path('permit', views.get_or_create_permit),
]
