import datetime

from django.db.models import Q, F
from rest_framework.decorators import action, permission_classes as permission
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from webapp.config import BookingStatus
from webapp.models import Slot, Booking
from ...authentication import BearerTokenAuthentication
from ...serializers import SlotAvailabilitySerializer, SlotSerializer, BookingSerializer
from django.shortcuts import get_object_or_404

from ...serializers.slot_serializer import TimeSerializer


class SlotViewSet(ReadOnlyModelViewSet):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Slot.objects.all()
    serializer_class = SlotAvailabilitySerializer

    def get_queryset(self):
        return super().get_queryset().filter(lot_id=self.get_lot_id())

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context()
        context['booking'] = get_object_or_404(Booking, id=kwargs.get('booking_id'))
        return context

    def get_lot_id(self):
        return self.kwargs.get('parking_lot_pk')

    def list(self, request, *args, **kwargs):
        return Response({
            'result': self.serializer_class(self.get_queryset(), many=True).data
        })

    @action("POST", url_path='add', detail=False)
    def addSlot(self):
        slotSerializer = SlotSerializer(self.request.data, many=True, lot_id=self.get_lot_id())
        slotSerializer.is_valid(raise_exception=True)
        slotSerializer.save()
        return Response(status=200, data='successful')

    @action("PUT", url_path="update-arrival-time", detail=False)
    def updateArrivalTime(self, request):
        arrivalSerializer = TimeSerializer(self.request.data, lot_id=self.get_lot_id())
        arrivalSerializer.is_valid(raise_exception=True)
        slot = Slot.objects.filter(lot_id=self.get_lot_id(), name=arrivalSerializer.validated_data['name'])
        now = datetime.datetime.now()
        booking = Booking.objects.filter(
            Q(booked_time__range=[now - F('duration'), now]),
            Q(status=BookingStatus.BOOKED.value), lot_id=self.get_lot_id(), slot_id=slot.pk)
        if not booking:
            return Response(status=400, data={"message": "invalid booking"})
        bookingSerializer = BookingSerializer(data=booking)
        bookingSerializer.save(status=BookingStatus.PARKED.value, arrived_time=now)
        return Response(status=200, data={'result': bookingSerializer.data})

    @action("PUT", url_path="update-dispatch-time", detail=False)
    def updateDispatchTime(self, request):
        dispatchSerializer = TimeSerializer(self.request.data, lot_id=self.get_lot_id())
        dispatchSerializer.is_valid(raise_exception=True)
        slot = Slot.objects.filter(lot_id=self.get_lot_id(), name=dispatchSerializer.validated_data['name'])
        now = datetime.datetime.now()
        booking = Booking.objects.filter(
            Q(booked_time__range=[now - F('duration'), now]),
            Q(status=BookingStatus.PARKED.value), lot_id=self.get_lot_id(), slot_id=slot.pk)
        if not booking:
            return Response(status=400, data={"message": "invalid booking"})
        bookingSerializer = BookingSerializer(data=booking)
        bookingSerializer.save(status=BookingStatus.COMPLETED.value, take_away_time=now)
        return Response(status=200, data={'result': bookingSerializer.data})
