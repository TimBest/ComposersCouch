# -*- coding: utf-8 -*-
import os, pytz
from datetime import datetime
from dateutil import rrule
from django.contrib.contenttypes import generic
from django.contrib.gis.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.template.defaultfilters import date
from django.utils.translation import ugettext, ugettext_lazy as _

from sorl.thumbnail import ImageField
from artist.models import ArtistProfile
from contact.models import Location
from photos.models import Image
from schedule.models.calendars import Calendar
from threads.models import Thread


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

def update_visible_and_approved(sender, instance, **kwargs):
    """
        one non approved event sets the shows visibility and approved to False.
        one visible event sets the shows visibility to True.
        all approved events sets the shows approved to True.
    """
    post_save.disconnect(update_visible_and_approved, sender=Show, dispatch_uid="update_visibility")
    approved = True
    visible = False
    for event in instance.events.all():
        if event.approved == False:
            approved = False
            visible = False
            break
        if event.visible == True:
            visible = True
    instance.visible = visible
    instance.approved = approved
    instance.save()
    post_save.connect(update_visible_and_approved, sender=Show, dispatch_uid="update_visibility")

post_save.connect(update_visible_and_approved, sender=Show, dispatch_uid="update_visibility")

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
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        app_label = 'schedule'

    def __unicode__(self):
        if self.show.info.title:
            return u'%s' % (self.show.info.title,)
        else:
            return u'%s at %s' % (self.show.info.headliner_text, self.show.info.venue_text)

    def get_absolute_url(self):
        return reverse('show', kwargs={'show_id':self.show.id})

    def get_location(self):
        try:
            location = self.show.info.location
        except:
            location = None
        if not location:
            try:
                location = self.show.info.venue.profile.contact_info.location
            except:
                location = self.calendar.owner.profile.contact_info.location
        return location
