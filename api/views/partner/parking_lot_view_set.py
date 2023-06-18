import datetime
import json

from django.db.models import Q, Sum
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from api.authentication import BearerTokenAuthentication
from api.serializers import ParkingLotSerializer
from webapp.config import BookingStatus
from webapp.models import ParkingLot, Booking


class ParkingLotViewSet(ModelViewSet):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer

    def get_queryset(self):
        return self.queryset.filter(owner_id=self.request.user.pk)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['location'] = {
            "coordinates": [
                float(data['long']), float(data['lat'])
            ], "type": "point"
        }
        serializer = self.serializer_class(data=data, context={"request": self.request,
                                                                       "images": self.request.FILES.getlist('images',
                                                                                                            None)})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super(ParkingLotViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def list(self, request, *args, **kwargs):
        return Response({
            'result': self.serializer_class(self.get_queryset(), many=True).data
        })

    def retrieve(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        monthly_bookings_set = self.get_object().booking_set.filter(
            Q(booked_time__year=now.year, booked_time__month=now.month) & Q(
                status__in=[BookingStatus.BOOKED.value, BookingStatus.PARKED.value, BookingStatus.COMPLETED.value]))
        monthly_count = monthly_bookings_set.count()
        monthly_revenue = monthly_bookings_set.aggregate(Sum('cost')).get('cost__sum', 0)
        return Response(data={
            "monthly_count": monthly_count,
            "monthly_revenue": monthly_revenue
        })
