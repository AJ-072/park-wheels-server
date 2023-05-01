import rest_framework.filters
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import QuerySet
from webapp.models import Booking
from api.serializers import ListBookingSerializer
from webapp.config import BookingStatus


class BookingViewSet(ReadOnlyModelViewSet):
    queryset: QuerySet = Booking.objects.all()
    serializer_class = ListBookingSerializer

    def get_queryset(self, ):
        return self.queryset.filter(user_id=self.request.user.pk,
                                    status__in=[BookingStatus.WAITING.value,
                                                BookingStatus.BOOKED.value,
                                                BookingStatus.PARKED.value]).order_by('-booked_time', 'status')
