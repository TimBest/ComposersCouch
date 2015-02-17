from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import RequestFactory

from threads import views

class ViewsTests(TestCase):
    """  """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',  
                 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks', 'media', 'venues']

    def test_inbox_views(self):
        """  """
        user = User.objects.get(pk=2)
        url_names = [
            ['threads:inbox',   {}],
            ['threads:sent',    {}],
            ['threads:trash',   {}],
            ['threads:compose', {}],
            ['threads:compose', {'recipient':user.username}],
        ]

        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertRedirects(response, '%s?next=%s' % (reverse('signin'),
                                 response.request['PATH_INFO']),
                                 status_code=302, target_status_code=200,)

        self.client.post(reverse('signin'),
                                 data={'identification': 'john@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)

    def test_thread_views(self):
        url_names = [
            ['threads:detail',     {'thread_id':1}],
        ]

        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertRedirects(response, '%s?next=%s' % (reverse('signin'),
                                 response.request['PATH_INFO']),
                                 status_code=302, target_status_code=200,)
        # user with out permission is denied
        self.client.post(reverse('signin'),
                                 data={'identification': 'john@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 403)
        self.client.logout()

        # user with permission is redirected
        self.client.post(reverse('signin'),
                                 data={'identification': 'jane@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)

    def test_thread_reply_view(self):
        url_names = [
            ['threads:reply', {'thread_id':1},
             {"body": "hey thanks for getting in touch. glad all is well",}],
        ]

        for url_name in url_names:
            response = self.client.post(reverse(url_name[0], kwargs=url_name[1]),
                                        data=url_name[2])
            self.assertRedirects(response, '%s?next=%s' % (reverse('signin'),
                                 response.request['PATH_INFO']),
                                 status_code=302, target_status_code=200,)
        # user with out permission is denied
        self.client.post(reverse('signin'),
                                 data={'identification': 'john@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.post(reverse(url_name[0], kwargs=url_name[1]),
                                        data=url_name[2])
            self.assertEqual(response.status_code, 403)
        self.client.logout()

        # user with permission is redirected
        self.client.post(reverse('signin'),
                                 data={'identification': 'jane@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.post(reverse(url_name[0], kwargs=url_name[1]),
                                        data=url_name[2])
            self.assertEqual(response.status_code, 200)

    def test_thread_batch_update_view(self):
        url_names = [
            ['threads:batch_update', {}, {"batchupdateids":[1,2]}],
        ]

        for url_name in url_names:
            response = self.client.post(reverse(url_name[0], kwargs=url_name[1]),
                                        data=url_name[2])
            self.assertRedirects(response, '%s?next=%s' % (reverse('signin'),
                                 response.request['PATH_INFO']),
                                 status_code=302, target_status_code=200,)

        # user with permission is redirected
        self.client.post(reverse('signin'),
                                 data={'identification': 'jane@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.post(reverse(url_name[0], kwargs=url_name[1]),
                                        data=url_name[2])
            self.assertEqual(response.status_code, 302)
