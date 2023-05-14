from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.authentication import BearerTokenAuthentication
from api.serializers import ParkingLotSerializer
from api.serializers.notifications_serializer import NotificationsSerializer
from webapp.models import Notification


class NotificationsViewSet(ReadOnlyModelViewSet):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Notification.objects.all()
    serializer_class = NotificationsSerializer

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.pk)

    def list(self, request, *args, **kwargs):
        return Response({
            'result': self.serializer_class(self.get_queryset(),many=True).data
        })