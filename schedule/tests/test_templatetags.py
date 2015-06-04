import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from schedule.models import Show
from schedule.templatetags.scheduletags import querystring_for_date, has_event_for_show


class TestTemplateTags(TestCase):

    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes',
                'profiles', 'applications', 'publicRequests', 'numApplicants',
                'privateRequests', 'requestParticipants', 'threads', 'messages',
                'participants', 'dates', 'genres', 'albums', 'artists',
                'tracks', 'calendars', 'info', 'shows', 'events',
                'venues']

    def test_querystring_for_datetime(self):
        date = datetime.datetime(2008,1,1,0,0,0)
        query_string=querystring_for_date(date)
        self.assertEqual("?year=2008&month=1&day=1", query_string)

    def test_has_event_for_show(self):
        show = Show.objects.get(pk=1)
        user = User.objects.get(pk=2)
        self.assertTrue(has_event_for_show(user, show))
        show = Show.objects.get(pk=1)
        user = User.objects.get(pk=1)
        self.assertFalse(has_event_for_show(user, show))
        show = Show.objects.get(pk=1)
        user = None
        self.assertFalse(has_event_for_show(user, show))
