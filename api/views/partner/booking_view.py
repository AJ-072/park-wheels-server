from rest_framework.viewsets import ModelViewSet
from django.db.models import QuerySet
from webapp.models import Booking
from api.serializers import BookingSerializer


class BookingView(ModelViewSet):
    queryset: QuerySet = Booking.objects.all()
    serializer_class = BookingSerializer
    http_method_names = ["get", "post"]

    def get_queryset(self):
        return self.queryset.filter(created_by_id=self.request.user.pk)


