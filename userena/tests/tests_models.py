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

class UserenaSignupModelTests(TestCase):
    """ Test the model of UserenaSignup """
    user_info = {'username': 'alice',
                 'password': 'swordfish',
                 'email': 'alice@example.com'}

    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles']

    def test_change_email(self):
        """ TODO """
        pass

    def test_activation_expired_account(self):
        """
        ``UserenaSignup.activation_key_expired()`` is ``True`` when the
        ``activation_key_created`` is more days ago than defined in
        ``USERENA_ACTIVATION_DAYS``.

        """
        user = UserenaSignup.objects.create_user(**self.user_info)
        user.date_joined -= datetime.timedelta(days=userena_settings.USERENA_ACTIVATION_DAYS + 1)
        user.save()

        user = User.objects.get(username='alice')
        self.failUnless(user.userena_signup.activation_key_expired())

    def test_activation_used_account(self):
        """
        An user cannot be activated anymore once the activation key is
        already used.

        """
        user = UserenaSignup.objects.create_user(**self.user_info)
        activated_user = UserenaSignup.objects.activate_user(user.userena_signup.activation_key)
        self.failUnless(activated_user.userena_signup.activation_key_expired())

    def test_activation_unexpired_account(self):
        """
        ``UserenaSignup.activation_key_expired()`` is ``False`` when the
        ``activation_key_created`` is within the defined timeframe.``

        """
        user = UserenaSignup.objects.create_user(**self.user_info)
        self.failIf(user.userena_signup.activation_key_expired())

class BaseProfileModelTest(TestCase):
    """ Test the ``BaseProfile`` model """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles']

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
        user = User.objects.get(pk=1)
        profile = user.profile

        # Profile #1 has a first and last name
        full_name = profile.get_full_name_or_username()
        self.failUnlessEqual(full_name, "John Doe")

        # Let's empty out his name, now we should get his username
        user.first_name = ''
        user.last_name = ''
        user.save()

        self.failUnlessEqual(profile.get_full_name_or_username(),
                             "john")

        # Finally, userena doesn't use any usernames, so we should return the
        # e-mail address.
        userena_settings.USERENA_WITHOUT_USERNAMES = True
        self.failUnlessEqual(profile.get_full_name_or_username(),
                             "john@example.com")
        userena_settings.USERENA_WITHOUT_USERNAMES = False
