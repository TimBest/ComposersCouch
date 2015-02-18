# coding=utf-8
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from schedule.models import DateRange
from schedule import forms


class TestScheduleForms(TestCase):
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',
                 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks', 'media', 'calendars', 'info',
                'shows', 'events']

    def test_date_form(self):
        date_range = DateRange(start=timezone.now(), end=timezone.now())
        # test field errors
        invalid_data_dicts = [
            # end date cant be before the start
            {'data': {"start_0": timezone.now().date() + timedelta(days=1),
                      "start_1": timezone.now().time(),
                      "end_0": timezone.now().date(),
                      "end_1": timezone.now().time(),},
             'error': ('__all__', [_(u'The end time must be later than start time.')])},
        ]

        for invalid_dict in invalid_data_dicts:
            form = forms.DateForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        # Test a valid form.
        valid_data_dicts = [
            {"start_0": timezone.now().date(),
             "start_1": timezone.now().time(),
             "end_0": timezone.now().date(),
             "end_1": timezone.now().time(),},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.DateForm(data=valid_dict)
            self.failUnless(form.is_valid())

    def test_event_form(self):
        # Test a valid form.
        valid_data_dicts = [
            { "visible": False,},
            { "visible": True,},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.EventForm(data=valid_dict)
            self.failUnless(form.is_valid())

    def test_date_form(self):
        user = User.objects.get(pk=2)

        # test field errors
        invalid_data_dicts = [
            # end date cant be before the start
            {'data': {"title": "",
                      "headliner_text": "",
                      "headliner": "",
                      "openers_text": "Mouse Rat",
                      "openers": [2,],
                      "venue_text": "Gasworks",
                      "venue": 3,
                      "description": "Were putting a show on. tickets are 5 bucks.",},
             'error': ('__all__', [_(u'A Title or a Headliner is required.')]),
             'user' : user,},
            {'data': {"title": "Gasworks concert fridays",
                      "headliner_text": "",
                      "headliner": "",
                      "openers_text": "Mouse Rat",
                      "openers": [2,],
                      "venue_text": "",
                      "venue": "",
                      "description": "Were putting a show on. tickets are 5 bucks.",},
             'error': ('__all__', [_(u'A Venue is required.')]),
             'user' : user,},
            {'data': {"title": "Gasworks concert fridays",
                      "headliner_text": "",
                      "headliner": "",
                      "openers_text": "Mouse Rat",
                      "openers": [2,],
                      "venue_text": "Gasworks",
                      "venue": "",
                      "description": "Were putting a show on. tickets are 5 bucks.",},
             'error': ('__all__', [_(u'You must be a participant in this show.')]),
             'user' : User.objects.get(pk=1),},

        ]

        for invalid_dict in invalid_data_dicts:
            form = forms.ShowInfoForm(data=invalid_dict['data'],user=invalid_dict['user'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        # Test a valid form.
        valid_data_dicts = [
            {"title": "Concert Title",
             "headliner_text": "Mouse Rat",
             "headliner": 2,
             "openers_text": "Mouse Rat",
             "openers": [2,],
             "venue_text": "Gasworks",
             "venue": 3,
             "description": "Were putting a show on. tickets are 5 bucks.",},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.ShowInfoForm(data=valid_dict, user=user)
            self.failUnless(form.is_valid())
