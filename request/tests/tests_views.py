from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.test import TestCase

from accounts.models import Profile
from request.models import PublicRequest
from threads.models import Thread


class ViewsTests(TestCase):
    """  """
    fixtures = ['users', 'profiles', 'artists', 'threads', 'messages',
                'participants', 'privateRequests', 'dates', 'calendars',
                'venues', 'requestParticipants', 'publicRequests', 'zipcodes',]

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

        self.client.post(reverse('signin'),
                                 data={'identification': 'jane@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)

class ParticipantViewsTests(TestCase):
    """  """
    fixtures = ['users', 'profiles', 'artists', 'threads', 'messages',
                'participants', 'privateRequests', 'dates', 'calendars',
                'venues', 'requestParticipants', 'publicRequests', 'zipcodes',
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

        self.client.post(reverse('signin'),
                                 data={'identification': 'john@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 403)
        self.client.logout()

        self.client.post(reverse('signin'),
                                 data={'identification': 'jane@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)
