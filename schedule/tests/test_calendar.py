from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from schedule.models import Event, Calendar, DateRange
from schedule.periods import Period, Day

class TestCalendar(TestCase):
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',
                 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks', 'media', 'calendars', 'info',
                'shows', 'events']

    def setUp(self):
        self.calendar = Calendar.objects.get(pk=2)
        for count,event in enumerate(self.calendar.events.all()):
            event.show.date.start = timezone.now() + timedelta(days=count+1)
            event.show.date.end = timezone.now() + timedelta(days=count+1)
            event.show.date.save()

    def __create_event(self, calendar, start, end):
        show = Show.objects.get(pk=1)
        show.date = DateRange(start=start, end=end)
        return Event (show=show, calendar=calendar,
                      approved=True, visible=True,)

    def test_get_or_create_calendar_for_object_without_calendar(self):
        """ Test create calendar """
        user = User.objects.get(pk=1)
        user.pk = 4
        user.username = "calendarTest"
        calendar = Calendar.objects.get_or_create_calendar(user=user, name='My Cal')
        user.save()
        self.assertEquals(calendar.name, 'My Cal')

    def test_get_or_create_calendar_for_object_with_calendar(self):
        """ Test get calendar """
        user = User.objects.get(pk=1)
        calendar_0 = user.calendar
        calendar_1 = Calendar.objects.get_or_create_calendar(user=user)
        self.assertEquals(calendar_0, calendar_1)

    def test_calendar_get_recent(self):
        """ Test get upcoming events for calendar """
        for count,event in enumerate(self.calendar.get_recent()):
            self.assertEquals(count+1, event.pk)

    def test_calendar_get_yearly_events(self):
        """ Test get yearly events """
        self.assertEquals(set(self.calendar.events.all()), set(self.calendar.get_yearly_events()))
        self.assertEquals(set([]), set(self.calendar.get_yearly_events(year=2014)))

    def test_calendar_get_prev_next_event(self):
        """ Test get previous and get next event """
        event = Event.objects.get(pk=2)
        prev = self.calendar.get_prev_event(event.show.date.start)
        next = self.calendar.get_next_event(event.show.date.end)
        self.assertEquals(prev.pk, 1)
        self.assertEquals(next.pk, 3)

    def test_calendar_get_events_in_range(self):
        """ Test get previous and get next event """
        event_1 = Event.objects.get(pk=1)
        event_3 = Event.objects.get(pk=3)
        events = self.calendar.get_events_in_range(start=event_1.show.date.start, end= event_3.show.date.end)
        self.assertEquals(set(self.calendar.events.all()), set(events))
        events = self.calendar.get_events_in_range(
            start=event_1.show.date.start - timedelta(days=2),
            end=event_1.show.date.start - timedelta(days=1)
        )
        self.assertEquals(set([]), set(events))
        events = self.calendar.get_events_in_range(
            start=event_3.show.date.end +  timedelta(days=1),
            end=event_3.show.date.end + timedelta(days=2)
        )
        self.assertEquals(set([]), set(events))
