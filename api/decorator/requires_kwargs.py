from rest_framework.exceptions import MethodNotAllowed
from functools import wraps


def requires_kwargs(required_kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            missing_kwargs = [kwarg for kwarg in required_kwargs if kwarg not in kwargs]
            if missing_kwargs:
                raise MethodNotAllowed
            return func(self, request, *args, **kwargs)

        return wrapper

    return decorator
