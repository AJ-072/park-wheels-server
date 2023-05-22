from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from api.decorator import custom_serializer
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK, HTTP_201_CREATED
)
from rest_framework.response import Response
from rest_framework.request import Request

from api.serializers.user_serializer import UserSerializer, LoginCredentialSerializer
from api.authentication import token_expire_handler, expires_in
from webapp.models import User


class AuthViewSet(GenericViewSet):
    permission_classes = [AllowAny]

    @action(["POST"], detail=False)
    @custom_serializer(serializer_class=LoginCredentialSerializer)
    def signin(self, request, serializer, user_type=None):
        user_info: User = authenticate(
            username=serializer.data['username'],
            password=serializer.data['password']
        )
        if user_info is not None:
            if not user_info.groups.filter(name=user_type).exists():
                return Response(status=403)
        else:
            return Response({'message': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user_info)

        user_serialized = UserSerializer(user_info)
        return Response({
            'user': user_serialized.data,
            'expires_in': expires_in(token),
            'token': token.key
        })

    @action(["POST"], detail=False)
    @custom_serializer(serializer_class=UserSerializer)
    def signup(self, request, serializer, user_type=None):
        user_info = serializer.create(serializer.validated_data)
        group = Group.objects.get(name=user_type)
        user_info.groups.add(group)

        token, _ = Token.objects.get_or_create(user=user_info)

        user_serialized = UserSerializer(user_info)

        return Response({
            'user': user_serialized.data,
            'expires_in': expires_in(token),
            'token': token.key
        }, status=HTTP_201_CREATED)

    @action(detail=False, methods=['GET'])
    def send_noti(self, request, user_type=None):
        from ..functions.push_notifications import send_push_notification

        send_push_notification(
            token='fKXvOB0sCKyxQhgB7_LoUr:APA91bH-k0Yanph-DUr9hq4w2lmsWDjrPfoVdQcL1F_DGBDNTBMHeTNVY3YQmByho-rCmttrrL6SXIgZrYH56NKpQSmJPULhPLZhMroEEbG5xnDdf60RGqFp8EGy0bteYwaMQpcLOfEw',
            title="title", body='body')
        return Response("send successfully")
