from django.test import TestCase

from customProfile import forms

class EditProfileFormTests(TestCase):
    """ Test the edit profile forms. """
    fixtures = ['genres']

    def test_artist_form(self):
        valid_data_dicts = [{'data': {'name': 'Father John Misty',},},]
        for valid_dict in valid_data_dicts:
            form = forms.ArtistProfileForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_venue_form(self):
        valid_data_dicts = [{'data': {'name': 'The Gas Works',},},]
        for valid_dict in valid_data_dicts:
            form = forms.VenueProfileForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_fan_form(self):
        valid_data_dicts = [
            {'data': {'first_name': 'Jane',
                      'last_name': 'Doe',},},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.UserForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_user_form(self):
        valid_data_dicts = [
            {'data': {'username': 'FatherJohnMisty',
                      'email': 'fdm@example.com',},},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.UsernameForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_profile_form(self):
        valid_data_dicts = [
            {'data': {'genre': ['1', '2'],},},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.ProfileForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())
