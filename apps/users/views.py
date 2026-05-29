from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import User
from .serializers import RegisterSerializer, UserProfileSerializer

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

    if target in request.user.following.all():
        request.user.following.remove(target)
        return Response({'status': 'dejaste de seguir'})
    else:
        request.user.following.add(target)
        return Response({'status': 'siguiendo'})