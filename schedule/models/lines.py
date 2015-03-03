from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _

from annoying.functions import get_object_or_None
from schedule.models.events import Event


class Line(models.Model):
    current = models.OneToOneField(Event, verbose_name=_("current_event"),
                                   related_name='line', primary_key=True)
    next = models.ForeignKey(Event, blank=True, null=True,
                                verbose_name=_("next_event"),
                                related_name='pervious_lines')
    # starting point is the location of the current event and end point is the location of the next event
    line = models.LineStringField(srid=4326, verbose_name="line",
                                  blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('line')
        app_label = 'schedule'

def create_or_update_line(sender, instance, **kwargs):
    """ """
    calendar = instance.calendar
    if instance.approved:
        line, created = Line.objects.get_or_create(current=instance)
        line.save()
    else:
        # if the current instance is denied has a line remove it
        line = get_object_or_None(Line, current=instance)
        if line:
            line.delete()

    next_event = calendar.get_next_event(in_datetime=instance.show.date.start)
    prev_event = calendar.get_prev_event(in_datetime=instance.show.date.start)
    """if next_event and prev_event:
        events = calendar.get_events_in_range(
            start = prev_event.show.date.start,
            end   = next_event.show.date.start,
        )
    elif next_event:
        events = calendar.get_events_in_range(
            end   = next_event.show.date.start,
        )
    elif prev_event:
        events = calendar.get_events_in_range(
            start = prev_event.show.date.start,
        )
    else:"""
    events = calendar.events.filter(approved=True)
    events = events.order_by('show__date__start')
    prev_line = None
    for event in events:
        update_line(prev_line, calendar, event)
        prev_line = event.line
    update_line(prev_line, calendar)

def update_line(line, calendar, next_event=None):
    if line:
        if next_event:
            line.next = next_event
            line.line = LineString(
                line.current.get_location().zip_code.point,
                next_event.get_location().zip_code.point
            )
        elif not line.next:
            line.line = LineString(
                line.current.get_location().zip_code.point,
                calendar.owner.profile.contact_info.location.zip_code.point
            )
        line.save()

post_save.connect(create_or_update_line, sender=Event, dispatch_uid="create_or_update_line")
