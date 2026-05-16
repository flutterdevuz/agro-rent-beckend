from rest_framework import serializers
from notifications.models import NotificationCategory, Notification, FCMToken
from agroRent.utils.mixins import TranslatableSerializerMixin

class NotificationCategorySerializer(TranslatableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = NotificationCategory
        fields = '__all__'
        translatable_fields = ['name']

class NotificationSerializer(TranslatableSerializerMixin, serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('created_at',)
        translatable_fields = ['title', 'description']

class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMToken
        fields = ('token',)
