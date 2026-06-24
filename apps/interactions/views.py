from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Like, Comment, Message, Notification
from .serializers import LikeSerializer, CommentSerializer, MessageSerializer, NotificationSerializer
from apps.posts.models import Post


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_like(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post no encontrado.'}, status=404)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
        return Response({'status': 'unliked', 'likes_count': post.likes.count()})
    return Response({'status': 'liked', 'likes_count': post.likes.count()})


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        try:
            post = Post.objects.get(id=self.kwargs['post_id'])
        except Post.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound('Post no encontrado.')
        serializer.save(user=self.request.user, post=post)


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        sent = Message.objects.filter(sender=user)
        received = Message.objects.filter(receiver=user)
        return (sent | received).order_by('-created_at')

    def perform_create(self, serializer):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        username = self.request.data.get('receiver_username')
        if username:
            try:
                receiver = User.objects.get(username=username)
            except User.DoesNotExist:
                from rest_framework.exceptions import NotFound
                raise NotFound('Usuario no encontrado.')
            serializer.save(sender=self.request.user, receiver=receiver)
        else:
            serializer.save(sender=self.request.user)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).order_by('-created_at')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notifications_read(request):
    Notification.objects.filter(user=request.user, read=False).update(read=True)
    return Response({'status': 'notificaciones marcadas como leídas'})