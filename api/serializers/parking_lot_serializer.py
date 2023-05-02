from rest_framework import serializers
from webapp.models.parking_lot import ParkingLot


class ParkingLotSerializer(serializers.ModelSerializer):

    owner = serializers.CurrentUserDefault()

    class Meta:
        model = ParkingLot
        fields = "__all__"

