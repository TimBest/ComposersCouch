from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile
from artist.models import ArtistProfile
from artist.views import MusicianContactsView


class ViewsTests(TestCase):
    """  """
    fixtures = ['users', 'profiles', 'artists', 'members', 'calendars']

    def test_artist_feed_view(self):
        """  """
        user = User.objects.get(pk=1)
        orders = ['new', 'all']
        scopes = ['local', 'all',]
        for order in orders:
            response = self.client.get(reverse('available_artists',
                kwargs={'order': order,
                        'year':2015,
                        'month':02,
                        'day':15,}))
            self.assertEqual(response.status_code, 200)
            response = self.client.get(reverse('available_artists',
                kwargs={'order': order,
                        'year':2015,
                        'month':02,
                        'day':15,
                        'zipcode':12065}))
            self.assertEqual(response.status_code, 200)
            for scope in scopes:
                response = self.client.get(reverse('artists',
                    kwargs={'order': order,'scope': scope}))
                self.assertEqual(response.status_code, 200)
                response = self.client.get(reverse('artists',
                    kwargs={'order': order,'scope': scope, 'zipcode': 12065}))
                self.assertEqual(response.status_code, 200)
        for order in orders:
            response = self.client.get(reverse('artists',
                kwargs={'order': order,'scope': 'following'}))
            self.assertEqual(response.status_code, 302)
            response = self.client.get(reverse('artists',
                kwargs={'order': order,'scope': 'following', 'zipcode': 12065}))
            self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('signin'),
                                    data={'identification': 'jane@example.com',
                                          'password': 'blowfish'})
        for order in orders:
            response = self.client.get(reverse('artists',
                kwargs={'order': order,'scope': 'following'}))
            self.assertEqual(response.status_code, 200)
            response = self.client.get(reverse('artists',
                kwargs={'order': order,'scope': 'following', 'zipcode': 12065}))
            self.assertEqual(response.status_code, 200)
