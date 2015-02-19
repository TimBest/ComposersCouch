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
    """
    TODO: if a new event is being created
          else its an edit so just return
    """
    if not instance.approved:
        return None
    calendar = instance.calendar
    # update previous event's line
    prev_event = calendar.get_prev_event(in_datetime=instance.show.date.start)
    if prev_event:
        # save old next event
        prev_event.next = instance
        #prev_event.line = LineString(
        #    prev_event.get_location().zip_code.point,
        #    instance.get_location().zip_code.point
        #)
        prev_event.save()

    # create or update current line
    next_event = calendar.get_next_event(in_datetime=instance.show.date.start)
    if next_event:
        line_string = LineString(
            instance.get_location().zip_code.point,
            next_event.get_location().zip_code.point,
         )
    else:
        # if no next event assume artist home location
        line_string = LineString(
            instance.get_location().zip_code.point,
            calendar.owner.profile.contact_info.location.zip_code.point
        )

    line = getattr(instance, "line", None)
    if line:
        line.next = next_event
        line.line = line_string
    else:
        line = Line(
            current = instance,
            next = next_event,
            line = line_string,
        )
    line.save()

def create_line_string(start=None, end=None):
    if start and end:
        return LineString(start,end)
    else:
        return None


post_save.connect(create_or_update_line, sender=Event, dispatch_uid="create_or_update_line")
