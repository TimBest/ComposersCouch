from django.test import TestCase

from contact.models import Zipcode
from feeds import forms


class FormTests(TestCase):
    fixtures = ['genres', 'zipcodes']

    def test_post_form(self):
        # Test a valid form.
        valid_data_dicts = [
            {'data': {'message': 'This is a message that I desire to post to\
                the composers couch comunity.',},},
        ]

        for valid_dict in valid_data_dicts:
            form = forms.PostForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_availability_form(self):
        # Test a valid form.
        valid_data_dicts = [{'data': {'date': '2015-01-02'},},]

        for valid_dict in valid_data_dicts:
            form = forms.AvailabilityForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_zipcode_form(self):
        # Test a valid form.
        valid_data_dicts = [{'data': {'zip_code': Zipcode(pk=12065)},},]
        for valid_dict in valid_data_dicts:
            form = forms.ZipcodeForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())
