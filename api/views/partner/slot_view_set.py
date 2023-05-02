from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from webapp.models import Slot, Booking
from ...authentication import BearerTokenAuthentication
from ...serializers import SlotAvailabilitySerializer, SlotSerializer
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

    def list(self, request, *args, **kwargs):
        return Response({
            'result': self.serializer_class(self.get_queryset(), many=True).data
        })

    @action("POST", url_path='add-slots', detail=True)
    @permission_classes([AllowAny])
    def addSlot(self):
        slotSerializer = SlotSerializer(self.request.data, many=True)
        slotSerializer.is_valid(raise_exception=True)
        slotSerializer.save()
        return Response(status=200, data='successful')
