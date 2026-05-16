import os
import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings

def initialize_firebase():
    """Initializes Firebase Admin SDK."""
    cred_path = os.path.join(settings.BASE_DIR, 'firebase-key.json')
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

def send_push_notification(user, title, body, data=None):
    """Sends a push notification to a user's FCM tokens."""
    from notifications.models import FCMToken
    
    tokens = FCMToken.objects.filter(user=user).values_list('token', flat=True)
    if not tokens:
        return
    
    # Initialize firebase if not already
    initialize_firebase()
    
    # Prepare message
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data or {},
        tokens=list(tokens),
    )
    
    # Send message
    response = messaging.send_multicast(message)
    return response
