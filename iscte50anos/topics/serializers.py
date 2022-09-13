from rest_framework import serializers

from topics.models import Topic

from content.serializers import ContentSerializer


class TopicSerializer(serializers.ModelSerializer):
    content = ContentSerializer(many=True, read_only=True,)

    class Meta:
        model = Topic
        fields = ['id', 'title', 'content']


class TopicQRSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ['title',  'id']



