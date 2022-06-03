import json

from django.http import HttpResponse
from rest_framework import status


def admin_or_staff_login_required(view_func):
    """[gets token and fetches user id verifying active status.
    If everything is proper delegates to the requested view]
    Args:
        view_func ([request]): [the get,post etc view requested]
    """

    def wrapper(request, *args, **kwargs):
        result = {}
        try:
            user = request.user
            if user.is_staff or user.is_superuser:
                return view_func(request, *args, **kwargs)
            return HttpResponse('Unauthorized access is detected', status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            result['message'] = 'some other issue please try after some time'
            return HttpResponse(json.dumps(result), status=status.HTTP_401_UNAUTHORIZED)

    return wrapper
