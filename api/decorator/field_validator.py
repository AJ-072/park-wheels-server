from functools import wraps
from rest_framework.exceptions import MethodNotAllowed


def validate_field(values: list, field_name: str = 'status', ):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            instance = self.get_object()
            field_value = getattr(instance, field_name)
            if field_value in values:
                return func(self, request, *args, **kwargs)
            raise MethodNotAllowed(method=request.method)

        return wrapper

    return decorator


def not_none_field(field_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            instance = self.get_object()
            field_value = getattr(instance, field_name)
            if field_value is not None:
                return func(self, request, *args, **kwargs)
            raise MethodNotAllowed

        return wrapper

    return decorator
