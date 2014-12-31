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
            calendar = get_object_or_None(Calendar, slug=kwargs.get('calendar_slug', None))
            if show and calendar:
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
        calendar = get_object_or_None(Calendar, slug=kwargs.get('calendar_slug', None))
        show = get_object_or_None(Show, pk=kwargs.get('show_id', None))
        if show and calendar:
            event = get_object_or_None(Event, show=show, calendar=request.user.calendar)
            if show.visible == False and not event:
                raise PermissionDenied
        else:
            raise Http404
        return function(request, *args, **kwargs)
    return decorator

def coerce_date_dict(date_dict):
    keys = ['year', 'month', 'day', 'hour', 'minute',]
    ret_val = {'year':1, 'month':1, 'day':1, 'hour':0, 'minute': 0,}
    for key in keys:
        try:
            ret_val[key] = int(date_dict[key])
        except KeyError:
            break
    try:
        return datetime.datetime(**ret_val)
    except:
        return timezone.now()
