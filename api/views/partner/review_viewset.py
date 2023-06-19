from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.authentication import BearerTokenAuthentication
from api.serializers.review_serializer import ReviewSerializer, ReviewWithUserSerializer
from webapp.models import Review


class ReviewViewSet(ReadOnlyModelViewSet):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Review.objects.all()
    serializer_class = ReviewWithUserSerializer

    def get_queryset(self):
        return super().get_queryset().filter(booking__lot_id=self.get_lot_id())

    def get_lot_id(self):
        return self.kwargs.get('parking_lot_pk')

    def list(self, request, *args, **kwargs):
        return Response({
            'result': self.serializer_class(self.get_queryset(), many=True).data
        })
