from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.select_related('user').all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def feed_view(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(
        user__in=following_users
    ).select_related('user').order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)