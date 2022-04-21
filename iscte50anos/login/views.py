from django.conf import settings

import requests
from rest_framework.authtoken.admin import User

from rest_framework.decorators import api_view

from login.serializers import SocialSerializer, SignupSerializer, LoginSerializer
from rest_framework.response import Response

from users.models import Profile, Affiliation
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate



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
            return Response(data={"api_token": token[0].key})

    else:
        return Response(status=400) # Bad request (invalid serializer)


@api_view(['POST'])
def openday_login(request):
    login_serializer = LoginSerializer(data=request.data)
    if login_serializer.is_valid():
        user = authenticate(username=login_serializer.validated_data["username"],
                            password=login_serializer.validated_data["password"])
        if user is not None:
            return Response({"message": f"Login bem sucedido: {user.username}",
                             "api_token": Token.objects.get_or_create(user=user)[0].key})
        else:
            return Response({"message": "Credenciais inválidas"}, status=400)
    else:
        return Response(status=400)


@api_view(['POST'])
def openday_signup(request):
    signup_serializer = SignupSerializer(data=request.data)
    if signup_serializer.is_valid():

        username = signup_serializer.validated_data["username"]
        email = signup_serializer.validated_data["email"]
        if User.objects.filter(username=username).exists():
            return Response(data={"message": "O username já existe"}, status=400)
        if User.objects.filter(email=email).exists():
            return Response(data={"message": "O email já está registado numa conta"}, status=400)

        affiliation_name = signup_serializer.validated_data["affiliation_name"]
        affiliation_type = signup_serializer.validated_data["affiliation_type"]

        password = signup_serializer.validated_data["password"]
        password_confirmation = signup_serializer.validated_data["password_confirmation"]
        if password != password_confirmation:
            return Response(data={"message":"As palavras-passe não coincidem"}, status=400)

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        affiliation = Affiliation.objects.get_or_create(type=affiliation_type, name=affiliation_name)[0]
        profile = Profile.objects.create(user=user, affiliation=affiliation)

        token = Token.objects.get_or_create(user=user)
        return Response(data={"message":"Perfil criado com sucesso", "api_token": token[0].key})

    else:
        return Response(status=400) # Bad request (invalid serializer)
