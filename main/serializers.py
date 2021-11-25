from rest_framework import serializers

from .models import Category, Discussion, Image


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class DiscussionSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d/%m/%Y  %H:%M:%S', read_only=True)
    class Meta:
        model = Discussion
        fields = ('id', 'title', 'text', 'category', 'created', 'author')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = DiscussionImageSerializer(instance.images.all(), many=True, context=self.context).data
        return representation


class DiscussionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

