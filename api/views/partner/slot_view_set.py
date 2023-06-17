import datetime

from django.db.models import Q, F
from rest_framework.decorators import action, permission_classes as permission
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from webapp.config import BookingStatus
from webapp.models import Slot, Booking
from ...authentication import BearerTokenAuthentication
from ...serializers import SlotAvailabilitySerializer, SlotSerializer, BookingSerializer
from django.shortcuts import get_object_or_404

from ...serializers.slot_serializer import TimeSerializer


class SlotViewSet(ModelViewSet):
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

    def create(self, request, *args, **kwargs):
        slotSerializer = SlotSerializer(data=[dict(item, lot_id=self.get_lot_id()) for item in self.request.data],
                                        many=True)
        slotSerializer.is_valid(raise_exception=True)
        slotSerializer.save()
        return Response(status=200, data='successful')
