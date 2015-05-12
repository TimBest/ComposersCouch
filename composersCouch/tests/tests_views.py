from django.core.urlresolvers import reverse
from django.test import TestCase


class TemplateViewsTests(TestCase):
    """  """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes',
                'profiles', 'artists', 'members', 'calendars', 'albums',
                'media', 'tracks','genres']

    def test_about_view(self):
        url_names = [
            ['home',  {}],
            ['about',  {}],
            ['team',  {}],
            ['credit',  {}],
            ['learn',  {}],
            ['changelog',  {}],
            ['pipeline',  {}],
            ['sitemap',  {}],
            ['robots_rule_list',  {}],
        ]

        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)
        self.client.logout()
        self.client.post(reverse('login'),
                         data={'identification': 'jane@example.com',
                               'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)
