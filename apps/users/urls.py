from django.urls import path
from .views import RegisterView, ProfileView, follow_user

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<str:username>/', follow_user, name='follow'),
]