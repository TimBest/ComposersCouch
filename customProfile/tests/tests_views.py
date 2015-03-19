from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile
from artist.models import ArtistProfile


class ViewsTests(TestCase):
    """ Test the account views """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles', 'artists', 'venues']

    def setUp(self):
        # create user and log them in
        response = self.client.post(reverse('login'),
                                    data={'identification': 'john@example.com',
                                          'password': 'blowfish'})
        self.user = User.objects.get(email='john@example.com')

    def test_fan_profile_edit_view(self):
        self.user.profile = Profile.objects.get(pk=1)
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)

    def test_artist_profile_edit_view(self):
        self.user.profile = Profile.objects.get(pk=2)
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)

    def test_venue_profile_edit_view(self):
        self.user.profile = Profile.objects.get(pk=3)
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
