from rest_framework import serializers
from .models import Post, Hashtag
from django.contrib.auth import get_user_model

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

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        self._process_hashtags(post)
        self._process_mentions(post)
        return post

    def _process_hashtags(self, post):
        for tag in post.extract_hashtags():
            hashtag, _ = Hashtag.objects.get_or_create(name=tag.lower())
            post.hashtags.add(hashtag)

    def _process_mentions(self, post):
        for username in post.extract_mentions():
            try:
                user = User.objects.get(username=username)
                post.mentions.add(user)
            except User.DoesNotExist:
                pass