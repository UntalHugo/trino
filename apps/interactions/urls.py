from django.urls import path
from .views import (
    toggle_like, CommentListCreateView,
    MessageListCreateView, NotificationListView,
    mark_notifications_read, mark_messages_read
)

urlpatterns = [
    path('posts/<int:post_id>/like/', toggle_like, name='toggle-like'),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comments'),
    path('messages/', MessageListCreateView.as_view(), name='messages'),
    path('messages/read/', mark_messages_read, name='messages-read'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/read/', mark_notifications_read, name='notifications-read'),
]