from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('api/posts/', include('apps.posts.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('api/search/', include('apps.search.urls')),
    path('api/', include('apps.interactions.urls')),
    path('feed/', TemplateView.as_view(template_name='feed.html'), name='feed'),
    path('search/', TemplateView.as_view(template_name='search.html'), name='search'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('notifications/', TemplateView.as_view(template_name='notifications.html'), name='notifications-page'),
    path('messages/', TemplateView.as_view(template_name='messages.html'), name='messages-page'),
    path('post/<int:pk>/', TemplateView.as_view(template_name='post_detail.html'), name='post-detail'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='django-login'),
    path('auth/complete/', TemplateView.as_view(template_name='oauth_complete.html'), name='oauth-complete'),
path('api/auth/logout/', TokenBlacklistView.as_view(), name='logout'),
    path('register/', TemplateView.as_view(template_name='registration/register.html'), name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)