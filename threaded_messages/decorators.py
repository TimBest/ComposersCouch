from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.utils.functional import wraps

from annoying.functions import get_object_or_None
from threaded_messages.models import Thread


def is_participant(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_URL)
        else:
            thread_id = kwargs.get('thread_id', None)
            if thread_id:
                thread = get_object_or_None(Thread, id=thread_id)
                for p in thread.participants.all():
                    if p.user == request.user:
                        return function(request, *args, **kwargs)
            return PermissionDenied
    return decorator
