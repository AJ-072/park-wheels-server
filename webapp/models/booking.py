from datetime import datetime, timedelta

import pytz
from django.db import models
from webapp.config import BookingStatus


class Booking(models.Model):
    lot = models.ForeignKey('ParkingLot', on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=5, null=False, decimal_places=2)
    slot = models.ForeignKey("Slot", on_delete=models.CASCADE)
    timeout = models.DurationField(default=timedelta(minutes=5))
    booked_time = models.DateTimeField(null=False)
    arrived_time = models.DateTimeField(null=True, blank=True)
    take_away_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(choices=BookingStatus.choices(), default=BookingStatus.WAITING.value, max_length=10)
    duration = models.DurationField(default=timedelta(hours=1), null=False)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    created_by = models.ForeignKey("User", on_delete=models.CASCADE, related_name="created_by")
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return str(self.cost)

    @property
    def is_expired(self):
        print(self.created_at + self.timeout)
        print(datetime.now(pytz.UTC))
        return self.created_at + self.timeout < (datetime.now(pytz.UTC))

    @property
    def end_date_time(self):
        return self.booked_time + self.duration
