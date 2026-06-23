from django.urls import path
from .views import RegisterView, ProfileView, follow_user, suggest_users, get_session_token, logout_user

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<str:username>/', follow_user, name='follow'),
    path('suggestions/', suggest_users, name='suggest-users'),
    path('session-token/', get_session_token, name='session-token'),
    path('logout/', logout_user, name='logout'),
]