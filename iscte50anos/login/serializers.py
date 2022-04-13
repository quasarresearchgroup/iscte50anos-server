
from rest_framework import serializers


class SocialSerializer(serializers.Serializer):
    # Serializer which accepts an OAuth2 access token and provider.
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True, trim_whitespace=True)
    password = serializers.CharField(max_length=30, required=True)

class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True, trim_whitespace=True)
    email = serializers.EmailField()
    #affiliation =
    password = serializers.CharField(max_length=30, required=True)
    password_confirmation = serializers.CharField(max_length=30, required=True)