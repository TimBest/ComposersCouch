from django.core.urlresolvers import reverse
from django.test import TestCase



class SearchViewsTests(TestCase):
    """  """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles', 'artists', 'threads', 'messages', 'fans',
                'participants', 'privateRequests', 'dates', 'calendars',
                'venues', 'requestParticipants', 'publicRequests', ]

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
