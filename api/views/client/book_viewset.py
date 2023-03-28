from rest_framework.viewsets import GenericViewSet
from django.db.models import QuerySet
from webapp.models import Booking, ParkingLot
from api.serializers import BookingSerializer, slot_serializer, SlotBookingSerializer
from webapp.config import BookingStatus, shared_task
from datetime import datetime, timedelta
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from ...decorator import validate_field, not_none_field, custom_serializer


class BookViewSet(GenericViewSet):
    queryset: QuerySet = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.pk, lot_id=self.kwargs.get("parking_lot_pk"))

    @action(methods=['post'], detail=False)
    @custom_serializer(SlotBookingSerializer)
    def request(self, request, serializer: SlotBookingSerializer, parking_lot_pk=None):
        lot: ParkingLot = get_object_or_404(ParkingLot, id=parking_lot_pk)
        booking_serializer = self.get_serializer(data={'lot': lot.pk,
                                                       'user': request.user.pk,
                                                       'created_by': request.user.pk,
                                                       'booked_time': serializer.data.get('booked_time'),
                                                       'status': BookingStatus.WAITING.value,
                                                       'duration': serializer.data.get('duration'),
                                                       'cost': int(
                                                           serializer.data.get('duration') * lot.rate_per_hour)})
        booking_serializer.is_valid(raise_exception=True)
        booking_serializer.save()
        return Response(booking_serializer.data)

    @action(methods=['post'], detail=True)
    @validate_field(values=[BookingStatus.WAITING])
    @not_none_field("slot_id")
    def confirm(self, parking_lot_pk=None):
        self.get_serializer().save(status=BookingStatus.BOOKED)
        return Response(self.get_serializer().data)

    @action(methods=['put'], detail=True, )
    @validate_field(values=[BookingStatus.WAITING])
    @custom_serializer(slot_serializer.SlotIdSerializer)
    def change_slot(self, serializer, parking_lot_pk=None):
        self.get_serializer().save(slot_id=serializer.validated_data['slot_id'])
        return Response(self.get_serializer().data)

    @action(methods=['post'], detail=True)
    @validate_field(values=[BookingStatus.BOOKED])
    def cancel(self, parking_lot_pk=None):
        self.get_serializer().save(status=BookingStatus.CANCELLED)
        return Response(self.get_serializer().data)
