from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Like, Comment, Message, Notification

User = get_user_model()

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # ─── CAMBIO AQUÍ: Agregamos 'first_name' para que viaje en los posts, comentarios, etc. ───
        fields = ['id', 'username', 'first_name', 'avatar']


class LikeSerializer(serializers.ModelSerializer):
    # Si preferís que el like use el serializer completo en vez de un string plano:
    # user = UserBasicSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    # Cambiamos StringRelatedField por UserBasicSerializer para que en los comentarios también salga el apodo
    user = UserBasicSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'post', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserBasicSerializer(read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        required=False
    )
    receiver_info = UserBasicSerializer(source='receiver', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'receiver_info', 'content', 'read', 'created_at']
        read_only_fields = ['id', 'sender', 'receiver_info', 'read', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    actor = UserBasicSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'notification_type', 'read', 'created_at']
        read_only_fields = ['id', 'actor', 'notification_type', 'created_at']