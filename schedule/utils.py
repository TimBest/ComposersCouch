import datetime

from django.utils import timezone


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
