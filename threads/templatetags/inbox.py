from __future__ import unicode_literals

from django.template.defaultfilters import date
from django.utils.timezone import localtime

import datetime
from threads.models import cached_inbox_count_for


def compact_date(value, same_day, same_year, other, timezone_active=True):
    """
    Output a date as short as possible.

    The argument must provide 3 patterns: for same day, for same year, otherwise
    Typical usage: |compact_date("G:i,j b,j/n/y")

    """
    if timezone_active:
        value = localtime(value)
    today = datetime.date.today()
    if value.date() == today:
        return date(value, same_day)
    elif value.year == today.year:
        return date(value, same_year)
    else:
        return date(value, other)

def local_time(value, format):
    """
    Output a date as localtime
    """
    value = localtime(value)
    return date(value, format)


InboxGlobals = {
    'inbox_count': cached_inbox_count_for,
    'compact_date': compact_date,
    'local_time': local_time,
}
