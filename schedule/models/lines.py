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
    if next_event and prev_event:
        lines_to_update = Line.objects.order_by('current__show__date__start').filter(
            current__show__date__start__gte=prev_event.show.date.start,
            current__show__date__start__lte=next_event.show.date.start,
            current__approved=True,
        )
    elif next_event:
        lines_to_update = Line.objects.order_by('current__show__date__start').filter(
            current__show__date__start__lte=next_event.show.date.start,
            current__approved=True,
        )
    elif prev_event:
        lines_to_update = Line.objects.order_by('current__show__date__start').filter(
            current__show__date__start__gte=prev_event.show.date.start,
            current__approved=True,
        )
    else:
        lines_to_update = Line.objects.all()
    prev_line = None
    for line in lines_to_update:
        update_line(prev_line, calendar, line.current)
        prev_line = line
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
