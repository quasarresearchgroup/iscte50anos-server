from django.conf import settings

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

from _controllers import users_controller

# PROFANITY FILTER REVIEW
with open('profane_words.txt') as f:
    curse_words = f.read().splitlines()
    curse_words = [s.lower() for s in curse_words]


def is_profane(str):
    str_low = str.lower()
    for word in curse_words:
        if word in str_low:
            return True
    return False


@api_view(['POST'])
@transaction.atomic
# Exchange OAuth2 access token by an in-house access token
# If the access token is valid and the user is not registered, it will be registered
def exchange_access_token(request):
    token_serializer = SocialSerializer(data=request.data)
    if token_serializer.is_valid():
        access_token = token_serializer.validated_data["access_token"]

        #proxies = {"https": "tostas"}
        profile_response = requests.get('https://login.iscte-iul.pt/oauth2/ausyeqjx8GS8Nj1Y9416/v1/userinfo',
                                headers={'Authorization': f'Bearer {access_token}'},)
                                        #proxies=proxies)

        if profile_response.status_code != 200:
            return Response(status=profile_response.status_code)
        else:
            profile_data = profile_response.json()

            try:
                user = User.objects.get(username=profile_data["preferred_username"])
            except User.DoesNotExist:
                user = users_controller.create_user(profile_data)

            Token.objects.filter(user=user).delete()
            user_token = Token.objects.create(user=user).key
            return Response(status=200, data={"api_token": user_token})

    else:
        return Response(status=400) # Bad request (invalid serializer)


@api_view(['POST'])
@transaction.atomic
def openday_login(request):
    login_serializer = LoginSerializer(data=request.data)
    if login_serializer.is_valid():
        user = authenticate(username=login_serializer.validated_data["username"],
                            password=login_serializer.validated_data["password"])
        if user is not None:
            profile = Profile.objects.select_for_update().filter(user=user).first()

            #if profile.is_logged:
                #return Response({"message": "O utilizador já efetuou Login"})

            #profile.is_logged = True

            Token.objects.filter(user=user).delete()
            user_token = Token.objects.create(user=user).key

            #profile.save()

            return Response({"message": f"Login bem sucedido: {user.username}",
                             "api_token": user_token})
        else:
            return Response({"message": "Credenciais inválidas"}, status=400)
    else:
        return Response({"message": "Pedido inválido"}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def openday_logout(request):
    profile = Profile.objects.select_for_update().filter(user=request.user).first()

    #if not profile.is_logged:
        #return Response({"message": "Logout já efetuado"}, status=400)

    #profile.is_logged = False

    Token.objects.filter(user=request.user).delete()
    #profile.save()

    return Response({"message": "Logout bem sucedido"}, status=200)


@api_view(['POST'])
@transaction.atomic
def openday_signup(request):
    signup_serializer = SignupSerializer(data=request.data)
    if signup_serializer.is_valid():

        # VALIDATION
        username = signup_serializer.validated_data["username"]
        email = signup_serializer.validated_data["email"]
        if User.objects.filter(username=username).exists():
            return Response(data={"message": "O username já existe", "code": 1}, status=400)
        if User.objects.filter(email=email).exists():
            return Response(data={"message": "O email já está registado numa conta", "code": 2}, status=400)

        password = signup_serializer.validated_data["password"]
        password_confirmation = signup_serializer.validated_data["password_confirmation"]
        if password != password_confirmation:
            return Response(data={"message": "As palavras-passe não coincidem", "code": 3}, status=400)

        first_name = signup_serializer.validated_data["first_name"]
        last_name = signup_serializer.validated_data["last_name"]

        '''
        affiliation_name = signup_serializer.validated_data["affiliation_name"]
        affiliation_type = signup_serializer.validated_data["affiliation_type"]

        try:
            affiliation = Affiliation.objects.get(subtype=affiliation_type, name=affiliation_name)
        except Affiliation.DoesNotExist:
            return Response(data={"message": "Afiliação Inválida", "code": 4}, status=400)
        '''

        # SUCCESS
        try:
            user = User(username=username, first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            user.save()
            profile = Profile.objects.create(user=user, )#affiliation=affiliation)
            token = Token.objects.get_or_create(user=user)
            return Response(data={"message": "Perfil criado com sucesso", "api_token": token[0].key})
        except Exception as e:
            return Response(data={"message": "Erro a criar utilizador. Tentar novamente.", "code": 6}, status=500)

    else:
        return Response(data={"message": "Email inválido", "code": 5}, status=400) # Bad request (invalid serializer)


@api_view(['POST'])
@transaction.atomic
def nei_signup(request):
    signup_serializer = SignupSerializer(data=request.data)
    if signup_serializer.is_valid():

        # VALIDATION
        username = signup_serializer.validated_data["username"]
        if User.objects.filter(username=username).exists():
            return Response(data={"message": "O username já existe", "code": 1}, status=400)

        if is_profane(username):
            return Response(data={"message": "O username é inválido", "code": 10}, status=400)

        password = signup_serializer.validated_data["password"]
        password_confirmation = signup_serializer.validated_data["password_confirmation"]
        if password != password_confirmation:
            return Response(data={"message": "As palavras-passe não coincidem", "code": 3}, status=400)

        '''
        affiliation_name = signup_serializer.validated_data["affiliation_name"]
        affiliation_type = signup_serializer.validated_data["affiliation_type"]

        try:
            affiliation = Affiliation.objects.get(subtype=affiliation_type, name=affiliation_name)
        except Affiliation.DoesNotExist:
            return Response(data={"message": "Afiliação Inválida", "code": 4}, status=400)
        '''

        # SUCCESS
        try:
            user = User(username=username)
            user.set_password(password)
            user.save()
            profile = Profile.objects.create(user=user, )#affiliation=affiliation)
            token = Token.objects.get_or_create(user=user)
            return Response(data={"message": "Perfil criado com sucesso", "api_token": token[0].key})
        except Exception as e:
            return Response(data={"message": "Erro a criar utilizador. Tentar novamente.", "code": 6}, status=500)

    else:
        return Response(data={"message": "Email inválido", "code": 5}, status=400) # Bad request (invalid serializer)