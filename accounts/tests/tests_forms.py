from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from accounts import forms


class SignupFormTests(TestCase):
    """ Test the signup form. """
    fixtures = ['users']

    def test_signup_form(self):
        """
        Test that the ``SignupForm``.
        """
        invalid_data_dicts = [
            # no band name for type artist
            {'data': {'profile_type': 'm',
                      'first_name': '',
                      'last_name': '',
                      'band_name': '',
                      'venue_name': ''},
            'error': ('band_name', [_(u'A band name is required for Artists.')])},

            # no venue name for type venue
            {'data': {'profile_type': 'v',
                      'first_name': '',
                      'last_name': '',
                      'band_name': '',
                      'venue_name': ''},
            'error': ('venue_name', [_(u'A venue name is required for Venues.')])},

            # no first name for type fan
            {'data': {'profile_type': 'f',
                      'first_name': '',
                      'last_name': 'last name',
                      'band_name': '',
                      'venue_name': ''},
            'error': ('first_name', [_(u'A first name is required for Fans.')])},

            # no last name for type fan
            {'data': {'profile_type': 'f',
                      'first_name': 'first name',
                      'last_name': '',
                      'band_name': '',
                      'venue_name': ''},
            'error': ('last_name', [_(u'A last name is required for Fans.')])},
        ]

        for invalid_dict in invalid_data_dicts:
            form = forms.SignupForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        # Test all 3 valid forms.
        valid_data_dicts = [
            {'data': {'profile_type': 'm',
                      'first_name': '',
                      'last_name': '',
                      'band_name': 'Band Name',
                      'venue_name': ''},},

            {'data': {'profile_type': 'v',
                      'first_name': '',
                      'last_name': '',
                      'band_name': '',
                      'venue_name': 'Venue Name'},},

            {'data': {'profile_type': 'f',
                      'first_name': 'First NAme',
                      'last_name': 'last name',
                      'band_name': '',
                      'venue_name': ''},},
        ]

        for valid_dict in valid_data_dicts:
            form = forms.SignupForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())


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
