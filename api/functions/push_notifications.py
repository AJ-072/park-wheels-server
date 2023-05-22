from firebase_admin import messaging
from django.dispatch import receiver
from django.db.models.signals import post_save
from webapp.models import Notification


@receiver(signal=post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if not created:
        return

    title = instance.title
    body = instance.message
    image = instance.image
    token = instance.user.fcm_token
    if token is None:
        return
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
            image=image
        ),
        token=token,
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)
