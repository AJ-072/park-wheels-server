from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.db.models import Avg

from webapp.config import ParkingLotStatus


class ParkingLot(models.Model):
    name = models.CharField(max_length=40, null=False)
    address = models.CharField(max_length=200, null=False)
    location = models.PointField(geography=True, default=Point(0.0, 0.0), srid=4326)
    description = models.TextField(blank=True, default='', null=True)
    rate_per_hour = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    status = models.CharField(choices=ParkingLotStatus.choices(), default=ParkingLotStatus.PENDING.value, max_length=10)
    owner = models.ForeignKey("User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True, auto_created=True)

    @property
    def avg_rating(self):
        if hasattr(self, "_avg_rating"):
            return self._avg_rating['rating__avg']
        return self.booking_set.filter(review__isnull=False).aggregate(Avg('review__rating'))['review__rating__avg']

    def __str__(self):
        return f"{self.name}"


class LotImage(models.Model):
    image = models.ImageField(upload_to='lot_images', blank=True, null=True)
    lot = models.ForeignKey('ParkingLot', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.image}"
