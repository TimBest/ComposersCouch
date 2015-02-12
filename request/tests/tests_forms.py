from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from schedule.models import DateRange
from request import forms


class FormTests(TestCase):

    def test_post_form(self):
        date_range = DateRange(start=timezone.now(), end=timezone.now())
        # test field errors
        invalid_data_dicts = [
            # Request must be in the future
            {'data': {"start_0": timezone.now().date() - timedelta(days=1),
                      "start_1": timezone.now().time(),
                      "end_0": timezone.now().date(),
                      "end_1": timezone.now().time(),},
             'error': ('__all__', [_(u'The start time must after today.')])},
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
