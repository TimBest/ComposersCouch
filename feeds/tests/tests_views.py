from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile
from artist.models import ArtistProfile
from artist.views import MusicianContactsView


class ViewsTests(TestCase):
    """  """
    fixtures = ['users', 'profiles', 'artists', 'members', 'calendars']

    def test_artist_feed_view(self):
        """  """
        user = User.objects.get(pk=1)
        orders = ['new', 'all']
        scopes = ['local','following', 'all']
        for order in orders:
            for scope in scopes:
                response = self.client.get(reverse('artists',
                    kwargs={'order': order,'scope': scope}))
                self.assertEqual(response.status_code, 200)
                response = self.client.get(reverse('artists',
                    kwargs={'order': order,'scope': scope, 'zipcode': 12065}))
                self.assertEqual(response.status_code, 200)
                response = self.client.get(reverse('available_artists',
                    kwargs={'order': order,
                            'year':2015,
                            'month':02,
                            'day':15,}))
                self.assertEqual(response.status_code, 200)
                response = self.client.get(reverse('available_artists',
                    kwargs={'order': order,
                            'year':2015,
                            'month':02,
                            'day':15,
                            'zipcode':12065}))
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
