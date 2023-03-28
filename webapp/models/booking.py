from django.db import models
from webapp.config import BookingStatus
from datetime import timedelta


class Booking(models.Model):
    lot = models.ForeignKey('ParkingLot', on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=5, null=False, decimal_places=2)
    slot = models.ForeignKey("Slot", on_delete=models.CASCADE, null=True)
    timeout = models.DurationField(default=timedelta(minutes=5))
    booked_time = models.DateTimeField(null=False)
    take_away_time = models.DateTimeField(null=True)
    status = models.CharField(choices=BookingStatus.choices(), default=BookingStatus.WAITING, max_length=10)
    duration = models.IntegerField(default=1, null=False)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    created_by = models.ForeignKey("User", on_delete=models.CASCADE, related_name="created_by")
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return str(self.cost)
