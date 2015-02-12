from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.test import TestCase

from accounts.models import Profile
from threads.models import Thread


class ViewsTests(TestCase):
    """  """
    fixtures = ['users', 'profiles', 'artists', 'threads', 'messages',
                'participants', 'privateRequests', 'dates', 'calendars',
                'venues',]

    def test_request_views(self):
        """ test views where login is required """
        user = User.objects.get(pk=1)
        url_names = ['private_requests', 'sent_private_requests',
                     'public_requests', 'public_applications', 'request_write',]
        for url_name in url_names:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 302)
        response = self.client.get(
                    reverse('request_write', kwargs={'username':user.username}))
        self.assertEqual(response.status_code, 302)

        self.client.post(reverse('signin'),
                                 data={'identification': 'jane@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)
        response = self.client.get(
                    reverse('request_write', kwargs={'username':user.username}))
        self.assertEqual(response.status_code, 200)

    def test_request_particpant_views(self):
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
                                 data={'identification': 'arie@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            self.assertRaises(PermissionDenied,
                              self.client.get,
                              reverse(url_name[0], kwargs=url_name[1])
            )

        self.client.post(reverse('signin'),
                                 data={'identification': 'jane@example.com',
                                       'password': 'blowfish'})

        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)
