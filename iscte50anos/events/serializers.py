from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    num_content = serializers.IntegerField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'scope', 'date', 'num_content']
