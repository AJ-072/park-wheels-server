from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.parsers import MultiPartParser, FormParser

from ...authentication import BearerTokenAuthentication
from ...decorator import custom_serializer
from ...permissions import IsClient
from ...serializers import UserSerializer, ChangePasswordSerializer


class ClientViewSet(GenericViewSet):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return self.request.user

    @action(methods=['GET'], url_path='user', detail=False)
    def user(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['PUT'], url_path='update', detail=False)
    def updateUser(self, request, *args, **kwargs):
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
