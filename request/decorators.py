from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.http import Http404
from django.utils import timezone
from django.utils.functional import wraps

from annoying.functions import get_object_or_None
from request.models import PrivateRequest


def is_participant(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_URL)
        else:
            request_id = kwargs.get('request_id', None)
            if request_id:
                private_request = get_object_or_None(PrivateRequest, id=request_id)
                for participant in private_request.thread.participants.all():
                    if participant.user == request.user:
                        return function(request, *args, **kwargs)
            return PermissionDenied
    return decorator

def can_apply(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_URL)
        else:
            if request.user.profile.profile_type != 'm':
                raise PermissionDenied
        return function(request, *args, **kwargs)
    return decorator
