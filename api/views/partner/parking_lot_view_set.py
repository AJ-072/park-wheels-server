from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from api.authentication import BearerTokenAuthentication
from api.serializers import ParkingLotSerializer
from webapp.models import ParkingLot


class ParkingLotViewSet(ModelViewSet):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer

    def get_queryset(self):
        return self.queryset.filter(owner_id=self.request.user.pk)

    def create(self, request, *args, **kwargs):
        data = self.request.data;
        serializer = self.serializer_class(data= data)
        serializer.data['owner_id'] = request.user.pk
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        return Response({
            'result': self.serializer_class(self.get_queryset(), many=True).data
        })
