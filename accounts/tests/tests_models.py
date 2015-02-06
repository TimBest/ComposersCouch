from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.models import Site
from django.core import mail
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile
from userena.models import UserenaSignup
from userena import settings as userena_settings

import datetime, hashlib, re

User = User

MUGSHOT_RE = re.compile('^[a-f0-9]{40}$')


class ProfileModelTest(TestCase):
    """ Test the ``BaseProfile`` model """
    fixtures = ['users', 'profiles']

    def test_mugshot_url(self):
        """TODO: The user has uploaded it's own mugshot. This should be returned. """
        pass

    def test_get_mugshot_url_without_gravatar(self):
        """
        TODO: Test if the correct mugshot is returned for the user when
        ``USERENA_MUGSHOT_GRAVATAR`` is set to ``False``.

        """
        pass


    def test_get_full_name_or_username(self):
        """ Test if the full name or username are returned correcly """
        pass

    def test_can_view_profile(self):
        """ Test if the user can see the profile with three type of users. """
        pass

class FanProfileModelTest(TestCase):
    """ Test the ``BaseProfile`` model """
    fixtures = ['users', 'profiles']

    def test_can_view_profile(self):
        """ Test if the user can see the profile with three type of users. """
        pass

class ArtistProfileModelTest(TestCase):
    """ Test the ``BaseProfile`` model """
    fixtures = ['users', 'profiles']

    def test_can_view_profile(self):
        """ Test if the user can see the profile with three type of users. """
        pass

class VenueProfileModelTest(TestCase):
    """ Test the ``BaseProfile`` model """
    fixtures = ['users', 'profiles']

    def test_can_view_profile(self):
        """ Test if the user can see the profile with three type of users. """
        pass
