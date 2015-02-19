from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _

from annoying.functions import get_object_or_None
from schedule.models.events import Event


class Line(models.Model):
    current = models.OneToOneField(Event, verbose_name=_("current_event"),
                                   related_name='line', primary_key=True)
    next = models.OneToOneField(Event, blank=True, null=True,
                                verbose_name=_("next_event"),
                                related_name='pervious_line')
    # starting point is the location of the current event and end point is the location of the next event
    line = models.LineStringField(srid=4326, verbose_name="line",
                                  blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('line')
        app_label = 'schedule'


def create_or_update_line(sender, instance, **kwargs):
    """ """
    lines_to_update = []
    # get line where next = instance (line_1)
    line_1 = get_object_or_None(Line, next=instance)
    if line_1:
        line_1.next = None
        line_1.save()
        lines_to_update.append(line_1)

    #get line where current = instance (line_2)
    line_2, created = Line.objects.get_or_create(current=instance)

    line_2.next = None
    line_2.save()
    lines_to_update.append(line_2)

    # get new previous event (line_3)
    prev_event = instance.calendar.get_prev_event(
                    in_datetime=instance.show.date.start)
    if prev_event:
        prev_event.line.next = None
        lines_to_update.append(prev_event.line)
        prev_event.line.save()

    for line in lines_to_update:
        update_line(line, instance.calendar)


def update_line(line, calendar):
    next_event = calendar.get_next_event(in_datetime=line.current.show.date.start)
    if next_event:
        line.next = next_event
        line.line = LineString(
            line.current.get_location().zip_code.point,
            next_event.get_location().zip_code.point
        )
    else:
        line.next = None
        line.line = LineString(
            line.current.get_location().zip_code.point,
            calendar.owner.profile.contact_info.location.zip_code.point
        )
    line.save()



post_save.connect(create_or_update_line, sender=Event, dispatch_uid="create_or_update_line")
