from rest_framework import viewsets, permissions, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Post
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]  # ← agregado
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def get_queryset(self):
        qs = Post.objects.select_related('user').all()
        username = self.request.query_params.get('username')
        if username:
            qs = qs.filter(user__username=username)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='feed')
    def feed(self, request):
        following = request.user.following.all()
        posts = Post.objects.filter(
            user__in=following
        ).select_related('user').order_by('-created_at')
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def liked(self, request):
        username = request.query_params.get('username')
        if username:
            user = get_object_or_404(User, username=username)
        else:
            user = request.user
        qs = Post.objects.filter(likes__user=user).select_related('user').order_by('-created_at')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)