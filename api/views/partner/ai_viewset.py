from datetime import datetime

from django.db.models import Q, F
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.authentication import BearerTokenAuthentication
from api.serializers import BookingSerializer
from api.serializers.slot_serializer import TimeSerializer
from webapp.config import BookingStatus
from webapp.models import Booking, Slot


class AIViewset(GenericViewSet):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @action("PUT", url_path="update-arrival-time", detail=False)
    def updateArrivalTime(self, request):
        arrivalSerializer = TimeSerializer(request.data)
        arrivalSerializer.is_valid(raise_exception=True)
        slot = Slot.objects.filter(lot_id=arrivalSerializer.validated_data['lot_id'],
                                   name=arrivalSerializer.validated_data['name'])
        now = datetime.datetime.now()
        booking = Booking.objects.filter(
            Q(booked_time__range=[now - F('duration'), now]),
            Q(status=BookingStatus.BOOKED.value), lot_id=arrivalSerializer.validated_data['lot_id'], slot_id=slot.pk)
        if not booking:
            return Response(status=400, data={"message": "invalid booking"})
        bookingSerializer = BookingSerializer(data=booking)
        bookingSerializer.save(status=BookingStatus.PARKED.value, arrived_time=now)
        return Response(status=200, data={'result': bookingSerializer.data})

    @action("PUT", url_path="update-dispatch-time", detail=False)
    def updateDispatchTime(self, request):
        dispatchSerializer = TimeSerializer(request.data)
        dispatchSerializer.is_valid(raise_exception=True)
        slot = Slot.objects.filter(lot_id=dispatchSerializer.validated_data['lot_id'],
                                   name=dispatchSerializer.validated_data['name'])
        now = datetime.datetime.now()
        booking = Booking.objects.filter(
            Q(booked_time__range=[now - F('duration'), now]),
            Q(status=BookingStatus.PARKED.value), lot_id=dispatchSerializer.validated_data['lot_id'], slot_id=slot.pk)
        if not booking:
            return Response(status=400, data={"message": "invalid booking"})
        bookingSerializer = BookingSerializer(data=booking)
        bookingSerializer.save(status=BookingStatus.COMPLETED.value, take_away_time=now)
        return Response(status=200, data={'result': bookingSerializer.data})
