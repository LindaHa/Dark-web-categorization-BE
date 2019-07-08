from rest_framework import serializers
from .models import Page, Component, Link


class LinkSerializer(serializers.Serializer):
    link = serializers.CharField()
    name = serializers.CharField()

    def create(self, validated_data):
        return Link(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance


class PageSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    url = serializers.CharField()
    content = serializers.CharField()
    links = LinkSerializer(many=True)
    title = serializers.CharField()

    def create(self, validated_data):
        return Page(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance


class ComponentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    links = LinkSerializer(many=True)
    members = PageSerializer(many=True)

    def create(self, validated_data):
        return Component(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance
