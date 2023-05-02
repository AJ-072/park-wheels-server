from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer
from webapp.models.parking_lot import ParkingLot


class ParkingLotSerializer(GeoModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ParkingLot
        fields = "__all__"
        geo_field = 'location'

    def create(self, validated_data):
        return ParkingLot.objects.create(
            owner=self.context['request'].user,
            **validated_data
        )
