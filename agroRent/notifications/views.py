from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from notifications.models import NotificationCategory, Notification, FCMToken
from notifications.serializers import (
    NotificationCategorySerializer, NotificationSerializer, FCMTokenSerializer
)
from drf_spectacular.utils import extend_schema, OpenApiResponse

class NotificationCategoryListView(generics.ListCreateAPIView):
    queryset = NotificationCategory.objects.all()
    serializer_class = NotificationCategorySerializer

class NotificationListView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'is_read']

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or self.request.user.is_anonymous:
            return Notification.objects.none()
        if self.request.user.is_staff:
            return Notification.objects.all().order_by('-created_at')
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class MarkNotificationReadView(APIView):
    @extend_schema(
        responses={200: OpenApiResponse(description="Notification marked as read")},
        description="Mark a specific notification as read"
    )
    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
            notification.is_read = True
            notification.save()
            return Response({"status": "read"}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

class FCMTokenUpdateView(generics.CreateAPIView):
    serializer_class = FCMTokenSerializer

    def perform_create(self, serializer):
        token = serializer.validated_data['token']
        # Update if exists or create new
        FCMToken.objects.update_or_create(
            user=self.request.user,
            token=token,
            defaults={'token': token}
        )

class UnreadNotificationCountView(APIView):
    @extend_schema(
        responses={200: OpenApiResponse(description="Count of unread notifications")},
        description="Get the total count of unread notifications for the current user"
    )
    def get(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({"unread_count": count}, status=status.HTTP_200_OK)
