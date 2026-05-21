from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, feed_view

router = DefaultRouter()
router.register(r'', PostViewSet, basename='post')

urlpatterns = [
    path('feed/', feed_view, name='feed'),
    path('', include(router.urls)),
]