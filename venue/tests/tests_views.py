from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile


class ViewsTests(TestCase):
    """  """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles', 'venues', 'calendars', 'staff', 'contacts']

    def test_view(self):
        """  """
        user = User.objects.get(pk=3)
        url_names = [
            ['venue:about',  {'username':user.username}],
            ['venue:news',   {'username':user.username}],
            ['venue:shows',  {'username':user.username}],
            ['venue:shows',  {'username':user.username,'year':2015}],
            ['venue:photos', {'username':user.username}],
        ]

        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('venue:home', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 302)


    def test_form_permissions_views(self):
        user = User.objects.get(pk=3)
        url_names = [
            ['venue:socialLinksForm', {}],
            ['venue:photoLinksForm',  {}],
            ['venue:biographyForm',   {}],
            ['venue:contactForm',     {}],
            ['venue:equipmentForm',   {'category':'sound'}],
            ['venue:equipmentForm',   {'category':'effects'}],
            ['venue:equipmentForm',   {'category':'accessories'}],
            ['venue:hoursForm',       {}],
            ['venue:policiesForm',    {}],
            ['venue:seatingForm',     {}],
            ['venue:staffForm',       {}],
            ['venue:staffForm',       {'staff_id':1}],
        ]

        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertRedirects(response, '%s?next=%s' % (reverse('login'),
                                 response.request['PATH_INFO']),
                                 status_code=302, target_status_code=200,)
        # user with out permission is denied
        self.client.post(reverse('login'),
                                 data={'identification': 'john@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 403)
        self.client.logout()

        # user with permission is redirected
        self.client.post(reverse('login'),
                                 data={'identification': 'arie@example.com',
                                       'password': 'blowfish'})
        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)
