from django.contrib.gis.db.models.functions import Distance
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.authentication import BearerTokenAuthentication
from webapp.config import ParkingLotStatus
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

    def get_queryset(self):
        return self.queryset.filter(status__in=[ParkingLotStatus.ACTIVE.value])

    def list(self, request, *args, **kwargs):
        location_serializer = LocationSerializer(data=request.query_params)
        location_serializer.is_valid(raise_exception=True)
        query_set = self.get_queryset().annotate(
            distance=Distance('location', location_serializer.point())).filter(distance__lte=5000)
        return Response({'result': self.serializer_class(query_set, many=True,
                                                         context={"location": location_serializer.point()}).data})
