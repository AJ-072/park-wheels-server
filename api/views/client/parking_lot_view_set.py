from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.authentication import BearerTokenAuthentication
from webapp.models import ParkingLot
from rest_framework.response import Response
from api.serializers import ParkingLotSerializer, LocationSerializer, SlotSerializer
from django.contrib.gis.measure import D
from django.db.models.query import Q
from rest_framework.viewsets import ReadOnlyModelViewSet


class ParkingLotViewSet(ReadOnlyModelViewSet):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer

    def list(self, request, *args, **kwargs):
        location_serializer = LocationSerializer(data=request.query_params)
        location_serializer.is_valid(raise_exception=True)
        query_set = self.get_queryset().filter(location__distance_lte=(location_serializer.point(), D(m=5000)))
        return Response({'result': self.serializer_class(query_set, many=True).data})

    @action("POST", url_path='add-slots', detail=True)
    def addSlot(self):
        slotSerializer = SlotSerializer(self.request.data, many=True)
        slotSerializer.is_valid(raise_exception=True)
        slotSerializer.save()
        return Response(status=200, data='successful')
