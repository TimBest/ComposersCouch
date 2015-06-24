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

        description = ""
        if show.info.headliner:
            description += "Headliner: %s\n" % show.info.headliner
        elif show.info.headliner_text:
            description += "Headliner: %s\n" % show.info.headliner_text
        if show.info.openers_text:
            description += "Openers: %s\n" % show.info.openers_text
        if show.info.venue:
            description += "Venue: %s\n" % show.info.venue
        else:
            description += "Venue: %s\n" % show.info.venue_text
        if show.info.description:
            description += "Description: %s\n" % show.info.description

        ical_event = iEvent()
        ical_event.add('summary', show.info.get_title())
        ical_event.add('description', description)
        ical_event.add('location', show.info.venue)
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
