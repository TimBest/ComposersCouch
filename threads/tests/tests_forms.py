from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from threads import forms


class FormTests(TestCase):
    fixtures = ['users', 'profiles', 'contactInfos','locations', 'contacts',
                'zipcodes', 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks', 'media']

    def test_compose_form(self):
        # Test a valid form.
        valid_data_dicts = [
            {"recipients": [1,2,],
             "subject":"Just Saying Hi",
             "body": "hey just want to drop ou a line and see whats up",},

        ]
        for valid_dict in valid_data_dicts:
            form = forms.ComposeForm(data=valid_dict)
            self.failUnless(form.is_valid())

    def test_reply_form(self):
        # Test a valid form.
        valid_data_dicts = [
            {"body": "hey thanks for getting in touch. glad all is well",},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.ReplyForm(data=valid_dict)
            self.failUnless(form.is_valid())
