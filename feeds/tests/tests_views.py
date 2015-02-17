from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile
from artist.models import ArtistProfile
from artist.views import MusicianContactsView


class ViewsTests(TestCase):
    """  """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles', 'artists', 'members', 'calendars']

    def test_artist_feed_view(self):
        """  """
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

    def test_venue_feed_view(self):
        """  """
        orders = ['new', 'all']
        scopes = ['local', 'all',]
        for order in orders:
            response = self.client.get(reverse('available_venues',
                kwargs={'order': order,
                        'year':2015,
                        'month':02,
                        'day':15,}))
            self.assertEqual(response.status_code, 200)
            response = self.client.get(reverse('available_venues_between',
                kwargs={'order': order,
                        'year':2015,
                        'month':02,
                        'day':15,}))
            self.assertEqual(response.status_code, 200)
            response = self.client.get(reverse('available_venues',
                kwargs={'order': order,
                        'year':2015,
                        'month':02,
                        'day':15,
                        'zipcode':12065}))
            self.assertEqual(response.status_code, 200)
            for scope in scopes:
                response = self.client.get(reverse('venues',
                    kwargs={'order': order,'scope': scope}))
                self.assertEqual(response.status_code, 200)
                response = self.client.get(reverse('venues',
                    kwargs={'order': order,'scope': scope, 'zipcode': 12065}))
                self.assertEqual(response.status_code, 200)
        for order in orders:
            response = self.client.get(reverse('venues',
                kwargs={'order': order,'scope': 'following'}))
            self.assertEqual(response.status_code, 302)
            response = self.client.get(reverse('venues',
                kwargs={'order': order,'scope': 'following', 'zipcode': 12065}))
            self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('signin'),
                                    data={'identification': 'jane@example.com',
                                          'password': 'blowfish'})
        for order in orders:
            response = self.client.get(reverse('venues',
                kwargs={'order': order,'scope': 'following'}))
            self.assertEqual(response.status_code, 200)
            response = self.client.get(reverse('venues',
                kwargs={'order': order,'scope': 'following', 'zipcode': 12065}))
            self.assertEqual(response.status_code, 200)

    def test_request_feed_view(self):
        """  """
        requests_for = ['venue', 'band']
        orders = ['new', 'all', 'expiring']
        scopes = ['local', 'all',]
        for request_for in requests_for:
            for order in orders:
                for scope in scopes:
                    response = self.client.get(reverse('requests',
                        kwargs={'order': order,
                                'for': request_for,
                                'scope': scope}))
                    self.assertEqual(response.status_code, 200)
                    response = self.client.get(reverse('requests',
                        kwargs={'order': order,
                                'for': request_for,
                                'scope': scope,
                                'zipcode': 12065}))
                    self.assertEqual(response.status_code, 200)
        for request_for in requests_for:
            for order in orders:
                response = self.client.get(reverse('requests',
                    kwargs={'order': order,
                            'for': request_for,
                            'scope': 'following'}))
                self.assertEqual(response.status_code, 302)
                response = self.client.get(reverse('requests',
                    kwargs={'order': order,
                            'for': request_for,
                            'scope': 'following',
                            'zipcode': 12065}))
                self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('signin'),
                                    data={'identification': 'jane@example.com',
                                          'password': 'blowfish'})
        for request_for in requests_for:
            for order in orders:
                response = self.client.get(reverse('requests',
                    kwargs={'order': order,
                            'for': request_for,
                            'scope': 'following'}))
                self.assertEqual(response.status_code, 200)
                response = self.client.get(reverse('requests',
                    kwargs={'order': order,
                            'for': request_for,
                            'scope': 'following',
                            'zipcode': 12065}))
                self.assertEqual(response.status_code, 200)

    def test_show_feed_view(self):
        """  """
        orders = ['new', 'all', 'upcoming']
        scopes = ['local', 'all',]
        for order in orders:
            for scope in scopes:
                response = self.client.get(reverse('shows',
                    kwargs={'order': order,'scope': scope}))
                self.assertEqual(response.status_code, 200)
                response = self.client.get(reverse('shows',
                    kwargs={'order': order,'scope': scope, 'zipcode': 12065}))
                self.assertEqual(response.status_code, 200)
        for order in orders:
            response = self.client.get(reverse('shows',
                kwargs={'order': order,'scope': 'following'}))
            self.assertEqual(response.status_code, 302)
            response = self.client.get(reverse('shows',
                kwargs={'order': order,'scope': 'following', 'zipcode': 12065}))
            self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('signin'),
                                    data={'identification': 'jane@example.com',
                                          'password': 'blowfish'})
        for order in orders:
            response = self.client.get(reverse('shows',
                kwargs={'order': order,'scope': 'following'}))
            self.assertEqual(response.status_code, 200)
            response = self.client.get(reverse('shows',
                kwargs={'order': order,'scope': 'following', 'zipcode': 12065}))
            self.assertEqual(response.status_code, 200)

    def test_updates_feed_view(self):
        """  """
        scopes = ['local', 'all',]
        for scope in scopes:
            response = self.client.get(reverse('updates',kwargs={'scope': scope}))
            self.assertEqual(response.status_code, 200)
            response = self.client.get(reverse('updates',
                kwargs={'scope': scope, 'zipcode': 12065}))
            self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('updates',
            kwargs={'scope': 'following'}))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('updates',
            kwargs={'scope': 'following', 'zipcode': 12065}))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('signin'),
                                    data={'identification': 'jane@example.com',
                                          'password': 'blowfish'})
        response = self.client.get(reverse('updates',
            kwargs={'scope': 'following'}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('updates',
            kwargs={'scope': 'following', 'zipcode': 12065}))
        self.assertEqual(response.status_code, 200)
