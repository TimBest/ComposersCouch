from django.test import TestCase
from django.contrib.auth.models import User

from accounts.utils import create_user_profile
from contact.models import Contact, ContactInfo, Location, Zipcode


class UtilsTests(TestCase):
    """ Test the extra utils methods """
    fixtures = ['users', 'profiles']

    def test_create_user_profile(self):
        creator = User.objects.get(pk=1)
        location = Location(zip_code=Zipcode(pk=12065))
        contact = Contact(name=creator.username)
        creator.profile.contact_info = ContactInfo(contact=contact,location=location)
        # test artist creation
        user = create_user_profile("Mouse Rat", "mouserat@example.com", "m", creator)
        self.failIf(user.profile.has_owner)
        self.assertIsNotNone(user.profile.artist_profile)
        self.assertIsNotNone(user.profile.contact_info)
        self.assertIsNotNone(user.calendar)
        # test venue creation
        user = create_user_profile("gasworks", "Gasworks@example.com", "v", creator)
        self.failIf(user.profile.has_owner)
        self.assertIsNotNone(user.profile.venueProfile)
        self.assertIsNotNone(user.profile.contact_info)
        self.assertIsNotNone(user.calendar)
