from django.dispatch import receiver
from django.utils import timezone

from .. import signals
from webapp.models.booking import Booking, BookingStatus
from webapp.models import User, Notification
from ..functions.push_notifications import send_push_notification


@receiver(signals.bookingNotification)
def send_booing_notification(sender, booking: Booking, user: User, **kwargs):
    if booking.status == BookingStatus.BOOKED.value:
        from_time = booking.booked_time
        to_time = from_time + booking.duration
        title, body = booking_confirmation_notification(
            slot_id=booking.slot.name,
            parking_lot=booking.lot.name,
            from_time=format_datetime(from_time),
            to_time=format_datetime(to_time)
        )
        noti: Notification = Notification.objects.save(
            title=title,
            message=body,
            user=user.pk
        )
        send_push_notification(user.device_token, noti.title, noti.message)
    elif booking.status == BookingStatus.CANCELLED.value:
        title, body = booking_cancellation_notification(
            slot_id=booking.slot.name,
            parking_lot=booking.lot.name,
        )
        noti: Notification = Notification.objects.save(
            title=title,
            message=body,
            user=user.pk
        )
        send_push_notification(user.device_token, noti.title, noti.message)
    elif booking.status == BookingStatus.PARKED.value:
        pass
    elif booking.status == BookingStatus.COMPLETED.value:
        pass


def booking_confirmation_notification(slot_id, parking_lot, from_time, to_time):
    notification_title = 'Booking Confirmation'
    notification_body = f'Your booking for Parking Slot {slot_id} in {parking_lot} has been confirmed.'
    notification_body += f' You have reserved the slot from {from_time} to {to_time}.'

    # Return the notification content
    return notification_title, notification_body


def booking_cancellation_notification(slot_id, parking_lot):
    notification_title = 'Booking Cancellation'
    notification_body = f'Your booking for Parking Slot {slot_id} in {parking_lot} has been canceled.'
    notification_body += f'If you have made any payment, a refund will be processed accordingly.'

    # Return the notification content
    return notification_title, notification_body


def format_datetime(dt):
    # Convert datetime to the desired format
    formatted_datetime = dt.strftime('%d %b %Y %I:%M %p')

    # Adjust the timezone if needed
    formatted_datetime = timezone.localtime(dt).strftime('%d %b %Y %I:%M %p')

    return formatted_datetime
