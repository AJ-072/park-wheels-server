from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from webapp.models import Slot, Booking
from ...authentication import BearerTokenAuthentication
from ...serializers import SlotAvailabilitySerializer
from django.shortcuts import get_object_or_404


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
