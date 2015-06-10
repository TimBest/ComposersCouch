from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase



class ViewsTests(TestCase):
    """  """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles', 'artists', 'threads', 'messages',
                'participants', 'privateRequests', 'dates', 'calendars',
                'venues', 'requestParticipants', 'publicRequests', ]

    def test_request_views(self):
        """ test views where login is required """
        user = User.objects.get(pk=1)
        url_names = [
            ['private_requests', {}],
            ['sent_private_requests', {}],
            ['public_requests', {}],
            ['public_applications', {}],
            ['request_write', {}],
            ['request_write', {'username':user.username}],
            ['public_band_request', {}],
            ['request_appy_to_band', {'request_id':1}],
        ]

        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 302)

        self.client.post(reverse('login'),
                                 data={'identification': 'jane@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)

class ParticipantViewsTests(TestCase):
    """  """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles', 'artists', 'threads', 'messages',
                'participants', 'privateRequests', 'dates', 'calendars',
                'venues', 'requestParticipants', 'publicRequests',
                'applications']

    def test_request_participant_views(self):
        """ test views where thread participant is required """
        url_names = [
            ['request_detail',   {'thread_id':1}],
            ['request_edit',     {'request_id':1}],
            ['application_view', {'thread_id':2}],
        ]
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 302)

        self.client.post(reverse('login'),
                                 data={'identification': 'john@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 403)
        self.client.logout()

        self.client.post(reverse('login'),
                                 data={'identification': 'jane@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)

class IsArtistViewsTests(TestCase):
    """  """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles', 'artists', 'threads', 'messages',
                'participants', 'privateRequests', 'dates', 'calendars',
                'venues', 'requestParticipants', 'publicRequests',
                'applications']

    def test_is_artist_views(self):
        """ test views where thread participant is required """
        url_names = [
            ['public_request', {}],
            ['request_appy_to_venue', {'request_id':1}],
        ]
        # login to view
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 302)

        # fans can't view
        self.client.post(reverse('login'),
                                 data={'identification': 'john@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 403)
        self.client.logout()

        # venues can't view
        self.client.post(reverse('login'),
                                 data={'identification': 'arie@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 403)
        self.client.logout()

        # artists can view
        self.client.post(reverse('login'),
                                 data={'identification': 'jane@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)

    def test_accept_decline_request_views(self):
        """ test views where thread participant is required """
        url_names = [
            ['request_accept',   {'private_request':1}],
            ['request_decline',     {'private_request':1}],
            ['approve_public_request', {'application':1}],
            ['deny_public_request', {'application':1}],
        ]
        # No user redirects to login
        for url_name in url_names:
            response = self.client.post(reverse(url_name[0]), url_name[1])
            self.assertRedirects(response, '%s?next=%s' % (reverse('login'),
                                 response.request['PATH_INFO']),
                                 status_code=302, target_status_code=200,)

        # user with out permission is denied
        self.client.post(reverse('login'),
                                 data={'identification': 'john@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.post(reverse(url_name[0]), url_name[1])
            self.assertEqual(response.status_code, 403)
        self.client.logout()

        # user with permission is redirected
        self.client.post(reverse('login'),
                                 data={'identification': 'arie@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.post(reverse(url_name[0]), url_name[1])
            self.assertEqual(response.status_code, 302)
        # POST is required
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0]), url_name[1])
            self.assertEqual(response.status_code, 405)
