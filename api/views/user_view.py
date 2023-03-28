from rest_framework.views import APIView
from api.serializers.user_serializer import UserSerializer
from rest_framework.response import Response


class UserView(APIView):
    def get(self, request, user_type=None):
        return Response({"user": UserSerializer(self.request.user).data}, status=200)
