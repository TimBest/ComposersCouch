from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from contact import forms
from contact.models import Zipcode


class ContactInfoFormsTests(TestCase):
    fixtures = ['zipcodes']

    def test_zipcode_form(self):
        valid_data_dicts = [
            {'data': {'zip_code': Zipcode(pk=12065)},},
        ]

        for valid_dict in valid_data_dicts:
            form = forms.ZipcodeForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_location_form(self):
        invalid_data_dicts = [
            # no band name for type artist
            {'data': {'address_1': '3 Zamora Court',
                      'address_2': 'apt. 215',
                      'city': 'Clifton Park',
                      'state': 'NY',
                      'zip_code': ''},
            'error': ('zip_code', [_(u'This field is required.')])},
        ]

        for invalid_dict in invalid_data_dicts:
            form = forms.LocationForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        valid_data_dicts = [
            {'data': {'address_1': '3 Zamora Court',
                      'address_2': 'apt. 215',
                      'city': 'Clifton Park',
                      'state': 'NY',
                      'zip_code': Zipcode(pk=12065)},},
        ]

        for valid_dict in valid_data_dicts:
            form = forms.LocationForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_non_user_location_form(self):
        valid_data_dicts = [
            {'data': {'address_1': '3 Zamora Court',
                      'address_2': 'apt. 215',
                      'city': 'Clifton Park',
                      'state': 'NY',
                      'zip_code': ''},},
        ]

        for valid_dict in valid_data_dicts:
            form = forms.NonUserLocationForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_contact_form(self):
        valid_data_dicts = [
            {'data': {'name': 'Santi White',
                      'email': 'santigold@example.com',
                      'phone': '8765309',
                      'url': 'www.example.com',},},
        ]

        for valid_dict in valid_data_dicts:
            form = forms.ContactForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())
