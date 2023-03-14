import requests
from django.db import transaction
from rest_framework.authtoken.admin import User

from rest_framework.decorators import api_view, permission_classes

from login.serializers import SocialSerializer, SignupSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Profile, Affiliation
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate

from _controllers import quiz_controller


def create_user(profile_data):
    user = User.objects.create(username=profile_data["upn"],
                               email=profile_data["upn"],
                               first_name=profile_data["givenName"],
                               last_name=profile_data["familyName"])

    affiliation = Affiliation.objects.get_or_create(title=profile_data["title"],
                                                    department=profile_data["department"])[0]
    profile = Profile.objects.create(user=user, affiliation=affiliation)
    #quiz_controller.create_first_quiz(user)

    return user