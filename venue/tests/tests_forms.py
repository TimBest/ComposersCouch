from django.test import TestCase
from django.utils import timezone

from venue import forms


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

    def test_hours_form(self):
        # Test a valid form.
        valid_data_dicts = [
            {'data': {'start': timezone.now().time(),
                      'end': timezone.now().time(),},},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.HoursForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_equipment_form(self):
        # Test a valid form.
        valid_data_dicts = [
            {'data': {'quantity': 5,
                      'name': "Name of the equipment",
                      'remove': False,},},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.EquipmentForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_policies_form(self):
        # Test a valid form.
        valid_data_dicts = [
            {'data': {'title': "hey this is a rule",
                      'description': "you better follow it. or else",
                      'remove': False,},},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.PoliciesForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_seating_form(self):
        # Test a valid form.
        valid_data_dicts = [
            {'data': {'capacity': 379,},},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.SeatingForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_staff_form(self):
        # Test a valid form.
        valid_data_dicts = [
            {'data': {'job_title': "manager",
                      'biography': "I am the manager",
                      'delete': False,},},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.StaffForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())
