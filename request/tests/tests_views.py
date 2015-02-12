from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile
from artist.models import ArtistProfile
from artist.views import MusicianContactsView


class ViewsTests(TestCase):
    """  """
    fixtures = ['user']

    def test_artist_feed_view(self):
        """  """
        pass
        orders = ['new', 'all']
        scopes = ['local', 'all',]
        for order in orders:
            response = self.client.get(reverse('available_artists',
                kwargs={'order': order,
                        'year':2015,
                        'month':02,
                        'day':15,}))
            self.assertEqual(response.status_code, 200)
