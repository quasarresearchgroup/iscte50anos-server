from rest_framework import serializers

from spots.models import Spot


class SpotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spot
        fields = ['description', 'location_photo_link']


