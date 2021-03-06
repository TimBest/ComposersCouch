from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from userena import forms
from userena import settings as userena_settings


class SignupFormTests(TestCase):
    """ Test the signup form. """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes',]

    def test_signup_form(self):
        """
        Test that the ``SignupForm`` checks for unique usernames and unique
        e-mail addresses.

        """
        invalid_data_dicts = [
            # Already taken email
            {'data': {'email': 'john@example.com',
                      'password1': 'foobar',
                      'tos': 'on'},
             'error': ('email', [_(u'This email is already in use. Please supply a different email.')])},
        ]

        for invalid_dict in invalid_data_dicts:
            form = forms.SignupForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])


        # And finally, a valid form.
        form = forms.SignupForm(data={'email': 'foo@example.com',
                                      'password1': 'foobar',
                                      'tos': 'on'})
        self.failUnless(form.is_valid())

class AuthenticationFormTests(TestCase):
    """ Test the ``AuthenticationForm`` """

    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes',]

    def test_signin_form(self):
        """
        Check that the ``SigninForm`` requires both identification and password

        """
        invalid_data_dicts = [
            {'data': {'identification': '',
                      'password': 'inhalefish'},
             'error': ('identification', [u'Please supply your email.'])},
            {'data': {'identification': 'john',
                      'password': 'inhalefish'},
             'error': ('__all__', [u'Please enter a correct email and password. Note that fields are case-sensitive.'])}
        ]

        for invalid_dict in invalid_data_dicts:
            form = forms.AuthenticationForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        valid_data_dicts = [
            {'identification': 'john@example.com',
             'password': 'blowfish'}
        ]

        for valid_dict in valid_data_dicts:
            form = forms.AuthenticationForm(valid_dict)
            self.failUnless(form.is_valid())

    def test_signin_form_email(self):
        """
        Test that the signin form has a different label is
        ``USERENA_WITHOUT_USERNAME`` is set to ``True``

        """
        userena_settings.USERENA_WITHOUT_USERNAMES = True

        form = forms.AuthenticationForm(data={'identification': "john",
                                              'password': "blowfish"})

        correct_label = "Email"
        self.assertEqual(form.fields['identification'].label,
                         correct_label)

        # Restore default settings
        userena_settings.USERENA_WITHOUT_USERNAMES = False

class SignupFormOnlyEmailTests(TestCase):
    """
    Test the :class:`SignupFormOnlyEmail`.

    This is the same form as :class:`SignupForm` but doesn't require an
    username for a successfull signup.

    """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes',]

    def test_signup_form_only_email(self):
        """
        Test that the form has no username field. And that the username is
        generated in the save method

        """
        valid_data = {'email': 'hans@gretel.com',
                      'password1': 'blowfish'}

        form = forms.SignupFormOnlyEmail(data=valid_data)

        # Should have no username field
        self.failIf(form.fields.get('username', False))

        # Form should be valid.
        self.failUnless(form.is_valid())

        # Creates an unique username
        user = form.save()

        self.failUnless(len(user.username), 5)

class ChangeEmailFormTests(TestCase):
    """ Test the ``ChangeEmailForm`` """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes',]

    def test_change_email_form(self):
        user = User.objects.get(pk=1)
        invalid_data_dicts = [
            # No change in e-mail address
            {'data': {'email': 'john@example.com'},
             'error': ('email', [u'You\'re already known under this email.'])},
            # An e-mail address used by another
            {'data': {'email': 'jane@example.com'},
             'error': ('email', [u'This email is already in use. Please supply a different email.'])},
        ]
        for invalid_dict in invalid_data_dicts:
            form = forms.ChangeEmailForm(user, data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        # Test a valid post
        form = forms.ChangeEmailForm(user,
                                     data={'email': 'john@newexample.com'})
        self.failUnless(form.is_valid())

    def test_form_init(self):
        """ The form must be initialized with a ``User`` instance. """
        self.assertRaises(TypeError, forms.ChangeEmailForm, None)

class EditAccountFormTest(TestCase):
    """ Test the ``EditAccountForm`` """
