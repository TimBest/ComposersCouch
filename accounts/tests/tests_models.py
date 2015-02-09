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

class FanProfileModelTest(TestCase):
    """ Test the ``BaseProfile`` model """
    fixtures = ['users', 'profiles']

class ArtistProfileModelTest(TestCase):
    """ Test the ``BaseProfile`` model """
    fixtures = ['users', 'profiles']

class VenueProfileModelTest(TestCase):
    """ Test the ``BaseProfile`` model """
    fixtures = ['users', 'profiles']
