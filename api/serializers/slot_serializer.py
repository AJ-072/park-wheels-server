from datetime import datetime, timedelta

import pytz
from rest_framework import serializers

from api.serializers.parking_lot_serializer import ParkingLotSerializer
from webapp.models import Slot, Booking, ParkingLot
from webapp.config import BookingStatus
from django.db.models import Q,F


class SlotSerializer(serializers.ModelSerializer):
    lot = ParkingLotSerializer(read_only=True)
    lot_id = serializers.PrimaryKeyRelatedField(source='lot', write_only=True, queryset=ParkingLot.objects.all())

    class Meta:
        model = Slot
        fields = '__all__'


class TimeSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=5)
    lot_id = serializers.IntegerField(required=True)


class SlotAvailabilitySerializer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()

    class Meta:
        model = Slot
        fields = '__all__'

    def get_available(self, obj):
        booking = self.context.get('booking')
        if booking is None:
            return {}
        end_date_time = booking.booked_time + booking.duration
        queryset = Booking.objects.filter(
            Q(booked_time__range=[booking.booked_time, end_date_time]) | Q(
                booked_time__range=[booking.booked_time - F('duration'), end_date_time - F('duration')]),
            ~Q(status=BookingStatus.WAITING.value) | Q(created_at__gt=datetime.now(pytz.UTC) - F("timeout")) & Q(
                status=BookingStatus.WAITING.value),
            slot=obj
        )
        return queryset.count() == 0


class SlotIdSerializer(serializers.Serializer):
    slot_id = serializers.IntegerField(required=True, )

    def validate_slot_id(self, value):
        try:
            obj = Slot.objects.get(id=value)
        except Slot.DoesNotExist:
            raise serializers.ValidationError('Object with this ID does not exist')
        return value
