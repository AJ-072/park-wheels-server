from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import ParkingLotSerializer
from webapp.models import Notifications


class NotificationsViewSet(ReadOnlyModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = ParkingLotSerializer

    def get_queryset(self):
        return self.queryset.filter(owner_id=self.request.user.pk)