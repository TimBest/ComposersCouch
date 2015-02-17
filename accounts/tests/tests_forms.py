from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from accounts import forms


class SignupFormTests(TestCase):
    """ Test the signup form. """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',  
                 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks', 'media', 'calendars', 'info',
                'shows', 'events']

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

    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',  
                 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks', 'media', 'calendars', 'info',
                'shows', 'events']

    def test_signin_email_form(self):
        """
        Test that the ``EmailForm`` checks for unique e-mail addresses.
        """
        # test field errors
        invalid_data_dicts = [
            # Already taken email
            {'data': {'email': 'john@example.com',
                      'password1': 'foobar',
                      'password2': 'foobar',},
             'error': ('email', [_(u'This email is already in use. Please supply a different email.')])},
            # Password is not the same
            {'data': {'email': 'katy@example.com',
                      'password1': 'foobar',
                      'password2': 'foobar2',},
             'error': ('__all__', [_(u'The two password fields didn\'t match.')])},
        ]

        for invalid_dict in invalid_data_dicts:
            form = forms.EmailForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        # And finally, a valid form.
        form = forms.EmailForm(data={'email': 'foo@example.com',
                                      'password1': 'foobar',
                                      'password2': 'foobar'})
        self.failUnless(form.is_valid())

class ClaimProfileFormTests(TestCase):
    """
    Test the :class:`ClaimProfileForm`.


    """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes',]

    def test_claim_profile_form(self):
        """
        Test that the ``ClaimProfileForm`` checks for unique e-mail addresses.
        """
        #TODO test field errors
        """invalid_data_dicts = [
            # Password is not the same
            {'data': {'new_password1': 'foobar',
                      'new_password2': 'foobar2',},
             'error': ('__all__', [_(u'The two password fields didn\'t match.')])},
        ]

        for invalid_dict in invalid_data_dicts:
            form = forms.ClaimProfileForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])"""

        #TODO And finally, a valid form.
        """form = forms.ClaimProfileForm(data={'password1': 'foobar',
                                     'password2': 'foobar'})
        self.failUnless(form.is_valid())"""
        pass

class SigninFormTests(TestCase):
    """ Test the ``ChangeEmailForm`` """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes',]

    def test_sigin_form(self):
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
            form = forms.SigninForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        valid_data_dicts = [
            {'identification': 'john@example.com',
             'password': 'blowfish'}
        ]

        for valid_dict in valid_data_dicts:
            form = forms.SigninForm(valid_dict)
            self.failUnless(form.is_valid())
