from rest_framework import serializers
from webapp.models import Booking, ParkingLot, User, Slot
from datetime import timedelta

from .review_serializer import ReviewSerializer
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
    slot = SlotSerializer(read_only=True)
    lot = ParkingLotSerializer(read_only=True)
    slot_id = serializers.PrimaryKeyRelatedField(source='slot', write_only=True, queryset=Slot.objects.all())
    lot_id = serializers.PrimaryKeyRelatedField(source='lot', write_only=True, queryset=ParkingLot.objects.all())
    review = ReviewSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        # fields = (
        #     'id',
        #     'cost',
        #     'slot',
        #     'slot_id',
        #     ''
        # )
        # extra_kwargs = {
        #     'slot_id': {'source': 'slot', 'write_only': True},
        #     'lot_id': {'source': 'lot', 'write_only': True},
        # }


class SlotBookingSerializer(serializers.Serializer):
    duration = serializers.IntegerField(required=True, min_value=1, max_value=24)
    booking_time = serializers.DateTimeField(required=True)
