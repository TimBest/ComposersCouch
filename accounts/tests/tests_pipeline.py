from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from accounts.models import Profile
from userena.utils import get_gravatar, get_protocol
from userena import settings as userena_settings
from userena.models import UserenaBaseProfile

import hashlib

class CreateProfileTests(TestCase):
    """ Test the extra utils methods """
    fixtures = ['users']

    def test_createprofile(self):
        pass
