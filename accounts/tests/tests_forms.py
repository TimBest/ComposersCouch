from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class SignupFormTests(TestCase):
    """ Test the signup form. """
    fixtures = ['users']

    def test_signup_form(self):
        pass

class EmailFormTests(TestCase):
    """ Test the ``EmailForm`` """

    fixtures = ['users',]

    def test_signin_email_form(self):
        pass

class ClaimProfileFormTests(TestCase):
    """
    Test the :class:`ClaimProfileForm`.


    """
    fixtures = ['users']

    def test_claim_profile_porm(self):
        pass

class SigninFormTests(TestCase):
    """ Test the ``ChangeEmailForm`` """
    fixtures = ['users']

    def test_sigin_form(self):
        pass
