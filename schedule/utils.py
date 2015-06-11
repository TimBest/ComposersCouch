from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.utils import timezone

from datetime import datetime
from icalendar import Calendar as iCalendar
from icalendar import Event as iEvent

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
            return datetime(**ret_val)
        except:
            pass
    return timezone.now()

def export(request, events, year=None):
    cal = iCalendar()
    site = Site.objects.get_current()

    cal.add('prodid', '-//%s Events Calendar//%s//' % (site.name, site.domain))
    cal.add('version', '2.0')

    site_token = site.domain.split('.')
    site_token.reverse()
    site_token = '.'.join(site_token)

    for event in events:
        show = event.show
        ical_event = iEvent()
        ical_event.add('summary', show.info.get_title())
        description = "Headliner: " + show.info.headliner_text + "\n"
        if show.info.openers_text:
            description += "Openers: " + show.info.openers_text + "\n"
        description += "Venue: " + show.info.venue_text + "\n"
        if show.info.openers_text:
            description += "Description: " + show.info.description + "\n"
        ical_event.add('description', description)
        ical_event.add('location', show.info.venue_text)
        ical_event.add('dtstart', show.date.start)
        ical_event.add('dtend', show.date.end and show.date.end or show.date.start)
        ical_event.add('dtstamp', show.date.end and show.date.end or show.date.start)
        ical_event['uid'] = '%d.event.events.%s' % (show.id, site_token)
        cal.add_component(ical_event)

    response = HttpResponse(cal.to_ical(), content_type="text/calendar")
    # title or headliner
    if year:
        response['Content-Disposition'] = 'attachment; filename=%ss-calendar-%s.ics' % (slugify(request.user.profile), year)
    else:
        response['Content-Disposition'] = 'attachment; filename=%s.ics' % slugify(events[0])
    return response
