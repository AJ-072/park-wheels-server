from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1,
                                 validators=[MaxValueValidator(5), MinValueValidator(0)])
    title = models.CharField(max_length=100)
    comment = models.TextField(null=True, blank=True)
    lot = models.ForeignKey("ParkingLot", on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True, auto_created=True)
