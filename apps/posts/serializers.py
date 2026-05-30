from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Hashtag

User = get_user_model()


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    mentions = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'image',
                  'hashtags', 'mentions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'hashtags', 'mentions',
                            'created_at', 'updated_at']