from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import QuerySet
from webapp.models import Booking
from api.serializers import BookingSerializer
from webapp.config import BookingStatus


class HistoryViewSet(ReadOnlyModelViewSet):
    queryset: QuerySet = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.pk,
                                    status__in=[BookingStatus.CANCELLED.value, BookingStatus.COMPLETED.value])
