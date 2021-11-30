from django.db.models import Avg
from rest_framework import serializers

from .models import MyUser
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class DiscussionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class DiscussionSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d/%m/%Y  %H:%M:%S', read_only=True)
    image = DiscussionImageSerializer(many=True, read_only=True)

    class Meta:
        model = Discussion
        exclude = ('author',)

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        discussion = Discussion.objects.create(**validated_data)
        return discussion

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['category'] = CategorySerializer(instance.category).data
        representation['images'] = DiscussionImageSerializer(instance.images.all(), many=True, context=self.context).data
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        representation['likes'] = instance.likes.all().count()
        representation['rating'] = instance.rating.aggregate(Avg('rating'))
        return representation


class ReplySerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d/%m/%Y  %H:%M:%S', read_only=True)

    class Meta:
        model = Reply
        exclude = ('author',)

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user.id
        validated_data['author_id'] = author
        reply = Reply.objects.create(**validated_data)
        return reply

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['discussion'] = DiscussionSerializer(instance.discussion).data
        representation['images'] = DiscussionImageSerializer(instance.images.all(), many=True, context=self.context).data

        return representation


class CommentSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d/%m/%Y  %H:%M:%S', read_only=True)

    class Meta:
        model = Comment
        exclude = ('author', )

    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(author=request.user, **validated_data)
        return comment

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        return representation


class FavoritesSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Favorites
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['discussion'] = instance.discussion.title
        return representation


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        exclude = ('author', )

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        discussion = validated_data.get('discussion')
        rating = Rating.objects.get_or_create(author=author, discussion=discussion)[0]
        rating.rating = validated_data['rating']
        rating.save()
        return rating


class LikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Likes
        exclude = ('author',)

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        discussion = validated_data.get('discussion')
        like = Likes.objects.get_or_create(author=author, discussion=discussion)[0]
        like.likes = True if like.likes is False else False
        like.save()
        return like

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        return representation
