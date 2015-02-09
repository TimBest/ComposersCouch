from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from accounts.models import Profile
from accounts.pipeline import create_profile, get_username
from contact.models import Location, Zipcode

import hashlib

class CreateProfileTests(TestCase):
    """ Test the extra utils methods """
    fixtures = ['users', 'profiles']

    def test_create_profile(self):
        # test fan createion
        user = User.objects.get(pk=1)

        profile_type='f'
        location = Location(zip_code=Zipcode(pk=12065))
        user = create_profile(user, profile_type, location, 'Jane', 'Doe')
        self.assertIsNotNone(user.profile.fanProfile)
        self.assertIsNotNone(user.profile.contact_info)
        self.assertIsNotNone(user.calendar)
        # test artist creation
        user = User.objects.get(pk=2)
        profile_type='m'
        location = Location(zip_code=Zipcode(pk=12065))
        user = create_profile(user, profile_type, location, band_name="Mouse Rat")
        self.assertIsNotNone(user.profile.musicianProfile)
        self.assertIsNotNone(user.profile.contact_info)
        self.assertIsNotNone(user.calendar)
        # test venue creation
        user = User.objects.get(pk=3)
        profile_type='v'
        location = Location(zip_code=Zipcode(pk=12065))
        user = create_profile(user, profile_type, location, venue_name="Gasworks")
        self.assertIsNotNone(user.profile.venueProfile)
        self.assertIsNotNone(user.profile.contact_info)
        self.assertIsNotNone(user.calendar)

    def test_get_username(self):
        # test to make shug username is properly sanitized
        username = get_username("+-)(*&^%$#@!;][.,VJohn Doe")
        slug_username = slugify(username)
        self.failUnlessEqual(username, slug_username)

        # test to make sure username is the correct length
        username = get_username("Johnsdasdaffdhcfgnnthk;narkgmdfngjknsiurgmgkmdfjgnsuerghuyebgunjfdjkgndiufgheruighyerhgjkfngoe")
        username_length = User._meta.get_field('username').max_length
        self.assertTrue(len(username)<=username_length)
