from rest_framework import serializers
from webapp.models import Booking, ParkingLot, User
from datetime import timedelta


class BookingSerializer(serializers.ModelSerializer):
    timeout = serializers.DurationField(required=False)

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = (
            'created_at',
            'updated_at',
            'id'
        )
        extra_kwargs = {
            '__all__': {'required': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data['timeout'] = timedelta(seconds=data['timeout'].total_seconds())
        return data


class SlotBookingSerializer(serializers.Serializer):
    duration = serializers.IntegerField(required=True, min_value=1, max_value=24)
    booked_time = serializers.DateTimeField(required=True)
