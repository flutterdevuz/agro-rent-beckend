import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class NotificationCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('name'), max_length=100)

    class Meta:
        verbose_name_plural = _('Notification Categories')

    def __str__(self):
        return self.name

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    category = models.ForeignKey(NotificationCategory, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'))
    is_read = models.BooleanField(_('is read'), default=False)
    status = models.CharField(_('status'), max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} for {self.user}"

class FCMToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fcm_tokens')
    token = models.TextField(_('FCM Token'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FCM Token for {self.user}"
