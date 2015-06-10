from django.test import TestCase

from artist import forms


class BiographyFormTests(TestCase):

    def test_biography_form(self):
        # Test a valid form.
        valid_data_dicts = [
            {'data': {'biography': 'This is a sample biography. This is a\
            second sentance about myself. And this is a Third. Now i will go on\
            to describe another thing about my self. Hopefully this is not to\
            long.',},},
        ]

        for valid_dict in valid_data_dicts:
            form = forms.BiographyForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

class MemberFormTests(TestCase):

    def test_member_form(self):
        # Test a valid form.
        valid_data_dicts = [
            {'data': {'name': 'Billy Washington',
                      'biography': 'I am Billy Washington and im the best.',
                      'current_member': True,
                      'remove_member': False,},},
        ]

        for valid_dict in valid_data_dicts:
            form = forms.MemberForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())
