from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import RequestFactory

from threads import views

class ViewsTests(TestCase):
    """  """
    fixtures = ['users', 'profiles', 'contactInfos','locations', 'contacts',
                'zipcodes', 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks', 'media', 'venues']

    '''def test_inbox_views(self):
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
            ['threads:delete',     {'thread_id':1}],
            ['threads:restore',    {'thread_id':1}],
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
    '''
    '''def test_thread_form_views(self):
        user = User.objects.get(pk=2)
        # create WSGIRequest object
        factory = RequestFactory()
        request = factory.get(reverse('home'))
        request.POST = {"body": "hey thanks for getting in touch. glad all is well",}
        request.user = user

        url_names = [
            ['threads:reply',        {'thread_id':1}],
            #['threads:batch_update', {}],
        ]

        """for url_name in url_names:
            response = self.client.post(reverse(url_name[0], kwargs=url_name[1]))
            self.assertRedirects(response, '%s?next=%s' % (reverse('signin'),
                                 response.request['PATH_INFO']),
                                 status_code=302, target_status_code=200,)
        # user with out permission is denied
        self.client.post(reverse('signin'),
                                 data={'identification': 'john@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.post(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 403)
        self.client.logout()"""

        # user with permission is redirected
        self.client.post(reverse('signin'),
                                 data={'identification': 'jane@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.post(views.message_ajax_reply(request, thread_id=1))
            self.assertEqual(response.status_code, 200)'''
