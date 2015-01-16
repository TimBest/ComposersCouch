import datetime

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.http import Http404
from django.utils import timezone
from django.utils.functional import wraps

from annoying.functions import get_object_or_None


def edit_show(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        from schedule.models import Calendar, Event, Show
        if not request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_URL)
        else:
            show = get_object_or_None(Show, pk=kwargs.get('show_id', None))
            if show:
                event = get_object_or_None(Event, show=show, calendar=request.user.calendar)
                if not event:
                    raise PermissionDenied
            else:
                raise Http404
        return function(request, *args, **kwargs)
    return decorator

def view_show(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        from schedule.models import Calendar, Event, Show
        show = get_object_or_None(Show, pk=kwargs.get('show_id', None))
        if show and request.user.calendar:
            try:
                event = get_object_or_None(Event, show=show, calendar=request.user.calendar)
            except:
                event = None
            if show.visible == False and not event:
                raise PermissionDenied
        else:
            raise Http404
        return function(request, *args, **kwargs)
    return decorator

def coerce_date_dict(date_dict):
    keys = ['year', 'month', 'day', 'hour', 'minute',]
    ret_val = {'year':1, 'month':1, 'day':1, 'hour':0, 'minute': 0,}
    modified = False
    for key in keys:
        try:
            ret_val[key] = int(date_dict[key])
            modified = True
        except KeyError:
            break
    if modified:
        try:
            return datetime.datetime(**ret_val)
        except:
            pass
    return timezone.now()
