from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect, get_object_or_404
from .models import User
from .serializers import RegisterSerializer, UserProfileSerializer, PublicUserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, username):
    try:
        target = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=404)

    if target == request.user:
        return Response({'error': 'No podés seguirte a vos mismo.'}, status=400)

    from apps.interactions.models import Notification

    if target in request.user.following.all():
        request.user.following.remove(target)
        Notification.objects.filter(
            user=target,
            actor=request.user,
            notification_type=Notification.FOLLOW
        ).delete()
        return Response({'status': 'dejaste de seguir'})
    else:
        request.user.following.add(target)
        Notification.objects.create(
            user=target,
            actor=request.user,
            notification_type=Notification.FOLLOW
        )
        return Response({'status': 'siguiendo'})


class FollowersList(generics.ListAPIView):
    serializer_class = PublicUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return user.followers.all()


class FollowingList(generics.ListAPIView):
    serializer_class = PublicUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return user.following.all()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def suggest_users(request):
    following = request.user.following.all()
    users = User.objects.exclude(
        id__in=[request.user.id] + [u.id for u in following]
    )[:5]
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_session_token(request):
    refresh = RefreshToken.for_user(request.user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })


def logout_user(request):
    django_logout(request)
    return redirect('/accounts/login/')