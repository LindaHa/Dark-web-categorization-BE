from rest_framework import serializers
from .models import Page


class PageSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    url = serializers.CharField()
    content = serializers.CharField()
    links = serializers.StringRelatedField(many=True)
    title = serializers.CharField()

    def create(self, validated_data):
        return Page(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance