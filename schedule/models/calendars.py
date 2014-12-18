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
    """
    >>> user1 = User(username='tony')
    >>> user1.save()
    """

    def get_or_create_calendar(self, user, distinction=None, name=None):
        """
        >>> user = User(username="jeremy")
        >>> user.save()
        >>> calendar = Calendar.objects.get_or_create_calendar_for_object(user, name = "Jeremy's Calendar")
        >>> calendar.name
        "Jeremy's Calendar"
        """
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
    '''
    This is for grouping events so that batch relations can be made to all
    events.  An example would be a project calendar.

    name: the name of the calendar
    events: all the events contained within the calendar.
    >>> calendar = Calendar(name = 'Test Calendar')
    >>> calendar.save()
    >>> data = {
    ...         'title': 'Recent Event',
    ...         'start': datetime.datetime(2008, 1, 5, 0, 0),
    ...         'end': datetime.datetime(2008, 1, 10, 0, 0)
    ...        }
    >>> event = Event(**data)
    >>> event.save()
    >>> calendar.events.add(event)
    >>> data = {
    ...         'title': 'Upcoming Event',
    ...         'start': datetime.datetime(2008, 1, 1, 0, 0),
    ...         'end': datetime.datetime(2008, 1, 4, 0, 0)
    ...        }
    >>> event = Event(**data)
    >>> event.save()
    >>> calendar.events.add(event)
    >>> data = {
    ...         'title': 'Current Event',
    ...         'start': datetime.datetime(2008, 1, 3),
    ...         'end': datetime.datetime(2008, 1, 6)
    ...        }
    >>> event = Event(**data)
    >>> event.save()
    >>> calendar.events.add(event)
    '''

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

    def get_recent(self, in_datetime=datetime.datetime.now, tzinfo=pytz.utc):
        """
        This shortcut function allows you to get events that have started
        recently.

        amount is the amount of events you want in the queryset. The default is
        5.

        in_datetime is the datetime you want to check against.  It defaults to
        datetime.datetime.now
        """
        return self.events.order_by('-show__date__start').filter(show__date__start__gte=timezone.now())
    def get_yearly_events(self, year=2014):
        """
        This shortcut function allows you to get events that will or haveb
        hapened in the given year.
        """
        start = datetime.date(year, 1, 1)
        end = datetime.date(year+1, 1, 1)
        return self.events.order_by('-show__date__start').filter(show__date__start__gte=start).filter(show__date__start__lt=end)

    def get_prev_event(self, in_datetime=datetime.datetime.now(), tzinfo=pytz.utc):
        """
        This shortcut function allows you to get the last event to start since the
        given date.
        """
        date = in_datetime.replace(tzinfo=tzinfo)
        try:
            return self.events.order_by('-show__date__end').filter(show__date__end__lte=date)[0]
        except:
            return None
    def get_next_event(self, in_datetime=datetime.datetime.now(), tzinfo=pytz.utc):
        """
        This shortcut function allows you to get the next event to start after the
        given date.
        """
        date = in_datetime.replace(tzinfo=tzinfo)
        try:
            return self.events.order_by('show__date__start').filter(show__date__start__gte=date)[0]
        except:
            return None
    def get_events_in_range(self, start=None, end=None, tzinfo=pytz.utc):
        """
        This shortcut function allows you to get the next event to start after the
        given date.
        """
        start = start.replace(tzinfo=tzinfo)
        end = end.replace(tzinfo=tzinfo)
        try:
            return self.events.order_by('show__date__start').filter(show__date__end__gte=start).filter(show__date__start__lte=end)
        except:
            return None

    def get_absolute_url(self):
        return reverse('calendar_home', kwargs={'calendar_slug': self.slug})

    def add_event_url(self):
        return reverse('calendar_create_event', args=[self.slug])
