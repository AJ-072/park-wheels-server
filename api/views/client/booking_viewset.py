from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import QuerySet
from webapp.models import Booking
from api.serializers import BookingSerializer
from webapp.config import BookingStatus


class BookingViewSet(ReadOnlyModelViewSet):
    queryset: QuerySet = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self, ):
        print(self.request.user.pk)
        return self.queryset.filter(user_id=self.request.user.pk,
                                    status__in=[BookingStatus.WAITING.value,
                                                BookingStatus.BOOKED.value,
                                                BookingStatus.PARKED.value])
