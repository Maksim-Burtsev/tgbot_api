from rest_framework import serializers


class PostSerializer(serializers.Serializer):
    url = serializers.CharField()
    votes = serializers.CharField()
    views = serializers.CharField()