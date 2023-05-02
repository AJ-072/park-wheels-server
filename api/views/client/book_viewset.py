import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.db.models import QuerySet
from webapp.models import Booking, ParkingLot, Slot
from api.serializers import BookingSerializer, SlotIdSerializer, SlotBookingSerializer, SlotAvailabilitySerializer
from webapp.config import BookingStatus, get_deltatime
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from ...authentication import BearerTokenAuthentication
from ...decorator import validate_field, not_none_field, custom_serializer

class BookViewSet(ModelViewSet):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset: QuerySet = Booking.objects.all()
    serializer_class = BookingSerializer

    # http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.pk, lot_id=self.kwargs.get("parking_lot_pk"))

    @custom_serializer(SlotBookingSerializer)
    def create(self, request, serializer: SlotBookingSerializer, parking_lot_pk=None):
        lot: ParkingLot = get_object_or_404(ParkingLot, id=parking_lot_pk)
        booking_serializer = self.get_serializer(data={'lot': lot.pk,
                                                       'user': request.user.pk,
                                                       'created_by': request.user.pk,
                                                       'booked_time': serializer.data.get('booking_time'),
                                                       'status': BookingStatus.WAITING.value,
                                                       'duration': datetime.timedelta(
                                                           hours=serializer.data.get('duration')),
                                                       'cost': float(serializer.data.get(
                                                           'duration') * lot.rate_per_hour)})
        booking_serializer.is_valid(raise_exception=True)
        booking_serializer.save()
        return Response(booking_serializer.data)

    @action(methods=['put'], detail=True)
    @validate_field(values=[BookingStatus.WAITING.value])
    @not_none_field("slot_id")
    def confirm(self, request, parking_lot_pk=None, pk=None):
        self.is_expired()
        booking_serializer = self.get_serializer(instance=self.get_object(),
                                                 data={"status": BookingStatus.BOOKED.value},
                                                 partial=True)
        booking_serializer.is_valid(raise_exception=True)
        booking_serializer.save()
        return Response(booking_serializer.data)

    @action(methods=['put'], detail=True, url_path="change-slot")
    @validate_field(values=[BookingStatus.WAITING.value])
    @custom_serializer(SlotIdSerializer)
    def change_slot(self, request, serializer: SlotIdSerializer, parking_lot_pk=None, pk=None):
        self.is_expired()
        slot_serializer = SlotAvailabilitySerializer(Slot.objects.get(id=serializer.validated_data['slot_id']),
                                                     context={"booking": self.get_object()})
        slot_serializer.is_valid()
        if ~slot_serializer.available:
            return Response({'message': "can't select slot : " + slot_serializer.validated_data['name']}, status=400)
        booking_serializer = self.get_serializer(instance=self.get_object(),
                                                 data={"slot": serializer.validated_data['slot_id']},
                                                 partial=True)
        booking_serializer.is_valid(raise_exception=True)
        booking_serializer.save()
        return Response(booking_serializer.data)

    @validate_field(values=[BookingStatus.WAITING.value])
    def destroy(self, request, parking_lot_pk=None, pk=None):
        self.is_expired()
        booking_serializer = self.get_serializer(instance=self.get_object(),
                                                 data={"status": BookingStatus.CANCELLED.value},
                                                 partial=True)
        booking_serializer.is_valid(raise_exception=True)
        booking_serializer.save()
        return Response(booking_serializer.data)

    def is_expired(self):
        booking = self.get_object()
        if booking.is_expired:
            raise ParseError(detail={'message': 'timeout'})
