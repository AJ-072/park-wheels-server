from celery import shared_task
from . import BookingStatus
from webapp.models import Booking


def booking_time_out(booking_id):
    booking = Booking.objets.get(id=booking_id)
    if booking.status == BookingStatus.WAITING:
        booking.delete()
