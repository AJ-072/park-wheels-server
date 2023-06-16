from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ...authentication import BearerTokenAuthentication
from ...decorator import custom_serializer
from ...permissions import IsPartner
from rest_framework.permissions import IsAuthenticated
from api.serializers import UserSerializer, ChangePasswordSerializer, ParkingLotSerializer


class PartnerViewSet(ModelViewSet):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.request.user

    @action(methods=['GET'], url_path='user', detail=False)
    def user(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['PUT'], url_path='update', detail=False)
    def updateUser(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], url_path='add-lot', detail=False)
    @custom_serializer(serializer_class=ParkingLotSerializer)
    def createLot(self, request, serializer, *args, **kwargs):
        serializer.save()
        return Response(serializer.data)

    @action(methods=['put'], url_path='update-password', detail=False)
    @custom_serializer(serializer_class=ChangePasswordSerializer)
    def updatePassword(self, request, serializer, *args, **kwargs):
        if request.user.check_password(serializer.confirm):
            request.user.set_password(serializer.new)
        else:
            return Response(status=400, data={'message': 'incorrect password'})
        return Response(status=200, data={'message': 'password successfully updated'})

    @action(detail=False, methods='PUT', url_path='update-fcm-token')
    def updateFCMToken(self, request, user_type=None):
        serializer = self.serializer_class(request.user, data={"fcm_token": request.data['fcm_token']}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(['POST'], detail=False)
    def logout(self, request, user_type=None):
        request.user.auth_token.delete()
        return Response(status=200, data={'message': 'Logged out successfully'})
