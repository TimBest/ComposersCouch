from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile
from artist.models import ArtistProfile
from artist.views import MusicianContactsView

class ViewsTests(TestCase):
    """  """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes',
                'profiles', 'artists', 'members', 'calendars']

    def _test_only_viewable_by_artist(self, url_name, kwargs):
        # Anonymous user is redirected to login
        self.client.logout()
        response = self.client.get(reverse(url_name, kwargs=kwargs))
        self.assertRedirects(response, '%s?next=%s' % (reverse('signin'),
                             response.request['PATH_INFO']), status_code=302,
                             target_status_code=200,)
        # Non Artist is given permission denied
        self.client.post(reverse('signin'),
                         data={'identification': 'john@example.com',
                               'password': 'blowfish'})
        response = self.client.get(reverse(url_name, kwargs=kwargs))
        self.assertEqual(response.status_code, 403)
        self.client.logout()
        # Artist is given the page
        self.client.post(reverse('signin'),
                         data={'identification': 'jane@example.com',
                               'password': 'blowfish'})
        response = self.client.get(reverse(url_name, kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

    def _signin_artist(self):
        self.client.logout()
        self.client.post(reverse('signin'),
                         data={'identification': 'jane@example.com',
                               'password': 'blowfish'})


    def test_view(self):
        """  """
        user = User.objects.get(pk=2)
        user.profile.artist_profile = ArtistProfile(pk=2)
        url_names = [
            ['artist:about',  {'username':user.username}],
            ['artist:news',   {'username':user.username}],
            ['artist:shows',  {'username':user.username}],
            ['artist:shows',  {'username':user.username,'year':2015}],
            ['artist:photos', {'username':user.username}],
            ['artist:music',  {'username':user.username}],
            ['artist:videos', {'username':user.username}],
        ]

        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('artist:home', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 302)


    def test_biography_form_view(self):
        url_name = 'artist:biographyForm'
        self._test_only_viewable_by_artist(url_name, {})
        values = {
            'biography': 'This is a sample biography. This is a\
                          second sentance about myself. And this is a Third.\
                          Now i will go on to describe another thing about my\
                          self. Hopefully this is not to long.',
        }
        self._signin_artist()
        response = self.client.post(reverse(url_name), values, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["user"].profile.artist_profile.biography,
            values['biography']
        )

    def test_contact_form_view(self):
        user = None
        values = {
            'name': 'Santi White',
            'email': 'santigold@example.com',
            'phone': '8765309',
            'url': 'www.example.com',
            'address_1': '3 Zamora Court',
            'address_2': 'apt. 215',
            'city': 'Clifton Park',
            'state': 'NY',
            'zip_code': 12065,
        }
        url_names = [['artist:userContactForm', {}],]
        for contact_type in MusicianContactsView.CONTACT_TYPES:
            url_names.append(['artist:contactForm',{'contactType':contact_type}],)
        self._signin_artist()
        for url_name in url_names:
            self._test_only_viewable_by_artist(url_name[0], url_name[1])
            response = self.client.post(
                reverse(url_name[0], kwargs=url_name[1]), values, follow=True
            )
            user = response.context["user"]
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(
                reverse(url_name[0], kwargs=url_name[1]),
                response.request['PATH_INFO']
            )
        self.assertEqual(
            user.profile.contact_info.contact.name,
            values['name']
        )

        for contact_type in MusicianContactsView.CONTACT_TYPES:
            contact_info = getattr(
                user.profile.artist_profile,
                MusicianContactsView.CONTACT_TYPES[contact_type]
            )
            self.assertEqual(contact_info.contact.name, values['name'])

    def test_form_permissions_views(self):
        user = User.objects.get(pk=2)
        user.profile.artist_profile = ArtistProfile(pk=2)
        url_names = [
            ['artist:memberForm',        {}],
            ['artist:memberForm',        {'memberID':1}],
            ['artist:albumForm',         {}],
            ['artist:editAlbumForm',     {'albumID':1}],
            ['artist:tracksForm',        {'albumID':1}],
            ['artist:video_album_form',  {}],
            ['artist:video_edit_album',  {'albumID':1}],
            ['artist:video_tracks_form', {'albumID':1}],
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
