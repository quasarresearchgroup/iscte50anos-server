from rest_framework import serializers

from topics.models import Topic

from content.serializers import ContentSerializer


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ['id', 'title']


class TopicQRSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ['title',  'id']



