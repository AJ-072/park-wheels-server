from firebase_admin import messaging


def send_push_notification(token, title, body, image=None):
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
