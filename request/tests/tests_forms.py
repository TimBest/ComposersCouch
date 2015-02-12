from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from contact.models import ContactInfo
from schedule.models import DateRange
from request import forms
from request.models import Application, PublicRequest


class FormTests(TestCase):
    fixtures = ['users', 'profiles', 'contactInfos','locations', 'contacts',
                'zipcodes', 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates']

    def test_date_form(self):
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

    def test_message_form(self):
        # Test a valid form.
        valid_data_dicts = [
            {"body": "This is the message that I would like to attatch to the\
                      request. I hope this extra personal touch gets me the\
                      gig."},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.MessageForm(data=valid_dict)
            self.failUnless(form.is_valid())

    def test_participant_form(self):
        # test field errors
        user = User.objects.get(pk=2)
        user.profile.contact_info = ContactInfo.objects.get(pk=2)
        user.profile.save()
        invalid_data_dicts = [
            # Request must be in the future
            {'data': {"user": "",
                      "email": "",
                      "name": "Devendra",},
             'error': ('__all__', [_(u'A user or email is required.')])},
        ]

        for invalid_dict in invalid_data_dicts:
            form = forms.ParticipantForm(data=invalid_dict['data'], user=user)
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        # Test a valid form.
        valid_data_dicts = [
            {"user": 3,
             "email": "",
             "name": "",},
            {"user": "",
             "email": "bob.belcher@example.com",
             "name": "Bob Belcher",},
            {"user": "",
             "email": "bob@example.com",
             "name": "",},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.ParticipantForm(data=valid_dict, user=user)
            self.failUnless(form.is_valid())

    def test_artist_participant_form(self):
        # test field errors
        user = User.objects.get(pk=2)
        user.profile.contact_info = ContactInfo.objects.get(pk=2)
        user.profile.save()
        invalid_data_dicts = [
            # Request must be in the future
            {'data': {"user": "",
                      "email": "",
                      "name": "Devendra",},
             'error': ('__all__', [_(u'A user or email is required.')])},
        ]

        for invalid_dict in invalid_data_dicts:
            form = forms.ArtistParticipantForm(data=invalid_dict['data'], user=user)
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        # Test a valid form.
        valid_data_dicts = [
            {"user": 3,
             "email": "",
             "name": "",},
            {"user": "",
             "email": "bob.belcher@example.com",
             "name": "Bob Belcher",},
            {"user": "",
             "email": "bob@example.com",
             "name": "",},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.ArtistParticipantForm(data=valid_dict, user=user)
            self.failUnless(form.is_valid())

    def test_public_request_form(self):
        # test field errors
        invalid_data_dicts = [
            # accept by must be in the future
            {'data': {"zip_code": 12065,
                      "details": "this is the message I will attach to a public\
                                  request in hopes someone applys.",
                      "accept_by": timezone.now().date()-timedelta(days=1),},
             'error': ('accept_by', [_(u'There must be time to accept the request.')])},
        ]
        for invalid_dict in invalid_data_dicts:
            form = forms.PublicRequestForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        # Test a valid form.
        valid_data_dicts = [
            {"zip_code": 12065,
             "details": "Hey play a show at my place.",
             "accept_by": timezone.now().date()+timedelta(days=1),},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.PublicRequestForm(data=valid_dict)
            self.failUnless(form.is_valid())

    def test_number_of_applicatants_form(self):
        # Test a valid form.
        valid_data_dicts = [
            {"zip_code": 12065,
             "details": "Hey play a show at my place.",
             "accept_by": timezone.now().date()+timedelta(days=1),
             "total": 10,},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.NumberOfApplicantsForm(data=valid_dict)
            form.is_valid()
            self.failUnless(form.is_valid())

    def test_approve_applicant_form(self):
        pass
        """public_request = PublicRequest.objects.get(pk=1)
        left = public_request.applicants.left
        form = forms.ApproveForm(data={})
        # Accept an applicatant
        application_1 = form.save(Application.objects.get(pk=1), True)
        left = left -1
        self.assertEqual(left, public_request.applicants.left)
        # Deny an applicant
        print public_request.applicants.left
        application_2 = form.save(Application.objects.get(pk=2), False)
        print public_request.applicants.left
        self.assertEqual(left, public_request.applicants.left)
        # Accept another applicant
        application_1 = form.save(Application.objects.get(pk=2), True)
        left = left -1
        self.assertEqual(left, application_1.public_request.applicants.left)
        # public request is fulfiled
        self.assertEqual(public_request.fulfilled, True)"""
