from django import template
from django.core.urlresolvers import reverse


register = template.Library()

@register.simple_tag
def querystring_for_date(date, num=3):
    query_string = '?'
    qs_parts = ['year=%d', 'month=%d', 'day=%d', 'hour=%d', 'minute=%d', 'second=%d']
    qs_vars = (date.year, date.month, date.day, date.hour, date.minute, date.second)
    query_string += '&'.join(qs_parts[:num]) % qs_vars[:num]
    return query_string

@register.simple_tag
def prev_url(period):
    return '%s%s' % (
        reverse("calendar", kwargs=dict(period=period.__class__.__name__.lower())),
        querystring_for_date(period.prev().start))

@register.simple_tag
def next_url(period):
    return '%s%s' % (
        reverse("calendar", kwargs=dict(period=period.__class__.__name__.lower())),
        querystring_for_date(period.next().start))
