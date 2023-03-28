from functools import wraps
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import serializers
from typing import TypeVar

T = TypeVar('T', serializers.ModelSerializer, serializers.Serializer, serializers.HyperlinkedModelSerializer,
            serializers.ListSerializer)


def custom_serializer(serializer_class: type(serializers.BaseSerializer) = None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            serializer = serializer_class(data = request.data)
            serializer.is_valid(raise_exception=True)
            kwargs['serializer'] = serializer
            return func(self, request, *args, **kwargs)

        return wrapper

    return decorator
