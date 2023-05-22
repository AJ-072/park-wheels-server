from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin

from api.authentication import BearerTokenAuthentication


class StatisticsViewSet(GenericViewSet, RetrieveModelMixin):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        pass

    def get_lot_id(self):
        return self.kwargs.get('parking_lot_pk')
