from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification
from notifications.utils import send_push_notification

@receiver(post_save, sender=Notification)
def trigger_push_notification(sender, instance, created, **kwargs):
    if created:
        try:
            send_push_notification(
                user=instance.user,
                title=instance.title,
                body=instance.description,
                data={
                    "category": instance.category.name,
                    "status": instance.status or "",
                    "notification_id": str(instance.id)
                }
            )
        except Exception as e:
            print(f"Failed to send push notification: {e}")
