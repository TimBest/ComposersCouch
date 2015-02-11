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
        response = self.client.get(reverse('artist:home', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('artist:about', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('artist:news', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('artist:shows', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('artist:photos', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('artist:music', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('artist:videos', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 200)

class FormViewsTests(TestCase):
    """  """
    fixtures = ['users', 'profiles', 'artists', 'members', 'calendars']

    def setUp(self):
        response = self.client.post(reverse('signin'),
                                            data={'identification': 'jane@example.com',
                                                  'password': 'blowfish'})
        self.user = User.objects.get(email='jane@example.com')

    def test_about_form_views(self):
        # biography
        response = self.client.get(reverse('artist:biographyForm'))
        self.assertEqual(response.status_code, 200)
        # artists contact info
        response = self.client.get(reverse('artist:userContactForm'))
        self.assertEqual(response.status_code, 200)
        # members
        response = self.client.get(reverse('artist:memberForm'))
        self.assertEqual(response.status_code, 200)
        # edit member
        response = self.client.get(reverse('artist:memberForm', kwargs={'memberID': 1}))
        self.assertEqual(response.status_code, 200)
        #artist contacts
        for contact_type in MusicianContactsView.CONTACT_TYPES:
            response = self.client.get(reverse('artist:contactForm', kwargs={'contactType': contact_type[0]}))
            self.assertEqual(response.status_code, 200)

    def test_music_form_views(self):
        # album
        response = self.client.get(reverse('artist:albumForm'))
        self.assertEqual(response.status_code, 200)
        # album edit
        response = self.client.get(reverse('artist:editAlbumForm', kwargs={'albumID': 1}))
        self.assertEqual(response.status_code, 200)
        # album track edit
        response = self.client.get(reverse('artist:tracksForm', kwargs={'albumID': 1}))
        self.assertEqual(response.status_code, 200)

    def test_videos_form_views(self):
        # album
        response = self.client.get(reverse('artist:video_album_form'))
        self.assertEqual(response.status_code, 200)
        # album edit
        response = self.client.get(reverse('artist:video_edit_album', kwargs={'albumID': 1}))
        self.assertEqual(response.status_code, 200)
        # album track edit
        response = self.client.get(reverse('artist:video_tracks_form', kwargs={'albumID': 1}))
        self.assertEqual(response.status_code, 200)
