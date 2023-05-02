from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin

from ...authentication import BearerTokenAuthentication
from ...decorator import custom_serializer
from ...permissions import IsPartner
from rest_framework.permissions import IsAuthenticated
from api.serializers import UserSerializer, ChangePasswordSerializer


class PartnerViewSet(GenericViewSet, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['put'], url_path='update-password', detail=False)
    @custom_serializer(serializer_class=ChangePasswordSerializer)
    def updatePassword(self, request, serializer, *args, **kwargs):
        if request.user.check_password(serializer.confirm):
            request.user.set_password(serializer.new)
        else:
            return Response(status=400, data={'message': 'incorrect password'})
        return Response(status=200, data={'message': 'password successfully updated'})

    @action(['POST'], detail=False)
    def logout(self, request, user_type=None):
        request.user.auth_token.delete()
        return Response(status=200, data={'message': 'Logged out successfully'})
