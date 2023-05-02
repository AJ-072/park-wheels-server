from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import QuerySet

from api.authentication import BearerTokenAuthentication
from webapp.models import Booking
from api.serializers import BookingSerializer, ListBookingSerializer


class BookingView(ModelViewSet):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset: QuerySet = Booking.objects.all()
    serializer_class = ListBookingSerializer
    http_method_names = ["get", "post"]

    def get_queryset(self):
        return self.queryset.filter(created_by_id=self.request.user.pk)

    def list(self, request, *args, **kwargs):
        return Response({
            'result': self.serializer_class(self.get_queryset(),many=True).data
        })


