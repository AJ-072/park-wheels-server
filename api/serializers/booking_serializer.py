from rest_framework import serializers
from webapp.models import Booking, ParkingLot, User, Slot
from datetime import timedelta
from .slot_serializer import SlotSerializer
from .parking_lot_serializer import ParkingLotSerializer


class BookingWithSlotSerializer(serializers.ModelSerializer):
    slot = SlotSerializer()

    class Meta:
        model = Booking
        fields = ('__all__',)


# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = '__all__'
#

class BookingSerializer(serializers.ModelSerializer):
    slot = SlotSerializer(read_only=True, required=True)
    lot = ParkingLotSerializer(read_only=True, required=True)

    class Meta:
        model = Booking
        fields = '__all__'


class SlotBookingSerializer(serializers.Serializer):
    duration = serializers.IntegerField(required=True, min_value=1, max_value=24)
    booking_time = serializers.DateTimeField(required=True)
