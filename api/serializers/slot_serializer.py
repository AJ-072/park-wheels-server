from datetime import datetime, timedelta

import pytz
from rest_framework import serializers

import api.serializers
from webapp.models import Slot, Booking
from webapp.config import get_slot_status, SlotStatus, BookingStatus
from django.shortcuts import get_object_or_404
from django.db.models import Q, Case, When, Value, F
from django.db import models
from rest_framework.validators import UniqueValidator


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'


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
            Q(booked_time__range=[booking.booked_time,end_date_time]) | Q(
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
