from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.test import TestCase

from accounts.models import Profile
from request.models import PublicRequest
from threads.models import Thread


class SearchViewsTests(TestCase):
    """  """
    fixtures = ['users', 'profiles', 'artists', 'threads', 'messages', 'fans',
                'participants', 'privateRequests', 'dates', 'calendars',
                'venues', 'requestParticipants', 'publicRequests', 'zipcodes',]

    def test_null_search_views(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

    def test_artist_search_views(self):
        response = self.client.get(reverse('search')+"?q=mouse+rat")
        self.assertEqual(response.status_code, 200)

    def test_venue_search_views(self):
        response = self.client.get(reverse('search')+"?q=gasworks")
        self.assertEqual(response.status_code, 200)

    def test_fan_search_views(self):
        response = self.client.get(reverse('search')+"?q=john")
        self.assertEqual(response.status_code, 200)
