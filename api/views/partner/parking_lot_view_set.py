from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import ParkingLotSerializer
from webapp.models import ParkingLot


class ParkingLotViewSet(ReadOnlyModelViewSet):
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer

    def get_queryset(self):
        return self.queryset.filter(owner_id=self.request.user.pk)


