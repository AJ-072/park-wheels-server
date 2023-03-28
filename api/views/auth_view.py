from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
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


@api_view(["POST"])
@permission_classes((AllowAny,))
def signin(request, user_type=None):
    credential_serializer = LoginCredentialSerializer(data=request.data)
    if not credential_serializer.is_valid():
        return Response(credential_serializer.errors, status=HTTP_400_BAD_REQUEST)
    user_info = authenticate(
        username=credential_serializer.data['username'],
        password=credential_serializer.data['password']
    )
    if not user_info:
        return Response({'message': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)

    # TOKEN STUFF
    token, _ = Token.objects.get_or_create(user=user_info)

    # is_expired, token = token_expire_handler(token)  # The implementation will be described further
    user_serialized = UserSerializer(user_info)
    return Response({
        'user': user_serialized.data,
        'expires_in': expires_in(token),
        'token': token.key
    }, status=HTTP_200_OK)


@api_view(["POST"])
@permission_classes((AllowAny,))
def signup(request, user_type=None):
    signup_serializer = UserSerializer(data=request.data)
    if not signup_serializer.is_valid():
        return Response(signup_serializer.errors, status=HTTP_400_BAD_REQUEST)
    user_info = signup_serializer.create(signup_serializer.validated_data)

    # TOKEN STUFF
    token, _ = Token.objects.get_or_create(user=user_info)

    # is_expired, token = token_expire_handler(token)  # The implementation will be described further
    user_serialized = UserSerializer(user_info)

    return Response({
        'user': user_serialized.data,
        'expires_in': expires_in(token),
        'token': token.key
    }, status=HTTP_201_CREATED)
