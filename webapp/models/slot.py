from django.db import models

POSITION_SCHEME = {'properties': {
    'X': {'type': 'integer', 'minimum': 0, 'required': True},
    'Y': {'type': 'integer', 'minimum': 0, 'required': True}
}}


class Slot(models.Model):
    lot = models.ForeignKey("ParkingLot", on_delete=models.CASCADE)
    name = models.CharField(max_length=10, null=False)
    position = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
