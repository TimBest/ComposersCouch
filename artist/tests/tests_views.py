from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile
from artist.models import ArtistProfile
from artist.views import MusicianContactsView


class AboutViewsTests(TestCase):
    """  """
    fixtures = ['users', 'profiles', 'artists', 'members']

    def test_about_view(self):
        """  """
        user = User.objects.get(pk=1)
        response = self.client.get(reverse('artist:about', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 200)

    def test_about_form_views(self):
        """  """
        response = self.client.post(reverse('signin'),
                                    data={'identification': 'john@example.com',
                                          'password': 'blowfish'})
        user = User.objects.get(email='john@example.com')
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

class MusicViewsTests(TestCase):
    """  """
    fixtures = ['users', 'profiles', 'artistProfiles']

    def test_about_view(self):
        """  """
        user = User.objects.get(pk=1)
        #response = self.client.get(reverse('artist:music', kwargs={'username': user.username}))
        #self.assertEqual(response.status_code, 200)

class VideosViewsTests(TestCase):
    """  """
    fixtures = ['users', 'profiles', 'artistProfiles']

    def test_videos_view(self):
        """  """
        user = User.objects.get(pk=1)
        #response = self.client.get(reverse('artist:videos', kwargs={'username': user.username}))
        #self.assertEqual(response.status_code, 200)
