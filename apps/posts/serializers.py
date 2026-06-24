from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Hashtag

User = get_user_model()


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'name']


class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar']


class PostSerializer(serializers.ModelSerializer):
    user = PostUserSerializer(read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    mentions = serializers.StringRelatedField(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'image',
                  'hashtags', 'mentions', 'likes_count', 'comments_count',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'hashtags', 'mentions',
                            'likes_count', 'comments_count',
                            'created_at', 'updated_at']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()