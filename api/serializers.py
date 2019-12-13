from rest_framework import serializers
from .models import Page, Link, Category, MetaGroup, PageDetails


class StringListField(serializers.ListField):
    child = serializers.CharField()


class LinkSerializer(serializers.Serializer):
    link = serializers.CharField()
    name = serializers.CharField()

    def create(self, validated_data):
        return Link(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    occurrence = serializers.IntegerField()

    def create(self, validated_data):
        return Category(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance


class PageSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    url = serializers.CharField()
    # commenting this out because it's too much data to send to the client's side
    # content = serializers.CharField()
    links = LinkSerializer(many=True)
    title = serializers.CharField()
    categories = CategorySerializer(many=True)

    def create(self, validated_data):
        return Page(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance


class MetaGroupSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    links = StringListField()
    first_members = PageSerializer(many=True)
    members_count = serializers.IntegerField()
    categories = CategorySerializer(many=True)

    def create(self, validated_data):
        return MetaGroup(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance


class PageDetailsSerializer(serializers.Serializer):
    url = serializers.CharField()
    title = serializers.CharField()
    category = serializers.CharField()
    content = serializers.CharField()
    links = StringListField()

    def create(self, validated_data):
        return PageDetails(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance
