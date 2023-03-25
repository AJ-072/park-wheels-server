from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)
from rest_framework.response import Response
from rest_framework.request import Request

from api.serializers.user_serializer import UserSerializer, UserSigninSerializer, UserSignUpSerializer
from api.authentication import token_expire_handler, expires_in


@api_view(["POST"])
@permission_classes((AllowAny,))
def signin(request):
    signin_serializer = UserSigninSerializer(data=request.data)
    if not signin_serializer.is_valid():
        return Response(signin_serializer.errors, status=HTTP_400_BAD_REQUEST)
    user_info = authenticate(
        username=signin_serializer.data['username'],
        password=signin_serializer.data['password']
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
def signup(request):
    signup_serializer = UserSignUpSerializer(data=request.data)
    if not signup_serializer.is_valid():
        return Response(signup_serializer.errors, status=HTTP_400_BAD_REQUEST)
    print(signup_serializer.validated_data)
    user_info = signup_serializer.create()

    # TOKEN STUFF
    token, _ = Token.objects.get_or_create(user=user_info)

    # is_expired, token = token_expire_handler(token)  # The implementation will be described further
    user_serialized = UserSerializer(user_info)

    return Response({
        'user': user_serialized.data,
        'expires_in': expires_in(token),
        'token': token.key
    }, status=HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def user(request: Request):
    if request.method == "GET":
        return Response({
            'user': UserSerializer(request.user).data,
        }, status=HTTP_200_OK)
    if request.method == 'POST':
        update_serializer = UserSignUpSerializer(data=request.data)
        if not update_serializer.is_valid():
            return Response(update_serializer.errors, status=HTTP_400_BAD_REQUEST)
        user_info = update_serializer.update()
        return Response({
            'user': UserSerializer(user_info).data,
        }, status=HTTP_200_OK)
