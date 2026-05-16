from django.urls import path
from notifications.views import (
    NotificationCategoryListView, NotificationListView, NotificationDetailView,
    MarkNotificationReadView, FCMTokenUpdateView,
    UnreadNotificationCountView
)

urlpatterns = [
    path('categories/', NotificationCategoryListView.as_view(), name='notification-category-list'),
    path('list/', NotificationListView.as_view(), name='notification-list'),
    path('list/<uuid:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('unread-count/', UnreadNotificationCountView.as_view(), name='notification-unread-count'),
    path('<uuid:pk>/read/', MarkNotificationReadView.as_view(), name='notification-read'),
    path('fcm-token/', FCMTokenUpdateView.as_view(), name='fcm-token-update'),
]
