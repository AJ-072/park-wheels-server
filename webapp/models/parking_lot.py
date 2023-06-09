from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from webapp.config import ParkingLotStatus


class ParkingLot(models.Model):
    name = models.CharField(max_length=40, null=False)
    address = models.CharField(max_length=200, null=False)
    location = models.PointField(geography=True, default=Point(0.0, 0.0))
    rate_per_hour = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    status = models.CharField(choices=ParkingLotStatus.choices(), default=ParkingLotStatus.PENDING, max_length=10)
    owner = models.ForeignKey("User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return f"{self.name}"
