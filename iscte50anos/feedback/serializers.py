from rest_framework import serializers

from feedback.models import TimelinePoll


class TimelinePollSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelinePoll
        fields = '__all__'
