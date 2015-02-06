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

    def test_signup_view_signout(self):
        """ TODO: Check that a newly signed user shouldn't be signed in. """
        pass

    def test_signup_view_success(self):
        """
        TODO: After a ``POST`` to the ``signup`` view a new user should be created,
        the user should be logged in and redirected to the signup success page.

        """
        pass

    def test_signup_view_with_signin(self):
        """
        TODO: After a ``POST`` to the ``signup`` view a new user should be created,
        the user should be logged in and redirected to the signup success page.

        """
        pass

    def test_signin_view(self):
        """ A ``GET`` to the signin view should render the correct form """
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'accounts/signin_form.html')

    def test_signin_view_remember_me_on(self):
        """
        A ``POST`` to the signin with tells it to remember the user for
        ``REMEMBER_ME_DAYS``.

        """
        response = self.client.post(reverse('signin'),
                                    data={'identification': 'john@example.com',
                                          'password': 'blowfish',
                                          'remember_me': True})
        self.assertEqual(self.client.session.get_expiry_age(),
                         userena_settings.USERENA_REMEMBER_ME_DAYS[1] * 3600 * 24)

    def test_signin_view_remember_off(self):
        """
        A ``POST`` to the signin view of which the user doesn't want to be
        remembered.

        """
        response = self.client.post(reverse('signin'),
                                    data={'identification': 'john@example.com',
                                          'password': 'blowfish'})

        self.failUnless(self.client.session.get_expire_at_browser_close())

    def test_signin_view_success(self):
        """
        TODO: A valid ``POST`` to the signin view should redirect the user to it's
        own profile page if no ``next`` value is supplied. Else it should
        redirect to ``next``.

        """
        pass


    def test_signout_view(self):
        """ A ``GET`` to the signout view """
        response = self.client.get(reverse('signout'))
        self.assertEqual(response.status_code, 302)

    def test_password_reset_view_success(self):
        """ A ``POST`` to the password reset view with email that exists"""
        response = self.client.post(reverse('userena_password_reset'),
                                    data={'email': 'john@example.com',})
        # check if there was success redirect to userena_password_reset_done
        # and email was sent
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('userena_password_reset_done'), str(response))
        self.assertTrue(mail.outbox)

    def test_password_reset_view_failure(self):
        """ A ``POST`` to the password reset view with incorrect email"""
        response = self.client.post(reverse('userena_password_reset'),
                                    data={'email': 'no.such.user@example.com',})
        # note: status code can be different depending on django version
        self.assertIn(response.status_code, [200, 302])
        self.assertFalse(mail.outbox)

    def test_password_reset_confirm(self):
        #TODO: post reset request and search form confirmation url
        """self.client.post(reverse('userena_password_reset'),
                         data={'email': 'john@example.com',})
        confirm_mail = mail.outbox[0]
        confirm_url = re.search(r'\bhttps?://\S+', confirm_mail.body)

        # get confirmation request page
        response = self.client.get(confirm_url)
        self.assertEqual(response.status_code, 200)

        # post new password and check if redirected with success
        response = self.client.post(confirm_url,
                                    data={'new_password1': 'pass',
                                          'new_password2': 'pass',})
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('userena_password_reset_complete'), str(response))"""
        pass
