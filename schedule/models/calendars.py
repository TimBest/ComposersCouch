# -*- coding: utf-8 -*-
import datetime, pytz
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from annoying.functions import get_object_or_None


class CalendarManager(models.Manager):
    """ """

    def get_or_create_calendar(self, user, name=None):
        """ """
        calendar = get_object_or_None(Calendar, owner=user)
        if calendar is None:
            if name is None:
                calendar = Calendar(name=unicode(user))
            else:
                calendar = Calendar(name=name)
            calendar.slug = slugify(calendar.name)
            calendar.owner = user
            calendar.save()
        return calendar


class Calendar(models.Model):
    """
    This is for grouping events so that batch relations can be made to all
    events.
    """

    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200)
    owner = models.OneToOneField(User, unique=True,
                                 verbose_name=_('owner'),
                                 related_name='calendar')
    objects = CalendarManager()

    class Meta:
        verbose_name = _('calendar')
        verbose_name_plural = _('calendar')
        app_label = 'schedule'

    def __unicode__(self):
        return self.name

    @property
    def events(self):
        return self.event_set

    def get_recent(self, in_datetime=datetime.datetime.now(), tzinfo=pytz.utc):
        """
        This shortcut function allows you to get events that have started
        recently.

        in_datetime is the datetime you want to check against.  It defaults to
        datetime.datetime.now
        """
        return self.events.order_by('show__date__start').filter(show__date__start__gte=timezone.now(), approved=True)

    def get_yearly_events(self, year=datetime.datetime.now().date().year,  tzinfo=pytz.utc):
        """
        This shortcut function allows you to get events that will or haveb
        hapened in the given year.
        """
        start = datetime.datetime(year, 1, 1).replace(tzinfo=tzinfo)
        end = datetime.datetime(year+1, 1, 1).replace(tzinfo=tzinfo)
        return self.events.order_by('show__date__start').filter(
            show__date__start__gte=start,
            show__date__start__lt=end,
            approved=True
        )

    def get_prev_event(self, in_datetime=datetime.datetime.now(), tzinfo=pytz.utc):
        """
        This shortcut function allows you to get the last event to start since the
        given date.
        """
        date = in_datetime.replace(tzinfo=tzinfo)
        try:
            return self.events.order_by('-show__date__start').filter(
                show__date__end__lt=date,
                approved=True
            )[0]
        except:
            return None

    def get_next_event(self, in_datetime=datetime.datetime.now(), tzinfo=pytz.utc):
        """
        This shortcut function allows you to get the next event to start after the
        given date.
        """
        date = in_datetime.replace(tzinfo=tzinfo)
        try:
            return self.events.order_by('show__date__start').filter(
                show__date__start__gt=date,
                approved=True
            )[0]
        except:
            return None

    def get_events_in_range(self, start=None, end=None, tzinfo=pytz.utc):
        """
        This shortcut function allows you to get the next event to start after the
        given date.
        """
        if start:
            start = start.replace(tzinfo=tzinfo)
        if end:
            end = end.replace(tzinfo=tzinfo)
        if start and end:
            return self.events.filter(
                show__date__start__gte=start,
                show__date__start__lte=end,
                approved=True,
            )
        elif start:
            return self.events.filter(
                show__date__start__gte=start,
                approved=True,
            )
        elif end:
            return self.events.filter(
                show__date__start__lte=end,
                approved=True,
            )
        else:
            return None
