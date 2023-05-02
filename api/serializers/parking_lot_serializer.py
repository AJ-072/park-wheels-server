from rest_framework import serializers
from webapp.models.parking_lot import ParkingLot


class ParkingLotSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ParkingLot
        fields = "__all__"

    def create(self, validated_data):
        return ParkingLot.objects.create(
            owner=self.context['request'].user,
            **validated_data
        )
