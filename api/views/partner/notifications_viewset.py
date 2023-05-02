from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.authentication import BearerTokenAuthentication
from api.serializers import ParkingLotSerializer
from webapp.models import Notifications


class NotificationsViewSet(ReadOnlyModelViewSet):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Notifications.objects.all()
    serializer_class = ParkingLotSerializer

    def get_queryset(self):
        return self.queryset.filter(owner_id=self.request.user.pk)