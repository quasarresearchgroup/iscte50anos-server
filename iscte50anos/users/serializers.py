
from rest_framework import serializers

from users.models import Profile, Affiliation


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'username', 'num_spots_read', 'total_time']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'ranking', 'initials', 'num_spots_read', 'total_time']

class ProfileSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'level', 'points', 'affiliation_name', 'ranking',
                  'affiliation_ranking', 'initials', 'num_spots_read', 'total_time']


class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = "__all__"
