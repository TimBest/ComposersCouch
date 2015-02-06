import re

from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.contrib.auth.models import User

from userena import forms
from userena import settings as userena_settings

User = User


class UserenaViewsTests(TestCase):
    """ Test the account views """
    fixtures = ['users', 'profiles']

    def test_signup_view(self):
        """TODO: A ``GET`` to the ``signup`` view """
        pass

    def test_signup_auth_view(self):
        """ TODO: Check that a newly signed user shouldn't be signed in. """
        pass

    def test_signup_email_view(self):
        """
        TODO: After a ``POST`` to the ``signup`` view a new user should be created,
        the user should be logged in and redirected to the signup success page.

        """
        pass

    def test_signup_social_view(self):
        """
        TODO: After a ``POST`` to the ``signup`` view a new user should be created,
        the user should be logged in and redirected to the signup success page.

        """
        pass

    def test_claim_profile_view(self):
        """ A ``GET`` to the signin view should render the correct form """
        pass

    def test_verify_profile_claim_view(self):
        """
        A ``POST`` to the signin with tells it to remember the user for
        ``REMEMBER_ME_DAYS``.

        """
        pass

    def test_claim_profile_confirm_view(self):
        """
        A ``POST`` to the signin view of which the user doesn't want to be
        remembered.

        """
        pass

    def test_signin_view(self):
        """
        TODO: A valid ``POST`` to the signin view should redirect the user to it's
        own profile page if no ``next`` value is supplied. Else it should
        redirect to ``next``.

        """
        pass

    def test_loginredirect_view(self):
        """ A ``GET`` to the signout view """
        pass
