
from rest_framework import serializers


class SocialSerializer(serializers.Serializer):

    # Serializer which accepts an OAuth2 access token and provider.
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)