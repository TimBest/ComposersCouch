from django.core.urlresolvers import reverse
from django.utils import timezone

from annoying.functions import get_object_or_None
from schedule.models import Event


def querystring_for_date(date, num=3):
    query_string = '?'
    qs_parts = ['year=%d', 'month=%d', 'day=%d', 'hour=%d', 'minute=%d', 'second=%d']
    qs_vars = (date.year, date.month, date.day, date.hour, date.minute, date.second)
    query_string += '&'.join(qs_parts[:num]) % qs_vars[:num]
    return query_string

def prev_url(period, filter):
    return '%s%s' % (
        reverse("calendar", kwargs=dict(period=period.__class__.__name__.lower(), filter=filter)),
        querystring_for_date(period.prev().start))

def next_url(period, filter):
    return '%s%s' % (
        reverse("calendar", kwargs=dict(period=period.__class__.__name__.lower(), filter=filter)),
        querystring_for_date(period.next().start))

def has_event_for_show(value, arg):
    # value: request.user
    # arg: show
    try:
        event = get_object_or_None(Event, show=arg, calendar=value.calendar)
    except:
        event = None
    if event:
        return True
    else:
        return False

def hide_confirm(show, user):
    event = get_object_or_None(Event, show=show, calendar=user.calendar)
    try:
        if event.approved:
            return "hidden"
    except:
        pass
    return None

def hide_deny(show, user):
    event = get_object_or_None(Event, show=show, calendar=user.calendar)
    try:
        if not event.approved:
            return "hidden"
    except:
        pass
    return None

def make_naive(date):
    return timezone.make_naive(date)

ScheduleGlobals = {
    'querystring_for_date': querystring_for_date,
    'prev_url': prev_url,
    'next_url': next_url,
    'has_event_for_show': has_event_for_show,
    'hide_confirm': hide_confirm,
    'hide_deny': hide_deny,
    'make_naive': make_naive,
}
