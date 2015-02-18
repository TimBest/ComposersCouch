import pytz
import datetime

from django.contrib.auth.models import User
from django.test.utils import override_settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import Client

from schedule.models import Calendar, Event
from schedule.views import PERIODS, FILTER


class ViewsTests(TestCase):
    """  """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',
                'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks', 'media', 'calendars', 'info',
                'shows', 'events']

    def test_calendar_views(self):
        """ test views where login is required """
        user = User.objects.get(pk=1)
        url_names = [
            ['calendar', {}],
            ['calendar_create_event', {}],
        ]
        for period in PERIODS:
            url_names.append(['calendar',{'period':period}],)
        for period in PERIODS:
            for filter in FILTER:
                url_names.append(['calendar',{'period':period, 'filter':filter}],)

        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 302)

        self.client.post(reverse('signin'),
                                 data={'identification': 'jane@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)





'''

class TestViews(TestCase):
    fixtures = ['schedule.json']

    def setUp(self):
        self.rule = Rule.objects.create(frequency="DAILY")
        self.calendar = Calendar.objects.create(name="MyCal", slug='MyCalSlug')
        data = {
            'title': 'Recent Event',
            'start': datetime.datetime(2008, 1, 5, 8, 0, tzinfo=pytz.utc),
            'end': datetime.datetime(2008, 1, 5, 9, 0, tzinfo=pytz.utc),
            'end_recurring_period': datetime.datetime(2008, 5, 5, 0, 0, tzinfo=pytz.utc),
            'rule': self.rule,
            'calendar': self.calendar
        }
        self.event = Event.objects.create(**data)

    @override_settings(USE_TZ=False)
    def test_timezone_off(self):
        url = reverse('day_calendar', kwargs={'calendar_slug': self.calendar.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.client.login(username="admin", password="admin")


class TestUrls(TestCase):
    fixtures = ['schedule.json']
    highest_event_id = 7

    def test_calendar_view(self):
        self.response = self.client.get(
            reverse("year_calendar", kwargs={"calendar_slug": 'example'}), {})
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.context[0]["calendar"].name,
                         "Example Calendar")

    def test_calendar_month_view(self):
        self.response = self.client.get(reverse("month_calendar",
                                      kwargs={"calendar_slug": 'example'}),
                              {'year': 2000, 'month': 11})
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.context[0]["calendar"].name,
                         "Example Calendar")
        month = self.response.context[0]["periods"]['month']
        self.assertEqual((month.start, month.end),
                         (datetime.datetime(2000, 11, 1, 0, 0, tzinfo=pytz.utc),
                          datetime.datetime(2000, 12, 1, 0, 0, tzinfo=pytz.utc)))

    def test_event_creation_anonymous_user(self):
        self.response = self.client.get(reverse("calendar_create_event",
                                      kwargs={"calendar_slug": 'example'}), {})
        self.assertEqual(self.response.status_code, 302)

    def test_event_creation_authenticated_user(self):
        self.client.login(username="admin", password="admin")
        self.response = self.client.get(reverse("calendar_create_event",
                                      kwargs={"calendar_slug": 'example'}), {})

        self.assertEqual(self.response.status_code, 200)

        self.response = self.client.post(reverse("calendar_create_event",
                                       kwargs={"calendar_slug": 'example'}),
                               {'description': 'description',
                                'title': 'title',
                                'end_recurring_period_1': '10:22:00', 'end_recurring_period_0': '2008-10-30',
                                'end_recurring_period_2': 'AM',
                                'end_1': '10:22:00', 'end_0': '2008-10-30', 'end_2': 'AM',
                                'start_0': '2008-10-30', 'start_1': '09:21:57', 'start_2': 'AM'
                               })
        self.assertEqual(self.response.status_code, 302)

        highest_event_id = self.highest_event_id
        highest_event_id += 1
        self.response = self.client.get(reverse("event",
                                      kwargs={"event_id": highest_event_id}), {})
        self.assertEqual(self.response.status_code, 200)
        self.client.logout()

    def test_view_event(self):
        self.response = self.client.get(reverse("event", kwargs={"event_id": 1}), {})
        self.assertEqual(self.response.status_code, 200)

    def test_delete_event_anonymous_user(self):
        # Only logged-in users should be able to delete, so we're redirected
        self.response = self.client.get(reverse("delete_event", kwargs={"event_id": 1}), {})
        self.assertEqual(self.response.status_code, 302)

    def test_delete_event_authenticated_user(self):
        self.client.login(username="admin", password="admin")
        # Load the deletion page
        self.response = self.client.get(reverse("delete_event", kwargs={"event_id": 1}), {})
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.context['next'],
                         reverse('day_calendar', args=[Event.objects.get(id=1).calendar.slug]))

        # Delete the event
        self.response = self.client.post(reverse("delete_event", kwargs={"event_id": 1}), {})
        self.assertEqual(self.response.status_code, 302)

        # Since the event is now deleted, we get a 404
        self.response = self.client.get(reverse("delete_event", kwargs={"event_id": 1}), {})
        self.assertEqual(self.response.status_code, 404)
        self.client.logout()
'''
