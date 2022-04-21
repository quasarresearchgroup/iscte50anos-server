
from rest_framework import serializers

from users.models import Profile


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['',  'points']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'level', 'points', 'affiliation_name', 'ranking', 'affiliation_ranking', 'initials']


class AffiliationSerializer(serializers.ModelSerializer):
    pass