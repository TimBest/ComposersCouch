from django.test import TestCase
from django.contrib.auth.models import User

from accounts.utils import create_user_profile
from contact.models import Contact, ContactInfo, Location, Zipcode


class UtilsTests(TestCase):
    """ Test the extra utils methods """

    def test_is_artist(self):
        pass

    def test_is_venue(self):
        pass
