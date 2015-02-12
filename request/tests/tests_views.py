from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile


class ViewsTests(TestCase):
    """  """
    fixtures = ['users', 'profiles', 'artists', 'calendars']

    def test_request_views(self):
        """ test views where login is required """
        url_names = ['private_requests', 'sent_private_requests',
                     'public_requests', 'public_applications', 'request_write',]
        for url_name in url_names:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 302)

        self.client.post(reverse('signin'),
                                 data={'identification': 'jane@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)
