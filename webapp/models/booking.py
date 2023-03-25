from django.db import models
from datetime import timedelta
from webapp.config import BookingStatus


class Booking(models.Model):
    lot = models.ForeignKey('ParkingLot', on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=5, null=False, decimal_places=2)
    slot = models.ForeignKey("Slot", on_delete=models.CASCADE)
    booked_time = models.DateTimeField(null=False)
    status = models.CharField(choices=BookingStatus.choices(), default=BookingStatus.WAITING, max_length=10)
    duration = models.DurationField(default=timedelta(hours=0))
    created_by = models.ForeignKey("User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.cost
