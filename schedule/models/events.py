# -*- coding: utf-8 -*-
import os, pytz
from datetime import datetime
from dateutil import rrule
from django.contrib.contenttypes import generic
from django.contrib.gis.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.template.defaultfilters import date
from django.utils.translation import ugettext, ugettext_lazy as _

from sorl.thumbnail import ImageField

from accounts.models import MusicianProfile
from contact.models import Location
from photos.models import Image
from schedule.models.calendars import Calendar
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _

from accounts.models import MusicianProfile
from contact.models import Location
from threaded_messages.models import Thread
from photos.models import Image

class DateRange(models.Model):
    start = models.DateTimeField(_("start"))
    end = models.DateTimeField(_("end"),help_text=_("The end time must be later than the start time."))
    class Meta:
        verbose_name = _('dateRange')
        verbose_name_plural = _('dateRanges')
        app_label = 'schedule'

class Show(models.Model):
    info = models.ForeignKey('schedule.Info', verbose_name=_("Info"), related_name='show')
    date = models.ForeignKey(DateRange,
                             verbose_name=_("date"),
                             related_name='show')
    thread = models.OneToOneField(Thread, verbose_name=_("messages"),
                                   related_name='show',
                                   null=True, blank=True)
    approved = models.NullBooleanField(_('approved'), default=None)
    visible = models.BooleanField(_('visible'), default=False)
    turnout = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.GeoManager()
    class Meta:
        verbose_name = _('show')
        verbose_name_plural = _('shows')
        app_label = 'schedule'

def update_visible_and_appoved(sender, instance, **kwargs):
    post_save.disconnect(update_visible_and_appoved, sender=Show, dispatch_uid="update_visibility")
    for event in instance.events.all():
        if event.approved == False:
            instance.approved = False
            instance.visible = False
            break
        if event.visible == True:
            instance.visible = True
    instance.save()
    post_save.connect(update_visible_and_appoved, sender=Show, dispatch_uid="update_visibility")

post_save.connect(update_visible_and_appoved, sender=Show, dispatch_uid="update_visibility")

class EventManager(models.Manager):

    def get_for_object(self, content_object, distinction=None, inherit=True):
        return EventRelation.objects.get_events_for_object(content_object, distinction, inherit)

class Event(models.Model):
    '''
    This model stores meta data for a date.  You can relate this data to many
    other models.
    '''
    show = models.ForeignKey(Show, verbose_name=_("show"), related_name='events')
    calendar = models.ForeignKey(Calendar,
                                  verbose_name=_("calendar"),
                                  related_name='events')
    approved = models.BooleanField(_('approved'), default=False)
    visible = models.BooleanField(_('visible'), default=False)
    objects = EventManager()
    geo = models.GeoManager()

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        app_label = 'schedule'

    def __unicode__(self):
        return ugettext('%(title)s') % {
            'title': self.show.info.title,
        }

    def get_absolute_url(self):
        return reverse('event', args=[self.id])

    def get_location(self):
        try:
            location = self.show.info.location
        except:
            location = None
        if not location:
            location = self.show.info.host.profile.contact_info.location
        return location

    def get_occurrences(self, start, end):
        """
        TODO: return all events in range
        """

        return None
