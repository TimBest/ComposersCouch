from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.utils.functional import wraps


def is_venue(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_URL)
        else:
            if request.user.profile.profile_type != 'v':
                raise PermissionDenied
        return function(request, *args, **kwargs)
    return decorator

def is_artist(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_URL)
        else:
            if request.user.profile.profile_type != 'm':
                raise PermissionDenied
        return function(request, *args, **kwargs)
    return decorator
