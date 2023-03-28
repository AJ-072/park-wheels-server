from rest_framework.viewsets import ReadOnlyModelViewSet
from webapp.models import Slot
from ...serializers import SlotSerializer
from django.shortcuts import get_object_or_404


class SlotViewSet(ReadOnlyModelViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

    def get_queryset(self):
        print(self.get_lot_id())
        return super().get_queryset().filter(lot_id=self.get_lot_id())

    def get_lot_id(self):
        return self.kwargs.get('parking_lot_pk')
