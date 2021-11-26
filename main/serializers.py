from rest_framework import serializers

from .models import Category, Discussion, Image, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class DiscussionSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d/%m/%Y  %H:%M:%S', read_only=True)

    class Meta:
        model = Discussion
        fields = ('id', 'title', 'text', 'category', 'created')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user.id
        validated_data['author_id'] = user
        discussion = Discussion.create(**validated_data)
        return discussion

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['category'] = CategorySerializer(instance.category).data
        representation['images'] = DiscussionImageSerializer(instance.images.all(), many=True, context=self.context).data
        return representation


class DiscussionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d/%m/%Y  %H:%M:%S', read_only=True)
    class Meta:
        model = Comment
        fields = ('discussion', 'comment', 'user')

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        comment = Comment.objects.create(author=author, **validated_data)
        return comment

