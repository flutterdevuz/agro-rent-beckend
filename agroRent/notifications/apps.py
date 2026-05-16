from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'notifications'

    def ready(self):
        import notifications.signals
        from notifications.utils import initialize_firebase
        try:
            initialize_firebase()
        except Exception as e:
            print(f"Firebase initialization failed: {e}")
