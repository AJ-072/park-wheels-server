from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from api.authentication import BearerTokenAuthentication
from api.serializers.review_serializer import ReviewSerializer
from webapp.models import Review


class ReviewViewSet(ModelViewSet):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return super().get_queryset().filter(lot_id=self.get_lot_id())

    def get_lot_id(self):
        return self.kwargs.get('parking_lot_pk')

    def create(self, request, *args, **kwargs):
        print(self.get_lot_id())
        serializer = self.serializer_class(data={
            'lot': self.get_lot_id(),
            'user': self.request.user.pk,
            'title': request.data['title'],
            'comment': request.data['comment'],
            'rating': request.data['rating']
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'result': serializer.data})
