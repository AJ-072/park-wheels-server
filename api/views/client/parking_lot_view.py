import rest_framework.request

from webapp.models import ParkingLot
from rest_framework.request import Request
from rest_framework.response import Response
from api.serializers.parking_lot_serializer import ParkingLotSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def get_parking_lot_list(request: Request):
    lat = request.query_params.get("lat")
    long = request.query_params.get("long")
    if lat is None:
        return Response({"message": "lat parameter required"}, status=400)
    if long is None:
        return Response({"message": "long parameter required"}, status=400)
    loc = Point(float(long), float(lat))
    query_set = ParkingLot.objects.filter(location__distance_lte=(loc, D(m=5000)))
    serializer = ParkingLotSerializer(query_set, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_parking_lot(request, ID):
    query_set = ParkingLot.objects.get(id=ID)
    serializer = ParkingLotSerializer(query_set)
    return Response(serializer.data)
