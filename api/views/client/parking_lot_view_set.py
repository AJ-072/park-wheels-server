from webapp.models import ParkingLot, Booking
from rest_framework.response import Response
from api.serializers import ParkingLotSerializer, LocationSerializer, SlotSerializer, BookingSerializer
from django.contrib.gis.measure import D
from django.db.models.query import Q
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action


class ParkingLotViewSet(ReadOnlyModelViewSet):
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer

    def list(self, request, *args, **kwargs):
        location_serializer = LocationSerializer(data=request.query_params)
        location_serializer.is_valid(raise_exception=True)
        query_set = self.get_queryset().filter(location__distance_lte=(location_serializer.point(), D(m=5000)))
        return Response(self.serializer_class(query_set, many=True).data)

