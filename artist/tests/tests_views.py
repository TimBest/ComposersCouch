from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile
from artist.models import ArtistProfile
from artist.views import MusicianContactsView

class ViewsTests(TestCase):
    """  """
    fixtures = ['users', 'profiles', 'artists', 'members', 'calendars']

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

    def test_form_permissions_views(self):
        user = User.objects.get(pk=2)
        user.profile.artist_profile = ArtistProfile(pk=2)
        url_names = [
            ['artist:biographyForm',     {}],
            ['artist:userContactForm',   {}],
            ['artist:memberForm',        {}],
            ['artist:memberForm',        {'memberID':1}],
            ['artist:albumForm',         {}],
            ['artist:editAlbumForm',     {'albumID':1}],
            ['artist:tracksForm',        {'albumID':1}],
            ['artist:video_album_form',  {}],
            ['artist:video_edit_album',  {'albumID':1}],
            ['artist:video_tracks_form', {'albumID':1}],
        ]
        for contact_type in MusicianContactsView.CONTACT_TYPES:
            url_names.append(['artist:contactForm',{'contactType':contact_type[0]}],)

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
