import pytz
import datetime

from django.contrib.auth.models import User
from django.test.utils import override_settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import Client

from schedule.models import Calendar, Event
from schedule.views import PERIODS, FILTER


class ViewsTests(TestCase):
    """  """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',
                'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks', 'media', 'calendars', 'info',
                'shows', 'events', 'venues']

    def test_calendar_views(self):
        """ test views where login is required """
        user = User.objects.get(pk=1)
        url_names = [
            ['calendar', {}],
            ['calendar_create_event', {}],

        ]
        for period in PERIODS:
            url_names.append(['calendar',{'period':period}],)
        for period in PERIODS:
            for filter in FILTER:
                url_names.append(
                    ['calendar',{'period':period, 'filter':filter}],
                )

        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 302)

        self.client.post(reverse('signin'),
                                 data={'identification': 'jane@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)


    def test_confirm_deny_show_views(self):
        """ test views where thread participant is required """
        url_names = [
            ['show_confirm', {'show':1}],
            ['show_deny',    {'show':1}],
        ]
        # No user redirects to login
        for url_name in url_names:
            response = self.client.post(reverse(url_name[0]), url_name[1])
            self.assertRedirects(response, '%s?next=%s' % (reverse('signin'),
                                 response.request['PATH_INFO']),
                                 status_code=302, target_status_code=200,)

        # user with out permission is denied
        self.client.post(reverse('signin'),
                                 data={'identification': 'john@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.post(reverse(url_name[0]), url_name[1])
            self.assertEqual(response.status_code, 403)
        self.client.logout()

        # user with permission is redirected
        self.client.post(reverse('signin'),
                                 data={'identification': 'jane@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.post(reverse(url_name[0]), url_name[1])
            self.assertEqual(response.status_code, 302)
        # POST is required
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0]), url_name[1])
            self.assertEqual(response.status_code, 405)

    def test_show_views(self):
        """ test views where login is required """
        user = User.objects.get(pk=1)
        url_names = [
            ['edit_event',                {'show_id':1}],
            #['calendar_request_to_event', {'request_id':1}],
            #['show_message',              {'thread_id':4}],
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

    '''def test_show_views(self):
        """ test views where login is required """
        user = User.objects.get(pk=1)
        url_names = [
            ['show', {'show_id':1}],
        ]

        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)

        self.client.post(reverse('signin'),
                                 data={'identification': 'jane@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)'''
