
from rest_framework import serializers

from users.models import Profile


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['' ,  'points']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'level', 'points', 'affiliation']
