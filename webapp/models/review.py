from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0,
                                 validators=[MaxValueValidator(5), MinValueValidator(0)])
    comment = models.TextField()
    lot = models.ForeignKey("ParkingLot", on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True, auto_created=True)
