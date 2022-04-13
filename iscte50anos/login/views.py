from django.conf import settings

import requests
from rest_framework.authtoken.admin import User

from rest_framework.decorators import api_view

from login.serializers import SocialSerializer
from rest_framework.response import Response

from users.models import Profile
from rest_framework.authtoken.models import Token



@api_view(['POST'])
# Exchange OAuth2 access token by an in-house access token
# If the access token is valid and the user is not registered, it will be registered
def exchange_access_token(request):
    token_serializer = SocialSerializer(data=request.data)
    if token_serializer.is_valid():
        access_token = token_serializer.validated_data["access_token"]

        profile_response = requests.get('https://login.iscte-iul.pt/oauth2/v1/userinfo',
                                headers={'Authorization': f'Bearer {access_token}'})

        if profile_response.status_code != 200:
            return Response(status=profile_response.status_code)
        else:
            profile_data = profile_response.json()

            try:
                user = User.objects.get(username=profile_data["preferred_username"])
            except User.DoesNotExist:
                user = User.objects.create(username=profile_data["preferred_username"],
                                           first_name=profile_data["given_name"],
                                           last_name=profile_data["family_name"])
                # TODO Get affiliation
                profile = Profile.objects.create(user=user)

            token = Token.objects.get_or_create(user=user)
            return Response(data={"access_token": token[0].key})

    else:
        return Response(status=400) # Bad request (invalid serializer)


@api_view(['POST'])
def openday_login(request):
    pass