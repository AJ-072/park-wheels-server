from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(http_method_names=['POST'])
def sign_up(request: Request):

    return Response()
