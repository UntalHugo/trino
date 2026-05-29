from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.posts.models import Post, Hashtag
from apps.posts.serializers import PostSerializer
from apps.users.models import User
from apps.users.serializers import UserProfileSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_view(request):
    query = request.query_params.get('q', '').strip()

    if not query:
        return Response({'error': 'Escribí algo para buscar.'}, status=400)

    posts = Post.objects.filter(
        content__icontains=query
    ).select_related('user')

    users = User.objects.filter(
        username__icontains=query
    )

    hashtags = Hashtag.objects.filter(
        name__icontains=query.replace('#', '')
    )

    return Response({
        'posts': PostSerializer(posts, many=True).data,
        'users': UserProfileSerializer(users, many=True).data,
        'hashtags': [f"#{h.name}" for h in hashtags],
    })