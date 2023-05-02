from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import QuerySet

from api.authentication import BearerTokenAuthentication
from webapp.models import Booking
from api.serializers import ListBookingSerializer
from webapp.config import BookingStatus


class HistoryViewSet(ReadOnlyModelViewSet):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset: QuerySet = Booking.objects.all()
    serializer_class = ListBookingSerializer

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.pk,
                                    status__in=[BookingStatus.CANCELLED.value, BookingStatus.COMPLETED.value]).order_by(
            '-booked_time', 'status')

    def list(self, request, *args, **kwargs):
        return Response({
            'result': self.get_queryset()
        })
